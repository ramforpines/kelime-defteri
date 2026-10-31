-- Toplam puan tutarlılık kontrolü. Salt okunur. Her sorguyu ayrı ayrı çalıştırın.

-- 1) Aynı düello kalemi birden fazla güne yazılmış mı? (çift sayım şüphesi)
select p.username, split_part(e.key,'|',2) as mac, split_part(e.key,'|',1) as tur,
       count(distinct d.key) as gun_sayisi, string_agg(distinct d.key, ', ') as gunler, sum((e.value->>'pts')::numeric) as toplam_pts
from public.user_state u
join public.profiles p on p.user_id = u.user_id
cross join lateral jsonb_each(coalesce(u.state->'days','{}'::jsonb)) d(key, val)
cross join lateral jsonb_each(coalesce(d.val->'ev','{}'::jsonb)) e
where split_part(e.key,'|',1) in ('dr','dp','ds') and e.value->>'t' <> 'n'
group by p.username, e.key
having count(distinct d.key) > 1
order by p.username;

-- 2) Toplam puan ile gün kayıtlarının toplamı arasındaki fark (büyük sapmalar şüpheli)
--    toplam = state.tp ; gunler = tüm günlerin p+adj toplamı ; n_kesinti = gün olaylarındaki 'n' tipi (yalnız toplamı etkileyen) kalemler
select p.username,
       round((u.state->>'tp')::numeric,1) as toplam,
       round(coalesce(sum(coalesce((d.val->>'p')::numeric,0)+coalesce((d.val->>'adj')::numeric,0)),0),1) as gunler_toplami,
       round(coalesce(sum((select coalesce(sum((x.value->>'pts')::numeric),0) from jsonb_each(coalesce(d.val->'ev','{}'::jsonb)) x where x.value->>'t'='n')),0),1) as n_kalemler,
       round((u.state->>'tp')::numeric - coalesce(sum(coalesce((d.val->>'p')::numeric,0)+coalesce((d.val->>'adj')::numeric,0)),0),1) as fark,
       count(d.key) as gun_sayisi
from public.user_state u
join public.profiles p on p.user_id = u.user_id
left join lateral jsonb_each(coalesce(u.state->'days','{}'::jsonb)) d(key, val) on true
group by p.username, u.state
order by abs((u.state->>'tp')::numeric - coalesce(sum(coalesce((d.val->>'p')::numeric,0)+coalesce((d.val->>'adj')::numeric,0)),0)) desc
limit 40;

-- 3) Aykırı değerler: negatif / aşırı büyük toplam
select p.username, (u.state->>'tp')::numeric as toplam
from public.user_state u join public.profiles p on p.user_id = u.user_id
where (u.state->>'tp') is null or (u.state->>'tp')::numeric < 0 or (u.state->>'tp')::numeric > 200000
order by 2 desc nulls first;
