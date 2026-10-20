-- Dosya: supabase-duel-guard.sql
-- Kelime Defteri: dereceli düelloda uygulamadan ayrılma (hile) koruması. ŞİMDİLİK YALNIZCA YÖNETİCİ İÇİN ÇALIŞIR.
-- SQL Editor'da bir kez çalıştır (önce supabase-admin.sql ve dereceli düello dosyaları çalışmış olmalı). Birden çok kez çalıştırılabilir.
--  * duels.status artık 'void' (iptal) değeri de alabilir; iptal edilen maç puan, geçmiş ve galibiyet sayısına girmez.
--  * duel_flags: ayrılma/odak kaybı kayıtları (yalnızca yönetici fonksiyonlarıyla okunur).
--  * duel_guard: istemci bildirir; yönetici değilse hiçbir şey yapmaz.
--  * duel_flag_list: yönetici listesi.

alter table public.duels drop constraint if exists duels_status_check;
alter table public.duels add constraint duels_status_check check (status in ('active','done','void'));
alter table public.duels add column if not exists void_reason text;
alter table public.duels add column if not exists void_by uuid;

create table if not exists public.duel_flags (
  id bigserial primary key,
  duel_id uuid references public.duels(id) on delete cascade,
  user_id uuid not null references auth.users(id) on delete cascade,
  kind text not null check (kind in ('hide','blur','blur2')),
  q int,
  away_ms int,
  created_at timestamptz not null default now()
);
create index if not exists duel_flags_user_idx on public.duel_flags(user_id, created_at desc);
alter table public.duel_flags enable row level security;
revoke all on public.duel_flags from anon, authenticated;

create or replace function public.duel_guard(did uuid, p_kind text, p_q int default null, p_away int default null) returns jsonb
language plpgsql security definer set search_path = public as $$
declare uid uuid := auth.uid(); d public.duels; fid bigint; wk int;
begin
  if uid is null then raise exception 'not allowed'; end if;
  select * into d from public.duels where id = did for update;
  if not found or uid not in (d.p1, d.p2) then raise exception 'not allowed'; end if;
  if p_kind not in ('hide','blur','blur2') then raise exception 'bad kind'; end if;
  -- şimdilik yalnızca yönetici: diğer kullanıcılar için kayıt da iptal de yok
  if not public.is_admin() then return jsonb_build_object('status', d.status, 'voids', 0); end if;
  if p_away is not null then
    select max(id) into fid from public.duel_flags where duel_id = did and user_id = uid and kind = p_kind and away_ms is null;
    if fid is not null then update public.duel_flags set away_ms = p_away where id = fid; end if;
  end if;
  if p_away is null or fid is null then
    insert into public.duel_flags(duel_id, user_id, kind, q, away_ms) values (did, uid, p_kind, p_q, p_away);
  end if;
  if d.status = 'active' and d.mode = 'ranked' and p_kind in ('hide','blur2') then
    update public.duels set status = 'void', void_reason = p_kind, void_by = uid, done_at = now() where id = did;
  end if;
  select count(*) into wk from public.duels where void_by = uid and status = 'void' and done_at >= now() - interval '7 days';
  return jsonb_build_object('status', (select status from public.duels where id = did), 'voids', wk);
end $$;
revoke all on function public.duel_guard(uuid, text, int, int) from public, anon;
grant execute on function public.duel_guard(uuid, text, int, int) to authenticated;

create or replace function public.duel_flag_list(n int default 100)
returns table(id bigint, user_id uuid, name text, un text, kind text, q int, away_ms int, created_at timestamptz, voided boolean, wk int)
language plpgsql stable security definer set search_path = public as $$
begin
  if not public.is_admin() then raise exception 'not allowed'; end if;
  return query
  select f.id, f.user_id, s.name::text, s.un::text, f.kind, f.q, f.away_ms, f.created_at,
         (d.status = 'void' and d.void_by = f.user_id) as voided,
         (select count(*)::int from public.duels v where v.void_by = f.user_id and v.status = 'void' and v.done_at >= now() - interval '7 days') as wk
  from public.duel_flags f
  left join public.scores s on s.user_id = f.user_id
  left join public.duels d on d.id = f.duel_id
  order by f.created_at desc limit least(greatest(coalesce(n, 100), 1), 300);
end $$;
revoke all on function public.duel_flag_list(int) from public, anon;
grant execute on function public.duel_flag_list(int) to authenticated;
