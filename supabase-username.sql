-- Kelime Defteri: profil kartında kullanıcı adı görünsün. SQL Editor'da bir kez çalıştır.
alter table public.scores add column if not exists un text not null default '';

-- Kullanıcı adı sunucuda, profil tablosundan doldurulur (istemci değiştiremez)
create or replace function public.scores_fill_un() returns trigger
language plpgsql security definer set search_path = public as $$
begin
  new.un := coalesce((select username from public.profiles where user_id = new.user_id), '');
  return new;
end $$;
drop trigger if exists scores_fill_un_trg on public.scores;
create trigger scores_fill_un_trg before insert or update on public.scores
  for each row execute function public.scores_fill_un();

-- Mevcut satırları doldur
update public.scores s set un = p.username from public.profiles p where p.user_id = s.user_id;
