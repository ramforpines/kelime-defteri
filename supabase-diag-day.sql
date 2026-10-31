-- Bir kullanıcının bugünkü günlük puan kalemlerini (olay kayıtları) gösterir. Salt okunur. Her sorguyu ayrı ayrı çalıştırın.

-- 1) Günün özeti: p = kazanılan puan, adj = kesinti/düzeltme toplamı, q = soru puanı
select p.username, u.state->'days'->'2026-10-31'->>'p' as p, u.state->'days'->'2026-10-31'->>'adj' as adj,
       u.state->'days'->'2026-10-31'->>'q' as q, u.state->>'tp' as toplam_puan
from public.profiles p join public.user_state u on u.user_id = p.user_id
where p.username ilike '%kaan.bozdogan%';

-- 2) Günün kalemleri: tur a = günlük puandan düşen/eklenen düzeltme, p = kazanç, n = yalnız toplam puandan düşen kesinti
select e.key as kalem, e.value->>'t' as tur, e.value->>'pts' as puan
from public.profiles p
join public.user_state u on u.user_id = p.user_id
cross join lateral jsonb_each(coalesce(u.state->'days'->'2026-10-31'->'ev', '{}'::jsonb)) e
where p.username ilike '%kaan.bozdogan%'
order by e.key;

-- 3) Son kesinti kayıtları (günlük hedef kesintisi: pen, zorunlu dereceli maç kesintisi: rpen)
select u.state->'pen' as hedef_kesintileri, u.state->'rpen' as dereceli_kesintileri
from public.profiles p join public.user_state u on u.user_id = p.user_id
where p.username ilike '%kaan.bozdogan%';
