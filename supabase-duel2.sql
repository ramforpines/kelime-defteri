-- Dosya: supabase-duel2.sql
-- Kelime Defteri: düelloya puan bahsi (20+20, 5 kesinti, 25 kazanan, 10 paylaşım) ve profil kartı istatistiği.
-- supabase-duel.sql'i daha önce çalıştırdıysan SADECE bu dosyayı çalıştır. (İlk kez kuruyorsan supabase-duel.sql yeterli, bunu çalıştırma.)
alter table public.duels add column if not exists pay1 numeric(6,1);
alter table public.duels add column if not exists pay2 numeric(6,1);

create or replace function public.duel_settle(did uuid) returns void
language plpgsql security definer set search_path = public as $$
declare d public.duels; w uuid; tot int; pw numeric(6,1); sw int; p1v numeric(6,1); p2v numeric(6,1);
begin
  select * into d from public.duels where id = did for update;
  if not found or d.status <> 'active' then return; end if;
  if not ((d.a1 >= d.qn and d.a2 >= d.qn) or now() > d.start_at + make_interval(secs => d.qn * d.per_q + 15)) then return; end if;
  w := case when d.s1 > d.s2 then d.p1 when d.s2 > d.s1 then d.p2
            when d.a1 >= d.qn and d.a2 >= d.qn and d.t1 < d.t2 then d.p1
            when d.a1 >= d.qn and d.a2 >= d.qn and d.t2 < d.t1 then d.p2
            else null end;
  tot := d.s1 + d.s2;
  -- Her oyuncu 20 puan koyar (havuz 40), 5 puan kesilir, kalan 35'in 25'i kazananın, 10'u maç puanına göre paylaşılır.
  if w is null then
    p1v := 17.5; p2v := 17.5;
  else
    sw := case when w = d.p1 then d.s1 else d.s2 end;
    pw := round(25 + case when tot = 0 then 5 else 10.0 * sw / tot end, 1);
    if w = d.p1 then p1v := pw; p2v := 35 - pw; else p2v := pw; p1v := 35 - pw; end if;
  end if;
  update public.duels set status = 'done', done_at = now(), winner = w, pay1 = p1v, pay2 = p2v where id = did;
end $$;
revoke all on function public.duel_settle(uuid) from public, anon, authenticated;

create or replace function public.duel_join(p_wn int) returns uuid
language plpgsql security definer set search_path = public as $$
declare uid uuid := auth.uid(); opp uuid; did uuid;
begin
  if uid is null or not public.is_approved() or public.is_blocked(uid) then raise exception 'not allowed'; end if;
  perform public.duel_settle(id) from public.duels where status = 'active' and (p1 = uid or p2 = uid);
  select id into did from public.duels where status = 'active' and (p1 = uid or p2 = uid) order by created_at desc limit 1;
  if did is not null then delete from public.duel_queue where user_id = uid; return did; end if;
  if coalesce((select ap from public.scores where user_id = uid), 0) < 20 then raise exception 'low points'; end if;
  delete from public.duel_queue where joined_at < now() - interval '10 seconds';
  select user_id into opp from public.duel_queue where user_id <> uid and wn = p_wn order by joined_at limit 1 for update skip locked;
  if opp is null then
    insert into public.duel_queue(user_id, wn, joined_at) values (uid, p_wn, now())
      on conflict (user_id) do update set joined_at = now(), wn = p_wn;
    return null;
  end if;
  delete from public.duel_queue where user_id in (uid, opp);
  insert into public.duels(p1, p2, seed, wn, start_at)
    values (opp, uid, floor(random() * 2147480000)::int, p_wn, now() + interval '5 seconds')
    returning id into did;
  return did;
end $$;

-- Bir kullanıcının düello istatistiği (profil kartında gösterilir)
create or replace function public.duel_stats(target uuid) returns jsonb
language plpgsql security definer set search_path = public as $$
declare r jsonb;
begin
  if not public.is_approved() then raise exception 'not allowed'; end if;
  select jsonb_build_object('n', count(*), 'w', count(*) filter (where winner = target),
         'l', count(*) filter (where winner is not null and winner <> target),
         'd', count(*) filter (where winner is null)) into r
  from public.duels where status = 'done' and (p1 = target or p2 = target);
  return r;
end $$;
revoke all on function public.duel_stats(uuid) from public, anon;
grant execute on function public.duel_stats(uuid) to authenticated;
