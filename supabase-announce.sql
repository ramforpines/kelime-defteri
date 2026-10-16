-- Dosya: supabase-announce.sql
-- Kelime Defteri: duyuru sınırını 500 kelimeye (4000 karakter) çıkarır. SQL Editor'da bir kez çalıştır.
create or replace function public.admin_set_announcement(msg text)
returns void language plpgsql security definer set search_path = public as $$
begin
  if not public.is_admin() then raise exception 'not allowed'; end if;
  update public.announcement set body = left(coalesce(msg, ''), 4000), updated_at = now() where id = 1;
end $$;
