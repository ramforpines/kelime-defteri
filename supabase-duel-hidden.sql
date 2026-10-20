-- Dereceli salon: kuyrukta arayanlar 'Maç arıyor', lobide bekleyenler 'Lobidekiler' olarak, ikisi de isimsiz (yalnızca id/lig) görünür.
-- Supabase SQL Editor'da bir kez çalıştırın.

drop function if exists public.duel_lobby();
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
          where q.user_id <> uid and q.mode = 'ranked' and q.joined_at > now() - interval '8 seconds'), '[]'::jsonb)
      else coalesce((select jsonb_agg(public.duel_person(p.user_id) || jsonb_build_object(
          'low', coalesce(s.ap, 0) < 20, 'lowr', coalesce(s.ap, 0) < 200, 'ap', coalesce(s.ap, 0),
          'st', case when public.duel_busy(p.user_id) then 'duel'
                     when exists(select 1 from public.duel_invites i where i.status = 'pending' and i.expires_at > now() and p.user_id in (i.from_user, i.to_user)) then 'invite'
                     else 'free' end) order by coalesce(s.name, p.username))
        from public.profiles p left join public.scores s on s.user_id = p.user_id
        where p.user_id <> uid and p.duel_seen > now() - interval '12 seconds' and p.duel_mode = m
          and (p.approved or exists(select 1 from public.admins a where a.user_id = p.user_id))), '[]'::jsonb) end,
    'wait', case when m = 'ranked' then
        coalesce((select jsonb_agg(jsonb_build_object('id', p.user_id) order by p.duel_seen)
          from public.profiles p
          where p.user_id <> uid and p.duel_seen > now() - interval '12 seconds' and p.duel_mode = 'ranked'
            and (p.approved or exists(select 1 from public.admins a where a.user_id = p.user_id))
            and not exists(select 1 from public.duel_queue q where q.user_id = p.user_id and q.joined_at > now() - interval '8 seconds')
            and not public.duel_busy(p.user_id)), '[]'::jsonb)
      else '[]'::jsonb end,
    'duels', coalesce((select jsonb_agg(jsonb_build_object('id', t.id, 'a', public.duel_person(t.p1), 'b', public.duel_person(t.p2),
          'a1', t.a1, 'a2', t.a2, 'qn', t.qn, 's1', t.s1, 's2', t.s2, 'mode', t.mode) order by t.created_at desc)
        from (select * from public.duels d where d.status = 'active' and d.mode = m and now() < d.start_at + make_interval(secs => d.qn * d.per_q + 15)
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

