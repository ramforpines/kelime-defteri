-- Sınavlar 2. adım (4.156.0): sıralama tablosu, seviye kilidi, haftada 1 sınav, haftada 1 yapay zekâ değerlendirmesi
-- Önce supabase-sinav.sql çalıştırılmış olmalı.

-- Seviye sırası: a2 → b1 → b2 → c1. Bir seviyenin sınavı, bir önceki seviyeden en az bir sınav bitmeden başlatılamaz.
-- Haftada 1 sınav: son 7 gün içinde başka bir sınava başlanmışsa yenisi başlatılamaz. Yöneticiler bu kurallardan muaftır.
create or replace function public.exam_can_start(p_exam text)
returns void language plpgsql security definer stable set search_path = public as $$
declare uid uuid := auth.uid(); lv text[] := array['a2','b1','b2','c1']; i int; last timestamptz;
begin
  if exists(select 1 from public.admins where user_id = uid) then return; end if;
  i := array_position(lv, left(p_exam, 2));
  if i is null then raise exception 'bad exam'; end if;
  if i > 1 and not exists(select 1 from public.exam_runs where user_id = uid and left(exam_id, 2) = lv[i-1] and status = 'done') then
    raise exception 'locked';
  end if;
  select max(started_at) into last from public.exam_runs where user_id = uid and exam_id <> p_exam;
  if last is not null and last > now() - interval '7 days' then raise exception 'week'; end if;
end $$;

create or replace function public.exam_save(p_exam text, p_state jsonb)
returns void language plpgsql security definer set search_path = public as $$
declare uid uuid := auth.uid(); st text;
begin
  if uid is null or not public.is_approved() then raise exception 'not allowed'; end if;
  if length(p_exam) > 20 or octet_length(p_state::text) > 200000 then raise exception 'too large'; end if;
  select status into st from public.exam_runs where user_id = uid and exam_id = p_exam for update;
  if st = 'done' then raise exception 'done'; end if;
  if st is null then
    perform public.exam_can_start(p_exam);
    insert into public.exam_runs(user_id, exam_id, state) values (uid, p_exam, p_state);
  else
    update public.exam_runs set state = p_state, updated_at = now() where user_id = uid and exam_id = p_exam;
  end if;
end $$;

create or replace function public.exam_finish(p_exam text, p_state jsonb, p_result jsonb)
returns void language plpgsql security definer set search_path = public as $$
declare uid uuid := auth.uid(); st text;
begin
  if uid is null or not public.is_approved() then raise exception 'not allowed'; end if;
  if octet_length(p_state::text) > 200000 or octet_length(p_result::text) > 50000 then raise exception 'too large'; end if;
  select status into st from public.exam_runs where user_id = uid and exam_id = p_exam for update;
  if st = 'done' then raise exception 'done'; end if;
  if st is null then perform public.exam_can_start(p_exam); end if;
  insert into public.exam_runs(user_id, exam_id, status, state, result, finished_at)
    values (uid, p_exam, 'done', p_state, p_result, now())
  on conflict (user_id, exam_id) do update set status = 'done', state = excluded.state, result = excluded.result, updated_at = now(), finished_at = now();
end $$;

-- Sıralama tablosu: bir sınavı bitirmiş herkesin sonucu (onaylı kullanıcılar görebilir)
create or replace function public.exam_board(p_exam text)
returns table(user_id uuid, username text, name text, result jsonb, finished_at timestamptz)
language plpgsql security definer stable set search_path = public as $$
begin
  if auth.uid() is null or not public.is_approved() then raise exception 'not allowed'; end if;
  return query
    select r.user_id, p.username, s.name, r.result, r.finished_at
    from public.exam_runs r
    join public.profiles p on p.user_id = r.user_id
    left join public.scores s on s.user_id = r.user_id
    where r.exam_id = p_exam and r.status = 'done' and p.approved
    order by r.finished_at;
end $$;
revoke all on function public.exam_board(text) from public, anon;
grant execute on function public.exam_board(text) to authenticated;
revoke all on function public.exam_can_start(text) from public, anon;

-- Yapay zekâ değerlendirmesi: kullanıcı haftada 1 (son 7 gün), yönetici günde 3
create or replace function public.pet_eval_left() returns int
language plpgsql security definer stable set search_path = public as $$
declare uid uuid := auth.uid(); adm boolean; used int;
begin
  if uid is null then return 0; end if;
  adm := exists(select 1 from public.admins where user_id = uid);
  if adm then
    select count(*) into used from public.pet_evals
     where user_id = uid and created_at >= (date_trunc('day', now() at time zone 'Europe/Istanbul') at time zone 'Europe/Istanbul');
    return greatest(3 - used, 0);
  end if;
  select count(*) into used from public.pet_evals where user_id = uid and created_at > now() - interval '7 days';
  return greatest(1 - used, 0);
end $$;
