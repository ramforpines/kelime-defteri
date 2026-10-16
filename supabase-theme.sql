-- Dosya: supabase-theme.sql
-- Kelime Defteri: kullanıcı adı ve yönetici işareti (liderlik/profil satırı temaları için). SQL Editor'da bir kez çalıştır.
-- supabase-username.sql'in yerini alır; onu çalıştırdıysan bunu da çalıştırman sorun olmaz.
alter table public.scores add column if not exists un text not null default '';
alter table public.scores add column if not exists ad boolean not null default false;

create or replace function public.scores_fill_un() returns trigger
language plpgsql security definer set search_path = public as $$
begin
  new.un := coalesce((select username from public.profiles where user_id = new.user_id), '');
  new.ad := exists(select 1 from public.admins where user_id = new.user_id);
  if new.av = 49 and not new.ad then new.av := 0; end if;   -- 49 = yalnızca yöneticiye açık F-16 avatarı
  return new;
end $$;
drop trigger if exists scores_fill_un_trg on public.scores;
create trigger scores_fill_un_trg before insert or update on public.scores
  for each row execute function public.scores_fill_un();

update public.scores s set un = coalesce(p.username, ''), ad = exists(select 1 from public.admins a where a.user_id = s.user_id)
from public.profiles p where p.user_id = s.user_id;
