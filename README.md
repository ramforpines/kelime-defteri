# Kelime Defteri

Sözlük, test, tekrar listesi ve liderlik tablosu olan, cihaza kurulabilen kelime çalışma uygulaması.

- `index.html`: uygulama
- `words.js`: kelime listesi (Google E-Tablo'dan aktarılır)
- `supabase.js`: Supabase istemcisi (yerel kopya)
- `sw.js`, `manifest.webmanifest`, `icon-*.png`: kurulabilir uygulama (PWA) dosyaları
- `supabase-setup.sql`: Supabase'de bir kez çalıştırılacak tablo ve güvenlik kuralları

## Kurulum
1. Supabase > SQL Editor'da `supabase-setup.sql` dosyasını çalıştır.
2. Supabase > Authentication > Sign In / Providers > Email: **Confirm email** seçeneğini kapat.
3. GitHub > Settings > Pages: Source "Deploy from a branch", branch `main`, klasör `/ (root)`.

Güncelleme: dosyalar bu depoya yüklendiğinde kullanıcılar bir sonraki açılışta yeni sürümü alır.
