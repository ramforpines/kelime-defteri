-- Dosya: supabase-reports3.sql
-- Kelime Defteri: rapor eden kullanıcılara yönetici yanıtı (kullanıcı Geri bildirim sekmesinde görür) + kimin bildirdiği bilgisi.
-- (Önce supabase-reports.sql ve supabase-feedback.sql çalıştırılmış olmalı. supabase-reports2.sql'in yerine geçer, ayrıca çalıştırmak gerekmez.)
alter table public.question_reports add column if not exists replied_at timestamptz;

drop function if exists public.admin_list_reports();
create or replace function public.admin_list_reports()
returns table(qkey text, word text, feat text, question text, options jsonb, correct text, status text,
              cnt bigint, reasons jsonb, notes jsonb, last_at timestamptz, reporters jsonb, replied_at timestamptz)
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
           max(r.created_at),
           jsonb_agg(jsonb_build_object('un', p.username, 'name', s.name, 'reason', r.reason, 'note', r.note,
                                        'picked', r.picked, 'at', r.created_at) order by r.created_at desc),
           max(r.replied_at)
    from public.question_reports r
    left join public.profiles p on p.user_id = r.user_id
    left join public.scores s on s.user_id = r.user_id
    group by r.qkey
    order by (case when bool_or(r.status = 'open') then 0 else 1 end), count(*) desc, max(r.created_at) desc
    limit 300;
end $$;
revoke all on function public.admin_list_reports() from public, anon;
grant execute on function public.admin_list_reports() to authenticated;

-- Yönetici: bu soruyu bildiren herkese yanıt gönderir. Yanıt kullanıcıların "Geri bildirim" sekmesinde görünür.
create or replace function public.admin_reply_report(k text, reply_text text)
returns int language plpgsql security definer set search_path = public as $$
declare n int;
begin
  if not public.is_admin() then raise exception 'not allowed'; end if;
  if reply_text is null or char_length(btrim(reply_text)) < 2 then raise exception 'empty'; end if;
  insert into public.feedback(user_id, kind, body, status, reply, replied_at)
  select r.user_id, 'hata', left('[Soru raporu] ' || r.word || ' — ' || replace(r.question, E'\n', ' '), 1000),
         'done', left(btrim(reply_text), 1000), now()
  from public.question_reports r where r.qkey = k;
  get diagnostics n = row_count;
  update public.question_reports set replied_at = now() where qkey = k;
  return n;
end $$;
revoke all on function public.admin_reply_report(text, text) from public, anon;
grant execute on function public.admin_reply_report(text, text) to authenticated;
