-- Dosya: supabase-scoring.sql
-- Kelime Defteri: yeni puanlama sistemi için herkesin puanını sıfırla. SQL Editor'da bir kez çalıştır.
-- (Uygulamanın 2.0.0 sürümü yayında olduktan sonra çalıştırman en iyisi.)
update public.scores set dp = 0, wp = 0, ap = 0;
