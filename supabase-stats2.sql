-- Dosya: supabase-stats2.sql
-- Kelime Defteri: Yönetici istatistiklerine "çözülen soru sayısı" grafiği. SQL Editor'da bir kez çalıştır.
-- (Önce supabase-stats.sql çalıştırılmış olmalı.)
-- Her kullanıcının kayıtlı ilerlemesindeki günlük cevap sayılarını (days -> a, c) toplar. Kişisel veri döndürmez.

create or replace function public.admin_solved_series(n int default 30) returns jsonb
language plpgsql security definer stable set search_path = public as $$
declare
  tz text := 'Europe/Istanbul';
  r jsonb;
begin
  if not public.is_admin() then raise exception 'not allowed'; end if;
  n := greatest(7, least(coalesce(n, 30), 90));
  select coalesce(jsonb_agg(jsonb_build_object('d', to_char(g.d, 'YYYY-MM-DD'), 'a', coalesce(t.a, 0), 'c', coalesce(t.c, 0)) order by g.d), '[]'::jsonb)
  into r
  from generate_series(((now() at time zone tz)::date - (n - 1)), (now() at time zone tz)::date, interval '1 day') as g(d)
  left join (
    select e.key as dk,
           sum(coalesce(nullif(e.value->>'a', '')::numeric, 0)) as a,
           sum(coalesce(nullif(e.value->>'c', '')::numeric, 0)) as c
    from public.user_state u,
         lateral jsonb_each(case when jsonb_typeof(u.state->'days') = 'object' then u.state->'days' else '{}'::jsonb end) e
    group by e.key
  ) t on t.dk = to_char(g.d, 'YYYY-MM-DD');
  return r;
end $$;
revoke all on function public.admin_solved_series(int) from public, anon;
grant execute on function public.admin_solved_series(int) to authenticated;
