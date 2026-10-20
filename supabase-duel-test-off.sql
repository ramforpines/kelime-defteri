-- Dosya: supabase-duel-test-off.sql
-- Test kısıtlamasını kaldırır: herkes herkesle oynar, maçlar normal kaydedilir.
-- (duel_is_test her zaman false döner; supabase-duel-test.sql'deki fonksiyonlar bu sayede eski davranışa döner.)
create or replace function public.duel_is_test(u uuid) returns boolean
language sql stable security definer set search_path = public as $$ select false $$;
revoke all on function public.duel_is_test(uuid) from public, anon, authenticated;
