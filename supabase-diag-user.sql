-- Bir kullanıcının son 2 günkü düello sonuçlarını ve günlük puanını inceler (salt okunur). İsim kalıbı giriş kullanıcı adına bakar (profiles.username).
with u as (
  select p.user_id, p.username, s.name, s.dk, s.dp, s.ap
  from public.profiles p left join public.scores s on s.user_id = p.user_id
  where p.username ilike '%kaan%' limit 5)
select u.username, u.name, u.dk as gun, u.dp as gunluk_puan, u.ap as toplam_puan,
       d.created_at at time zone 'Europe/Istanbul' as saat, d.mode, d.status,
       case when d.id is null then null when d.winner = u.user_id then 'KAZANDI' when d.winner is null then 'beraber/iptal' else 'kaybetti' end as sonuc,
       case when d.p1 = u.user_id then d.dl1 else d.dl2 end as puan_degisimi,
       case when d.p1 = u.user_id then d.pay1 else d.pay2 end as klasik_odeme,
       case when d.p1 = u.user_id then d.s1 else d.s2 end as skor, case when d.p1 = u.user_id then d.s2 else d.s1 end as rakip_skor,
       case when d.p1 = u.user_id then d.elg1 else d.elg2 end as etkin_lig
from u left join public.duels d on u.user_id in (d.p1, d.p2) and d.created_at >= now() - interval '2 days'
order by d.created_at;
