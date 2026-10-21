-- Dosya: supabase-chat-ban.sql
-- Kelime Defteri: yönetici sohbet yasağı. Yasaklı kullanıcı genel sohbete ve özel mesajlara yazamaz (okuyabilir); süreli ya da süresiz olabilir.
-- Gerek: supabase-chat.sql, supabase-chat-limit.sql, supabase-chat-admin.sql, supabase-admin.sql. SQL Editor'da bir kez çalıştırın; tekrar çalıştırmak güvenlidir.

create table if not exists public.chat_bans (
  user_id uuid primary key references auth.users(id) on delete cascade,
  until timestamptz,                -- null = süresiz
  note text,
  by_user uuid,
  created_at timestamptz not null default now()
);
alter table public.chat_bans enable row level security;
revoke all on public.chat_bans from anon, authenticated;

create or replace function public.chat_banned(uid uuid) returns boolean
language sql security definer stable set search_path = public as $$
  select exists(select 1 from public.chat_bans b where b.user_id = uid and (b.until is null or b.until > now()))
$$;
revoke all on function public.chat_banned(uuid) from public, anon;
grant execute on function public.chat_banned(uuid) to authenticated;

-- Yazma politikası: mevcut kurallar + sohbet yasağı olmamak (yönetici yasaklanamaz)
drop policy if exists "chat_insert" on public.chat_messages;
create policy "chat_insert" on public.chat_messages for insert to authenticated
  with check (
    user_id = auth.uid() and public.is_approved() and not public.is_blocked(auth.uid())
    and not public.chat_banned(auth.uid())
    and (
      (to_user is null and (public.is_admin() or (select count(*) from public.chat_messages m
         where m.user_id = auth.uid() and m.to_user is null and m.created_at > now() - interval '1 minute') < 5))
      or
      (to_user is not null and public.chat_can_receive(to_user)
         and (public.is_admin() or (select count(*) from public.chat_messages m
         where m.user_id = auth.uid() and m.to_user is not null and m.created_at > now() - interval '1 minute') < 60))
    )
  );

-- Kullanıcı: kendi yasağı (yoksa null)
create or replace function public.chat_my_ban() returns jsonb
language sql stable security definer set search_path = public as $$
  select jsonb_build_object('until', b.until, 'forever', b.until is null, 'note', b.note)
  from public.chat_bans b where b.user_id = auth.uid() and (b.until is null or b.until > now())
$$;
revoke all on function public.chat_my_ban() from public, anon;
grant execute on function public.chat_my_ban() to authenticated;

-- Yönetici: yasakla (p_min boş ya da 0 = süresiz)
create or replace function public.admin_chat_ban(target uuid, p_min int default null, p_note text default null) returns void
language plpgsql security definer set search_path = public as $$
begin
  if not public.is_admin() then raise exception 'not allowed'; end if;
  if exists(select 1 from public.admins where user_id = target) then raise exception 'admin'; end if;
  insert into public.chat_bans(user_id, until, note, by_user)
    values (target, case when coalesce(p_min, 0) > 0 then now() + make_interval(mins => least(p_min, 525600)) end, left(coalesce(p_note, ''), 300), auth.uid())
  on conflict (user_id) do update set until = excluded.until, note = excluded.note, by_user = excluded.by_user, created_at = now();
end $$;
revoke all on function public.admin_chat_ban(uuid, int, text) from public, anon;
grant execute on function public.admin_chat_ban(uuid, int, text) to authenticated;

-- Yönetici: yasağı kaldır
create or replace function public.admin_chat_unban(target uuid) returns void
language plpgsql security definer set search_path = public as $$
begin
  if not public.is_admin() then raise exception 'not allowed'; end if;
  delete from public.chat_bans where user_id = target;
end $$;
revoke all on function public.admin_chat_unban(uuid) from public, anon;
grant execute on function public.admin_chat_unban(uuid) to authenticated;

-- Yönetici: süren yasaklar
create or replace function public.admin_chat_bans() returns table(user_id uuid, name text, until timestamptz, note text, created_at timestamptz)
language plpgsql stable security definer set search_path = public as $$
begin
  if not public.is_admin() then raise exception 'not allowed'; end if;
  return query select b.user_id, coalesce(s.name, 'Kullanıcı')::text, b.until, b.note, b.created_at
    from public.chat_bans b left join public.scores s on s.user_id = b.user_id
    where b.until is null or b.until > now() order by b.created_at desc;
end $$;
revoke all on function public.admin_chat_bans() from public, anon;
grant execute on function public.admin_chat_bans() to authenticated;
