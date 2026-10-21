-- Dosya: supabase-duel-guard.sql
-- Kelime Defteri: dereceli düelloda uygulamadan ayrılma (hile) koruması. ŞİMDİLİK YALNIZCA YÖNETİCİ VE TEST HESABI (kullanici52541) İÇİN ÇALIŞIR.
-- SQL Editor'da bir kez çalıştır (önce supabase-admin.sql ve dereceli düello dosyaları çalışmış olmalı). Birden çok kez çalıştırılabilir.
--  * duels.status artık 'void' (iptal) değeri de alabilir; iptal edilen maç puan, geçmiş ve galibiyet sayısına girmez.
--  * duel_flags: ayrılma/odak kaybı kayıtları (yalnızca yönetici fonksiyonlarıyla okunur).
--    Türler: hide (maçı iptal eder), hide_short (1 sn'den kısa, yalnızca kayıt), hide_off (çevrimdışıyken, yalnızca kayıt), blur (uyarı), blur2 (iptal), trap (tuzak düğmeye tıklandı, yalnızca kayıt).
--  * duel_guard: istemci bildirir; yönetici ya da test hesabı değilse hiçbir şey yapmaz.
--  * Ceza kademesi (7 gün): 1. ayrılma yalnızca uyarı, 2. normal yenilgi puanı, 3. 1,5 katı, 4. 2 katı + 15 dk dereceli mola, 5. 1 saat, 6. 3 saat, 7+ hep 2 katı + 12 saat.
--    Test grubu (yönetici + test hesabı) maçlarında puan kesilmez, yalnızca ne kesileceği gösterilir. Gerek: supabase-duel-test.sql (duel_is_test).
--  * Herkese açmak için duel_guard_user() fonksiyonunu 'select true' yap.
--  * duel_flag_list: yönetici listesi.

alter table public.duels drop constraint if exists duels_status_check;
alter table public.duels add constraint duels_status_check check (status in ('active','done','void','test'));
alter table public.duels add column if not exists void_reason text;
alter table public.duels add column if not exists void_by uuid;

create table if not exists public.duel_flags (
  id bigserial primary key,
  duel_id uuid references public.duels(id) on delete cascade,
  user_id uuid not null references auth.users(id) on delete cascade,
  kind text not null,
  q int,
  away_ms int,
  created_at timestamptz not null default now()
);
alter table public.duel_flags drop constraint if exists duel_flags_kind_check;
alter table public.duel_flags add constraint duel_flags_kind_check check (kind in ('hide','hide_short','hide_off','blur','blur2','trap'));
create index if not exists duel_flags_user_idx on public.duel_flags(user_id, created_at desc);
alter table public.duel_flags enable row level security;
revoke all on public.duel_flags from anon, authenticated;

-- ceza: ayrılan oyuncu kural ihlali sayılır. 1. ayrılma yalnızca uyarı (maç iptal, puan yok), sonrası puan cezası.
alter table public.duels add column if not exists pen_lv int;
alter table public.duels add column if not exists pen1 numeric;
alter table public.duels add column if not exists pen2 numeric;
alter table public.duels add column if not exists pen_t boolean;
create table if not exists public.duel_bans (user_id uuid primary key references auth.users(id) on delete cascade, until timestamptz not null);
alter table public.duel_bans enable row level security;
revoke all on public.duel_bans from anon, authenticated;

create or replace function public.duel_ban_left() returns int
language sql stable security definer set search_path = public as $$
  select coalesce((select greatest(0, ceil(extract(epoch from (b.until - now()))))::int from public.duel_bans b where b.user_id = auth.uid()), 0)
$$;
revoke all on function public.duel_ban_left() from public, anon;
grant execute on function public.duel_ban_left() to authenticated;

create or replace function public.duel_guard_user() returns boolean
language sql stable security definer set search_path = public as $$
  select public.is_admin()
      or coalesce((select lower(split_part(u.email, '@', 1)) = any (array['kullanici52541']) from auth.users u where u.id = auth.uid()), false)
$$;
revoke all on function public.duel_guard_user() from public, anon;
grant execute on function public.duel_guard_user() to authenticated;

create or replace function public.duel_guard(did uuid, p_kind text, p_q int default null, p_away int default null) returns jsonb
language plpgsql security definer set search_path = public as $$
declare uid uuid := auth.uid(); d public.duels; fid bigint; wk int; v_n int; v_lv int := 0; v_mult numeric := 0; v_pen numeric := 0; v_test boolean := false; v_ban int := 0; v_share numeric; v_lk numeric; v_ok numeric; v_base numeric; v_so numeric; v_sm numeric;
begin
  if uid is null then raise exception 'not allowed'; end if;
  select * into d from public.duels where id = did for update;
  if not found or uid not in (d.p1, d.p2) then raise exception 'not allowed'; end if;
  if p_kind not in ('hide','hide_short','hide_off','blur','blur2','trap') then raise exception 'bad kind'; end if;
  -- şimdilik yalnızca yönetici ve test hesabı: diğer kullanıcılar için kayıt da iptal de yok
  if not public.duel_guard_user() then return jsonb_build_object('status', d.status, 'voids', 0); end if;
  if p_away is not null then
    select max(id) into fid from public.duel_flags where duel_id = did and user_id = uid and kind = p_kind and away_ms is null;
    if fid is not null then update public.duel_flags set away_ms = p_away where id = fid; end if;
  end if;
  if p_away is null or fid is null then
    insert into public.duel_flags(duel_id, user_id, kind, q, away_ms) values (did, uid, p_kind, p_q, p_away);
  end if;
  if d.status = 'active' and d.mode = 'ranked' and p_kind in ('hide','blur2') then
    -- kademe: son 7 günde iptal ettirdiği maç sayısı + 1
    select count(*) into v_n from public.duels where void_by = uid and status = 'void' and id <> did and done_at >= now() - interval '7 days';
    v_lv := v_n + 1;
    v_mult := case when v_lv <= 1 then 0 when v_lv = 2 then 1 when v_lv = 3 then 1.5 else 2 end;
    v_test := coalesce(public.duel_is_test(d.p1), false) and coalesce(public.duel_is_test(d.p2), false);
    if v_mult > 0 then
      -- normal yenilgi puanı: rakip galip sayılır, pay en az 0,5
      v_sm := greatest(case when uid = d.p1 then d.s1 else d.s2 end, 0);
      v_so := greatest(case when uid = d.p1 then d.s2 else d.s1 end, 0);
      v_share := greatest(0.5, case when v_sm + v_so = 0 then 0.5 else v_so / (v_sm + v_so) end);
      v_lk := coalesce(case when uid = d.p1 then d.rk1 else d.rk2 end, 0);
      v_ok := coalesce(case when uid = d.p1 then d.rk2 else d.rk1 end, 0);
      v_base := round(least(v_lk * v_share, 4 * v_ok), 1);
      v_pen := round(v_base * v_mult, 1);
    end if;
    v_ban := case when v_lv <= 3 then 0 when v_lv = 4 then 900 when v_lv = 5 then 3600 when v_lv = 6 then 10800 else 43200 end;   -- mola: 15 dk, 1 sa, 3 sa, en çok 12 sa (7. ve sonrası hep 12 sa)
    if v_ban > 0 then
      insert into public.duel_bans(user_id, until) values (uid, now() + make_interval(secs => v_ban))
      on conflict (user_id) do update set until = excluded.until;
    end if;
    update public.duels set status = 'void', void_reason = p_kind, void_by = uid, done_at = now(),
      pen_lv = v_lv, pen_t = v_test,
      pen1 = case when uid = p1 then v_pen end, pen2 = case when uid = p2 then v_pen end,
      dl1 = case when uid = p1 and v_pen > 0 and not v_test then -v_pen end,
      dl2 = case when uid = p2 and v_pen > 0 and not v_test then -v_pen end
    where id = did;
  end if;
  select count(*) into wk from public.duels where void_by = uid and status = 'void' and done_at >= now() - interval '7 days';
  return jsonb_build_object('status', (select status from public.duels where id = did), 'voids', wk, 'lv', v_lv, 'pen', v_pen, 'ban', v_ban);
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
