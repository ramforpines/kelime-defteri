-- Maç geçmişi sayfalama: klasik ve dereceli ayrı, istenen kadar eskiye kaydırılır (sayfa başına en çok 100).
-- Gerek: supabase-duel-ranked.sql (duels.mode, dl1, dl2). SQL Editor'da bir kez çalıştırın.
create or replace function public.duel_history_page(p_mode text default 'classic', p_off int default 0, p_n int default 50)
returns table(id uuid, p1 uuid, p2 uuid, s1 numeric, s2 numeric, c1 int, c2 int, a1 int, a2 int, t1 numeric, t2 numeric, winner uuid, created_at timestamptz, mode text, dl1 numeric, dl2 numeric)
language sql stable security definer set search_path = public as $$
  select d.id, d.p1, d.p2, d.s1::numeric, d.s2::numeric, d.c1::int, d.c2::int, d.a1::int, d.a2::int, d.t1::numeric, d.t2::numeric, d.winner, d.created_at, d.mode, d.dl1, d.dl2
  from public.duels d
  where d.status = 'done' and auth.uid() is not null
    and ((p_mode = 'ranked' and d.mode = 'ranked') or (p_mode <> 'ranked' and coalesce(d.mode, 'classic') <> 'ranked'))
  order by d.created_at desc, d.id
  limit least(greatest(coalesce(p_n, 50), 1), 100) offset greatest(coalesce(p_off, 0), 0);
$$;
revoke all on function public.duel_history_page(text, int, int) from public, anon;
grant execute on function public.duel_history_page(text, int, int) to authenticated;
