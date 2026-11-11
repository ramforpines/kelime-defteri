-- Dosya: supabase-duel-pencere2.sql
-- Kelime Defteri: dereceli düello hafta içi gündüz pencereleri eklendi.
-- Hafta içi: 13.00-19.00 arası her saat başı ilk 15 dk (13:00-13:15 ... 19:00-19:15) + 20.30-21.30 ve 22.25-23.55 (eskisi gibi)
-- Hafta sonu: değişmedi (14.00'ten itibaren her saat başı ilk 15 dk, 22:00-22:15'e kadar, ve 23.00-23.55)
-- SQL Editor'da bir kez çalıştır. Yalnızca pencere kuralını değiştirir; diğer düello fonksiyonları bunu kullanır.

create or replace function public.rk_window_open(t timestamptz default now()) returns boolean
language sql immutable set search_path = public as $$
  select case
    when extract(isodow from (t at time zone 'Europe/Istanbul')) in (6, 7) then
      ((t at time zone 'Europe/Istanbul')::time >= time '23:00' and (t at time zone 'Europe/Istanbul')::time < time '23:55')
      or (extract(hour from (t at time zone 'Europe/Istanbul')) between 14 and 22 and extract(minute from (t at time zone 'Europe/Istanbul')) < 15)
    else
      (extract(hour from (t at time zone 'Europe/Istanbul')) between 13 and 19 and extract(minute from (t at time zone 'Europe/Istanbul')) < 15)
      or ((t at time zone 'Europe/Istanbul')::time >= time '20:30' and (t at time zone 'Europe/Istanbul')::time < time '21:30')
      or ((t at time zone 'Europe/Istanbul')::time >= time '22:25' and (t at time zone 'Europe/Istanbul')::time < time '23:55')
  end
$$;
