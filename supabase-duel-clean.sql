-- Hatalı dereceli maçlarda (iki tarafın da skoru 0 ya da altı) kalan puan geçişini sıfırla.
-- ÖNEMLİ: Önce etkilenen kullanıcılar uygulamayı açıp iadelerini almalı (uygulama iadeyi dl1/dl2 değerinden hesaplar).
-- Sonra Supabase SQL Editor'da bir kez çalıştırın.
update public.duels set winner = null, dl1 = 0, dl2 = 0
where mode = 'ranked' and status = 'done' and s1 <= 0 and s2 <= 0 and (winner is not null or coalesce(dl1,0) <> 0 or coalesce(dl2,0) <> 0);
