-- Dosya: supabase-duel-speed4.sql
-- Kelime Defteri: düello hız çarpanı üstel eğri (klasik ve dereceli ortak). Yalnızca duel_spd fonksiyonunu değiştirir;
-- duel_report (supabase-duel-speed2.sql) bunu zaten kullanır. speed3'ün yerine geçer; Supabase SQL Editor'da bir kez çalıştırın.
--   0–1,5 sn: x1,50 | sonrası: x1,50 * e^(-0,24 * (sn - 1,5)), en az x0,10
--   Ayar hedefi: 20 soruda 15 doğru @4 sn maç skoru ≈ 16 doğru @4,5 sn maç skoru
create or replace function public.duel_spd(m int, per int) returns numeric language sql immutable as $$
  select case
    when m <= 1500 then 1.5
    else greatest(0.10, 1.5 * exp(-0.24 * (least(m, per * 1000) - 1500)::numeric / 1000)) end
$$;
revoke all on function public.duel_spd(int, int) from public, anon, authenticated;
