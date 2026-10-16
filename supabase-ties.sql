-- Dosya: supabase-ties.sql
-- Kelime Defteri: eşitlikte ödül/rol paylaşılır. Gün/hafta lideri, "Günün lideri" ve "En çok düello kazanan" için
-- aynı puana sahip herkes birlikte lider sayılır (hepsine "x Gün Lideri / Hafta Lideri" yazılır).
-- (Önce supabase-leaders.sql ve supabase-stats.sql çalıştırılmış olmalı.)

drop function if exists public.leader_winners();
create or replace function public.leader_winners()
returns table(kind text, pk text, user_id uuid, pts numeric, ans int, cor int)
language sql security definer stable set search_path = public as $$
  with t as (
    select to_char(now() at time zone 'Europe/Istanbul', 'YYYY-MM-DD') as td,
           to_char(date_trunc('week', now() at time zone 'Europe/Istanbul'), 'YYYY-MM-DD') as wk
  ), cand as (
    select s.user_id, 'day'::text as kind, s.dk as pk, s.dp as pts, s.da as ans, s.dc as cor from public.scores s where s.dk is not null and s.dp > 0
    union all
    select s.user_id, 'week', s.wk, s.wp, s.wa, s.wc from public.scores s where s.wk is not null and s.wp > 0
    union all
    select h.user_id, h.kind, h.pk, h.pts, h.ans, h.cor from public.score_history h where h.pts > 0
  ), ok as (
    select c.* from cand c
      join public.profiles p on p.user_id = c.user_id
    where p.approved or exists (select 1 from public.admins a where a.user_id = c.user_id)
  ), rk as (
    select o.*, rank() over (partition by o.kind, o.pk order by o.pts desc) as r
    from ok o, t
    where (o.kind = 'day' and o.pk < t.td) or (o.kind = 'week' and o.pk < t.wk)
  )
  select rk.kind, rk.pk, rk.user_id, rk.pts, rk.ans, rk.cor from rk where rk.r = 1
$$;
revoke all on function public.leader_winners() from public, anon, authenticated;

-- Dünün ve geçen haftanın lider(ler)i (eşitlikte birden fazla kişi)
create or replace function public.leaders_info() returns jsonb
language plpgsql security definer stable set search_path = public as $$
declare
  td date := (now() at time zone 'Europe/Istanbul')::date;
  kd text := to_char(td - 1, 'YYYY-MM-DD');
  kw text := to_char(date_trunc('week', now() at time zone 'Europe/Istanbul')::date - 7, 'YYYY-MM-DD');
begin
  if not public.is_approved() then raise exception 'not allowed'; end if;
  return jsonb_build_object(
    'day', (select jsonb_agg(jsonb_build_object('pk', w.pk, 'id', w.user_id, 'name', s.name, 'un', s.un, 'color', s.color, 'av', s.av, 'fr', s.fr,
                                      'pts', w.pts, 'ans', w.ans, 'cor', w.cor) order by s.name)
            from public.leader_winners() w join public.scores s on s.user_id = w.user_id where w.kind = 'day' and w.pk = kd),
    'week', (select jsonb_agg(jsonb_build_object('pk', w.pk, 'id', w.user_id, 'name', s.name, 'un', s.un, 'color', s.color, 'av', s.av, 'fr', s.fr,
                                       'pts', w.pts, 'ans', w.ans, 'cor', w.cor) order by s.name)
             from public.leader_winners() w join public.scores s on s.user_id = w.user_id where w.kind = 'week' and w.pk = kw));
end $$;
revoke all on function public.leaders_info() from public, anon;
grant execute on function public.leaders_info() to authenticated;

-- Uygulama geneli sayılar: günün lideri ve düello kralı eşitlikte hepsi
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
    'leader',      (select jsonb_build_object('name', string_agg(coalesce(name, '?'), ', ' order by name), 'pts', max(dp))
                    from public.scores where dk = tk and dp > 0 and dp = (select max(dp) from public.scores where dk = tk and dp > 0)),
    'duel_king',   (select jsonb_build_object('name', string_agg(coalesce(s.name, '?'), ', ' order by s.name), 'wins', max(w.n))
                    from (select winner, count(*) n from public.duels where winner is not null group by winner) w
                    left join public.scores s on s.user_id = w.winner
                    where w.n = (select max(c) from (select count(*) c from public.duels where winner is not null group by winner) z))
  ) into r;
  return r;
end $$;
revoke all on function public.app_stats() from public, anon;
grant execute on function public.app_stats() to authenticated;
