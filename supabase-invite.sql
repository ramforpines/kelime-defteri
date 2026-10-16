-- Dosya: supabase-invite.sql
-- Kelime Defteri: düello salonu (çevrimiçi liste, aktif düellolar) + düello teklifi (15 sn). SQL Editor'da bir kez çalıştır.
-- (supabase-admin.sql, supabase-theme.sql ve supabase-duel.sql çalıştırılmış olmalı.)

alter table public.profiles add column if not exists duel_seen timestamptz;

create table if not exists public.duel_invites (
  id uuid primary key default gen_random_uuid(),
  from_user uuid not null references auth.users(id) on delete cascade,
  to_user uuid not null references auth.users(id) on delete cascade,
  status text not null default 'pending' check (status in ('pending','accepted','declined','cancelled')),
  duel_id uuid,
  created_at timestamptz not null default now(),
  expires_at timestamptz not null default now() + interval '15 seconds',
  check (from_user <> to_user)
);
create index if not exists duel_inv_to_idx on public.duel_invites(to_user, created_at desc);
create index if not exists duel_inv_from_idx on public.duel_invites(from_user, created_at desc);
alter table public.duel_invites enable row level security;
revoke all on public.duel_invites from anon, authenticated;

-- iç: kullanıcı şu an süren bir düelloda mı?
create or replace function public.duel_busy(u uuid) returns boolean
language sql security definer stable set search_path = public as $$
  select exists(select 1 from public.duels d
    where d.status = 'active' and u in (d.p1, d.p2)
      and now() < d.start_at + make_interval(secs => d.qn * d.per_q + 15))
$$;
revoke all on function public.duel_busy(uuid) from public, anon, authenticated;

-- iç: kullanıcı kartı
create or replace function public.duel_person(u uuid) returns jsonb
language sql security definer stable set search_path = public as $$
  select jsonb_build_object('id', p.user_id, 'un', p.username, 'name', coalesce(s.name, p.username),
    'color', coalesce(s.color, 0), 'av', coalesce(s.av, 0), 'fr', coalesce(s.fr, ''),
    'ad', exists(select 1 from public.admins a where a.user_id = p.user_id))
  from public.profiles p left join public.scores s on s.user_id = p.user_id where p.user_id = u
$$;
revoke all on function public.duel_person(uuid) from public, anon, authenticated;

-- Salon: kendini "düello sekmesindeyim" diye işaretler (birkaç saniyede bir çağrılır) ve durumu döner
create or replace function public.duel_lobby() returns jsonb
language plpgsql security definer set search_path = public as $$
declare uid uuid := auth.uid(); r jsonb;
begin
  if uid is null or not public.is_approved() then raise exception 'not allowed'; end if;
  update public.profiles set duel_seen = now() where user_id = uid;
  select jsonb_build_object(
    'online', coalesce((select jsonb_agg(public.duel_person(p.user_id) || jsonb_build_object(
          'low', coalesce(s.ap, 0) < 20,
          'st', case when public.duel_busy(p.user_id) then 'duel'
                     when exists(select 1 from public.duel_invites i where i.status = 'pending' and i.expires_at > now() and p.user_id in (i.from_user, i.to_user)) then 'invite'
                     else 'free' end) order by coalesce(s.name, p.username))
        from public.profiles p left join public.scores s on s.user_id = p.user_id
        where p.user_id <> uid and p.duel_seen > now() - interval '12 seconds'
          and (p.approved or exists(select 1 from public.admins a where a.user_id = p.user_id))), '[]'::jsonb),
    'duels', coalesce((select jsonb_agg(jsonb_build_object('id', t.id, 'a', public.duel_person(t.p1), 'b', public.duel_person(t.p2),
          'a1', t.a1, 'a2', t.a2, 'qn', t.qn, 's1', t.s1, 's2', t.s2) order by t.created_at desc)
        from (select * from public.duels d where d.status = 'active' and now() < d.start_at + make_interval(secs => d.qn * d.per_q + 15)
              order by d.created_at desc limit 10) t), '[]'::jsonb),
    'inbox', (select jsonb_build_object('id', i.id, 'from', public.duel_person(i.from_user),
                'left_ms', greatest(0, floor(extract(epoch from (i.expires_at - now())) * 1000))::int)
              from public.duel_invites i where i.to_user = uid and i.status = 'pending' and i.expires_at > now()
              order by i.created_at desc limit 1),
    'outbox', (select jsonb_build_object('id', i.id, 'to', public.duel_person(i.to_user), 'duel_id', i.duel_id,
                'status', case when i.status = 'pending' and i.expires_at <= now() then 'expired' else i.status end,
                'left_ms', greatest(0, floor(extract(epoch from (i.expires_at - now())) * 1000))::int)
               from public.duel_invites i where i.from_user = uid and i.created_at > now() - interval '60 seconds'
               order by i.created_at desc limit 1)
  ) into r;
  return r;
end $$;

-- Teklif gönder (15 sn geçerli)
create or replace function public.duel_invite(target uuid) returns jsonb
language plpgsql security definer set search_path = public as $$
declare uid uuid := auth.uid(); iid uuid;
begin
  if uid is null or not public.is_approved() or public.is_blocked(uid) then raise exception 'not allowed'; end if;
  if target is null or target = uid then raise exception 'bad target'; end if;
  if not public.chat_can_receive(target) then raise exception 'bad target'; end if;
  perform public.duel_settle(id) from public.duels where status = 'active' and (p1 in (uid, target) or p2 in (uid, target));
  if coalesce((select ap from public.scores where user_id = uid), 0) < 20 then raise exception 'low points'; end if;
  if coalesce((select ap from public.scores where user_id = target), 0) < 20 then raise exception 'target low'; end if;
  if public.duel_busy(uid) then raise exception 'me busy'; end if;
  if public.duel_busy(target) then raise exception 'target busy'; end if;
  if not exists(select 1 from public.profiles where user_id = target and duel_seen > now() - interval '15 seconds') then raise exception 'offline'; end if;
  if exists(select 1 from public.duel_invites i where i.status = 'pending' and i.expires_at > now()
            and (i.from_user in (uid, target) or i.to_user in (uid, target))) then raise exception 'invite busy'; end if;
  if (select count(*) from public.duel_invites where from_user = uid and created_at > now() - interval '1 minute') >= 8 then raise exception 'too many'; end if;
  delete from public.duel_invites where created_at < now() - interval '1 hour';
  insert into public.duel_invites(from_user, to_user) values (uid, target) returning id into iid;
  return jsonb_build_object('id', iid, 'left_ms', 15000);
end $$;

-- Teklifi geri çek
create or replace function public.duel_invite_cancel(inv uuid) returns void
language plpgsql security definer set search_path = public as $$
begin
  update public.duel_invites set status = 'cancelled' where id = inv and from_user = auth.uid() and status = 'pending';
end $$;

-- Teklife cevap: kabulde düello oluşur ve düello id'si döner
create or replace function public.duel_respond(inv uuid, accept boolean, p_wn int) returns jsonb
language plpgsql security definer set search_path = public as $$
declare uid uuid := auth.uid(); i public.duel_invites; did uuid;
begin
  if uid is null or not public.is_approved() then raise exception 'not allowed'; end if;
  select * into i from public.duel_invites where id = inv and to_user = uid for update;
  if not found or i.status <> 'pending' or i.expires_at <= now() then return jsonb_build_object('status', 'expired'); end if;
  if not accept then
    update public.duel_invites set status = 'declined' where id = inv;
    return jsonb_build_object('status', 'declined');
  end if;
  perform public.duel_settle(id) from public.duels where status = 'active' and (p1 in (uid, i.from_user) or p2 in (uid, i.from_user));
  if public.duel_busy(uid) or public.duel_busy(i.from_user) then
    update public.duel_invites set status = 'cancelled' where id = inv;
    return jsonb_build_object('status', 'busy');
  end if;
  if coalesce((select ap from public.scores where user_id = uid), 0) < 20
     or coalesce((select ap from public.scores where user_id = i.from_user), 0) < 20 then
    update public.duel_invites set status = 'cancelled' where id = inv;
    return jsonb_build_object('status', 'low');
  end if;
  delete from public.duel_queue where user_id in (uid, i.from_user);
  insert into public.duels(p1, p2, seed, wn, start_at)
    values (i.from_user, uid, floor(random() * 2147480000)::int, p_wn, now() + interval '5 seconds') returning id into did;
  update public.duel_invites set status = 'accepted', duel_id = did where id = inv;
  return jsonb_build_object('status', 'accepted', 'duel_id', did);
end $$;

revoke all on function public.duel_lobby() from public, anon;
revoke all on function public.duel_invite(uuid) from public, anon;
revoke all on function public.duel_invite_cancel(uuid) from public, anon;
revoke all on function public.duel_respond(uuid, boolean, int) from public, anon;
grant execute on function public.duel_lobby() to authenticated;
grant execute on function public.duel_invite(uuid) to authenticated;
grant execute on function public.duel_invite_cancel(uuid) to authenticated;
grant execute on function public.duel_respond(uuid, boolean, int) to authenticated;
