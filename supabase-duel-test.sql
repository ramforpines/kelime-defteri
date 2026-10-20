-- Dosya: supabase-duel-test.sql
-- GEÇİCİ KISITLAMA (ben diyene kadar): yönetici + test hesabı (kullanici52541) yalnızca birbirleriyle düello oynar.
--  * Diğer kullanıcılarla eşleşemez, teklif gönderemez/alamaz, salonda birbirlerini görmez.
--  * Kendi aralarındaki maçlar kayda geçmez: durum 'test' olur; puan, geçmiş, galibiyet sayısı ve istatistiğe işlenmez.
--  * Diğer kullanıcılar için hiçbir şey değişmez.
-- Önce supabase-duel-guard.sql (veya en azından aşağıdaki kısıt güncellemesi) ve diğer düello dosyaları çalışmış olmalı.
-- SQL Editor'da bir kez çalıştır; birden çok kez çalıştırılabilir. Kaldırmak için supabase-duel-test-off.sql.

alter table public.duels drop constraint if exists duels_status_check;
alter table public.duels add constraint duels_status_check check (status in ('active','done','void','test'));

create or replace function public.duel_is_test(u uuid) returns boolean
language sql stable security definer set search_path = public as $$
  select exists(select 1 from public.admins a where a.user_id = u)
      or coalesce((select lower(split_part(x.email, '@', 1)) = any (array['kullanici52541']) from auth.users x where x.id = u), false)
$$;
revoke all on function public.duel_is_test(uuid) from public, anon, authenticated;

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
      and public.duel_is_test(q.user_id) = public.duel_is_test(uid)
      and (m = 'classic' or (
            abs(public.duel_elg(q.user_id) - public.duel_elg(uid)) <= 1
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

create or replace function public.duel_invite(target uuid, p_mode text default 'classic') returns jsonb
language plpgsql security definer set search_path = public as $$
declare uid uuid := auth.uid(); iid uuid; m text := case when p_mode = 'ranked' then 'ranked' else 'classic' end; need numeric := case when p_mode = 'ranked' then 200 else 20 end;
begin
  if uid is null or not public.is_approved() or public.is_blocked(uid) then raise exception 'not allowed'; end if;
  if target is null or target = uid then raise exception 'bad target'; end if;
  if not public.chat_can_receive(target) then raise exception 'bad target'; end if;
  if public.duel_is_test(uid) <> public.duel_is_test(target) then raise exception 'bad target'; end if;
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
  if public.duel_is_test(uid) <> public.duel_is_test(i.from_user) then
    update public.duel_invites set status = 'cancelled' where id = inv;
    return jsonb_build_object('status', 'expired');
  end if;
  if not accept then
    update public.duel_invites set status = 'declined' where id = inv;
    return jsonb_build_object('status', 'declined');
  end if;
  if i.mode = 'ranked' and not coalesce(p_rk, false) then
    update public.duel_invites set status = 'cancelled' where id = inv;
    return jsonb_build_object('status', 'old');
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

create or replace function public.duel_lobby(p_mode text default 'classic') returns jsonb
language plpgsql security definer set search_path = public as $$
declare uid uuid := auth.uid(); r jsonb; m text := case when p_mode = 'ranked' then 'ranked' else 'classic' end;
begin
  if uid is null or not public.is_approved() then raise exception 'not allowed'; end if;
  update public.profiles set duel_seen = now(), duel_mode = m where user_id = uid;
  select jsonb_build_object(
    'online', case when m = 'ranked' then
        -- dereceli: yalnızca "Dereceli rakip bul"a basıp kuyrukta bekleyenler; isim/profil gönderilmez
        coalesce((select jsonb_agg(jsonb_build_object('id', q.user_id, 'st', 'free', 'low', false, 'lowr', false, 'ap', coalesce(s.ap, 0)) order by q.joined_at)
          from public.duel_queue q left join public.scores s on s.user_id = q.user_id
          where q.user_id <> uid and q.mode = 'ranked' and q.joined_at > now() - interval '8 seconds'
            and public.duel_is_test(q.user_id) = public.duel_is_test(uid)), '[]'::jsonb)
      else coalesce((select jsonb_agg(public.duel_person(p.user_id) || jsonb_build_object(
          'low', coalesce(s.ap, 0) < 20, 'lowr', coalesce(s.ap, 0) < 200, 'ap', coalesce(s.ap, 0),
          'st', case when public.duel_busy(p.user_id) then 'duel'
                     when exists(select 1 from public.duel_invites i where i.status = 'pending' and i.expires_at > now() and p.user_id in (i.from_user, i.to_user)) then 'invite'
                     else 'free' end) order by coalesce(s.name, p.username))
        from public.profiles p left join public.scores s on s.user_id = p.user_id
        where p.user_id <> uid and p.duel_seen > now() - interval '12 seconds' and p.duel_mode = m
          and public.duel_is_test(p.user_id) = public.duel_is_test(uid)
          and (p.approved or exists(select 1 from public.admins a where a.user_id = p.user_id))), '[]'::jsonb) end,
    'wait', case when m = 'ranked' then
        coalesce((select jsonb_agg(jsonb_build_object('id', p.user_id) order by p.duel_seen)
          from public.profiles p
          where p.user_id <> uid and p.duel_seen > now() - interval '12 seconds' and p.duel_mode = 'ranked'
            and public.duel_is_test(p.user_id) = public.duel_is_test(uid)
            and (p.approved or exists(select 1 from public.admins a where a.user_id = p.user_id))
            and not exists(select 1 from public.duel_queue q where q.user_id = p.user_id and q.joined_at > now() - interval '8 seconds')
            and not public.duel_busy(p.user_id)), '[]'::jsonb)
      else '[]'::jsonb end,
    'duels', coalesce((select jsonb_agg(jsonb_build_object('id', t.id, 'a', public.duel_person(t.p1), 'b', public.duel_person(t.p2),
          'a1', t.a1, 'a2', t.a2, 'qn', t.qn, 's1', t.s1, 's2', t.s2, 'mode', t.mode) order by t.created_at desc)
        from (select * from public.duels d where d.status = 'active' and d.mode = m and public.duel_is_test(d.p1) = public.duel_is_test(uid) and now() < d.start_at + make_interval(secs => d.qn * d.per_q + 15)
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

  -- test grubu (yönetici + test hesabı) kendi aralarında oynadıkları maçlar: kayda geçmez, puan/istatistik işlenmez
  if public.duel_is_test(d.p1) and public.duel_is_test(d.p2) then
    w := case when d.s1 > d.s2 then d.p1 when d.s2 > d.s1 then d.p2 else null end;
    update public.duels set status = 'test', done_at = now(), winner = w, pay1 = 0, pay2 = 0, dl1 = 0, dl2 = 0 where id = did;
    return;
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
    p1v := 22.5; p2v := 22.5;
  else
    sw := greatest(case when w = d.p1 then d.s1 else d.s2 end, 0);
    pw := round(25 + case when tot = 0 then 10 else 20.0 * sw / tot end, 1);
    if w = d.p1 then p1v := pw; p2v := 45 - pw; else p2v := pw; p1v := 45 - pw; end if;
  end if;
  update public.duels set status = 'done', done_at = now(), winner = w, pay1 = p1v, pay2 = p2v where id = did;
end $$;

revoke all on function public.duel_join(int, text) from public, anon;
grant execute on function public.duel_join(int, text) to authenticated;
revoke all on function public.duel_invite(uuid, text) from public, anon;
grant execute on function public.duel_invite(uuid, text) to authenticated;
revoke all on function public.duel_respond(uuid, boolean, int, boolean) from public, anon;
grant execute on function public.duel_respond(uuid, boolean, int, boolean) to authenticated;
revoke all on function public.duel_lobby(text) from public, anon;
grant execute on function public.duel_lobby(text) to authenticated;
revoke all on function public.duel_settle(uuid) from public, anon, authenticated;
