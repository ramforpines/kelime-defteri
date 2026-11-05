-- Seviye sınavları (A2 Key, B1 Preliminary, B2 First, C1 Advanced): ilerleme, tek seferlik hak, sonuç (4.155.0)
-- Kullanıcı her sınavı bir kez çözer; ilerleme sunucuda saklanır, başka gün / cihazda kaldığı yerden devam eder.
-- Yönetici tüm sonuçları görür ve gerekirse bir kullanıcının sınavını sıfırlayabilir.

create table if not exists public.exam_runs (
  user_id uuid not null references auth.users(id) on delete cascade,
  exam_id text not null,
  status text not null default 'active' check (status in ('active','done')),
  state jsonb not null default '{}'::jsonb,
  result jsonb,
  started_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  finished_at timestamptz,
  primary key (user_id, exam_id)
);
alter table public.exam_runs enable row level security;
revoke all on public.exam_runs from anon, authenticated;

-- kendi sınavlarım
create or replace function public.exam_mine()
returns table(exam_id text, status text, state jsonb, result jsonb, started_at timestamptz, updated_at timestamptz, finished_at timestamptz)
language sql security definer stable set search_path = public as $$
  select exam_id, status, state, result, started_at, updated_at, finished_at
  from public.exam_runs where user_id = auth.uid();
$$;

-- ilerlemeyi kaydet (sınav bittiyse reddedilir)
create or replace function public.exam_save(p_exam text, p_state jsonb)
returns void language plpgsql security definer set search_path = public as $$
declare uid uuid := auth.uid(); st text;
begin
  if uid is null or not public.is_approved() then raise exception 'not allowed'; end if;
  if length(p_exam) > 20 or octet_length(p_state::text) > 200000 then raise exception 'too large'; end if;
  select status into st from public.exam_runs where user_id = uid and exam_id = p_exam for update;
  if st = 'done' then raise exception 'done'; end if;
  if st is null then
    insert into public.exam_runs(user_id, exam_id, state) values (uid, p_exam, p_state);
  else
    update public.exam_runs set state = p_state, updated_at = now() where user_id = uid and exam_id = p_exam;
  end if;
end $$;

-- sınavı bitir (bir kez)
create or replace function public.exam_finish(p_exam text, p_state jsonb, p_result jsonb)
returns void language plpgsql security definer set search_path = public as $$
declare uid uuid := auth.uid(); st text;
begin
  if uid is null or not public.is_approved() then raise exception 'not allowed'; end if;
  if octet_length(p_state::text) > 200000 or octet_length(p_result::text) > 50000 then raise exception 'too large'; end if;
  select status into st from public.exam_runs where user_id = uid and exam_id = p_exam for update;
  if st = 'done' then raise exception 'done'; end if;
  insert into public.exam_runs(user_id, exam_id, status, state, result, finished_at)
    values (uid, p_exam, 'done', p_state, p_result, now())
  on conflict (user_id, exam_id) do update set status = 'done', state = excluded.state, result = excluded.result, updated_at = now(), finished_at = now();
end $$;

-- bitmiş sınava yapay zekâ değerlendirmesini ekle
create or replace function public.exam_ai(p_exam text, p_ai jsonb)
returns void language plpgsql security definer set search_path = public as $$
declare uid uuid := auth.uid();
begin
  if uid is null then raise exception 'not allowed'; end if;
  if octet_length(p_ai::text) > 60000 then raise exception 'too large'; end if;
  update public.exam_runs set result = coalesce(result, '{}'::jsonb) || jsonb_build_object('ai', p_ai), updated_at = now()
   where user_id = uid and exam_id = p_exam and status = 'done';
end $$;

-- yönetici: tüm sonuçlar
create or replace function public.exam_admin_list()
returns table(user_id uuid, username text, name text, exam_id text, status text, result jsonb, started_at timestamptz, updated_at timestamptz, finished_at timestamptz, secs jsonb)
language plpgsql security definer stable set search_path = public as $$
begin
  if not public.is_admin() then raise exception 'not allowed'; end if;
  return query
    select r.user_id, p.username, s.name, r.exam_id, r.status, r.result, r.started_at, r.updated_at, r.finished_at,
           (select jsonb_object_agg(k, coalesce((r.state->'sec'->k->>'done')::boolean, false)) from unnest(array['R','L','W','S']) k)
    from public.exam_runs r
    left join public.profiles p on p.user_id = r.user_id
    left join public.scores s on s.user_id = r.user_id
    order by coalesce(r.finished_at, r.updated_at) desc;
end $$;

-- yönetici: bir kullanıcının sınavını sıfırla (sorun yaşandığında yeniden çözebilsin)
create or replace function public.exam_admin_reset(p_user uuid, p_exam text)
returns void language plpgsql security definer set search_path = public as $$
begin
  if not public.is_admin() then raise exception 'not allowed'; end if;
  delete from public.exam_runs where user_id = p_user and exam_id = p_exam;
end $$;

revoke all on function public.exam_mine() from public, anon;
revoke all on function public.exam_save(text, jsonb) from public, anon;
revoke all on function public.exam_finish(text, jsonb, jsonb) from public, anon;
revoke all on function public.exam_ai(text, jsonb) from public, anon;
revoke all on function public.exam_admin_list() from public, anon;
revoke all on function public.exam_admin_reset(uuid, text) from public, anon;
grant execute on function public.exam_mine() to authenticated;
grant execute on function public.exam_save(text, jsonb) to authenticated;
grant execute on function public.exam_finish(text, jsonb, jsonb) to authenticated;
grant execute on function public.exam_ai(text, jsonb) to authenticated;
grant execute on function public.exam_admin_list() to authenticated;
grant execute on function public.exam_admin_reset(uuid, text) to authenticated;

-- yapay zekâ değerlendirmesi: sınav türü ('x') eklenir; günlük hak kullanıcı 1, yönetici 3 (tüm sınav tek hak)
alter table public.pet_evals drop constraint if exists pet_evals_kind_check;
alter table public.pet_evals add constraint pet_evals_kind_check check (kind in ('w','s','x'));
create or replace function public.pet_eval_take(p_kind text, p_task text default null) returns jsonb
language plpgsql security definer set search_path = public as $$
declare uid uuid := auth.uid(); l int; nid bigint;
begin
  if uid is null or not public.is_approved() then raise exception 'not allowed'; end if;
  if p_kind not in ('w','s','x') then raise exception 'bad kind'; end if;
  perform pg_advisory_xact_lock(hashtext('pet_eval:' || uid::text));
  l := public.pet_eval_left();
  if l <= 0 then raise exception 'limit'; end if;
  insert into public.pet_evals(user_id, kind, task) values (uid, p_kind, left(coalesce(p_task, ''), 40)) returning id into nid;
  return jsonb_build_object('id', nid, 'left', l - 1);
end $$;
