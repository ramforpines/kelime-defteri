-- Dosya: supabase-duel-speed2.sql
-- Kelime Defteri: düello hız çarpanı yeni eğri (klasik ve dereceli ortak)
--   0–2 sn: x1,50 | 2–6 sn: x1,50 -> x1,00 (doğrusal) | 6–7 sn: x1,00 | 7 sn -> süre sonu (15 sn): x1,00 -> x0,50 (doğrusal)
--   Dereceli yanlış cevap cezası = doğru puanının %66'sı, ama ceza tabanında hız çarpanı en az 1,00 alınır
--   (yavaş yanlış ya da süre dolması ucuzlamaz). Klasikte yanlış cezası aynı kalır (-75 x seviye, süre dolması yarısı).
-- supabase-duel-ceza.sql'deki duel_report fonksiyonunun yerine geçer. Supabase SQL Editor'da bir kez çalıştırın.

create or replace function public.duel_spd(m int, per int) returns numeric language sql immutable as $$
  select case
    when m <= 2000 then 1.5
    when m <= 6000 then 1.5 - 0.5 * (m - 2000)::numeric / 4000
    when m <= 7000 then 1.0
    else greatest(0.5, 1 - 0.5 * (least(m, per * 1000) - 7000)::numeric / greatest(per * 1000 - 7000, 1)) end
$$;
revoke all on function public.duel_spd(int, int) from public, anon, authenticated;

drop function if exists public.duel_report(uuid, int, boolean, int);
drop function if exists public.duel_report(uuid, int, boolean, int, numeric);
create or replace function public.duel_report(did uuid, idx int, ok boolean, ms int, lv numeric default 1, "to" boolean default false) returns void
language plpgsql security definer set search_path = public as $$
declare uid uuid := auth.uid(); d public.duels; mine int; pts int; m int; l numeric; zq int;
begin
  select * into d from public.duels where id = did for update;
  if not found or d.status <> 'active' or uid not in (d.p1, d.p2) then raise exception 'not allowed'; end if;
  if now() < d.start_at - interval '1 second' then raise exception 'early'; end if;
  mine := case when uid = d.p1 then d.a1 else d.a2 end;
  if idx <> mine or idx >= d.qn then return; end if;
  m := least(greatest(coalesce(ms, 0), 300), d.per_q * 1000);
  l := least(greatest(coalesce(lv, 1), 1), 1.85);
  if d.mode = 'ranked' then
    -- dereceli: doğru = 100 x seviye x hız çarpanı; yanlış = (100 x seviye x max(1, hız çarpanı)) puanının %66'sı kadar eksi
    if not ok and coalesce("to", false) then m := d.per_q * 1000; end if;
    if ok then
      pts := round(100 * l * public.duel_spd(m, d.per_q))::int;
    else
      pts := -round(round(100 * l * greatest(1, public.duel_spd(m, d.per_q)))::int * 0.66)::int;
    end if;
  else
    -- klasik: doğru hız çarpanlı, yanlış -75 x seviye, süre dolması yarısı
    pts := case when ok then round(100 * l * public.duel_spd(m, d.per_q))::int
                else -round(75 * l * (case when coalesce("to", false) then 0.5 else 1 end))::int end;
  end if;
  zq := case when uid = d.p1 then d.zq1 else d.zq2 end;
  if ok and zq is not null and zq = idx then pts := 0; end if;
  if uid = d.p1 then
    update public.duels set a1 = a1 + 1, s1 = s1 + pts, c1 = c1 + (case when ok then 1 else 0 end), t1 = t1 + m where id = did;
  else
    update public.duels set a2 = a2 + 1, s2 = s2 + pts, c2 = c2 + (case when ok then 1 else 0 end), t2 = t2 + m where id = did;
  end if;
  perform public.duel_settle(did);
end $$;
revoke all on function public.duel_report(uuid, int, boolean, int, numeric, boolean) from public, anon;
grant execute on function public.duel_report(uuid, int, boolean, int, numeric, boolean) to authenticated;
