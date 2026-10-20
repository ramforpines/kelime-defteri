-- Yönetici için sohbet mesajı karakter sınırı yok (diğer kullanıcılar için 500 karakter aynı kalır).
-- supabase-chat.sql çalıştırılmış olmalı (is_admin için supabase-admin.sql). SQL Editor'da bir kez çalıştırın.
do $$
declare c record;
begin
  for c in select conname from pg_constraint
           where conrelid = 'public.chat_messages'::regclass and contype = 'c'
             and pg_get_constraintdef(oid) ilike '%char_length%'
  loop
    execute format('alter table public.chat_messages drop constraint %I', c.conname);
  end loop;
end $$;

create or replace function public.chat_body_check() returns trigger
language plpgsql security definer set search_path = public as $$
begin
  if char_length(btrim(new.body)) < 1 then raise exception 'empty message'; end if;
  if char_length(btrim(new.body)) > 500 and not public.is_admin() then raise exception 'message too long'; end if;
  return new;
end $$;
drop trigger if exists chat_body_check_trg on public.chat_messages;
create trigger chat_body_check_trg before insert or update of body on public.chat_messages
  for each row execute function public.chat_body_check();
