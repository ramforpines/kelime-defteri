-- Klasik düello havuzu: iki oyuncu 20+20 = 40 koyar, sistem 5 ekler (45 puan dağıtılır).
-- Kazanan 25 + maç skoruna göre paylaşılan 20 puanın payını alır; beraberlikte 22,5 / 22,5.
-- Dereceli kuralları (beraberlik dahil) aynı fonksiyonda korunur. Bir kez çalıştırın.

create or replace function public.duel_settle(did uuid) returns void
language plpgsql security definer set search_path = public as $$
declare d public.duels; w uuid; tot int; pw numeric(6,1); sw int; p1v numeric(6,1); p2v numeric(6,1); expired boolean; both_done boolean;
        v_c1 numeric; v_c2 numeric; v_share numeric; v_lk numeric; v_wk numeric; v_t numeric; v_tx numeric;
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
    v_t := round(least(v_lk * v_share, 4 * v_wk), 1);
    v_tx := least(v_t, greatest(1, round(0.05 * v_t, 1)));
    if v_t <= 0 then v_tx := 0; end if;
    update public.duels set status = 'done', done_at = now(), winner = w,
      dl1 = case when w = p1 then v_t - v_tx else -v_t end,
      dl2 = case when w = p2 then v_t - v_tx else -v_t end
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
