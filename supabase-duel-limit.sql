-- Dosya: supabase-duel-limit.sql
-- Kelime Defteri: aynı rakiple 24 saatteki dereceli maç sınırı lige göre değişir
--   Altın ve altı: 3 maç, Platin ve Zümrüt: 2 maç, Elmas ve üstü: 1 maç (iki oyuncudan ligi YÜKSEK olana göre).
-- Ayrıca günlük zorunlu dereceli maç sayımı için kullanıcının kendi dereceli maç zamanlarını döndürür.
-- Supabase SQL Editor'da bir kez çalıştırın (tekrar çalıştırmak zararsızdır).

create or replace function public.duel_pair_ok(a uuid, b uuid) returns boolean language sql stable security definer set search_path = public as $$
  select count(*) < (
    case
      when public.duel_lg(greatest(coalesce((select ap from public.scores where user_id = a), 0),
                                   coalesce((select ap from public.scores where user_id = b), 0))) >= 6 then 1
      when public.duel_lg(greatest(coalesce((select ap from public.scores where user_id = a), 0),
                                   coalesce((select ap from public.scores where user_id = b), 0))) >= 4 then 2
      else 3 end)
  from public.duels d
  where d.mode = 'ranked' and d.status in ('active', 'done') and d.created_at > now() - interval '24 hours'
    and ((d.p1 = a and d.p2 = b) or (d.p1 = b and d.p2 = a))
$$;
revoke all on function public.duel_pair_ok(uuid, uuid) from public, anon, authenticated;

-- kullanıcının kendi dereceli maçlarının başlama zamanları (iptal/geçersiz sayılanlar hariç)
create or replace function public.duel_my_ranked_times(p_since timestamptz) returns setof timestamptz
language sql stable security definer set search_path = public as $$
  select d.created_at from public.duels d
  where auth.uid() is not null and d.mode = 'ranked' and d.status in ('active', 'done')
    and (d.p1 = auth.uid() or d.p2 = auth.uid()) and d.created_at >= p_since
  order by d.created_at
$$;
revoke all on function public.duel_my_ranked_times(timestamptz) from public, anon;
grant execute on function public.duel_my_ranked_times(timestamptz) to authenticated;
