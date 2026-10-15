-- Kelime Defteri: 1v1 düello (eşleştirme + aynı 20 soru + süre). SQL Editor'da bir kez çalıştır.
-- (Önce supabase-admin.sql çalıştırılmış olmalı.)
create table if not exists public.duels (
  id uuid primary key default gen_random_uuid(),
  p1 uuid not null references auth.users(id) on delete cascade,
  p2 uuid not null references auth.users(id) on delete cascade,
  seed int not null,
  wn int not null,
  qn int not null default 20,
  per_q int not null default 15,
  created_at timestamptz not null default now(),
  start_at timestamptz not null,
  status text not null default 'active' check (status in ('active','done')),
  s1 int not null default 0, s2 int not null default 0,
  c1 int not null default 0, c2 int not null default 0,
  a1 int not null default 0, a2 int not null default 0,
  t1 bigint not null default 0, t2 bigint not null default 0,
  winner uuid,
  pay1 numeric(6,1), pay2 numeric(6,1),
  done_at timestamptz
);
alter table public.duels add column if not exists pay1 numeric(6,1);
alter table public.duels add column if not exists pay2 numeric(6,1);
create index if not exists duels_p1_idx on public.duels(p1, created_at desc);
create index if not exists duels_p2_idx on public.duels(p2, created_at desc);
create table if not exists public.duel_queue (
  user_id uuid primary key references auth.users(id) on delete cascade,
  wn int not null,
  joined_at timestamptz not null default now()
);
alter table public.duels enable row level security;
alter table public.duel_queue enable row level security;
drop policy if exists "duels_select" on public.duels;
create policy "duels_select" on public.duels for select to authenticated
  using (p1 = auth.uid() or p2 = auth.uid());
revoke all on public.duels from anon, authenticated;
revoke all on public.duel_queue from anon, authenticated;
grant select on public.duels to authenticated;

-- Düello bitirme: iki taraf da bitirdiyse ya da süre dolduysa kazananı belirler (iç kullanım)
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

-- Eşleşme ara: bekleyen biri varsa düello oluşturur ve id döner, yoksa kuyruğa girer (null döner).
-- İstemci rakip bulunana kadar birkaç saniyede bir bu fonksiyonu tekrar çağırır.
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

create or replace function public.duel_cancel() returns void
language plpgsql security definer set search_path = public as $$
begin
  delete from public.duel_queue where user_id = auth.uid();
end $$;

-- Düello durumu (iki oyuncudan biri okuyabilir). now: sunucu saati, istemci geri sayımı buna göre ayarlar.
create or replace function public.duel_state(did uuid) returns jsonb
language plpgsql security definer set search_path = public as $$
declare uid uuid := auth.uid(); d public.duels;
begin
  perform public.duel_settle(did) from public.duels where id = did and (p1 = uid or p2 = uid);
  select * into d from public.duels where id = did and (p1 = uid or p2 = uid);
  if not found then return null; end if;
  return jsonb_build_object('d', to_jsonb(d), 'now', now());
end $$;

-- Bir soruyu cevapla: sıra numarası (idx) sırayla gitmeli. Puan sunucuda hesaplanır: doğruysa 100 + en çok 50 hız bonusu.
create or replace function public.duel_report(did uuid, idx int, ok boolean, ms int) returns void
language plpgsql security definer set search_path = public as $$
declare uid uuid := auth.uid(); d public.duels; mine int; pts int; m int;
begin
  select * into d from public.duels where id = did for update;
  if not found or d.status <> 'active' or uid not in (d.p1, d.p2) then raise exception 'not allowed'; end if;
  if now() < d.start_at - interval '1 second' then raise exception 'early'; end if;
  mine := case when uid = d.p1 then d.a1 else d.a2 end;
  if idx <> mine or idx >= d.qn then return; end if;
  m := least(greatest(coalesce(ms, 0), 300), d.per_q * 1000);
  pts := case when ok then 100 + round(50.0 * (1 - m::numeric / (d.per_q * 1000)))::int else 0 end;
  if uid = d.p1 then
    update public.duels set a1 = a1 + 1, s1 = s1 + pts, c1 = c1 + (case when ok then 1 else 0 end), t1 = t1 + m where id = did;
  else
    update public.duels set a2 = a2 + 1, s2 = s2 + pts, c2 = c2 + (case when ok then 1 else 0 end), t2 = t2 + m where id = did;
  end if;
  perform public.duel_settle(did);
end $$;

revoke all on function public.duel_join(int) from public, anon;
revoke all on function public.duel_cancel() from public, anon;
revoke all on function public.duel_state(uuid) from public, anon;
revoke all on function public.duel_report(uuid, int, boolean, int) from public, anon;
grant execute on function public.duel_join(int) to authenticated;
grant execute on function public.duel_cancel() to authenticated;
grant execute on function public.duel_state(uuid) to authenticated;
grant execute on function public.duel_report(uuid, int, boolean, int) to authenticated;

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
