-- Dosya: supabase-duel-history.sql
-- Kelime Defteri: tüm tamamlanmış düelloların herkese açık maç geçmişi (oyuncular + maç puanları).
-- Supabase SQL Editor'da bir kez çalıştır. Tabloyu açmaz; yalnızca bu fonksiyon yalnız gerekli alanları döndürür.
drop function if exists public.duel_history(int);
create or replace function public.duel_history(n int default 50) returns table(id uuid, p1 uuid, p2 uuid, s1 numeric, s2 numeric, c1 int, c2 int, a1 int, a2 int, t1 numeric, t2 numeric, winner uuid, created_at timestamptz)
language sql stable security definer set search_path = public as $$
  select d.id, d.p1, d.p2, d.s1::numeric, d.s2::numeric, d.c1::int, d.c2::int, d.a1::int, d.a2::int, d.t1::numeric, d.t2::numeric, d.winner, d.created_at
  from public.duels d
  where d.status = 'done' and auth.uid() is not null
  order by d.created_at desc
  limit least(greatest(coalesce(n, 50), 1), 100);
$$;
revoke all on function public.duel_history(int) from public, anon;
grant execute on function public.duel_history(int) to authenticated;
