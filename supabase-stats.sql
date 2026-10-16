-- Dosya: supabase-stats.sql
-- Kelime Defteri: uygulama geneli istatistikler + çevrimiçi durumu. SQL Editor'da bir kez çalıştır.
-- (Önce supabase-admin.sql, supabase-chat.sql ve supabase-duel.sql çalıştırılmış olmalı.)

alter table public.profiles add column if not exists last_seen timestamptz;
alter table public.scores add column if not exists dn int not null default 0;

-- Uygulama açıkken periyodik "buradayım" bilgisi
create or replace function public.app_ping() returns void
language sql security definer set search_path = public as $$
  update public.profiles set last_seen = now() where user_id = auth.uid()
$$;
revoke all on function public.app_ping() from public, anon;
grant execute on function public.app_ping() to authenticated;

-- Onaylı herkesin gördüğü genel sayılar (kişisel veri yok)
create or replace function public.app_stats() returns jsonb
language plpgsql security definer stable set search_path = public as $$
declare
  tz text := 'Europe/Istanbul';
  tk text := to_char(now() at time zone tz, 'YYYY-MM-DD');
  d0 timestamptz := date_trunc('day', now() at time zone tz) at time zone tz;
  r jsonb;
begin
  if not public.is_approved() then raise exception 'not allowed'; end if;
  select jsonb_build_object(
    'online',      (select count(*) from public.profiles where last_seen > now() - interval '2 minutes'),
    'dau',         (select count(*) from public.profiles where last_seen >= d0),
    'users',       (select count(*) from public.profiles where approved or user_id in (select user_id from public.admins)),
    'solved_today',(select coalesce(sum(da), 0) from public.scores where dk = tk),
    'solved_total',(select coalesce(sum(ans), 0) from public.scores),
    'correct_total',(select coalesce(sum(cor), 0) from public.scores),
    'learned_today',(select coalesce(sum(dn), 0) from public.scores where dk = tk),
    'learned_total',(select coalesce(sum(lrn), 0) from public.scores),
    'best_streak', (select coalesce(max(st), 0) from public.scores),
    'duels_today', (select count(*) from public.duels where created_at >= d0),
    'duels_total', (select count(*) from public.duels),
    'msgs_today',  (select count(*) from public.chat_messages where to_user is null and created_at >= d0),
    'leader',      (select jsonb_build_object('name', name, 'pts', dp) from public.scores where dk = tk and dp > 0 order by dp desc limit 1),
    'duel_king',   (select jsonb_build_object('name', coalesce(s.name, '?'), 'wins', w.n)
                    from (select winner, count(*) n from public.duels where winner is not null group by winner order by n desc limit 1) w
                    left join public.scores s on s.user_id = w.winner)
  ) into r;
  return r;
end $$;
revoke all on function public.app_stats() from public, anon;
grant execute on function public.app_stats() to authenticated;

-- Yönetici: ayrıntılı rapor (son 14 gün serileri dahil)
create or replace function public.admin_stats() returns jsonb
language plpgsql security definer stable set search_path = public as $$
declare
  tz text := 'Europe/Istanbul';
  d0 timestamptz := date_trunc('day', now() at time zone tz) at time zone tz;
  r jsonb;
begin
  if not public.is_admin() then raise exception 'not allowed'; end if;
  select jsonb_build_object(
    'online',   (select count(*) from public.profiles where last_seen > now() - interval '2 minutes'),
    'online15', (select count(*) from public.profiles where last_seen > now() - interval '15 minutes'),
    'dau',      (select count(*) from public.profiles where last_seen >= d0),
    'wau',      (select count(*) from public.profiles where last_seen >= now() - interval '7 days'),
    'mau',      (select count(*) from public.profiles where last_seen >= now() - interval '30 days'),
    'total',    (select count(*) from public.profiles),
    'pending',  (select count(*) from public.profiles where not approved and user_id not in (select user_id from public.admins)),
    'new_today',(select count(*) from public.profiles where created_at >= d0),
    'new_7d',   (select count(*) from public.profiles where created_at >= now() - interval '7 days'),
    'never',    (select count(*) from public.profiles p where not exists (select 1 from public.scores s where s.user_id = p.user_id and s.ans > 0)),
    'fb_open',  (select count(*) from public.feedback where status = 'new'),
    'duels_done',(select count(*) from public.duels where status = 'done'),
    'duels_active',(select count(*) from public.duels where status = 'active'),
    'duel_queue',(select count(*) from public.duel_queue),
    'msgs_total',(select count(*) from public.chat_messages where to_user is null),
    'dms_total', (select count(*) from public.chat_messages where to_user is not null),
    'dms_today', (select count(*) from public.chat_messages where to_user is not null and created_at >= d0),
    'avg_points',(select coalesce(round(avg(ap)::numeric, 1), 0) from public.scores),
    'series', (select coalesce(jsonb_agg(jsonb_build_object('d', to_char(g.d, 'YYYY-MM-DD'),
        'duels',  (select count(*) from public.duels x where (x.created_at at time zone tz)::date = g.d),
        'msgs',   (select count(*) from public.chat_messages x where x.to_user is null and (x.created_at at time zone tz)::date = g.d),
        'joined', (select count(*) from public.profiles x where (x.created_at at time zone tz)::date = g.d),
        'active', (select count(*) from public.profiles x where (x.last_seen at time zone tz)::date = g.d)
      ) order by g.d), '[]'::jsonb)
      from generate_series(((now() at time zone tz)::date - 13), (now() at time zone tz)::date, interval '1 day') as g(d)),
    'top_today', (select coalesce(jsonb_agg(jsonb_build_object('name', t.name, 'un', t.un, 'pts', t.dp, 'cor', t.dc, 'ans', t.da)), '[]'::jsonb)
      from (select name, un, dp, dc, da from public.scores where dk = to_char(now() at time zone tz, 'YYYY-MM-DD') and dp > 0 order by dp desc limit 5) t)
  ) into r;
  return r;
end $$;
revoke all on function public.admin_stats() from public, anon;
grant execute on function public.admin_stats() to authenticated;
