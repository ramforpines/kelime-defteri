-- Bir kullanıcının son 2 günkü düello sonuçlarını ve günlük puanını inceler (salt okunur). İsim kalıbı giriş kullanıcı adına bakar (profiles.username).
select p.username, s.name, s.dk as gun, s.dp as gunluk_puan, s.ap as toplam_puan,
       d.created_at at time zone 'Europe/Istanbul' as saat, d.mode, d.status,
       case when d.id is null then null when d.winner = p.user_id then 'KAZANDI' when d.winner is null then 'beraber/iptal' else 'kaybetti' end as sonuc,
       case when d.p1 = p.user_id then d.dl1 else d.dl2 end as puan_degisimi,
       case when d.p1 = p.user_id then d.pay1 else d.pay2 end as klasik_odeme,
       case when d.p1 = p.user_id then d.s1 else d.s2 end as skor,
       case when d.p1 = p.user_id then d.s2 else d.s1 end as rakip_skor,
       case when d.p1 = p.user_id then d.elg1 else d.elg2 end as etkin_lig
from public.profiles p
left join public.scores s on s.user_id = p.user_id
left join public.duels d on p.user_id in (d.p1, d.p2) and d.created_at >= now() - interval '2 days'
where p.username ilike '%kaan%'
order by d.created_at;
