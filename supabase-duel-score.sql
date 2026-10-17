-- Dosya: supabase-duel-score.sql
-- Kelime Defteri: düello puanı = 100 x seviye çarpanı (1,00-1,85) x hız çarpanı (ilk 6 sn'de 1,85'ten 1,00'a). Yanlış cevap 0.
-- Supabase SQL Editor'da bir kez çalıştır. Eski uygulama sürümü seviye göndermez, çarpan 1,00 sayılır.
drop function if exists public.duel_report(uuid, int, boolean, int);
create or replace function public.duel_report(did uuid, idx int, ok boolean, ms int, lv numeric default 1) returns void
language plpgsql security definer set search_path = public as $$
declare uid uuid := auth.uid(); d public.duels; mine int; pts int; m int; l numeric;
begin
  select * into d from public.duels where id = did for update;
  if not found or d.status <> 'active' or uid not in (d.p1, d.p2) then raise exception 'not allowed'; end if;
  if now() < d.start_at - interval '1 second' then raise exception 'early'; end if;
  mine := case when uid = d.p1 then d.a1 else d.a2 end;
  if idx <> mine or idx >= d.qn then return; end if;
  m := least(greatest(coalesce(ms, 0), 300), d.per_q * 1000);
  l := least(greatest(coalesce(lv, 1), 1), 1.85);
  pts := case when ok then round(100 * l * (1 + 0.85 * (1 - least(m, 6000)::numeric / 6000)))::int else 0 end;
  if uid = d.p1 then
    update public.duels set a1 = a1 + 1, s1 = s1 + pts, c1 = c1 + (case when ok then 1 else 0 end), t1 = t1 + m where id = did;
  else
    update public.duels set a2 = a2 + 1, s2 = s2 + pts, c2 = c2 + (case when ok then 1 else 0 end), t2 = t2 + m where id = did;
  end if;
  perform public.duel_settle(did);
end $$;
revoke all on function public.duel_report(uuid, int, boolean, int, numeric) from public, anon;
grant execute on function public.duel_report(uuid, int, boolean, int, numeric) to authenticated;
