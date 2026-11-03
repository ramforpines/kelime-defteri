-- DERECELİ DÜELLO: saat pencereleri + toplu eşleştirme (5 sn toplama, farklı rakip önceliği, 30 sn kuyruk) + kuyruk sayacı
-- Supabase SQL Editor'da bir kez çalıştırın. Klasik düello etkilenmez.
-- Devreye girme: yönetici hesapları hemen, diğer herkes 04.11.2026 00:00 (TR) itibarıyla (rk_live fonksiyonundaki tarih).
-- Yönetici testi için pencere dışında da girebilsin diye rk_cfg'de admin_bypass='on' gelir. Kapatmak için:
--   update public.rk_cfg set val = 'off' where key = 'admin_bypass';

-- 0) ayar tablosu + kuyruk sütunları
create table if not exists public.rk_cfg (key text primary key, val text not null);
insert into public.rk_cfg(key, val) values ('admin_bypass', 'on') on conflict (key) do nothing;
alter table public.rk_cfg enable row level security;
revoke all on public.rk_cfg from anon, authenticated;

alter table public.duel_queue add column if not exists first_at timestamptz;
update public.duel_queue set first_at = joined_at where first_at is null;

-- 1) pencere kuralları (Türkiye saati)
--    Hafta içi: 20.30-21.30 ve 22.25-23.55
--    Hafta sonu: 14.00'ten itibaren her saat başı ilk 15 dk (14:00-14:15 ... 22:00-22:15) ve 23.00-23.55
create or replace function public.rk_window_open(t timestamptz default now()) returns boolean
language sql immutable set search_path = public as $$
  select case
    when extract(isodow from (t at time zone 'Europe/Istanbul')) in (6, 7) then
      ((t at time zone 'Europe/Istanbul')::time >= time '23:00' and (t at time zone 'Europe/Istanbul')::time < time '23:55')
      or (extract(hour from (t at time zone 'Europe/Istanbul')) between 14 and 22 and extract(minute from (t at time zone 'Europe/Istanbul')) < 15)
    else
      ((t at time zone 'Europe/Istanbul')::time >= time '20:30' and (t at time zone 'Europe/Istanbul')::time < time '21:30')
      or ((t at time zone 'Europe/Istanbul')::time >= time '22:25' and (t at time zone 'Europe/Istanbul')::time < time '23:55')
  end
$$;

create or replace function public.rk_next_open(t timestamptz default now()) returns timestamptz
language sql stable set search_path = public as $$
  select min(ts) from generate_series(date_trunc('minute', t) + interval '1 minute', t + interval '8 days', interval '1 minute') ts
  where public.rk_window_open(ts)
$$;

create or replace function public.rk_close_at(t timestamptz default now()) returns timestamptz
language sql stable set search_path = public as $$
  select min(ts) from generate_series(date_trunc('minute', t) + interval '1 minute', t + interval '4 hours', interval '1 minute') ts
  where not public.rk_window_open(ts)
$$;

-- 2) devreye girme: yönetici hemen, herkes için 04.11.2026 00:00 TR
create or replace function public.rk_live() returns boolean
language sql stable security definer set search_path = public as $$
  select public.is_admin() or now() >= timestamptz '2026-11-04 00:00:00+03'
$$;

-- kullanıcı için dereceli arama şu an açık mı (yönetici testi: admin_bypass)
create or replace function public.rk_can_search() returns boolean
language sql stable security definer set search_path = public as $$
  select (not public.rk_live())
      or public.rk_window_open()
      or (public.is_admin() and coalesce((select val from public.rk_cfg where key = 'admin_bypass'), 'off') = 'on')
$$;

-- 3) istemci için durum: şu an açık mı, bir sonraki açılış, kapanış
create or replace function public.rk_status() returns jsonb
language plpgsql stable security definer set search_path = public as $$
declare live boolean := public.rk_live(); real boolean := public.rk_window_open(); eff boolean := public.rk_can_search();
begin
  if auth.uid() is null then raise exception 'not allowed'; end if;
  return jsonb_build_object('now', now(), 'live', live, 'real', real, 'open', eff,
    'next', case when real then null else public.rk_next_open() end,
    'close', case when real then public.rk_close_at() else null end);
end $$;
revoke all on function public.rk_status() from public, anon;
grant execute on function public.rk_status() to authenticated;

-- 4) kuyrukta eşleşmeye uygun kişi sayısı (benimle eşleşebilecekler: lig farkı <= 1, günlük sınır uygun)
create or replace function public.rk_queue_count(p_wn int) returns int
language plpgsql stable security definer set search_path = public as $$
declare uid uuid := auth.uid(); n int;
begin
  if uid is null then raise exception 'not allowed'; end if;
  select count(*) into n from public.duel_queue q
   where q.user_id <> uid and q.mode = 'ranked' and q.wn = p_wn and q.joined_at > now() - interval '10 seconds'
     and abs(public.duel_elg(q.user_id) - public.duel_elg(uid)) <= 1
     and coalesce((select ap from public.scores where user_id = q.user_id), 0) >= 200
     and not public.duel_pen_block(q.user_id)
     and public.duel_pair_ok(uid, q.user_id);
  return n;
end $$;
revoke all on function public.rk_queue_count(int) from public, anon;
grant execute on function public.rk_queue_count(int) to authenticated;

-- 5) toplu eşleştirme: ilk 5 sn'yi doldurmuş bekleyenler arasından, en çok kişiyi eşleştir; eşit olanlarda
--    birbirleriyle daha az maç yapmış çiftlere öncelik ver (lig farkı <= 1, günlük çift sınırı, ceza ve puan şartları geçerli)
create or replace function public.rk_match_round(p_wn int) returns int
language plpgsql security definer set search_path = public as $$
declare
  ids uuid[]; el int[]; n int; i int; j int; k int; mk int; fm int; rest int; lo int;
  w int[]; fc int[]; fw int[]; fch int[];
  bc int; bw int; bj int; cc int; cw int; made int := 0; a uuid; b uuid; pr int;
begin
  select array_agg(s.user_id order by s.first_at) into ids from (
    select q.user_id, q.first_at from public.duel_queue q
     where q.mode = 'ranked' and q.wn = p_wn and q.joined_at > now() - interval '10 seconds' and q.first_at <= now() - interval '5 seconds'
       and coalesce((select ap from public.scores where user_id = q.user_id), 0) >= 200
       and not public.duel_pen_block(q.user_id)
       and not exists (select 1 from public.duels d where d.status = 'active' and (d.p1 = q.user_id or d.p2 = q.user_id))
     order by q.first_at limit 12) s;
  n := coalesce(array_length(ids, 1), 0);
  if n < 2 then return 0; end if;
  el := array[]::int[];
  for i in 1..n loop el := el || public.duel_elg(ids[i]); end loop;
  w := array_fill(-1, array[n * n]);
  for i in 1..n loop for j in i + 1..n loop
    if abs(el[i] - el[j]) <= 1 and public.duel_pair_ok(ids[i], ids[j]) then
      select count(*) into pr from public.duels d
       where d.mode = 'ranked' and d.status in ('active', 'done') and d.created_at > now() - interval '24 hours'
         and ((d.p1 = ids[i] and d.p2 = ids[j]) or (d.p1 = ids[j] and d.p2 = ids[i]));
      w[(i - 1) * n + j] := pr; w[(j - 1) * n + i] := pr;
    end if;
  end loop; end loop;
  fm := (1 << n) - 1;
  fc := array_fill(0, array[fm + 1]); fw := array_fill(0, array[fm + 1]); fch := array_fill(-1, array[fm + 1]);
  for mk in 1..fm loop
    lo := 0; while ((mk >> lo) & 1) = 0 loop lo := lo + 1; end loop;
    rest := mk & ~(1 << lo);
    bc := fc[rest + 1]; bw := fw[rest + 1]; bj := -1;
    for k in lo + 1..n - 1 loop
      if ((rest >> k) & 1) = 1 and w[lo * n + k + 1] >= 0 then
        cc := fc[(rest & ~(1 << k)) + 1] + 1; cw := fw[(rest & ~(1 << k)) + 1] + w[lo * n + k + 1];
        if cc > bc or (cc = bc and cw < bw) then bc := cc; bw := cw; bj := k; end if;
      end if;
    end loop;
    fc[mk + 1] := bc; fw[mk + 1] := bw; fch[mk + 1] := bj;
  end loop;
  mk := fm;
  while mk > 0 loop
    lo := 0; while ((mk >> lo) & 1) = 0 loop lo := lo + 1; end loop;
    bj := fch[mk + 1];
    if bj >= 0 then
      a := ids[lo + 1]; b := ids[bj + 1];
      delete from public.duel_queue where user_id in (a, b);
      perform public.duel_make(a, b, p_wn, 'ranked');
      made := made + 1;
      mk := mk & ~(1 << lo) & ~(1 << bj);
    else
      mk := mk & ~(1 << lo);
    end if;
  end loop;
  return made;
end $$;
revoke all on function public.rk_match_round(int) from public, anon, authenticated;

-- 6) eşleşme girişi: klasik aynen; dereceli: pencere kontrolü, 5 sn toplama, toplu eşleştirme, 30 sn
create or replace function public.duel_join(p_wn int, p_mode text default 'classic') returns uuid
language plpgsql security definer set search_path = public as $$
declare uid uuid := auth.uid(); opp uuid; did uuid; mp numeric; m text := case when p_mode = 'ranked' then 'ranked' else 'classic' end; fa timestamptz;
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

  if m = 'classic' then
    delete from public.duel_queue where joined_at < now() - interval '10 seconds';
    select q.user_id into opp from public.duel_queue q
      where q.user_id <> uid and q.wn = p_wn and q.mode = 'classic'
      order by q.joined_at limit 1 for update skip locked;
    if opp is null then
      insert into public.duel_queue(user_id, wn, joined_at, mode, first_at) values (uid, p_wn, now(), 'classic', now())
        on conflict (user_id) do update set joined_at = now(), wn = p_wn, mode = 'classic', first_at = now();
      return null;
    end if;
    delete from public.duel_queue where user_id in (uid, opp);
    return public.duel_make(opp, uid, p_wn, 'classic');
  end if;

  -- dereceli
  if not public.rk_can_search() then
    delete from public.duel_queue where user_id = uid;
    raise exception 'ranked closed';
  end if;
  delete from public.duel_queue where joined_at < now() - interval '10 seconds' or first_at < now() - interval '40 seconds';
  insert into public.duel_queue(user_id, wn, joined_at, mode, first_at) values (uid, p_wn, now(), 'ranked', now())
    on conflict (user_id) do update set joined_at = now(), wn = p_wn,
      first_at = case when public.duel_queue.mode = 'ranked' and public.duel_queue.first_at is not null then public.duel_queue.first_at else now() end,
      mode = 'ranked';
  select first_at into fa from public.duel_queue where user_id = uid;
  if fa > now() - interval '5 seconds' then return null; end if;   -- ilk 5 saniye: yalnızca toplanır
  perform pg_advisory_xact_lock(7440);
  perform public.rk_match_round(p_wn);
  select id into did from public.duels where status = 'active' and (p1 = uid or p2 = uid) order by created_at desc limit 1;
  return did;
end $$;
revoke all on function public.duel_join(int, text) from public, anon;
grant execute on function public.duel_join(int, text) to authenticated;
