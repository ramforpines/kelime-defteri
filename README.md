# Kelime Defteri

Cihaza kurulabilen (PWA) İngilizce çalışma uygulaması: sözlük, Odak modu, test, tekrar, gramer, kalıplar, sınav, düello, sıralama ve sohbet.

- Yayın: https://ramforpines.github.io/kelime-defteri/
- Beta (yönetici): https://ramforpines.github.io/kelime-defteri/beta/

## Dallar
- `next`: geliştirme. Her değişiklik önce buraya gider, `./beta-sync.sh` ile `beta/` klasörüne kopyalanır.
- `main`: yayın. GitHub Pages bu daldan sunulur; `next` test edildikten sonra `main` ile birleştirilir.

## Dosyalar
- `index.html`: uygulamanın tamamı (tek dosya)
- `words.js`: sözlük (kelime, deyim, phrasal verb); `tools/vocab/add.py` ile eklenir
- `examples.js`, `extr.js`, `senses.js`, `gloss.js`: örnek cümleler, çevirileri, ek anlamlar, yardımcı kelimeler
- `grammar.js`: gramer konuları (`tools/grammar/build.py` üretir)
- `phrases.js`: kalıp grupları (`tools/phrases/build.py` üretir)
- `core.js`, `freq.js`: Odak listesi ve sıklık; `afx.js`, `fam.js`, `pat.js`, `conf.js`, `lab.js`: kart ekleri (ek örnekleri, kelime ailesi, kalıplar, karıştırılanlar, etiketler)
- `sinav.js`: A2–C1 sınavları ve çalışma bölümleri; `exam.js`, `mock.js`: ünite soruları ve örnek vize
- `d/`: yukarıdaki veri dosyalarının içerik adresli parçaları (`tools/release/assets.py` üretir; elle düzenlenmez)
- `audio/`, `img/`: sınav ses kayıtları ve görseller
- `supabase.js`: Supabase istemcisi (yerel kopya)
- `sw.js`, `manifest.webmanifest`, `icon-*.png`: PWA dosyaları
- `supabase-*.sql`, `supabase/`: veritabanı tabloları, kuralları ve sunucu işlevleri
- `tools/`: içerik üretim ve yayın betikleri
- `BACKUP.md`: günlük şifreli yedek ve geri yükleme

## Kurulum (bir kez)
1. Supabase > SQL Editor'da `supabase-setup.sql` dosyasını, ardından gereken diğer `supabase-*.sql` dosyalarını çalıştır.
2. Supabase > Authentication > Sign In / Providers > Email: **Confirm email** seçeneğini kapat.
3. GitHub > Settings > Pages: Source "Deploy from a branch", branch `main`, klasör `/ (root)`.

## Güncelleme
1. Değişikliği `next` dalında yap, veri değiştiyse `python3 tools/release/assets.py` çalıştır.
2. Commit + `git push origin HEAD:next`, sonra `./beta-sync.sh` (beta güncellenir).
3. Test edildikten sonra `next`, `main` ile birleştirilir; kullanıcılar bir sonraki açılışta yalnızca değişen parçaları indirir.
