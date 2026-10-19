-- Dosya: supabase-duel-elg.sql
-- Kelime Defteri: dereceli galibiyet sayımında "2 lig farkı" kuralı artık GERÇEK (etkin) lige göre uygulanır:
--   gerçek lig = puan ligi ile galibiyet şartının düşüğü. Puanı yetse de şartı karşılamayan biri bir alt ligde sayılır.
-- Maç başında iki oyuncunun gerçek ligi maça kaydedilir (elg1, elg2). Eski maçlar kronolojik olarak yeniden hesaplanıp doldurulur.
-- Önce supabase-duel-ranked.sql çalıştırılmış olmalı. Supabase SQL Editor'da bir kez çalıştır.

alter table public.duels add column if not exists elg1 int;
alter table public.duels add column if not exists elg2 int;

-- Galibiyet sayımı: kazananın ve rakibin maç başındaki gerçek ligi (kayıt yoksa puan ligi) en çok 2 lig farklıysa sayılır.
create or replace function public.duel_wincount(u uuid) returns int language sql stable security definer set search_path = public as $$
  select count(*)::int from public.duels d
  where d.mode = 'ranked' and d.status = 'done' and d.winner = u
    and abs(coalesce(case when d.winner = d.p1 then d.elg1 else d.elg2 end, public.duel_lg(case when d.winner = d.p1 then d.rp1 else d.rp2 end))
          - coalesce(case when d.winner = d.p1 then d.elg2 else d.elg1 end, public.duel_lg(case when d.winner = d.p1 then d.rp2 else d.rp1 end))) <= 2
$$;
revoke all on function public.duel_wincount(uuid) from public, anon, authenticated;

create or replace function public.duel_wins() returns table(user_id uuid, w int)
language sql stable security definer set search_path = public as $$
  select d.winner, count(*)::int from public.duels d
  where auth.uid() is not null and d.mode = 'ranked' and d.status = 'done' and d.winner is not null
    and abs(coalesce(case when d.winner = d.p1 then d.elg1 else d.elg2 end, public.duel_lg(case when d.winner = d.p1 then d.rp1 else d.rp2 end))
          - coalesce(case when d.winner = d.p1 then d.elg2 else d.elg1 end, public.duel_lg(case when d.winner = d.p1 then d.rp2 else d.rp1 end))) <= 2
  group by d.winner
$$;
revoke all on function public.duel_wins() from public, anon;
grant execute on function public.duel_wins() to authenticated;

-- Maç oluştururken gerçek ligleri de kaydet
create or replace function public.duel_make(a uuid, b uuid, p_wn int, p_mode text) returns uuid
language plpgsql security definer set search_path = public as $$
declare did uuid; pa numeric; pb numeric;
begin
  pa := coalesce((select ap from public.scores where user_id = a), 0);
  pb := coalesce((select ap from public.scores where user_id = b), 0);
  insert into public.duels(p1, p2, seed, wn, start_at, mode, rp1, rp2, rk1, rk2, elg1, elg2)
    values (a, b, floor(random() * 2147480000)::int, p_wn, now() + interval '5 seconds', p_mode,
            case when p_mode = 'ranked' then pa end, case when p_mode = 'ranked' then pb end,
            case when p_mode = 'ranked' then public.duel_risk(pa) end, case when p_mode = 'ranked' then public.duel_risk(pb) end,
            case when p_mode = 'ranked' then public.duel_elg(a) end, case when p_mode = 'ranked' then public.duel_elg(b) end)
    returning id into did;
  return did;
end $$;
revoke all on function public.duel_make(uuid, uuid, int, text) from public, anon, authenticated;

-- Eski dereceli maçları kronolojik olarak yeniden hesapla: her maçta iki oyuncunun gerçek ligi =
-- min(maç başı puan ligi, o ana kadarki sayılan galibiyetin açtığı lig sınırı)
do $$
declare d record; w1 int; w2 int; e1 int; e2 int;
begin
  create temp table _wc(u uuid primary key, w int not null) on commit drop;
  for d in select id, p1, p2, rp1, rp2, winner, status from public.duels where mode = 'ranked' order by created_at, id loop
    w1 := coalesce((select w from _wc where u = d.p1), 0);
    w2 := coalesce((select w from _wc where u = d.p2), 0);
    e1 := least(public.duel_lg(coalesce(d.rp1, 0)), public.duel_wcap(w1));
    e2 := least(public.duel_lg(coalesce(d.rp2, 0)), public.duel_wcap(w2));
    update public.duels set elg1 = e1, elg2 = e2 where id = d.id;
    if d.status = 'done' and d.winner is not null and abs(e1 - e2) <= 2 then
      insert into _wc(u, w) values (d.winner, 1) on conflict (u) do update set w = _wc.w + 1;
    end if;
  end loop;
end $$;
