-- Dosya: supabase-reports.sql
-- Kelime Defteri: soru raporlama (hatalı / birden fazla uygun şıklı sorular). SQL Editor'da bir kez çalıştır.
-- (Önce supabase-admin.sql çalıştırılmış olmalı.)
create table if not exists public.question_reports (
  id bigint generated always as identity primary key,
  user_id uuid not null references auth.users(id) on delete cascade,
  qkey text not null check (char_length(qkey) <= 400),
  word text not null check (char_length(word) <= 120),
  feat text not null default '' check (char_length(feat) <= 20),
  question text not null check (char_length(question) <= 600),
  options jsonb not null default '[]'::jsonb,
  correct text not null default '' check (char_length(correct) <= 300),
  picked text check (picked is null or char_length(picked) <= 300),
  reason text not null default 'other' check (reason in ('multi','wrong','typo','other')),
  note text check (note is null or char_length(note) <= 300),
  status text not null default 'open' check (status in ('open','fixed','dismissed')),
  created_at timestamptz not null default now(),
  unique (user_id, qkey)
);
create index if not exists qrep_status_idx on public.question_reports(status, qkey);
alter table public.question_reports enable row level security;
revoke all on public.question_reports from anon, authenticated;

-- Kullanıcı yalnızca bu fonksiyonla rapor gönderir (onaylı, günde en fazla 40)
create or replace function public.report_question(p_word text, p_feat text, p_question text, p_options jsonb,
  p_correct text, p_picked text, p_reason text, p_note text default null)
returns void language plpgsql security definer set search_path = public as $$
declare k text;
begin
  if auth.uid() is null or not public.is_approved() then raise exception 'not allowed'; end if;
  if (select count(*) from public.question_reports where user_id = auth.uid() and created_at > now() - interval '1 day') >= 40
    then raise exception 'limit'; end if;
  if jsonb_typeof(p_options) <> 'array' or jsonb_array_length(p_options) > 8 then raise exception 'bad options'; end if;
  k := left(coalesce(p_word,'') || '|' || coalesce(p_feat,'') || '|' || coalesce(p_question,''), 400);
  insert into public.question_reports(user_id, qkey, word, feat, question, options, correct, picked, reason, note)
  values (auth.uid(), k, left(p_word,120), left(coalesce(p_feat,''),20), left(p_question,600), p_options,
          left(coalesce(p_correct,''),300), left(p_picked,300),
          case when p_reason in ('multi','wrong','typo','other') then p_reason else 'other' end,
          nullif(left(btrim(coalesce(p_note,'')),300),''))
  on conflict (user_id, qkey) do update set reason = excluded.reason, note = excluded.note,
    picked = excluded.picked, status = 'open', created_at = now();
end $$;
revoke all on function public.report_question(text,text,text,jsonb,text,text,text,text) from public, anon;
grant execute on function public.report_question(text,text,text,jsonb,text,text,text,text) to authenticated;

-- Yönetici: sorulara göre toplu liste (kaç kişi raporlamış, nedenleri)
create or replace function public.admin_list_reports()
returns table(qkey text, word text, feat text, question text, options jsonb, correct text, status text,
              cnt bigint, reasons jsonb, notes jsonb, last_at timestamptz)
language plpgsql security definer set search_path = public as $$
begin
  if not public.is_admin() then raise exception 'not allowed'; end if;
  return query
    select r.qkey, min(r.word), min(r.feat), min(r.question), (array_agg(r.options order by r.created_at desc))[1],
           min(r.correct),
           case when bool_or(r.status = 'open') then 'open' else min(r.status) end,
           count(*),
           coalesce(
             (select jsonb_object_agg(x.reason, x.c) from (select r2.reason, count(*) c from public.question_reports r2 where r2.qkey = r.qkey group by r2.reason) x), '{}'::jsonb),
           coalesce(jsonb_agg(r.note) filter (where r.note is not null), '[]'::jsonb),
           max(r.created_at)
    from public.question_reports r
    group by r.qkey
    order by (case when bool_or(r.status = 'open') then 0 else 1 end), count(*) desc, max(r.created_at) desc
    limit 300;
end $$;

create or replace function public.admin_set_reports(k text, new_status text)
returns void language plpgsql security definer set search_path = public as $$
begin
  if not public.is_admin() then raise exception 'not allowed'; end if;
  if new_status = 'delete' then delete from public.question_reports where qkey = k;
  elsif new_status in ('open','fixed','dismissed') then update public.question_reports set status = new_status where qkey = k;
  else raise exception 'bad status'; end if;
end $$;
revoke all on function public.admin_list_reports() from public, anon;
revoke all on function public.admin_set_reports(text, text) from public, anon;
grant execute on function public.admin_list_reports() to authenticated;
grant execute on function public.admin_set_reports(text, text) to authenticated;
