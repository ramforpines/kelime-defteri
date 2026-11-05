-- PET yazma / konuşma yapay zekâ değerlendirmesi: kota ve kayıt (4.154.0)
-- Edge function (pet-eval) bu fonksiyonları kullanıcının kendi oturumuyla çağırır.
-- Günlük sınır: kullanıcı 5, yönetici 50 değerlendirme (Türkiye saatine göre gün).

create table if not exists public.pet_evals (
  id bigint generated always as identity primary key,
  user_id uuid not null references auth.users(id) on delete cascade,
  kind text not null check (kind in ('w','s')),
  task text,
  created_at timestamptz not null default now(),
  output jsonb
);
create index if not exists pet_evals_user_idx on public.pet_evals(user_id, created_at desc);
alter table public.pet_evals enable row level security;
revoke all on public.pet_evals from anon, authenticated;

create or replace function public.pet_eval_left() returns int
language plpgsql security definer stable set search_path = public as $$
declare uid uuid := auth.uid(); lim int; used int;
begin
  if uid is null then return 0; end if;
  lim := case when exists(select 1 from public.admins where user_id = uid) then 50 else 5 end;
  select count(*) into used from public.pet_evals
   where user_id = uid and created_at >= (date_trunc('day', now() at time zone 'Europe/Istanbul') at time zone 'Europe/Istanbul');
  return greatest(lim - used, 0);
end $$;

create or replace function public.pet_eval_take(p_kind text, p_task text default null) returns jsonb
language plpgsql security definer set search_path = public as $$
declare uid uuid := auth.uid(); l int; nid bigint;
begin
  if uid is null or not public.is_approved() then raise exception 'not allowed'; end if;
  if p_kind not in ('w','s') then raise exception 'bad kind'; end if;
  perform pg_advisory_xact_lock(hashtext('pet_eval:' || uid::text));
  l := public.pet_eval_left();
  if l <= 0 then raise exception 'limit'; end if;
  insert into public.pet_evals(user_id, kind, task) values (uid, p_kind, left(coalesce(p_task, ''), 40)) returning id into nid;
  return jsonb_build_object('id', nid, 'left', l - 1);
end $$;

-- sonuç kaydı; p_out null ise (değerlendirme başarısız) hak geri verilir
create or replace function public.pet_eval_save(p_id bigint, p_out jsonb) returns void
language plpgsql security definer set search_path = public as $$
declare uid uuid := auth.uid();
begin
  if uid is null then raise exception 'not allowed'; end if;
  if p_out is null then delete from public.pet_evals where id = p_id and user_id = uid;
  else update public.pet_evals set output = p_out where id = p_id and user_id = uid; end if;
end $$;

revoke all on function public.pet_eval_left() from public, anon;
revoke all on function public.pet_eval_take(text, text) from public, anon;
revoke all on function public.pet_eval_save(bigint, jsonb) from public, anon;
grant execute on function public.pet_eval_left() to authenticated;
grant execute on function public.pet_eval_take(text, text) to authenticated;
grant execute on function public.pet_eval_save(bigint, jsonb) to authenticated;
