-- Dosya: supabase-flags.sql
-- Kelime Defteri: şerit flamalar (yöneticinin kullanıcılara verdiği ünvan flamaları). SQL Editor'da bir kez çalıştır.
-- (Önce supabase-admin.sql çalıştırılmış olmalı.)
create table if not exists public.user_flags (
  user_id uuid primary key references auth.users(id) on delete cascade,
  flag text not null check (char_length(flag) between 1 and 24),
  set_at timestamptz not null default now()
);
alter table public.user_flags enable row level security;
revoke all on public.user_flags from anon, authenticated;

-- Onaylı herkes kimde hangi flama olduğunu görür (kişisel veri yok)
create or replace function public.all_flags()
returns table(user_id uuid, flag text)
language plpgsql security definer stable set search_path = public as $$
begin
  if auth.uid() is null then raise exception 'not allowed'; end if;
  return query select f.user_id, f.flag from public.user_flags f;
end $$;

-- Yönetici: flama ver / kaldır (flag_id boş ya da null ise kaldırır)
create or replace function public.admin_set_flag(target uuid, flag_id text)
returns void language plpgsql security definer set search_path = public as $$
begin
  if not public.is_admin() then raise exception 'not allowed'; end if;
  if flag_id is null or btrim(flag_id) = '' then
    delete from public.user_flags where user_id = target;
  else
    insert into public.user_flags(user_id, flag) values (target, left(btrim(flag_id), 24))
    on conflict (user_id) do update set flag = excluded.flag, set_at = now();
  end if;
end $$;

revoke all on function public.all_flags() from public, anon;
revoke all on function public.admin_set_flag(uuid, text) from public, anon;
grant execute on function public.all_flags() to authenticated;
grant execute on function public.admin_set_flag(uuid, text) to authenticated;

-- Mevcut yöneticilere "Test eden yapımcı" flamasını ver
insert into public.user_flags(user_id, flag)
select a.user_id, 'maker' from public.admins a
on conflict (user_id) do nothing;
