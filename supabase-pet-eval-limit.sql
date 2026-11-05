-- PET yapay zekâ değerlendirmesi günlük sınırı: kullanıcı 1, yönetici 3 (Türkiye saatine göre gün)
create or replace function public.pet_eval_left() returns int
language plpgsql security definer stable set search_path = public as $$
declare uid uuid := auth.uid(); lim int; used int;
begin
  if uid is null then return 0; end if;
  lim := case when exists(select 1 from public.admins where user_id = uid) then 3 else 1 end;
  select count(*) into used from public.pet_evals
   where user_id = uid and created_at >= (date_trunc('day', now() at time zone 'Europe/Istanbul') at time zone 'Europe/Istanbul');
  return greatest(lim - used, 0);
end $$;
