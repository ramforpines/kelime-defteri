-- Dosya: supabase-leaders.sql
-- Kelime Defteri: gün ve hafta liderleri. Geçmiş günlerin/haftaların puanı saklanır; profillerde "N x Gün Lideri / Hafta Lideri",
-- ana sayfada dünün ve geçen haftanın lideri görünür.
-- (Önce supabase-setup.sql, supabase-admin.sql, supabase-theme.sql ve supabase-security.sql çalıştırılmış olmalı.)
-- Not: Sayım bu SQL çalıştırıldığı andan itibaren başlar; geçmiş günlerin puanı daha önce saklanmadığı için geriye dönük sayılamaz.

create table if not exists public.score_history (
  user_id uuid not null references auth.users(id) on delete cascade,
  kind text not null check (kind in ('day', 'week')),
  pk text not null,
  pts numeric not null default 0,
  ans int not null default 0,
  cor int not null default 0,
  primary key (user_id, kind, pk)
);
alter table public.score_history enable row level security;
revoke all on public.score_history from anon, authenticated;

-- Bir kullanıcının satırı yeni güne/haftaya geçerken eski günün/haftanın puanı kaydedilir
create or replace function public.scores_history_fn() returns trigger
language plpgsql security definer set search_path = public as $$
begin
  if old.dk is not null and new.dk is distinct from old.dk and new.dk > old.dk and old.dp > 0 then
    insert into public.score_history(user_id, kind, pk, pts, ans, cor) values (old.user_id, 'day', old.dk, old.dp, old.da, old.dc)
    on conflict (user_id, kind, pk) do update set pts = greatest(score_history.pts, excluded.pts),
      ans = greatest(score_history.ans, excluded.ans), cor = greatest(score_history.cor, excluded.cor);
  end if;
  if old.wk is not null and new.wk is distinct from old.wk and new.wk > old.wk and old.wp > 0 then
    insert into public.score_history(user_id, kind, pk, pts, ans, cor) values (old.user_id, 'week', old.wk, old.wp, old.wa, old.wc)
    on conflict (user_id, kind, pk) do update set pts = greatest(score_history.pts, excluded.pts),
      ans = greatest(score_history.ans, excluded.ans), cor = greatest(score_history.cor, excluded.cor);
  end if;
  return null;
end $$;
drop trigger if exists scores_history_trg on public.scores;
create trigger scores_history_trg after update on public.scores
  for each row execute function public.scores_history_fn();

-- İç yardımcı: bitmiş her gün/hafta için kazanan (yalnızca diğer fonksiyonlar çağırır)
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
      join public.scores s on s.user_id = c.user_id
      join public.profiles p on p.user_id = c.user_id
    where not s.hide and not p.lb_blocked
      and (p.approved or exists (select 1 from public.admins a where a.user_id = c.user_id))
  )
  select distinct on (o.kind, o.pk) o.kind, o.pk, o.user_id, o.pts, o.ans, o.cor
  from ok o, t
  where (o.kind = 'day' and o.pk < t.td) or (o.kind = 'week' and o.pk < t.wk)
  order by o.kind, o.pk, o.pts desc, o.cor desc, o.user_id
$$;
revoke all on function public.leader_winners() from public, anon, authenticated;

-- Dünün ve geçen haftanın lideri
create or replace function public.leaders_info() returns jsonb
language plpgsql security definer stable set search_path = public as $$
declare
  td date := (now() at time zone 'Europe/Istanbul')::date;
  kd text := to_char(td - 1, 'YYYY-MM-DD');
  kw text := to_char(date_trunc('week', now() at time zone 'Europe/Istanbul')::date - 7, 'YYYY-MM-DD');
begin
  if not public.is_approved() then raise exception 'not allowed'; end if;
  return jsonb_build_object(
    'day', (select jsonb_build_object('pk', w.pk, 'id', w.user_id, 'name', s.name, 'un', s.un, 'color', s.color, 'av', s.av, 'fr', s.fr,
                                      'pts', w.pts, 'ans', w.ans, 'cor', w.cor)
            from public.leader_winners() w join public.scores s on s.user_id = w.user_id where w.kind = 'day' and w.pk = kd),
    'week', (select jsonb_build_object('pk', w.pk, 'id', w.user_id, 'name', s.name, 'un', s.un, 'color', s.color, 'av', s.av, 'fr', s.fr,
                                       'pts', w.pts, 'ans', w.ans, 'cor', w.cor)
             from public.leader_winners() w join public.scores s on s.user_id = w.user_id where w.kind = 'week' and w.pk = kw));
end $$;
revoke all on function public.leaders_info() from public, anon;
grant execute on function public.leaders_info() to authenticated;

-- Kaç kez gün / hafta lideri olmuş
create or replace function public.leader_counts() returns table(user_id uuid, d int, w int)
language plpgsql security definer stable set search_path = public as $$
begin
  if not public.is_approved() then raise exception 'not allowed'; end if;
  return query select x.user_id, (count(*) filter (where x.kind = 'day'))::int, (count(*) filter (where x.kind = 'week'))::int
    from public.leader_winners() x group by x.user_id;
end $$;
revoke all on function public.leader_counts() from public, anon;
grant execute on function public.leader_counts() to authenticated;
