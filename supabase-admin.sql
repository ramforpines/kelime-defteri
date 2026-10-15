-- Kelime Defteri: yönetici onayı ve kullanıcı silme. SQL Editor'da bir kez çalıştır.
-- (Önce supabase-setup.sql çalıştırılmış olmalı.)

-- 1) Kullanıcı profilleri: yeni kayıtlar onay bekler
create table if not exists public.profiles (
  user_id uuid primary key references auth.users(id) on delete cascade,
  username text not null,
  approved boolean not null default false,
  created_at timestamptz not null default now()
);
create table if not exists public.admins (
  user_id uuid primary key references auth.users(id) on delete cascade
);
alter table public.profiles enable row level security;
alter table public.admins enable row level security;

-- Yeni kayıt olunca otomatik profil (onaysız) oluştur
create or replace function public.handle_new_user() returns trigger
language plpgsql security definer set search_path = public as $$
begin
  insert into public.profiles(user_id, username, approved)
  values (new.id, split_part(new.email, '@', 1), false)
  on conflict do nothing;
  return new;
end $$;
drop trigger if exists on_auth_user_created on auth.users;
create trigger on_auth_user_created after insert on auth.users
  for each row execute function public.handle_new_user();

-- Şu an kayıtlı olan herkes onaylı sayılır
insert into public.profiles(user_id, username, approved)
select id, split_part(email, '@', 1), true from auth.users
on conflict do nothing;

-- 2) Yardımcı fonksiyonlar
create or replace function public.is_admin() returns boolean
language sql security definer stable set search_path = public as $$
  select exists(select 1 from public.admins where user_id = auth.uid())
$$;
create or replace function public.is_approved() returns boolean
language sql security definer stable set search_path = public as $$
  select coalesce((select approved from public.profiles where user_id = auth.uid()), false)
         or exists(select 1 from public.admins where user_id = auth.uid())
$$;

-- 3) Güvenlik kuralları: onaysız kullanıcılar veri yazamaz, tabloyu göremez
drop policy if exists "profiles_select" on public.profiles;
create policy "profiles_select" on public.profiles for select to authenticated
  using (user_id = auth.uid() or public.is_admin());
drop policy if exists "admins_select_self" on public.admins;
create policy "admins_select_self" on public.admins for select to authenticated using (user_id = auth.uid());

drop policy if exists "state_select_own" on public.user_state;
drop policy if exists "state_insert_own" on public.user_state;
drop policy if exists "state_update_own" on public.user_state;
create policy "state_select_own" on public.user_state for select to authenticated
  using (auth.uid() = user_id and public.is_approved());
create policy "state_insert_own" on public.user_state for insert to authenticated
  with check (auth.uid() = user_id and public.is_approved());
create policy "state_update_own" on public.user_state for update to authenticated
  using (auth.uid() = user_id and public.is_approved())
  with check (auth.uid() = user_id and public.is_approved());

drop policy if exists "scores_select" on public.scores;
drop policy if exists "scores_insert_own" on public.scores;
drop policy if exists "scores_update_own" on public.scores;
create policy "scores_select" on public.scores for select to authenticated
  using (public.is_approved() and (hide = false or auth.uid() = user_id));
create policy "scores_insert_own" on public.scores for insert to authenticated
  with check (auth.uid() = user_id and public.is_approved());
create policy "scores_update_own" on public.scores for update to authenticated
  using (auth.uid() = user_id and public.is_approved())
  with check (auth.uid() = user_id and public.is_approved());

revoke all on public.profiles from anon;
revoke all on public.admins from anon;

-- 4) Yönetici işlemleri (yalnızca admins tablosundakiler çağırabilir)
create or replace function public.admin_list_users()
returns table(user_id uuid, username text, name text, approved boolean, is_admin boolean,
              created_at timestamptz, last_sign_in_at timestamptz)
language plpgsql security definer set search_path = public, auth as $$
begin
  if not public.is_admin() then raise exception 'not allowed'; end if;
  return query
    select p.user_id, p.username, s.name, p.approved,
           exists(select 1 from public.admins a where a.user_id = p.user_id),
           p.created_at, u.last_sign_in_at
    from public.profiles p
    left join public.scores s on s.user_id = p.user_id
    left join auth.users u on u.id = p.user_id
    order by p.approved asc, p.created_at desc;
end $$;

create or replace function public.admin_set_approved(target uuid, flag boolean)
returns void language plpgsql security definer set search_path = public as $$
begin
  if not public.is_admin() then raise exception 'not allowed'; end if;
  update public.profiles set approved = flag where user_id = target;
end $$;

create or replace function public.admin_delete_user(target uuid)
returns void language plpgsql security definer set search_path = public, auth as $$
begin
  if not public.is_admin() then raise exception 'not allowed'; end if;
  if target = auth.uid() then raise exception 'cannot delete yourself'; end if;
  if exists(select 1 from public.admins where user_id = target) then raise exception 'cannot delete an admin'; end if;
  delete from auth.users where id = target;   -- profil, ilerleme ve puan satırları da silinir
end $$;

revoke all on function public.admin_list_users() from public, anon;
revoke all on function public.admin_set_approved(uuid, boolean) from public, anon;
revoke all on function public.admin_delete_user(uuid) from public, anon;
grant execute on function public.admin_list_users() to authenticated;
grant execute on function public.admin_set_approved(uuid, boolean) to authenticated;
grant execute on function public.admin_delete_user(uuid) to authenticated;
grant execute on function public.is_admin() to authenticated;
grant execute on function public.is_approved() to authenticated;

-- 5) Kendinizi yönetici yapın: aşağıdaki satırdaki KULLANICI_ADINIZ yerine uygulamadaki kullanıcı adınızı yazın (küçük harf)
insert into public.admins(user_id)
select user_id from public.profiles where username = 'KULLANICI_ADINIZ'
on conflict do nothing;
