-- Dosya: supabase-duel-speed3.sql
-- Kelime Defteri: düello hız çarpanı daha dik (klasik ve dereceli ortak). Yalnızca duel_spd fonksiyonunu değiştirir;
-- duel_report (supabase-duel-speed2.sql) bunu zaten kullanır. Supabase SQL Editor'da bir kez çalıştırın.
--   0–1,5 sn: x1,50 | 1,5–6 sn: x1,50 -> x1,00 (doğrusal) | 6 sn -> süre sonu (15 sn): x1,00 -> x0,10 (doğrusal)
create or replace function public.duel_spd(m int, per int) returns numeric language sql immutable as $$
  select case
    when m <= 1500 then 1.5
    when m <= 6000 then 1.5 - 0.5 * (m - 1500)::numeric / 4500
    else greatest(0.10, 1 - 0.90 * (least(m, per * 1000) - 6000)::numeric / greatest(per * 1000 - 6000, 1)) end
$$;
revoke all on function public.duel_spd(int, int) from public, anon, authenticated;
