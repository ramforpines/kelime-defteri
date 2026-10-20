# Günlük yedek

`.github/workflows/backup.yml` her gün 04:17'de (TR) çalışır: veritabanını (`public` + `auth`) ve kodun tüm git geçmişini
paketler, **AES-256 ile şifreler** ve Actions > ilgili çalışma > Artifacts altında 30 gün saklar.
Depo herkese açık olduğu için yedek asla şifresiz yüklenmez ve depoya commit edilmez.

## Kurulum (bir kez)
1. Supabase > Project Settings > Database > **Connection string** > *Session pooler* (IPv4, port 5432) bağlantısını kopyala,
   `[YOUR-PASSWORD]` yerine veritabanı şifreni yaz.
   (Doğrudan `db.xxx.supabase.co` bağlantısı IPv6'dır, GitHub çalıştırıcıları ulaşamaz.)
2. GitHub > Settings > Secrets and variables > Actions > New repository secret:
   - `SUPABASE_DB_URL` = yukarıdaki bağlantı
   - `BACKUP_PASSPHRASE` = uzun, rastgele bir parola (bir yere de kendin kaydet; kaybolursa yedek açılmaz)
3. Actions sekmesi > "Günlük yedek" > **Run workflow** ile bir kez elle çalıştırıp yeşil olduğunu gör.

## Geri yükleme
```
gpg -d yedek-YYYY-MM-DD.tar.gz.gpg > yedek.tar.gz && tar xzf yedek.tar.gz
pg_restore --no-owner --no-privileges -d "<HEDEF_DB_URL>" db-YYYY-MM-DD.dump
git clone kod-YYYY-MM-DD.bundle kelime-defteri-geri
```
