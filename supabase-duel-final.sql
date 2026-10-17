-- Dosya: supabase-duel-final.sql
-- Kelime Defteri: düello puanlaması (tek dosya, başka düello SQL'i gerekmez; supabase-duel.sql/duel2/invite daha önce çalıştırılmış olmalı).
--  * Doğru: 100 x seviye (1,00-1,85) x hız (ilk 3 sn 1,50, 7 sn'ye kadar 1,00'a düşer)
--  * Yanlış: -75 x seviye; süre dolması (cevapsız): -37,5 x seviye
--  * Maç yarıda kalırsa cevaplanmayan her soru -100
--  * Ödemede negatif maç puanı 0 sayılır; kazanan ham puana göre belirlenir
--  * Herkese açık maç geçmişi (duel_history) dahildir
-- Supabase SQL Editor'da bir kez çalıştır.

-- 1) Maç puanı negatif olabilir, sütunlar zaten int; ek bir değişiklik gerekmez.

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
  pts := case when ok then round(100 * l * (1 + 0.5 * (1 - (least(greatest(m, 3000), 7000) - 3000)::numeric / 4000)))::int
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

-- 3) Maç sonu: yarıda kalan sorular -100, ödemede negatif puan 0
create or replace function public.duel_settle(did uuid) returns void
language plpgsql security definer set search_path = public as $$
declare d public.duels; w uuid; tot int; pw numeric(6,1); sw int; p1v numeric(6,1); p2v numeric(6,1); expired boolean; both_done boolean;
begin
  select * into d from public.duels where id = did for update;
  if not found or d.status <> 'active' then return; end if;
  both_done := d.a1 >= d.qn and d.a2 >= d.qn;
  expired := now() > d.start_at + make_interval(secs => d.qn * d.per_q + 15);
  if not (both_done or expired) then return; end if;
  if expired and not both_done then
    update public.duels set
      s1 = s1 - 100 * greatest(qn - a1, 0), s2 = s2 - 100 * greatest(qn - a2, 0),
      a1 = greatest(a1, qn), a2 = greatest(a2, qn)
    where id = did;
    select * into d from public.duels where id = did;
    w := case when d.s1 > d.s2 then d.p1 when d.s2 > d.s1 then d.p2 else null end;
  else
    w := case when d.s1 > d.s2 then d.p1 when d.s2 > d.s1 then d.p2
              when d.t1 < d.t2 then d.p1 when d.t2 < d.t1 then d.p2
              else null end;
  end if;
  tot := greatest(d.s1, 0) + greatest(d.s2, 0);
  -- Her oyuncu 20 puan koyar (havuz 40), 5 puan kesilir, kalan 35'in 25'i kazananın, 10'u (negatif puan 0 sayılarak) maç puanına göre paylaşılır.
  if w is null then
    p1v := 17.5; p2v := 17.5;
  else
    sw := greatest(case when w = d.p1 then d.s1 else d.s2 end, 0);
    pw := round(25 + case when tot = 0 then 5 else 10.0 * sw / tot end, 1);
    if w = d.p1 then p1v := pw; p2v := 35 - pw; else p2v := pw; p1v := 35 - pw; end if;
  end if;
  update public.duels set status = 'done', done_at = now(), winner = w, pay1 = p1v, pay2 = p2v where id = did;
end $$;
revoke all on function public.duel_settle(uuid) from public, anon, authenticated;

-- 4) Herkese açık maç geçmişi
drop function if exists public.duel_history(int);
create or replace function public.duel_history(n int default 50) returns table(id uuid, p1 uuid, p2 uuid, s1 numeric, s2 numeric, c1 int, c2 int, a1 int, a2 int, t1 numeric, t2 numeric, winner uuid, created_at timestamptz)
language sql stable security definer set search_path = public as $$
  select d.id, d.p1, d.p2, d.s1::numeric, d.s2::numeric, d.c1::int, d.c2::int, d.a1::int, d.a2::int, d.t1::numeric, d.t2::numeric, d.winner, d.created_at
  from public.duels d
  where d.status = 'done' and auth.uid() is not null
  order by d.created_at desc
  limit least(greatest(coalesce(n, 50), 1), 100);
$$;
revoke all on function public.duel_history(int) from public, anon;
grant execute on function public.duel_history(int) to authenticated;
