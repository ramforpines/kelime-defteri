-- Dosya: supabase-duel-ranked.sql
-- Kelime Defteri: DERECELİ DÜELLO (klasik düello aynen kalır). Önce supabase-duel-final.sql çalıştırılmış olmalı.
-- Kurallar:
--  * Bronz ligden (200 puan) itibaren oynanır. Bahis yok; maç başında iki oyuncunun toplam puanı kaydedilir.
--  * Kaybedenin riski = puanı x lig oranı (bronz %10 -> 9, gümüş 9 -> 8, altın 8 -> 7, platin 7 -> 6, zümrüt 6 -> 5, elmas 5 -> 4, ustalık ve üstü %4; ligin içinde doğrusal).
--  * Kazanan, riskin kendi maç skor payı kadarını alır; kendi riskinin 4 katından fazlasını alamaz. Kazanandan max(1, %5) kesilir.
--  * Skorlar eşitse beraberlik: kimse puan almaz/kaybetmez. Negatif maç puanı payda 0 sayılır.
--  * Rastgele eşleştirme aynı veya komşu ligde yapılır. Aynı iki kişi arasında 24 saatte en çok 3 dereceli maç oynanabilir.
-- Supabase SQL Editor'da bir kez çalıştır.

alter table public.duels add column if not exists mode text not null default 'classic';
alter table public.duels add column if not exists rp1 numeric; alter table public.duels add column if not exists rp2 numeric;
alter table public.duels add column if not exists rk1 numeric; alter table public.duels add column if not exists rk2 numeric;
alter table public.duels add column if not exists dl1 numeric(9,1); alter table public.duels add column if not exists dl2 numeric(9,1);
alter table public.duel_queue add column if not exists mode text not null default 'classic';
alter table public.duel_invites add column if not exists mode text not null default 'classic';
create index if not exists duels_mode_idx on public.duels(mode, created_at desc);

-- iç yardımcılar: lig oranı, risk, lig sırası
create or replace function public.duel_rate(p numeric) returns numeric language sql immutable as $$
  select case
    when p >= 10000 then 0.04
    when p >= 6000 then 0.05 - 0.01 * (p - 6000) / 4000
    when p >= 3500 then 0.06 - 0.01 * (p - 3500) / 2500
    when p >= 2000 then 0.07 - 0.01 * (p - 2000) / 1500
    when p >= 1000 then 0.08 - 0.01 * (p - 1000) / 1000
    when p >= 500 then 0.09 - 0.01 * (p - 500) / 500
    else 0.10 - 0.01 * (greatest(p, 200) - 200) / 300 end
$$;
create or replace function public.duel_risk(p numeric) returns numeric language sql immutable as $$
  select round(p * public.duel_rate(p), 1)
$$;
create or replace function public.duel_lg(p numeric) returns int language sql immutable as $$
  select case when p >= 10000 then 7 when p >= 6000 then 6 when p >= 3500 then 5 when p >= 2000 then 4
              when p >= 1000 then 3 when p >= 500 then 2 when p >= 200 then 1 else 0 end
$$;
revoke all on function public.duel_rate(numeric), public.duel_risk(numeric), public.duel_lg(numeric) from public, anon, authenticated;

-- iç: aynı iki kişi son 24 saatte 3'ten az dereceli maç yaptı mı?
create or replace function public.duel_pair_ok(a uuid, b uuid) returns boolean language sql stable security definer set search_path = public as $$
  select count(*) < 3 from public.duels d
  where d.mode = 'ranked' and d.created_at > now() - interval '24 hours'
    and ((d.p1 = a and d.p2 = b) or (d.p1 = b and d.p2 = a))
$$;
revoke all on function public.duel_pair_ok(uuid, uuid) from public, anon, authenticated;

-- iç: dereceli düelloyu oluştur (puanlar ve riskler maç başında sunucu puanından kaydedilir)
create or replace function public.duel_make(a uuid, b uuid, p_wn int, p_mode text) returns uuid
language plpgsql security definer set search_path = public as $$
declare did uuid; pa numeric; pb numeric;
begin
  pa := coalesce((select ap from public.scores where user_id = a), 0);
  pb := coalesce((select ap from public.scores where user_id = b), 0);
  insert into public.duels(p1, p2, seed, wn, start_at, mode, rp1, rp2, rk1, rk2)
    values (a, b, floor(random() * 2147480000)::int, p_wn, now() + interval '5 seconds', p_mode,
            case when p_mode = 'ranked' then pa end, case when p_mode = 'ranked' then pb end,
            case when p_mode = 'ranked' then public.duel_risk(pa) end, case when p_mode = 'ranked' then public.duel_risk(pb) end)
    returning id into did;
  return did;
end $$;
revoke all on function public.duel_make(uuid, uuid, int, text) from public, anon, authenticated;

-- Maç sonu: klasik = havuz payı, dereceli = puan transferi
create or replace function public.duel_settle(did uuid) returns void
language plpgsql security definer set search_path = public as $$
declare d public.duels; w uuid; tot int; pw numeric(6,1); sw int; p1v numeric(6,1); p2v numeric(6,1); expired boolean; both_done boolean;
        v_c1 numeric; v_c2 numeric; v_share numeric; v_lk numeric; v_wk numeric; v_t numeric; v_tx numeric;
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
    if w is null then
      update public.duels set status = 'done', done_at = now(), winner = null, dl1 = 0, dl2 = 0 where id = did;
      return;
    end if;
    v_c1 := greatest(d.s1, 0); v_c2 := greatest(d.s2, 0);
    v_share := case when v_c1 + v_c2 = 0 then 0.5 else (case when w = d.p1 then v_c1 else v_c2 end) / (v_c1 + v_c2) end;
    v_lk := coalesce(case when w = d.p1 then d.rk2 else d.rk1 end, 0);
    v_wk := coalesce(case when w = d.p1 then d.rk1 else d.rk2 end, 0);
    v_t := round(least(v_lk * v_share, 4 * v_wk), 1);
    v_tx := least(v_t, greatest(1, round(0.05 * v_t, 1)));
    if v_t <= 0 then v_tx := 0; end if;
    update public.duels set status = 'done', done_at = now(), winner = w,
      dl1 = case when w = p1 then v_t - v_tx else -v_t end,
      dl2 = case when w = p2 then v_t - v_tx else -v_t end
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
    p1v := 17.5; p2v := 17.5;
  else
    sw := greatest(case when w = d.p1 then d.s1 else d.s2 end, 0);
    pw := round(25 + case when tot = 0 then 5 else 10.0 * sw / tot end, 1);
    if w = d.p1 then p1v := pw; p2v := 35 - pw; else p2v := pw; p1v := 35 - pw; end if;
  end if;
  update public.duels set status = 'done', done_at = now(), winner = w, pay1 = p1v, pay2 = p2v where id = did;
end $$;
revoke all on function public.duel_settle(uuid) from public, anon, authenticated;

-- Eşleşme ara (klasik: en az 20 puan; dereceli: en az 200 puan, aynı/komşu lig, aynı çift sınırı)
drop function if exists public.duel_join(int);
create or replace function public.duel_join(p_wn int, p_mode text default 'classic') returns uuid
language plpgsql security definer set search_path = public as $$
declare uid uuid := auth.uid(); opp uuid; did uuid; mp numeric; m text := case when p_mode = 'ranked' then 'ranked' else 'classic' end;
begin
  if uid is null or not public.is_approved() or public.is_blocked(uid) then raise exception 'not allowed'; end if;
  perform public.duel_settle(id) from public.duels where status = 'active' and (p1 = uid or p2 = uid);
  select id into did from public.duels where status = 'active' and (p1 = uid or p2 = uid) order by created_at desc limit 1;
  if did is not null then delete from public.duel_queue where user_id = uid; return did; end if;
  mp := coalesce((select ap from public.scores where user_id = uid), 0);
  if mp < (case when m = 'ranked' then 200 else 20 end) then raise exception 'low points'; end if;
  delete from public.duel_queue where joined_at < now() - interval '10 seconds';
  select q.user_id into opp from public.duel_queue q
    where q.user_id <> uid and q.wn = p_wn and q.mode = m
      and (m = 'classic' or (
            abs(public.duel_lg(coalesce((select ap from public.scores where user_id = q.user_id), 0)) - public.duel_lg(mp)) <= 1
            and coalesce((select ap from public.scores where user_id = q.user_id), 0) >= 200
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
revoke all on function public.duel_join(int, text) from public, anon;
grant execute on function public.duel_join(int, text) to authenticated;

-- Salon: kişi başına ap (puan), lowr = dereceli için yetersiz; teklif ve düello satırlarında mode
create or replace function public.duel_lobby() returns jsonb
language plpgsql security definer set search_path = public as $$
declare uid uuid := auth.uid(); r jsonb;
begin
  if uid is null or not public.is_approved() then raise exception 'not allowed'; end if;
  update public.profiles set duel_seen = now() where user_id = uid;
  select jsonb_build_object(
    'online', coalesce((select jsonb_agg(public.duel_person(p.user_id) || jsonb_build_object(
          'low', coalesce(s.ap, 0) < 20, 'lowr', coalesce(s.ap, 0) < 200, 'ap', coalesce(s.ap, 0),
          'st', case when public.duel_busy(p.user_id) then 'duel'
                     when exists(select 1 from public.duel_invites i where i.status = 'pending' and i.expires_at > now() and p.user_id in (i.from_user, i.to_user)) then 'invite'
                     else 'free' end) order by coalesce(s.name, p.username))
        from public.profiles p left join public.scores s on s.user_id = p.user_id
        where p.user_id <> uid and p.duel_seen > now() - interval '12 seconds'
          and (p.approved or exists(select 1 from public.admins a where a.user_id = p.user_id))), '[]'::jsonb),
    'duels', coalesce((select jsonb_agg(jsonb_build_object('id', t.id, 'a', public.duel_person(t.p1), 'b', public.duel_person(t.p2),
          'a1', t.a1, 'a2', t.a2, 'qn', t.qn, 's1', t.s1, 's2', t.s2, 'mode', t.mode) order by t.created_at desc)
        from (select * from public.duels d where d.status = 'active' and now() < d.start_at + make_interval(secs => d.qn * d.per_q + 15)
              order by d.created_at desc limit 10) t), '[]'::jsonb),
    'inbox', (select jsonb_build_object('id', i.id, 'mode', i.mode, 'from', public.duel_person(i.from_user) || jsonb_build_object('ap', coalesce((select ap from public.scores where user_id = i.from_user), 0)),
                'left_ms', greatest(0, floor(extract(epoch from (i.expires_at - now())) * 1000))::int)
              from public.duel_invites i where i.to_user = uid and i.status = 'pending' and i.expires_at > now()
              order by i.created_at desc limit 1),
    'outbox', (select jsonb_build_object('id', i.id, 'mode', i.mode, 'to', public.duel_person(i.to_user), 'duel_id', i.duel_id,
                'status', case when i.status = 'pending' and i.expires_at <= now() then 'expired' else i.status end,
                'left_ms', greatest(0, floor(extract(epoch from (i.expires_at - now())) * 1000))::int)
               from public.duel_invites i where i.from_user = uid and i.created_at > now() - interval '60 seconds'
               order by i.created_at desc limit 1)
  ) into r;
  return r;
end $$;

-- Teklif gönder
drop function if exists public.duel_invite(uuid);
create or replace function public.duel_invite(target uuid, p_mode text default 'classic') returns jsonb
language plpgsql security definer set search_path = public as $$
declare uid uuid := auth.uid(); iid uuid; m text := case when p_mode = 'ranked' then 'ranked' else 'classic' end; need numeric := case when p_mode = 'ranked' then 200 else 20 end;
begin
  if uid is null or not public.is_approved() or public.is_blocked(uid) then raise exception 'not allowed'; end if;
  if target is null or target = uid then raise exception 'bad target'; end if;
  if not public.chat_can_receive(target) then raise exception 'bad target'; end if;
  perform public.duel_settle(id) from public.duels where status = 'active' and (p1 in (uid, target) or p2 in (uid, target));
  if coalesce((select ap from public.scores where user_id = uid), 0) < need then raise exception 'low points'; end if;
  if coalesce((select ap from public.scores where user_id = target), 0) < need then raise exception 'target low'; end if;
  if m = 'ranked' and not public.duel_pair_ok(uid, target) then raise exception 'pair limit'; end if;
  if public.duel_busy(uid) then raise exception 'me busy'; end if;
  if public.duel_busy(target) then raise exception 'target busy'; end if;
  if not exists(select 1 from public.profiles where user_id = target and duel_seen > now() - interval '15 seconds') then raise exception 'offline'; end if;
  if exists(select 1 from public.duel_invites i where i.status = 'pending' and i.expires_at > now()
            and (i.from_user in (uid, target) or i.to_user in (uid, target))) then raise exception 'invite busy'; end if;
  if (select count(*) from public.duel_invites where from_user = uid and created_at > now() - interval '1 minute') >= 8 then raise exception 'too many'; end if;
  delete from public.duel_invites where created_at < now() - interval '1 hour';
  insert into public.duel_invites(from_user, to_user, mode) values (uid, target, m) returning id into iid;
  return jsonb_build_object('id', iid, 'left_ms', 15000);
end $$;
revoke all on function public.duel_invite(uuid, text) from public, anon;
grant execute on function public.duel_invite(uuid, text) to authenticated;

-- Teklife cevap
create or replace function public.duel_respond(inv uuid, accept boolean, p_wn int) returns jsonb
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
revoke all on function public.duel_lobby() from public, anon;
revoke all on function public.duel_respond(uuid, boolean, int) from public, anon;
grant execute on function public.duel_lobby() to authenticated;
grant execute on function public.duel_respond(uuid, boolean, int) to authenticated;

-- Herkese açık maç geçmişi (mode ve puan değişimiyle)
drop function if exists public.duel_history(int);
create or replace function public.duel_history(n int default 50) returns table(id uuid, p1 uuid, p2 uuid, s1 numeric, s2 numeric, c1 int, c2 int, a1 int, a2 int, t1 numeric, t2 numeric, winner uuid, created_at timestamptz, mode text, dl1 numeric, dl2 numeric)
language sql stable security definer set search_path = public as $$
  select d.id, d.p1, d.p2, d.s1::numeric, d.s2::numeric, d.c1::int, d.c2::int, d.a1::int, d.a2::int, d.t1::numeric, d.t2::numeric, d.winner, d.created_at, d.mode, d.dl1, d.dl2
  from public.duels d
  where d.status = 'done' and auth.uid() is not null
  order by d.created_at desc
  limit least(greatest(coalesce(n, 50), 1), 100);
$$;
revoke all on function public.duel_history(int) from public, anon;
grant execute on function public.duel_history(int) to authenticated;
