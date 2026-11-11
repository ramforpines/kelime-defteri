-- Dosya: supabase-wp-neg.sql
-- Kelime Defteri: haftalık puan da eksiye inebilsin (haftayı dereceli düello kaybıyla eksi kapatan kullanıcı sıralamada eksi puanla görünsün).
-- SQL Editor'da bir kez çalıştır. Yalnızca haftalık puan sınırını değiştirir; toplam puan (ap) eskisi gibi 0'ın altına inmez.
-- Çalıştırmazsan uygulama eksi haftalık puanı sunucuya 0 olarak yazar, bir şey bozulmaz.

alter table public.scores drop constraint if exists scores_wp_check;
alter table public.scores add constraint scores_wp_check check (wp between -42000 and 42000);
