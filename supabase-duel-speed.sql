-- Dosya: supabase-duel-speed.sql
-- Kelime Defteri: düello hız çarpanı okuma süresi 3 sn -> 2 sn (ilk 2 sn 1,50; 6 sn'ye kadar 1,00'a düşer).
-- Yalnızca duel_report fonksiyonunu yeniler. supabase-duel-final.sql daha önce çalıştırılmış olmalı. SQL Editor'da bir kez çalıştır.

-- 2) Cevap bildirimi
drop function if exists public.duel_report(uuid, int, boolean, int);
drop function if exists public.duel_report(uuid, int, boolean, int, numeric);
create or replace function public.duel_report(did uuid, idx int, ok boolean, ms int, lv numeric default 1, "to" boolean default false) returns void
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
  pts := case when ok then round(100 * l * (1 + 0.5 * (1 - (least(greatest(m, 2000), 6000) - 2000)::numeric / 4000)))::int
              else -round(75 * l * (case when coalesce("to", false) then 0.5 else 1 end))::int end;
  if uid = d.p1 then
    update public.duels set a1 = a1 + 1, s1 = s1 + pts, c1 = c1 + (case when ok then 1 else 0 end), t1 = t1 + m where id = did;
  else
    update public.duels set a2 = a2 + 1, s2 = s2 + pts, c2 = c2 + (case when ok then 1 else 0 end), t2 = t2 + m where id = did;
  end if;
  perform public.duel_settle(did);
end $$;
revoke all on function public.duel_report(uuid, int, boolean, int, numeric, boolean) from public, anon;
grant execute on function public.duel_report(uuid, int, boolean, int, numeric, boolean) to authenticated;

