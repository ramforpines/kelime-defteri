-- Düello 30 saniye kuralı, yalnızca bir taraf bitirdikten sonra (4.152.8)
-- Önceki: bitirmemiş oyuncudan 30 sn cevap gelmezse maç her durumda kapanıyordu.
-- Yeni: kural, taraflardan biri 20 sorunun hepsini cevapladıktan sonra başlar.
--   Sayaç = max(bitiren oyuncunun son cevabı, diğerinin son cevabı). Bu andan itibaren
--   bitirmemiş oyuncudan 30 sn cevap gelmezse maç kapanır, kalan soruları cevapsız sayılır.
-- İki taraf da bitirmeden koparsa maç her zamanki gibi toplam süre dolunca (20 x 15 sn + 15 sn) kapanır.
-- duel_settle ve duel_sweep bu fonksiyonu kullandığı için yalnızca bu fonksiyon değişir.

create or replace function public.duel_afk(d public.duels) returns boolean
language sql stable set search_path = public as $$
  select d.status = 'active' and (
         (d.a2 >= d.qn and d.a1 < d.qn
          and now() - greatest(coalesce(d.act1, d.start_at), coalesce(d.act2, d.start_at), d.start_at) > interval '30 seconds')
      or (d.a1 >= d.qn and d.a2 < d.qn
          and now() - greatest(coalesce(d.act1, d.start_at), coalesce(d.act2, d.start_at), d.start_at) > interval '30 seconds'))
$$;
