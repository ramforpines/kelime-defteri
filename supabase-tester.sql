-- Beta test kullanıcıları: yönetici gibi en güncel (beta/) sürümü açar ama yönetici yetkisi almaz.
create table if not exists public.beta_testers (
  user_id uuid primary key references auth.users(id) on delete cascade,
  added_at timestamptz not null default now()
);
alter table public.beta_testers enable row level security;
revoke all on public.beta_testers from anon, authenticated;

-- giriş yapan kullanıcı beta sürümü görmeli mi? (yönetici ya da test kullanıcısı)
create or replace function public.is_beta() returns boolean
language sql security definer stable set search_path = public as $$
  select exists(select 1 from public.admins where user_id = auth.uid())
      or exists(select 1 from public.beta_testers where user_id = auth.uid());
$$;
revoke all on function public.is_beta() from public, anon;
grant execute on function public.is_beta() to authenticated;

-- test kullanıcısı: mustafa.cetiner
insert into public.beta_testers(user_id)
select user_id from public.profiles where lower(username) = 'mustafa.cetiner'
on conflict do nothing;

-- kontrol: eklenen test kullanıcıları
select p.username, b.added_at from public.beta_testers b join public.profiles p on p.user_id = b.user_id;
