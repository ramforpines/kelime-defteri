-- Kelime Defteri: TÜM KULLANICILAR İÇİN İLERLEMEYİ SIFIRLA. GERİ ALINAMAZ.
-- Silinenler: öğrenilen kelimeler, tekrar/yanlış listeleri, puanlar ve ligler, rozetler, seriler, istatistikler,
--             liderlik tablosu satırları, tüm düello kayıtları, eşleşme kuyruğu ve tüm sohbet mesajları (genel + özel).
-- Korunanlar: hesaplar, kullanıcı adları, görünen ad/avatar/çerçeve, yönetici yetkileri, duyuru. Tablolar, fonksiyonlar, güvenlik kuralları ve diğer tüm yapı olduğu gibi kalır (hiçbir tablo silinmez, yalnızca içindeki veri).
-- Kullanıcıların uygulaması açıldığında (açıksa en geç ~1 dakika içinde) yerel verisini de otomatik sıfırlar.
-- SQL Editor'a yapıştırıp Run'a basınca HEMEN çalışır.
begin;
delete from public.chat_messages;
delete from public.duel_queue;
delete from public.duels;
delete from public.scores;
delete from public.user_state;
update public.profiles set reset_at = now();
commit;
