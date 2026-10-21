-- Dosya: supabase-duel-ceza.sql
-- Kelime Defteri: dereceli düello ayrılma / odak kaybı cezaları (HERKES İÇİN). supabase-duel-guard.sql ve supabase-duel-test.sql'in yerine geçer.
-- SQL Editor'da bir kez çalıştır; birden çok kez çalıştırılabilir. Önce diğer düello dosyaları (ranked, final, speed, history, tie, pool45...) çalışmış olmalı.
--
-- Maç içi sayaçlar (aynı düello):
--   * Uygulamadan ayrılma (1 sn'den uzun, çevrimiçi): 1. uyarı (o an açık soru 0 puan), 2. maç iptal.
--   * Ekran odağı kaybı (700 ms üstü): 1. ve 2. uyarı, 3. maç iptal.
--   * Çevrimdışı ayrılma ve 1 sn'den kısa ayrılma: yalnızca kayıt (hide_off, hide_short). Tuzak düğme: yalnızca kayıt (trap).
-- İptal olunca:
--   * İptal ettiren: normal yenilgi puanı ×1, ×1,5, ×2 (15 günlük sayaç: 1., 2., 3.+ iptal). Rakibe kaybedilen puanın %20'si verilir.
--   * Dereceli cezası (süre): 3, 5, 15, 30, 60, 360, 720 dk (1.-7.+ iptal, 15 gün içinde). Sunucu join/invite/respond'da kontrol eder.
--   * Ceza kartında kullanıcı kurallara uyacağına söz verir (duel_pen_ack); söz verilmeden dereceli maç aranamaz, teklif gönderilemez/kabul edilemez.
--   * Klasik düello etkilenmez.
-- Yönetici: duel_admin_* fonksiyonları (özet, vakalar, ceza kayıtları, uyarı, ceza ver, ceza kaldır, puan iade).

-- 0) Test kısıtı kalktı: herkes herkesle oynar, maçlar normal kaydedilir.
create or replace function public.duel_is_test(u uuid) returns boolean
language sql stable security definer set search_path = public as $$ select false $$;
revoke all on function public.duel_is_test(uuid) from public, anon, authenticated;

-- 1) Tablolar ve sütunlar
alter table public.duels drop constraint if exists duels_status_check;
alter table public.duels add constraint duels_status_check check (status in ('active','done','void','test'));
alter table public.duels add column if not exists void_reason text;
alter table public.duels add column if not exists void_by uuid;
alter table public.duels add column if not exists pen_lv int;
alter table public.duels add column if not exists pen1 numeric;
alter table public.duels add column if not exists pen2 numeric;
alter table public.duels add column if not exists pen_t boolean;
alter table public.duels add column if not exists pen_ban int;     -- dakika
alter table public.duels add column if not exists pen_rf boolean;  -- yönetici puan iadesi yaptı
alter table public.duels add column if not exists pen_ack timestamptz;  -- ceza alan kullanıcının kurallara uyacağına söz verdiği an
alter table public.duels add column if not exists zq1 int;         -- uyarı alınan ayrılmada 0 puan sayılan soru
alter table public.duels add column if not exists zq2 int;
alter table public.duels add column if not exists dl1 numeric(9,1);
alter table public.duels add column if not exists dl2 numeric(9,1);

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
create index if not exists duel_flags_duel_idx on public.duel_flags(duel_id, user_id, kind);
alter table public.duel_flags enable row level security;
revoke all on public.duel_flags from anon, authenticated;

create table if not exists public.duel_bans (user_id uuid primary key references auth.users(id) on delete cascade, until timestamptz not null);
alter table public.duel_bans add column if not exists lv int;
alter table public.duel_bans add column if not exists source text;
alter table public.duel_bans enable row level security;
revoke all on public.duel_bans from anon, authenticated;

-- ceza ve yönetici işlem kayıtları (kullanıcının aldığı tüm cezalar burada)
create table if not exists public.duel_penalties (
  id bigserial primary key,
  user_id uuid not null references auth.users(id) on delete cascade,
  duel_id uuid references public.duels(id) on delete cascade,
  kind text not null,          -- auto, admin_ban, admin_unban, admin_warn, admin_refund
  lv int,
  pts numeric,                 -- kesilen puan (pozitif sayı)
  ban_min int,
  note text,
  by_user uuid,
  created_at timestamptz not null default now()
);
create index if not exists duel_penalties_user_idx on public.duel_penalties(user_id, created_at desc);
alter table public.duel_penalties enable row level security;
revoke all on public.duel_penalties from anon, authenticated;

create table if not exists public.duel_notices (
  id bigserial primary key,
  user_id uuid not null references auth.users(id) on delete cascade,
  msg text not null,
  created_at timestamptz not null default now(),
  seen boolean not null default false
);
create index if not exists duel_notices_user_idx on public.duel_notices(user_id, seen);
alter table public.duel_notices enable row level security;
revoke all on public.duel_notices from anon, authenticated;

-- 2) Ceza süresi (saniye); iç kullanım
create or replace function public.duel_pen_left(u uuid) returns int
language sql stable security definer set search_path = public as $$
  select coalesce((select greatest(0, ceil(extract(epoch from (b.until - now()))))::int from public.duel_bans b where b.user_id = u), 0)
$$;
revoke all on function public.duel_pen_left(uuid) from public, anon, authenticated;

-- kullanıcının kendi cezası (kalan saniye)
create or replace function public.duel_ban_left() returns int
language sql stable security definer set search_path = public as $$
  select public.duel_pen_left(auth.uid())
$$;
revoke all on function public.duel_ban_left() from public, anon;
grant execute on function public.duel_ban_left() to authenticated;

-- dereceliye girişi engelleyen durum: ceza süresi sürüyor VEYA ceza kartındaki söz henüz verilmedi
create or replace function public.duel_pen_block(u uuid) returns boolean
language sql stable security definer set search_path = public as $$
  select public.duel_pen_left(u) > 0
      or exists(select 1 from public.duels d where d.void_by = u and d.status = 'void' and d.pen_lv is not null
                and d.pen_ack is null and coalesce(d.pen_rf, false) = false and coalesce(d.pen_t, false) = false)
$$;
revoke all on function public.duel_pen_block(uuid) from public, anon, authenticated;

-- ceza kartı bilgileri: kalan süre ve söz verilmemiş cezalar
create or replace function public.duel_pen_info() returns jsonb
language plpgsql stable security definer set search_path = public as $$
declare uid uuid := auth.uid(); items jsonb;
begin
  if uid is null then raise exception 'not allowed'; end if;
  select coalesce(jsonb_agg(jsonb_build_object('id', d.id, 'at', coalesce(d.done_at, d.created_at), 'opp', o.name,
           'kind', d.void_reason, 'pen', coalesce(case when uid = d.p1 then d.pen1 else d.pen2 end, 0),
           'gain', coalesce(case when uid = d.p1 then d.dl2 else d.dl1 end, 0), 'ban', d.pen_ban, 'lv', d.pen_lv) order by d.done_at desc), '[]'::jsonb)
    into items
  from public.duels d
  left join public.scores o on o.user_id = (case when uid = d.p1 then d.p2 else d.p1 end)
  where d.void_by = uid and d.status = 'void' and d.pen_lv is not null and d.pen_ack is null
        and coalesce(d.pen_rf, false) = false and coalesce(d.pen_t, false) = false;
  return jsonb_build_object('left', public.duel_pen_left(uid), 'until', (select b.until from public.duel_bans b where b.user_id = uid), 'items', items);
end $$;
revoke all on function public.duel_pen_info() from public, anon;
grant execute on function public.duel_pen_info() to authenticated;

-- söz ver: kullanıcının tüm bekleyen cezaları onaylanır
create or replace function public.duel_pen_ack() returns int
language plpgsql security definer set search_path = public as $$
declare uid uuid := auth.uid(); n int;
begin
  if uid is null then raise exception 'not allowed'; end if;
  update public.duels set pen_ack = now() where void_by = uid and status = 'void' and pen_lv is not null and pen_ack is null;
  get diagnostics n = row_count;
  if n > 0 then insert into public.duel_penalties(user_id, kind, note) values (uid, 'user_ack', 'Kurallara uyacağına söz verdi'); end if;
  return n;
end $$;
revoke all on function public.duel_pen_ack() from public, anon;
grant execute on function public.duel_pen_ack() to authenticated;

-- 3) Ayrılma / odak kaybı bildirimi
drop function if exists public.duel_guard(uuid, text, int, int);
create or replace function public.duel_guard(did uuid, p_kind text, p_q int default null, p_away int default null) returns jsonb
language plpgsql security definer set search_path = public as $$
declare uid uuid := auth.uid(); d public.duels; fid bigint; kd text := p_kind; v_n int := 0; v_lv int := 0; v_mult numeric := 1; v_pen numeric := 0; v_opp numeric := 0;
        v_ban int := 0; v_share numeric; v_lk numeric; v_ok numeric; v_base numeric; v_so numeric; v_sm numeric; v_void boolean := false; v_warn boolean := false;
        v_zq int; v_opp_id uuid; v_vc int;
begin
  if uid is null then raise exception 'not allowed'; end if;
  select * into d from public.duels where id = did for update;
  if not found or uid not in (d.p1, d.p2) then raise exception 'not allowed'; end if;
  if kd = 'blur2' then kd := 'blur'; end if;
  if kd not in ('hide','hide_short','hide_off','blur','trap') then raise exception 'bad kind'; end if;
  v_opp_id := case when uid = d.p1 then d.p2 else d.p1 end;
  if p_away is not null then
    select max(id) into fid from public.duel_flags where duel_id = did and user_id = uid and kind = kd and away_ms is null;
    if fid is not null then update public.duel_flags set away_ms = p_away where id = fid; end if;
  end if;
  if p_away is null or fid is null then
    insert into public.duel_flags(duel_id, user_id, kind, q, away_ms) values (did, uid, kd, p_q, p_away);
  end if;

  if d.status = 'active' and d.mode = 'ranked' and kd in ('hide','blur') then
    select count(*) into v_n from public.duel_flags where duel_id = did and user_id = uid and kind = kd;
    if kd = 'hide' then
      if v_n >= 2 then v_void := true; else v_warn := true; end if;
    else
      if v_n >= 3 then v_void := true; else v_warn := true; end if;
    end if;

    if v_warn and kd = 'hide' then
      -- uyarı alınan ayrılmada o an açık soru 0 puan sayılır
      v_zq := least(greatest(coalesce(p_q, 0), 0), d.qn - 1);
      if uid = d.p1 then update public.duels set zq1 = v_zq where id = did; else update public.duels set zq2 = v_zq where id = did; end if;
    end if;

    if v_void then
      select count(*) into v_vc from public.duels where void_by = uid and status = 'void' and id <> did and done_at >= now() - interval '15 days';
      v_lv := v_vc + 1;
      v_mult := case when v_lv <= 1 then 1 when v_lv = 2 then 1.5 else 2 end;
      v_sm := greatest(case when uid = d.p1 then d.s1 else d.s2 end, 0);
      v_so := greatest(case when uid = d.p1 then d.s2 else d.s1 end, 0);
      v_share := greatest(0.5, case when v_sm + v_so = 0 then 0.5 else v_so / (v_sm + v_so) end);
      v_lk := coalesce(case when uid = d.p1 then d.rk1 else d.rk2 end, 0);
      v_ok := coalesce(case when uid = d.p1 then d.rk2 else d.rk1 end, 0);
      v_base := round(least(v_lk * v_share, 4 * v_ok), 1);
      v_pen := round(v_base * v_mult, 1);
      v_opp := round(v_pen * 0.2, 1);
      v_ban := case when v_lv <= 1 then 3 when v_lv = 2 then 5 when v_lv = 3 then 15 when v_lv = 4 then 30 when v_lv = 5 then 60 when v_lv = 6 then 360 else 720 end;
      insert into public.duel_bans(user_id, until, lv, source) values (uid, now() + make_interval(mins => v_ban), v_lv, 'auto')
        on conflict (user_id) do update set until = excluded.until, lv = excluded.lv, source = 'auto';
      update public.duels set status = 'void', void_reason = (case when kd = 'blur' then 'blur3' else 'hide' end), void_by = uid, done_at = now(),
        pen_lv = v_lv, pen_t = false, pen_ban = v_ban,
        pen1 = case when uid = p1 then v_pen end, pen2 = case when uid = p2 then v_pen end,
        dl1 = case when uid = p1 then (case when v_pen > 0 then -v_pen end) else (case when v_opp > 0 then v_opp end) end,
        dl2 = case when uid = p2 then (case when v_pen > 0 then -v_pen end) else (case when v_opp > 0 then v_opp end) end
      where id = did;
      insert into public.duel_penalties(user_id, duel_id, kind, lv, pts, ban_min, note)
        values (uid, did, 'auto', v_lv, v_pen, v_ban, case when kd = 'blur' then 'Odak kaybı (3.)' else 'Uygulamadan ayrılma (2.)' end);
    end if;
  end if;

  select count(*) into v_vc from public.duels where void_by = uid and status = 'void' and done_at >= now() - interval '15 days';
  return jsonb_build_object('status', (select status from public.duels where id = did), 'n', v_n, 'warn', v_warn, 'zq', v_zq,
                            'lv', v_lv, 'pen', v_pen, 'opp', v_opp, 'ban', v_ban, 'voids', v_vc);
end $$;
revoke all on function public.duel_guard(uuid, text, int, int) from public, anon;
grant execute on function public.duel_guard(uuid, text, int, int) to authenticated;

-- 4) Cevap bildirimi: uyarı alınan ayrılmada açık olan soru 0 puan
drop function if exists public.duel_report(uuid, int, boolean, int);
drop function if exists public.duel_report(uuid, int, boolean, int, numeric);
create or replace function public.duel_report(did uuid, idx int, ok boolean, ms int, lv numeric default 1, "to" boolean default false) returns void
language plpgsql security definer set search_path = public as $$
declare uid uuid := auth.uid(); d public.duels; mine int; pts int; m int; l numeric; zq int;
begin
  select * into d from public.duels where id = did for update;
  if not found or d.status <> 'active' or uid not in (d.p1, d.p2) then raise exception 'not allowed'; end if;
  if now() < d.start_at - interval '1 second' then raise exception 'early'; end if;
  mine := case when uid = d.p1 then d.a1 else d.a2 end;
  if idx <> mine or idx >= d.qn then return; end if;
  m := least(greatest(coalesce(ms, 0), 300), d.per_q * 1000);
  l := least(greatest(coalesce(lv, 1), 1), 1.85);
  if d.mode = 'ranked' then
    -- dereceli: doğru ve yanlış aynı hesap: 100 × seviye × hız çarpanı (yanlışta eksi). Süre dolması: en yavaş cevap (hız 1,00)
    if not ok and coalesce("to", false) then m := d.per_q * 1000; end if;
    pts := round(100 * l * (1 + 0.5 * (1 - (least(greatest(m, 2000), 6000) - 2000)::numeric / 4000)))::int * (case when ok then 1 else -1 end);
  else
    -- klasik: eski kural (doğru hız bonuslu, yanlış −75 × seviye, süre dolması yarısı)
    pts := case when ok then round(100 * l * (1 + 0.5 * (1 - (least(greatest(m, 2000), 6000) - 2000)::numeric / 4000)))::int
                else -round(75 * l * (case when coalesce("to", false) then 0.5 else 1 end))::int end;
  end if;
  zq := case when uid = d.p1 then d.zq1 else d.zq2 end;
  if ok and zq is not null and zq = idx then pts := 0; end if;
  if uid = d.p1 then
    update public.duels set a1 = a1 + 1, s1 = s1 + pts, c1 = c1 + (case when ok then 1 else 0 end), t1 = t1 + m where id = did;
  else
    update public.duels set a2 = a2 + 1, s2 = s2 + pts, c2 = c2 + (case when ok then 1 else 0 end), t2 = t2 + m where id = did;
  end if;
  perform public.duel_settle(did);
end $$;
revoke all on function public.duel_report(uuid, int, boolean, int, numeric, boolean) from public, anon;
grant execute on function public.duel_report(uuid, int, boolean, int, numeric, boolean) to authenticated;

-- 5) Eşleşme, teklif, kabul: ceza altındaki kullanıcı dereceliye giremez (sunucu kontrolü)
create or replace function public.duel_join(p_wn int, p_mode text default 'classic') returns uuid
language plpgsql security definer set search_path = public as $$
declare uid uuid := auth.uid(); opp uuid; did uuid; mp numeric; m text := case when p_mode = 'ranked' then 'ranked' else 'classic' end;
begin
  if uid is null or not public.is_approved() or public.is_blocked(uid) then raise exception 'not allowed'; end if;
  perform public.duel_settle(id) from public.duels where status = 'active' and (p1 = uid or p2 = uid);
  select id into did from public.duels where status = 'active' and (p1 = uid or p2 = uid) order by created_at desc limit 1;
  if did is not null then delete from public.duel_queue where user_id = uid; return did; end if;
  if m = 'ranked' and public.duel_pen_block(uid) then
    delete from public.duel_queue where user_id = uid;
    raise exception 'ranked penalty';
  end if;
  mp := coalesce((select ap from public.scores where user_id = uid), 0);
  if mp < (case when m = 'ranked' then 200 else 20 end) then raise exception 'low points'; end if;
  delete from public.duel_queue where joined_at < now() - interval '10 seconds';
  select q.user_id into opp from public.duel_queue q
    where q.user_id <> uid and q.wn = p_wn and q.mode = m
      and (m = 'classic' or (
            abs(public.duel_elg(q.user_id) - public.duel_elg(uid)) <= 1
            and coalesce((select ap from public.scores where user_id = q.user_id), 0) >= 200
            and not public.duel_pen_block(q.user_id)
            and public.duel_pair_ok(uid, q.user_id)))
    order by q.joined_at limit 1 for update skip locked;
  if opp is null then
    insert into public.duel_queue(user_id, wn, joined_at, mode) values (uid, p_wn, now(), m)
      on conflict (user_id) do update set joined_at = now(), wn = p_wn, mode = m;
    return null;
  end if;
  delete from public.duel_queue where user_id in (uid, opp);
  return public.duel_make(opp, uid, p_wn, m);
end $$;

create or replace function public.duel_invite(target uuid, p_mode text default 'classic') returns jsonb
language plpgsql security definer set search_path = public as $$
declare uid uuid := auth.uid(); iid uuid; m text := case when p_mode = 'ranked' then 'ranked' else 'classic' end; need numeric := case when p_mode = 'ranked' then 200 else 20 end;
begin
  if uid is null or not public.is_approved() or public.is_blocked(uid) then raise exception 'not allowed'; end if;
  if target is null or target = uid then raise exception 'bad target'; end if;
  if m = 'ranked' then raise exception 'ranked invite closed'; end if;   -- dereceli yalnızca gizli kullanıcılı rastgele eşleşme
  if not public.chat_can_receive(target) then raise exception 'bad target'; end if;
  if m = 'ranked' and public.duel_pen_block(uid) then raise exception 'ranked penalty'; end if;
  if m = 'ranked' and public.duel_pen_block(target) then raise exception 'target penalty'; end if;
  perform public.duel_settle(id) from public.duels where status = 'active' and (p1 in (uid, target) or p2 in (uid, target));
  if coalesce((select ap from public.scores where user_id = uid), 0) < need then raise exception 'low points'; end if;
  if coalesce((select ap from public.scores where user_id = target), 0) < need then raise exception 'target low'; end if;
  if m = 'ranked' and not public.duel_pair_ok(uid, target) then raise exception 'pair limit'; end if;
  if public.duel_busy(uid) then raise exception 'me busy'; end if;
  if public.duel_busy(target) then raise exception 'target busy'; end if;
  if not exists(select 1 from public.profiles where user_id = target and duel_seen > now() - interval '15 seconds' and duel_mode = m) then raise exception 'offline'; end if;
  if exists(select 1 from public.duel_invites i where i.status = 'pending' and i.expires_at > now()
            and (i.from_user in (uid, target) or i.to_user in (uid, target))) then raise exception 'invite busy'; end if;
  if (select count(*) from public.duel_invites where from_user = uid and created_at > now() - interval '1 minute') >= 8 then raise exception 'too many'; end if;
  delete from public.duel_invites where created_at < now() - interval '1 hour';
  insert into public.duel_invites(from_user, to_user, mode) values (uid, target, m) returning id into iid;
  return jsonb_build_object('id', iid, 'left_ms', 15000);
end $$;

create or replace function public.duel_respond(inv uuid, accept boolean, p_wn int, p_rk boolean default false) returns jsonb
language plpgsql security definer set search_path = public as $$
declare uid uuid := auth.uid(); i public.duel_invites; did uuid; need numeric;
begin
  if uid is null or not public.is_approved() then raise exception 'not allowed'; end if;
  select * into i from public.duel_invites where id = inv and to_user = uid for update;
  if not found or i.status <> 'pending' or i.expires_at <= now() then return jsonb_build_object('status', 'expired'); end if;
  if not accept then
    update public.duel_invites set status = 'declined' where id = inv;
    return jsonb_build_object('status', 'declined');
  end if;
  if i.mode = 'ranked' and not coalesce(p_rk, false) then
    update public.duel_invites set status = 'cancelled' where id = inv;
    return jsonb_build_object('status', 'old');
  end if;
  if i.mode = 'ranked' and (public.duel_pen_block(uid) or public.duel_pen_block(i.from_user)) then
    update public.duel_invites set status = 'cancelled' where id = inv;
    return jsonb_build_object('status', 'penalty');
  end if;
  need := case when i.mode = 'ranked' then 200 else 20 end;
  perform public.duel_settle(id) from public.duels where status = 'active' and (p1 in (uid, i.from_user) or p2 in (uid, i.from_user));
  if public.duel_busy(uid) or public.duel_busy(i.from_user) then
    update public.duel_invites set status = 'cancelled' where id = inv;
    return jsonb_build_object('status', 'busy');
  end if;
  if coalesce((select ap from public.scores where user_id = uid), 0) < need
     or coalesce((select ap from public.scores where user_id = i.from_user), 0) < need then
    update public.duel_invites set status = 'cancelled' where id = inv;
    return jsonb_build_object('status', 'low');
  end if;
  if i.mode = 'ranked' and not public.duel_pair_ok(uid, i.from_user) then
    update public.duel_invites set status = 'cancelled' where id = inv;
    return jsonb_build_object('status', 'limit');
  end if;
  delete from public.duel_queue where user_id in (uid, i.from_user);
  did := public.duel_make(i.from_user, uid, p_wn, i.mode);
  update public.duel_invites set status = 'accepted', duel_id = did where id = inv;
  return jsonb_build_object('status', 'accepted', 'duel_id', did);
end $$;

revoke all on function public.duel_join(int, text) from public, anon;
grant execute on function public.duel_join(int, text) to authenticated;
revoke all on function public.duel_invite(uuid, text) from public, anon;
grant execute on function public.duel_invite(uuid, text) to authenticated;
revoke all on function public.duel_respond(uuid, boolean, int, boolean) from public, anon;
grant execute on function public.duel_respond(uuid, boolean, int, boolean) to authenticated;

-- 6) Herkese açık maç geçmişi: iptal edilen dereceli maçlar da görünür (durum, ayrılan, puanlar)
drop function if exists public.duel_history_page(text, int, int);
create or replace function public.duel_history_page(p_mode text default 'classic', p_off int default 0, p_n int default 50)
returns table(id uuid, p1 uuid, p2 uuid, s1 numeric, s2 numeric, c1 int, c2 int, a1 int, a2 int, t1 numeric, t2 numeric, winner uuid, created_at timestamptz, mode text, dl1 numeric, dl2 numeric, status text, void_by uuid, void_reason text)
language sql stable security definer set search_path = public as $$
  select d.id, d.p1, d.p2, d.s1::numeric, d.s2::numeric, d.c1::int, d.c2::int, d.a1::int, d.a2::int, d.t1::numeric, d.t2::numeric, d.winner, d.created_at, d.mode, d.dl1, d.dl2, d.status, d.void_by, d.void_reason
  from public.duels d
  where auth.uid() is not null
    and ((p_mode = 'ranked' and d.mode = 'ranked' and d.status in ('done', 'void'))
      or (p_mode <> 'ranked' and coalesce(d.mode, 'classic') <> 'ranked' and d.status = 'done'))
  order by d.created_at desc, d.id
  limit least(greatest(coalesce(p_n, 50), 1), 100) offset greatest(coalesce(p_off, 0), 0);
$$;
revoke all on function public.duel_history_page(text, int, int) from public, anon;
grant execute on function public.duel_history_page(text, int, int) to authenticated;

-- 7) Kullanıcıya yönetici uyarısı: bir kez okunur
create or replace function public.duel_notice_pull() returns table(id bigint, msg text, created_at timestamptz)
language plpgsql security definer set search_path = public as $$
begin
  if auth.uid() is null then raise exception 'not allowed'; end if;
  return query
  with u as (update public.duel_notices n set seen = true where n.user_id = auth.uid() and n.seen = false returning n.id, n.msg, n.created_at)
  select u.id, u.msg, u.created_at from u order by u.id;
end $$;
revoke all on function public.duel_notice_pull() from public, anon;
grant execute on function public.duel_notice_pull() to authenticated;

-- 8) Yönetici fonksiyonları
create or replace function public.duel_flag_list(n int default 100)
returns table(id bigint, user_id uuid, name text, un text, kind text, q int, away_ms int, created_at timestamptz, voided boolean, wk int)
language plpgsql stable security definer set search_path = public as $$
begin
  if not public.is_admin() then raise exception 'not allowed'; end if;
  return query
  select f.id, f.user_id, s.name::text, s.un::text, f.kind, f.q, f.away_ms, f.created_at,
         (d.status = 'void' and d.void_by = f.user_id) as voided,
         (select count(*)::int from public.duels v where v.void_by = f.user_id and v.status = 'void' and v.done_at >= now() - interval '15 days') as wk
  from public.duel_flags f
  left join public.scores s on s.user_id = f.user_id
  left join public.duels d on d.id = f.duel_id
  order by f.created_at desc limit least(greatest(coalesce(n, 100), 1), 300);
end $$;
revoke all on function public.duel_flag_list(int) from public, anon;
grant execute on function public.duel_flag_list(int) to authenticated;

-- kullanıcı bazında kategorilenmiş özet (süre kayıtlarıyla)
create or replace function public.duel_admin_summary()
returns table(user_id uuid, name text, un text, hide int, hide_short int, hide_off int, blur int, trap int, voids int, voids7 int,
              away_total bigint, away_max int, away_avg int, last_at timestamptz, ban_left int, pen_pts numeric)
language plpgsql stable security definer set search_path = public as $$
begin
  if not public.is_admin() then raise exception 'not allowed'; end if;
  return query
  select f.user_id, s.name::text, s.un::text,
         count(*) filter (where f.kind = 'hide')::int, count(*) filter (where f.kind = 'hide_short')::int,
         count(*) filter (where f.kind = 'hide_off')::int, count(*) filter (where f.kind in ('blur','blur2'))::int,
         count(*) filter (where f.kind = 'trap')::int,
         (select count(*)::int from public.duels v where v.void_by = f.user_id and v.status = 'void'),
         (select count(*)::int from public.duels v where v.void_by = f.user_id and v.status = 'void' and v.done_at >= now() - interval '15 days'),
         coalesce(sum(f.away_ms) filter (where f.kind in ('hide','hide_short','hide_off','blur','blur2')), 0)::bigint,
         coalesce(max(f.away_ms), 0)::int, coalesce(round(avg(f.away_ms))::int, 0), max(f.created_at),
         public.duel_pen_left(f.user_id),
         coalesce((select sum(p.pts) from public.duel_penalties p where p.user_id = f.user_id and p.kind = 'auto'), 0)
  from public.duel_flags f
  left join public.scores s on s.user_id = f.user_id
  group by f.user_id, s.name, s.un
  order by max(f.created_at) desc limit 200;
end $$;
revoke all on function public.duel_admin_summary() from public, anon;
grant execute on function public.duel_admin_summary() to authenticated;

-- iptal edilen maçlar
drop function if exists public.duel_admin_cases(int);
create or replace function public.duel_admin_cases(n int default 60)
returns table(id uuid, created_at timestamptz, done_at timestamptz, by_id uuid, by_name text, by_un text, opp_id uuid, opp_name text, s_by numeric, s_opp numeric,
              reason text, lv int, pen numeric, opp_gain numeric, ban_min int, refunded boolean, acked timestamptz)
language plpgsql stable security definer set search_path = public as $$
begin
  if not public.is_admin() then raise exception 'not allowed'; end if;
  return query
  select d.id, d.created_at, d.done_at, d.void_by, a.name::text, a.un::text,
         case when d.void_by = d.p1 then d.p2 else d.p1 end, b.name::text,
         case when d.void_by = d.p1 then d.s1 else d.s2 end::numeric, case when d.void_by = d.p1 then d.s2 else d.s1 end::numeric,
         d.void_reason, d.pen_lv, coalesce(case when d.void_by = d.p1 then d.pen1 else d.pen2 end, 0),
         coalesce(case when d.void_by = d.p1 then d.dl2 else d.dl1 end, 0), d.pen_ban, coalesce(d.pen_rf, false), d.pen_ack
  from public.duels d
  left join public.scores a on a.user_id = d.void_by
  left join public.scores b on b.user_id = (case when d.void_by = d.p1 then d.p2 else d.p1 end)
  where d.status = 'void'
  order by d.done_at desc nulls last limit least(greatest(coalesce(n, 60), 1), 200);
end $$;
revoke all on function public.duel_admin_cases(int) from public, anon;
grant execute on function public.duel_admin_cases(int) to authenticated;

-- ceza ve işlem kayıtları (tümü ya da tek kullanıcı)
create or replace function public.duel_admin_penalty_log(p_user uuid default null, n int default 100)
returns table(id bigint, user_id uuid, name text, un text, kind text, lv int, pts numeric, ban_min int, note text, by_name text, created_at timestamptz)
language plpgsql stable security definer set search_path = public as $$
begin
  if not public.is_admin() then raise exception 'not allowed'; end if;
  return query
  select p.id, p.user_id, s.name::text, s.un::text, p.kind, p.lv, p.pts, p.ban_min, p.note, bs.name::text, p.created_at
  from public.duel_penalties p
  left join public.scores s on s.user_id = p.user_id
  left join public.scores bs on bs.user_id = p.by_user
  where p_user is null or p.user_id = p_user
  order by p.created_at desc limit least(greatest(coalesce(n, 100), 1), 300);
end $$;
revoke all on function public.duel_admin_penalty_log(uuid, int) from public, anon;
grant execute on function public.duel_admin_penalty_log(uuid, int) to authenticated;

-- uyarı gönder
create or replace function public.duel_admin_warn(target uuid, p_msg text) returns void
language plpgsql security definer set search_path = public as $$
begin
  if not public.is_admin() then raise exception 'not allowed'; end if;
  if target is null or coalesce(trim(p_msg), '') = '' then raise exception 'bad input'; end if;
  insert into public.duel_notices(user_id, msg) values (target, left(trim(p_msg), 300));
  insert into public.duel_penalties(user_id, kind, note, by_user) values (target, 'admin_warn', left(trim(p_msg), 300), auth.uid());
end $$;
revoke all on function public.duel_admin_warn(uuid, text) from public, anon;
grant execute on function public.duel_admin_warn(uuid, text) to authenticated;

-- dereceli cezası ver (dakika)
create or replace function public.duel_admin_ban(target uuid, p_min int, p_note text default null) returns void
language plpgsql security definer set search_path = public as $$
begin
  if not public.is_admin() then raise exception 'not allowed'; end if;
  if target is null or p_min is null or p_min < 1 or p_min > 43200 then raise exception 'bad input'; end if;
  insert into public.duel_bans(user_id, until, lv, source) values (target, now() + make_interval(mins => p_min), null, 'admin')
    on conflict (user_id) do update set until = excluded.until, source = 'admin';
  insert into public.duel_penalties(user_id, kind, ban_min, note, by_user) values (target, 'admin_ban', p_min, left(coalesce(p_note, ''), 300), auth.uid());
end $$;
revoke all on function public.duel_admin_ban(uuid, int, text) from public, anon;
grant execute on function public.duel_admin_ban(uuid, int, text) to authenticated;

-- dereceli cezasını kaldır
create or replace function public.duel_admin_unban(target uuid, p_note text default null) returns void
language plpgsql security definer set search_path = public as $$
begin
  if not public.is_admin() then raise exception 'not allowed'; end if;
  delete from public.duel_bans where user_id = target;
  insert into public.duel_penalties(user_id, kind, note, by_user) values (target, 'admin_unban', left(coalesce(p_note, ''), 300), auth.uid());
end $$;
revoke all on function public.duel_admin_unban(uuid, text) from public, anon;
grant execute on function public.duel_admin_unban(uuid, text) to authenticated;

-- iptal edilen maçta kesilen puanı iade et (istemci açılışta uygular); rakibe verilen %20 geri alınmaz
create or replace function public.duel_admin_refund(did uuid, p_unban boolean default true, p_note text default null) returns void
language plpgsql security definer set search_path = public as $$
declare d public.duels;
begin
  if not public.is_admin() then raise exception 'not allowed'; end if;
  select * into d from public.duels where id = did for update;
  if not found or d.status <> 'void' or d.void_by is null then raise exception 'not a void duel'; end if;
  if coalesce(d.pen_rf, false) then return; end if;
  update public.duels set pen_rf = true where id = did;
  if p_unban then delete from public.duel_bans where user_id = d.void_by; end if;
  insert into public.duel_penalties(user_id, duel_id, kind, pts, note, by_user)
    values (d.void_by, did, 'admin_refund', coalesce(case when d.void_by = d.p1 then d.pen1 else d.pen2 end, 0), left(coalesce(p_note, ''), 300), auth.uid());
end $$;
revoke all on function public.duel_admin_refund(uuid, boolean, text) from public, anon;
grant execute on function public.duel_admin_refund(uuid, boolean, text) to authenticated;

-- Dereceli puan geçişi (v4.101): komisyon yok, kazanana kaybedenin lig oranı kadar sistem bonusu; kazanan kendi riskinin 3 katından fazlasını alamaz.
-- Klasik havuz (20+20+5 sistem) ve diğer kurallar değişmedi.
create or replace function public.duel_settle(did uuid) returns void
language plpgsql security definer set search_path = public as $$
declare d public.duels; w uuid; tot int; pw numeric(6,1); sw int; p1v numeric(6,1); p2v numeric(6,1); expired boolean; both_done boolean;
        v_c1 numeric; v_c2 numeric; v_share numeric; v_lk numeric; v_wk numeric; v_t numeric; v_tx numeric; v_rate numeric;
begin
  select * into d from public.duels where id = did for update;
  if not found or d.status <> 'active' then return; end if;
  both_done := d.a1 >= d.qn and d.a2 >= d.qn;
  expired := now() > d.start_at + make_interval(secs => d.qn * d.per_q + 15);
  if not (both_done or expired) then return; end if;
  if expired and not both_done then
    update public.duels set
      s1 = s1 - 100 * greatest(qn - a1, 0), s2 = s2 - 100 * greatest(qn - a2, 0),
      a1 = greatest(a1, qn), a2 = greatest(a2, qn)
    where id = did;
    select * into d from public.duels where id = did;
  end if;

  if d.mode = 'ranked' then
    w := case when d.s1 > d.s2 then d.p1 when d.s2 > d.s1 then d.p2 else null end;
    -- iki tarafın da puanı (negatifler 0 sayılır) 0 ise kimse bir şey kazanmadı: berabere, puan değişmez
    if greatest(d.s1, 0) + greatest(d.s2, 0) = 0 then w := null; end if;
    if w is null then
      update public.duels set status = 'done', done_at = now(), winner = null, dl1 = 0, dl2 = 0 where id = did;
      return;
    end if;
    v_c1 := greatest(d.s1, 0); v_c2 := greatest(d.s2, 0);
    v_share := case when v_c1 + v_c2 = 0 then 0.5 else (case when w = d.p1 then v_c1 else v_c2 end) / (v_c1 + v_c2) end;
    v_lk := coalesce(case when w = d.p1 then d.rk2 else d.rk1 end, 0);
    v_wk := coalesce(case when w = d.p1 then d.rk1 else d.rk2 end, 0);
    -- kazanan, kendi riskinin 3 katından fazlasını alamaz (fazlası kaybedene geri ödenir: kaybeden de en çok bu kadar kaybeder)
    v_t := round(least(v_lk * v_share, 3 * v_wk), 1);
    -- komisyon yok; kazanana, kaybedenin lig oranı kadar sistem bonusu eklenir (üst sınıra dahil değil)
    v_rate := public.duel_rate(coalesce(case when w = d.p1 then d.rp2 else d.rp1 end, 200));
    v_tx := case when v_t <= 0 then 0 else round(v_t * v_rate, 1) end;
    update public.duels set status = 'done', done_at = now(), winner = w,
      dl1 = case when w = p1 then v_t + v_tx else -v_t end,
      dl2 = case when w = p2 then v_t + v_tx else -v_t end
    where id = did;
    return;
  end if;

  if expired and not both_done then
    w := case when d.s1 > d.s2 then d.p1 when d.s2 > d.s1 then d.p2 else null end;
  else
    w := case when d.s1 > d.s2 then d.p1 when d.s2 > d.s1 then d.p2
              when d.t1 < d.t2 then d.p1 when d.t2 < d.t1 then d.p2
              else null end;
  end if;
  tot := greatest(d.s1, 0) + greatest(d.s2, 0);
  if w is null then
    p1v := 22.5; p2v := 22.5;
  else
    sw := greatest(case when w = d.p1 then d.s1 else d.s2 end, 0);
    pw := round(25 + case when tot = 0 then 10 else 20.0 * sw / tot end, 1);
    if w = d.p1 then p1v := pw; p2v := 45 - pw; else p2v := pw; p1v := 45 - pw; end if;
  end if;
  update public.duels set status = 'done', done_at = now(), winner = w, pay1 = p1v, pay2 = p2v where id = did;
end $$;
revoke all on function public.duel_settle(uuid) from public, anon, authenticated;
