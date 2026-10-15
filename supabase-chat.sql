-- Kelime Defteri: genel sohbet + özel mesajlar. SQL Editor'da bir kez çalıştır.
-- (Önce supabase-admin.sql çalıştırılmış olmalı.)
create table if not exists public.chat_messages (
  id bigint generated always as identity primary key,
  user_id uuid not null references auth.users(id) on delete cascade,
  to_user uuid references auth.users(id) on delete cascade,   -- null = genel sohbet
  sname text not null default '',
  body text not null check (char_length(btrim(body)) between 1 and 500),
  created_at timestamptz not null default now(),
  check (to_user is null or to_user <> user_id)
);
create index if not exists chat_pub_idx on public.chat_messages(id desc) where to_user is null;
create index if not exists chat_dm_to_idx on public.chat_messages(to_user, id desc) where to_user is not null;
create index if not exists chat_dm_from_idx on public.chat_messages(user_id, id desc) where to_user is not null;
alter table public.chat_messages enable row level security;

-- Gönderen adı sunucuda, liderlik tablosundaki isimden doldurulur (taklit edilemez)
create or replace function public.chat_fill() returns trigger
language plpgsql security definer set search_path = public as $$
begin
  new.sname := coalesce((select name from public.scores where user_id = new.user_id), 'Kullanıcı');
  new.body := btrim(new.body);
  return new;
end $$;
drop trigger if exists chat_fill_trg on public.chat_messages;
create trigger chat_fill_trg before insert on public.chat_messages
  for each row execute function public.chat_fill();

-- Okuma: genel mesajlar herkese (onaylı), özel mesajlar yalnızca taraflara
drop policy if exists "chat_select" on public.chat_messages;
create policy "chat_select" on public.chat_messages for select to authenticated
  using (public.is_approved() and (to_user is null or user_id = auth.uid() or to_user = auth.uid()));

-- Yazma: onaylı, tablodan çıkarılmamış, dakikada en fazla 12 mesaj
drop policy if exists "chat_insert" on public.chat_messages;
create policy "chat_insert" on public.chat_messages for insert to authenticated
  with check (
    user_id = auth.uid() and public.is_approved() and not public.is_blocked(auth.uid())
    and (to_user is null or exists(select 1 from public.profiles p where p.user_id = to_user and p.approved))
    and (select count(*) from public.chat_messages m where m.user_id = auth.uid() and m.created_at > now() - interval '1 minute') < 12
  );

-- Kullanıcı yalnızca kendi mesajını silebilir
drop policy if exists "chat_delete_own" on public.chat_messages;
create policy "chat_delete_own" on public.chat_messages for delete to authenticated using (user_id = auth.uid());

revoke all on public.chat_messages from anon;
revoke all on public.chat_messages from authenticated;
grant select, delete on public.chat_messages to authenticated;
grant insert (to_user, body) on public.chat_messages to authenticated;
-- insert sırasında user_id istemciden gelir
grant insert (user_id) on public.chat_messages to authenticated;

-- Yönetici herhangi bir genel mesajı silebilir
create or replace function public.admin_delete_chat(mid bigint)
returns void language plpgsql security definer set search_path = public as $$
begin
  if not public.is_admin() then raise exception 'not allowed'; end if;
  delete from public.chat_messages where id = mid;
end $$;
revoke all on function public.admin_delete_chat(bigint) from public, anon;
grant execute on function public.admin_delete_chat(bigint) to authenticated;
