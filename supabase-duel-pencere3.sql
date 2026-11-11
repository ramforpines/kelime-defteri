-- Dosya: supabase-duel-pencere3.sql
-- Kelime Defteri: dereceli düelloya her gün 00.00-01.55 penceresi eklendi (00.00-00.09 bakım arasında uygulama zaten kapalı).
-- Hafta içi: 00.00-01.55, 13.00-19.00 arası her saat başı ilk 15 dk, 20.30-21.30, 22.25-23.55
-- Hafta sonu: 00.00-01.55, 14.00'ten itibaren her saat başı ilk 15 dk (22:00-22:15'e kadar), 23.00-23.55
-- SQL Editor'da bir kez çalıştır (supabase-duel-pencere2.sql'in yerine geçer; ikisini de çalıştırmak sorun değil).

create or replace function public.rk_window_open(t timestamptz default now()) returns boolean
language sql immutable set search_path = public as $$
  select ((t at time zone 'Europe/Istanbul')::time < time '01:55') or case
    when extract(isodow from (t at time zone 'Europe/Istanbul')) in (6, 7) then
      ((t at time zone 'Europe/Istanbul')::time >= time '23:00' and (t at time zone 'Europe/Istanbul')::time < time '23:55')
      or (extract(hour from (t at time zone 'Europe/Istanbul')) between 14 and 22 and extract(minute from (t at time zone 'Europe/Istanbul')) < 15)
    else
      (extract(hour from (t at time zone 'Europe/Istanbul')) between 13 and 19 and extract(minute from (t at time zone 'Europe/Istanbul')) < 15)
      or ((t at time zone 'Europe/Istanbul')::time >= time '20:30' and (t at time zone 'Europe/Istanbul')::time < time '21:30')
      or ((t at time zone 'Europe/Istanbul')::time >= time '22:25' and (t at time zone 'Europe/Istanbul')::time < time '23:55')
  end
$$;
