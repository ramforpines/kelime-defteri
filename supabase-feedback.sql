-- Dosya: supabase-feedback.sql
-- Kelime Defteri: kullanıcıdan yöneticiye geri bildirim mesajları. SQL Editor'da bir kez çalıştır.
-- (Önce supabase-admin.sql çalıştırılmış olmalı.)
create table if not exists public.feedback (
  id bigint generated always as identity primary key,
  user_id uuid not null references auth.users(id) on delete cascade,
  kind text not null default 'oneri' check (kind in ('oneri','hata','soru','diger')),
  body text not null check (char_length(body) between 5 and 1000),
  status text not null default 'new' check (status in ('new','read','done')),
  reply text check (reply is null or char_length(reply) <= 1000),
  created_at timestamptz not null default now(),
  replied_at timestamptz
);
create index if not exists feedback_user_idx on public.feedback(user_id, created_at desc);
alter table public.feedback enable row level security;

drop policy if exists "fb_select_own" on public.feedback;
create policy "fb_select_own" on public.feedback for select to authenticated using (user_id = auth.uid());

-- Kullanıcı yalnızca kendi adına, onaylıysa ve günde en fazla 5 mesaj ekleyebilir
drop policy if exists "fb_insert_own" on public.feedback;
create policy "fb_insert_own" on public.feedback for insert to authenticated
  with check (
    user_id = auth.uid() and public.is_approved()
    and status = 'new' and reply is null and replied_at is null
    and (select count(*) from public.feedback f where f.user_id = auth.uid() and f.created_at > now() - interval '1 day') < 5
  );

revoke all on public.feedback from anon;
revoke all on public.feedback from authenticated;
grant select, insert (user_id, kind, body) on public.feedback to authenticated;

create or replace function public.admin_list_feedback()
returns table(id bigint, user_id uuid, username text, name text, kind text, body text, status text,
              reply text, created_at timestamptz, replied_at timestamptz)
language plpgsql security definer set search_path = public as $$
begin
  if not public.is_admin() then raise exception 'not allowed'; end if;
  return query
    select f.id, f.user_id, p.username, s.name, f.kind, f.body, f.status, f.reply, f.created_at, f.replied_at
    from public.feedback f
    left join public.profiles p on p.user_id = f.user_id
    left join public.scores s on s.user_id = f.user_id
    order by (f.status = 'new') desc, f.created_at desc
    limit 300;
end $$;

create or replace function public.admin_set_feedback(fid bigint, new_status text, reply_text text default null)
returns void language plpgsql security definer set search_path = public as $$
begin
  if not public.is_admin() then raise exception 'not allowed'; end if;
  if new_status not in ('new','read','done') then raise exception 'bad status'; end if;
  update public.feedback set status = new_status,
    reply = case when reply_text is not null and btrim(reply_text) <> '' then left(btrim(reply_text), 1000) else reply end,
    replied_at = case when reply_text is not null and btrim(reply_text) <> '' then now() else replied_at end
  where id = fid;
end $$;

create or replace function public.admin_delete_feedback(fid bigint)
returns void language plpgsql security definer set search_path = public as $$
begin
  if not public.is_admin() then raise exception 'not allowed'; end if;
  delete from public.feedback where id = fid;
end $$;

revoke all on function public.admin_list_feedback() from public, anon;
revoke all on function public.admin_set_feedback(bigint, text, text) from public, anon;
revoke all on function public.admin_delete_feedback(bigint) from public, anon;
grant execute on function public.admin_list_feedback() to authenticated;
grant execute on function public.admin_set_feedback(bigint, text, text) to authenticated;
grant execute on function public.admin_delete_feedback(bigint) to authenticated;
