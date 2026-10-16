-- Dosya: supabase-signup-open.sql
-- Kelime Defteri: toplu kayıt sınırını kapatır (10 dakikada 40 / bekleyen 300). SQL Editor'da bir kez çalıştır.
-- Kullanıcı adı biçimi ve ayrılmış ad denetimi kalır.
create or replace function public.handle_new_user() returns trigger
language plpgsql security definer set search_path = public as $$
declare un text := split_part(new.email, '@', 1);
begin
  if un !~ '^[a-z0-9][a-z0-9_.-]{2,19}$' then raise exception 'invalid username'; end if;
  if public.reserved_name(un) then raise exception 'reserved username'; end if;
  insert into public.profiles(user_id, username, approved) values (new.id, un, false) on conflict do nothing;
  return new;
end $$;
