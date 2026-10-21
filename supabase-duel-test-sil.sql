-- Dosya: supabase-duel-test-sil.sql
-- Yönetici ve test hesabının TEST MAÇ KAYITLARINI siler (geri alınamaz!). supabase-duel-ceza.sql çalıştırıldıktan sonra, YEDEK aldıktan sonra çalıştır.
--  * 'test' durumundaki maçlar ve test grubunda iptal olan (pen_t) maçlar silinir; bunlara bağlı ayrılma kayıtları ve ceza kayıtları da silinir (cascade).
--  * Yönetici ve test hesabının test sırasında aldığı dereceli ceza (süre) ve bildirimleri temizlenir.
-- Gerçek maçlar ve gerçek puanlar etkilenmez.
begin;
delete from public.duels where status = 'test' or (status = 'void' and coalesce(pen_t, false));
delete from public.duel_bans where user_id in (select a.user_id from public.admins a)
   or user_id in (select u.id from auth.users u where lower(split_part(u.email, '@', 1)) = 'kullanici52541');
delete from public.duel_notices where user_id in (select a.user_id from public.admins a)
   or user_id in (select u.id from auth.users u where lower(split_part(u.email, '@', 1)) = 'kullanici52541');
delete from public.duel_penalties where duel_id is null and by_user is null and kind = 'auto';
commit;
