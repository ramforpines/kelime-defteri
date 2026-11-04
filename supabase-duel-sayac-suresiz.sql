-- Düello hile cezası sayacı süresiz (4.152.4)
-- Önceki kural: ceza merdiveni son 15 gündeki iptal sayısına göre artıyordu (15 gün sonra sayaçtan düşüyordu).
-- Yeni kural: sayaç hiç sıfırlanmaz; n. iptal = ×n puan cezası + n×100 dk yasak (en çok ×7 / 700 dk), tüm zamanlar sayılır.
-- Yönetici iadesi yapılmış (duel_admin_refund) iptaller sayaca girmez.
-- Değişen: duel_guard (ceza hesabı), duel_flag_list ve duel_admin_summary (yönetici ekranındaki sayaç).

create or replace function public.duel_guard(did uuid, p_kind text, p_q int default null, p_away int default null) returns jsonb
language plpgsql security definer set search_path = public as $$
declare uid uuid := auth.uid(); d public.duels; fid bigint; kd text := p_kind; v_n int := 0; v_lv int := 0; v_mult numeric := 1; v_pen numeric := 0; v_opp numeric := 0;
        v_ban int := 0; v_share numeric; v_lk numeric; v_ok numeric; v_base numeric; v_so numeric; v_sm numeric; v_void boolean := false; v_warn boolean := false;
        v_zq int; v_opp_id uuid; v_vc int;
begin
  if uid is null then raise exception 'not allowed'; end if;
  select * into d from public.duels where id = did for update;
  if not found or uid not in (d.p1, d.p2) then raise exception 'not allowed'; end if;
  if kd = 'blur2' then kd := 'blur'; end if;
  if kd not in ('hide','hide_short','hide_off','blur','trap') then raise exception 'bad kind'; end if;
  v_opp_id := case when uid = d.p1 then d.p2 else d.p1 end;
  if p_away is not null then
    select max(id) into fid from public.duel_flags where duel_id = did and user_id = uid and kind = kd and away_ms is null;
    if fid is not null then update public.duel_flags set away_ms = p_away where id = fid; end if;
  end if;
  if p_away is null or fid is null then
    insert into public.duel_flags(duel_id, user_id, kind, q, away_ms) values (did, uid, kd, p_q, p_away);
  end if;

  if d.status = 'active' and d.mode = 'ranked' and kd in ('hide','blur') then
    select count(*) into v_n from public.duel_flags where duel_id = did and user_id = uid and kind = kd;
    if kd = 'hide' then
      if v_n >= 2 then v_void := true; else v_warn := true; end if;
    else
      if v_n >= 3 then v_void := true; else v_warn := true; end if;
    end if;

    if v_warn and kd = 'hide' then
      -- uyarı alınan ayrılmada o an açık soru 0 puan sayılır
      v_zq := least(greatest(coalesce(p_q, 0), 0), d.qn - 1);
      if uid = d.p1 then update public.duels set zq1 = v_zq where id = did; else update public.duels set zq2 = v_zq where id = did; end if;
    end if;

    if v_void then
      select count(*) into v_vc from public.duels where void_by = uid and status = 'void' and id <> did and not exists(select 1 from public.duel_penalties rp where rp.duel_id = public.duels.id and rp.kind = 'admin_refund');
      v_lv := v_vc + 1;
      v_mult := least(v_lv, 7);
      v_sm := greatest(case when uid = d.p1 then d.s1 else d.s2 end, 0);
      v_so := greatest(case when uid = d.p1 then d.s2 else d.s1 end, 0);
      v_share := greatest(0.5, case when v_sm + v_so = 0 then 0.5 else v_so / (v_sm + v_so) end);
      v_lk := coalesce(case when uid = d.p1 then d.rk1 else d.rk2 end, 0);
      v_ok := coalesce(case when uid = d.p1 then d.rk2 else d.rk1 end, 0);
      v_base := round(least(v_lk * v_share, 4 * v_ok), 1);
      v_pen := round(v_base * v_mult, 1);
      v_opp := round(v_pen * 0.2, 1);
      v_ban := least(v_lv, 7) * 100;
      insert into public.duel_bans(user_id, until, lv, source) values (uid, now() + make_interval(mins => v_ban), v_lv, 'auto')
        on conflict (user_id) do update set until = excluded.until, lv = excluded.lv, source = 'auto';
      update public.duels set status = 'void', void_reason = (case when kd = 'blur' then 'blur3' else 'hide' end), void_by = uid, done_at = now(),
        pen_lv = v_lv, pen_t = false, pen_ban = v_ban,
        pen1 = case when uid = p1 then v_pen end, pen2 = case when uid = p2 then v_pen end,
        dl1 = case when uid = p1 then (case when v_pen > 0 then -v_pen end) else (case when v_opp > 0 then v_opp end) end,
        dl2 = case when uid = p2 then (case when v_pen > 0 then -v_pen end) else (case when v_opp > 0 then v_opp end) end
      where id = did;
      insert into public.duel_penalties(user_id, duel_id, kind, lv, pts, ban_min, note)
        values (uid, did, 'auto', v_lv, v_pen, v_ban, case when kd = 'blur' then 'Odak kaybı (3.)' else 'Uygulamadan ayrılma (2.)' end);
    end if;
  end if;

  select count(*) into v_vc from public.duels where void_by = uid and status = 'void' and not exists(select 1 from public.duel_penalties rp where rp.duel_id = public.duels.id and rp.kind = 'admin_refund');
  return jsonb_build_object('status', (select status from public.duels where id = did), 'n', v_n, 'warn', v_warn, 'zq', v_zq,
                            'lv', v_lv, 'pen', v_pen, 'opp', v_opp, 'ban', v_ban, 'voids', v_vc);
end $$;
revoke all on function public.duel_guard(uuid, text, int, int) from public, anon;
grant execute on function public.duel_guard(uuid, text, int, int) to authenticated;

create or replace function public.duel_flag_list(n int default 100)
returns table(id bigint, user_id uuid, name text, un text, kind text, q int, away_ms int, created_at timestamptz, voided boolean, wk int)
language plpgsql stable security definer set search_path = public as $$
begin
  if not public.is_admin() then raise exception 'not allowed'; end if;
  return query
  select f.id, f.user_id, s.name::text, s.un::text, f.kind, f.q, f.away_ms, f.created_at,
         (d.status = 'void' and d.void_by = f.user_id) as voided,
         (select count(*)::int from public.duels v where v.void_by = f.user_id and v.status = 'void' and not exists(select 1 from public.duel_penalties rp where rp.duel_id = v.id and rp.kind = 'admin_refund')) as wk
  from public.duel_flags f
  left join public.scores s on s.user_id = f.user_id
  left join public.duels d on d.id = f.duel_id
  order by f.created_at desc limit least(greatest(coalesce(n, 100), 1), 300);
end $$;
revoke all on function public.duel_flag_list(int) from public, anon;
grant execute on function public.duel_flag_list(int) to authenticated;

create or replace function public.duel_admin_summary()
returns table(user_id uuid, name text, un text, hide int, hide_short int, hide_off int, blur int, trap int, voids int, voids7 int,
              away_total bigint, away_max int, away_avg int, last_at timestamptz, ban_left int, pen_pts numeric)
language plpgsql stable security definer set search_path = public as $$
begin
  if not public.is_admin() then raise exception 'not allowed'; end if;
  return query
  select f.user_id, s.name::text, s.un::text,
         count(*) filter (where f.kind = 'hide')::int, count(*) filter (where f.kind = 'hide_short')::int,
         count(*) filter (where f.kind = 'hide_off')::int, count(*) filter (where f.kind in ('blur','blur2'))::int,
         count(*) filter (where f.kind = 'trap')::int,
         (select count(*)::int from public.duels v where v.void_by = f.user_id and v.status = 'void' and not exists(select 1 from public.duel_penalties rp where rp.duel_id = v.id and rp.kind = 'admin_refund')),
         (select count(*)::int from public.duels v where v.void_by = f.user_id and v.status = 'void' and not exists(select 1 from public.duel_penalties rp where rp.duel_id = v.id and rp.kind = 'admin_refund')),
         coalesce(sum(f.away_ms) filter (where f.kind in ('hide','hide_short','hide_off','blur','blur2')), 0)::bigint,
         coalesce(max(f.away_ms), 0)::int, coalesce(round(avg(f.away_ms))::int, 0), max(f.created_at),
         public.duel_pen_left(f.user_id),
         coalesce((select sum(p.pts) from public.duel_penalties p where p.user_id = f.user_id and p.kind = 'auto'), 0)
  from public.duel_flags f
  left join public.scores s on s.user_id = f.user_id
  group by f.user_id, s.name, s.un
  order by max(f.created_at) desc limit 200;
end $$;
revoke all on function public.duel_admin_summary() from public, anon;
grant execute on function public.duel_admin_summary() to authenticated;
