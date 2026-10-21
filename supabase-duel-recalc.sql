-- Dereceli puan geçişi geriye dönük güncelleme (v4.102): tüm bitmiş dereceli maçlar yeni kurala göre yeniden hesaplanır.
-- Önce supabase-duel-ceza.sql çalışmış olmalı. ÖNCE YEDEK ALIN. Bir kez çalıştırın; tekrar çalıştırmak güvenlidir (hesaplanan maçlar atlanır).
-- Her kullanıcı uygulamayı açınca farkı bir kez alır ve "dereceli sistem değişikliği nedeniyle X puan iade edildi" bildirimini görür.

create table if not exists public.duel_recalc (
  duel_id uuid not null,
  user_id uuid not null references auth.users(id) on delete cascade,
  old_dl numeric not null,
  new_dl numeric not null,
  delta numeric not null,
  done_at timestamptz,
  acked boolean not null default false,
  created_at timestamptz not null default now(),
  primary key (duel_id, user_id)
);
create index if not exists duel_recalc_user_idx on public.duel_recalc(user_id, acked);
alter table public.duel_recalc enable row level security;
revoke all on public.duel_recalc from anon, authenticated;

create or replace function public.duel_recalc_run() returns text
language plpgsql security definer set search_path = public as $$
declare d public.duels; w uuid; c1 numeric; c2 numeric; sh numeric; lk numeric; wk numeric; t numeric; bn numeric; rt numeric;
        n1 numeric; n2 numeric; n int := 0; nu int := 0; tot numeric := 0;
begin
  for d in select * from public.duels
           where mode = 'ranked' and status = 'done' and winner is not null
             and rp1 is not null and rp2 is not null and rk1 is not null and rk2 is not null
             and not exists (select 1 from public.duel_recalc r where r.duel_id = duels.id)
           order by done_at
           for update
  loop
    w := d.winner;
    c1 := greatest(d.s1, 0); c2 := greatest(d.s2, 0);
    if c1 + c2 = 0 then continue; end if;   -- iki skor da 0 ya da altı: berabere sayılır, puan geçişi yok
    sh := (case when w = d.p1 then c1 else c2 end) / (c1 + c2);
    lk := case when w = d.p1 then d.rk2 else d.rk1 end;
    wk := case when w = d.p1 then d.rk1 else d.rk2 end;
    t := round(least(lk * sh, 3 * wk), 1);
    rt := public.duel_rate(coalesce(case when w = d.p1 then d.rp2 else d.rp1 end, 200));
    bn := case when t <= 0 then 0 else round(t * rt, 1) end;
    n1 := case when w = d.p1 then t + bn else -t end;
    n2 := case when w = d.p2 then t + bn else -t end;
    if coalesce(d.dl1, 0) <> n1 then
      insert into public.duel_recalc(duel_id, user_id, old_dl, new_dl, delta, done_at) values (d.id, d.p1, coalesce(d.dl1, 0), n1, n1 - coalesce(d.dl1, 0), d.done_at);
      nu := nu + 1; tot := tot + (n1 - coalesce(d.dl1, 0));
    end if;
    if coalesce(d.dl2, 0) <> n2 then
      insert into public.duel_recalc(duel_id, user_id, old_dl, new_dl, delta, done_at) values (d.id, d.p2, coalesce(d.dl2, 0), n2, n2 - coalesce(d.dl2, 0), d.done_at);
      nu := nu + 1; tot := tot + (n2 - coalesce(d.dl2, 0));
    end if;
    update public.duels set dl1 = n1, dl2 = n2 where id = d.id;
    n := n + 1;
  end loop;
  return n || ' maç yeniden hesaplandı, ' || nu || ' kullanıcı satırı, toplam fark ' || tot;
end $$;
revoke all on function public.duel_recalc_run() from public, anon, authenticated;

-- kullanıcı: bekleyen farkları çeker
create or replace function public.duel_recalc_pull() returns jsonb
language sql stable security definer set search_path = public as $$
  select coalesce(jsonb_agg(jsonb_build_object('id', duel_id, 'delta', delta, 'done_at', done_at) order by done_at), '[]'::jsonb)
  from public.duel_recalc where user_id = auth.uid() and not acked
$$;
revoke all on function public.duel_recalc_pull() from public, anon;
grant execute on function public.duel_recalc_pull() to authenticated;

-- kullanıcı: işlenen farkları onaylar
create or replace function public.duel_recalc_ack(p_ids uuid[]) returns void
language sql security definer set search_path = public as $$
  update public.duel_recalc set acked = true where user_id = auth.uid() and duel_id = any(p_ids)
$$;
revoke all on function public.duel_recalc_ack(uuid[]) from public, anon;
grant execute on function public.duel_recalc_ack(uuid[]) to authenticated;

select public.duel_recalc_run();
