-- Düello: 30 saniye tepki yoksa maç biter (4.152.5)
-- Sorun: rakibin bağlantısı koptuğunda maç ancak toplam süre (20 soru x 15 sn + 15 sn) dolunca bitiyordu;
-- maça kimse bakmıyorsa hiç kapanmıyor, maç geçmişine düşmüyor ve puan aktarılmıyordu.
-- Çözüm:
--   * Her cevapta oyuncunun son tepki zamanı (act1 / act2) kaydedilir.
--   * Bitirmemiş bir oyuncudan 30 saniye boyunca hiç cevap gelmezse maç "süresi doldu" gibi kapatılır:
--     kalan soruları süre dolmuş (cevapsız) sayılır, puan ve kazanan her zamanki kurallarla hesaplanır.
--   * duel_sweep(): askıda kalmış maçları kapatır; uygulama maç geçmişini açarken çağırır.
-- Not: Online bir oyuncu her soruda en geç 15 sn içinde (süre dolunca otomatik) cevap gönderir; 30 sn sessizlik = kopma.

alter table public.duels add column if not exists act1 timestamptz;
alter table public.duels add column if not exists act2 timestamptz;
-- şu an süren maçlar yanlışlıkla kapanmasın: sayaçlarını şimdiden başlat
update public.duels set act1 = coalesce(act1, now()), act2 = coalesce(act2, now()) where status = 'active';

create or replace function public.duel_afk(d public.duels) returns boolean
language sql stable set search_path = public as $$
  select d.status = 'active' and now() > d.start_at + interval '30 seconds' and (
         (d.a1 < d.qn and now() - greatest(coalesce(d.act1, d.start_at), d.start_at) > interval '30 seconds')
      or (d.a2 < d.qn and now() - greatest(coalesce(d.act2, d.start_at), d.start_at) > interval '30 seconds'))
$$;

create or replace function public.duel_settle(did uuid) returns void
language plpgsql security definer set search_path = public as $$
declare d public.duels; w uuid; tot int; pw numeric(6,1); sw int; p1v numeric(6,1); p2v numeric(6,1); expired boolean; both_done boolean;
        v_c1 numeric; v_c2 numeric; v_share numeric; v_lk numeric; v_wk numeric; v_t numeric; v_tx numeric; v_rate numeric;
begin
  select * into d from public.duels where id = did for update;
  if not found or d.status <> 'active' then return; end if;
  both_done := d.a1 >= d.qn and d.a2 >= d.qn;
  expired := now() > d.start_at + make_interval(secs => d.qn * d.per_q + 15) or public.duel_afk(d);
  if not (both_done or expired) then return; end if;
  if expired and not both_done then
    update public.duels set
      s1 = s1 - (case when mode = 'ranked' then 200 else 100 end) * greatest(qn - a1, 0), s2 = s2 - (case when mode = 'ranked' then 200 else 100 end) * greatest(qn - a2, 0),
      a1 = greatest(a1, qn), a2 = greatest(a2, qn)
    where id = did;
    select * into d from public.duels where id = did;
  end if;

  if d.mode = 'ranked' then
    w := case when d.s1 > d.s2 then d.p1 when d.s2 > d.s1 then d.p2 else null end;
    -- iki tarafın da puanı (negatifler 0 sayılır) 0 ise kimse bir şey kazanmadı: berabere, puan değişmez
    if greatest(d.s1, 0) + greatest(d.s2, 0) = 0 then w := null; end if;
    if w is null then
      update public.duels set status = 'done', done_at = now(), winner = null, dl1 = 0, dl2 = 0 where id = did;
      return;
    end if;
    v_c1 := greatest(d.s1, 0); v_c2 := greatest(d.s2, 0);
    v_share := case when v_c1 + v_c2 = 0 then 0.5 else (case when w = d.p1 then v_c1 else v_c2 end) / (v_c1 + v_c2) end;
    v_lk := coalesce(case when w = d.p1 then d.rk2 else d.rk1 end, 0);
    v_wk := coalesce(case when w = d.p1 then d.rk1 else d.rk2 end, 0);
    v_t := round(least(v_lk * v_share, 3 * v_wk), 1);
    v_rate := public.duel_rate(coalesce(case when w = d.p1 then d.rp2 else d.rp1 end, 200));
    v_tx := case when v_t <= 0 then 0 else round(v_t * v_rate, 1) end;
    update public.duels set status = 'done', done_at = now(), winner = w,
      dl1 = case when w = p1 then v_t + v_tx else -v_t end,
      dl2 = case when w = p2 then v_t + v_tx else -v_t end
    where id = did;
    return;
  end if;

  if expired and not both_done then
    w := case when d.s1 > d.s2 then d.p1 when d.s2 > d.s1 then d.p2 else null end;
  else
    w := case when d.s1 > d.s2 then d.p1 when d.s2 > d.s1 then d.p2
              when d.t1 < d.t2 then d.p1 when d.t2 < d.t1 then d.p2
              else null end;
  end if;
  tot := greatest(d.s1, 0) + greatest(d.s2, 0);
  if w is null then
    p1v := 22.5; p2v := 22.5;
  else
    sw := greatest(case when w = d.p1 then d.s1 else d.s2 end, 0);
    pw := round(25 + case when tot = 0 then 10 else 20.0 * sw / tot end, 1);
    if w = d.p1 then p1v := pw; p2v := 45 - pw; else p2v := pw; p1v := 45 - pw; end if;
  end if;
  update public.duels set status = 'done', done_at = now(), winner = w, pay1 = p1v, pay2 = p2v where id = did;
end $$;
revoke all on function public.duel_settle(uuid) from public, anon, authenticated;

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
    if not ok and coalesce("to", false) then m := d.per_q * 1000; end if;
    if ok then
      pts := round(100 * l * public.duel_spd(m, d.per_q))::int;
    else
      pts := -round(round(100 * l * greatest(1, public.duel_spd(m, d.per_q)))::int * 0.66)::int;
    end if;
  else
    pts := case when ok then round(100 * l * public.duel_spd(m, d.per_q))::int
                else -round(75 * l * (case when coalesce("to", false) then 0.5 else 1 end))::int end;
  end if;
  zq := case when uid = d.p1 then d.zq1 else d.zq2 end;
  if ok and zq is not null and zq = idx then pts := 0; end if;
  if uid = d.p1 then
    update public.duels set a1 = a1 + 1, s1 = s1 + pts, c1 = c1 + (case when ok then 1 else 0 end), t1 = t1 + m, act1 = now() where id = did;
  else
    update public.duels set a2 = a2 + 1, s2 = s2 + pts, c2 = c2 + (case when ok then 1 else 0 end), t2 = t2 + m, act2 = now() where id = did;
  end if;
  perform public.duel_settle(did);
end $$;
revoke all on function public.duel_report(uuid, int, boolean, int, numeric, boolean) from public, anon;
grant execute on function public.duel_report(uuid, int, boolean, int, numeric, boolean) to authenticated;

-- askıda kalmış maçları kapatır (süresi dolmuş ya da 30 sn tepkisiz)
create or replace function public.duel_sweep() returns int
language plpgsql security definer set search_path = public as $$
declare n int := 0; r record;
begin
  if auth.uid() is null then return 0; end if;
  for r in select id from public.duels d
           where d.status = 'active' and (now() > d.start_at + make_interval(secs => d.qn * d.per_q + 15) or public.duel_afk(d))
           order by d.start_at limit 30 for update skip locked loop
    perform public.duel_settle(r.id); n := n + 1;
  end loop;
  return n;
end $$;
revoke all on function public.duel_sweep() from public, anon;
grant execute on function public.duel_sweep() to authenticated;

-- süresi çoktan dolmuş, askıda kalmış maçları hemen kapat (puanları ve geçmişleri işlenir)
select public.duel_settle(id) from public.duels d
 where d.status = 'active' and now() > d.start_at + make_interval(secs => d.qn * d.per_q + 15);
