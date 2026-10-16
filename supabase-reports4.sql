-- Dosya: supabase-reports4.sql
-- Kelime Defteri: gönderilen rapor yanıtını görme / düzenleme / silme. supabase-reports3.sql'in yerine geçer (ayrıca çalıştırmak gerekmez).
-- (Önce supabase-reports.sql ve supabase-feedback.sql çalıştırılmış olmalı.)
alter table public.question_reports add column if not exists replied_at timestamptz;
alter table public.question_reports add column if not exists reply text;
alter table public.feedback add column if not exists qkey text;
create index if not exists feedback_qkey_idx on public.feedback(qkey) where qkey is not null;

-- Daha önce reports3 ile gönderilmiş yanıtları bu yapıya bağla
update public.feedback f set qkey = r.qkey
from public.question_reports r
where f.qkey is null and f.user_id = r.user_id and f.reply is not null
  and f.body = left('[Soru raporu] ' || r.word || ' — ' || replace(r.question, E'\n', ' '), 1000);
update public.question_reports r set reply = f.reply, replied_at = coalesce(r.replied_at, f.replied_at)
from public.feedback f
where f.qkey = r.qkey and f.user_id = r.user_id and r.reply is null;

drop function if exists public.admin_list_reports();
create or replace function public.admin_list_reports()
returns table(qkey text, word text, feat text, question text, options jsonb, correct text, status text,
              cnt bigint, reasons jsonb, notes jsonb, last_at timestamptz, reporters jsonb, replied_at timestamptz, reply text)
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
           max(r.replied_at),
           (array_agg(r.reply order by r.replied_at desc nulls last))[1]
    from public.question_reports r
    left join public.profiles p on p.user_id = r.user_id
    left join public.scores s on s.user_id = r.user_id
    group by r.qkey
    order by (case when bool_or(r.status = 'open') then 0 else 1 end), count(*) desc, max(r.created_at) desc
    limit 300;
end $$;
revoke all on function public.admin_list_reports() from public, anon;
grant execute on function public.admin_list_reports() to authenticated;

-- Yanıt gönder ya da var olan yanıtı güncelle (kullanıcılar Geri bildirim sekmesinde görür)
create or replace function public.admin_reply_report(k text, reply_text text)
returns int language plpgsql security definer set search_path = public as $$
declare n int;
begin
  if not public.is_admin() then raise exception 'not allowed'; end if;
  if reply_text is null or char_length(btrim(reply_text)) < 2 then raise exception 'empty'; end if;
  update public.feedback set reply = left(btrim(reply_text), 1000), replied_at = now(), status = 'done'
    where qkey = k and user_id in (select user_id from public.question_reports where qkey = k);
  insert into public.feedback(user_id, kind, body, status, reply, replied_at, qkey)
  select r.user_id, 'hata', left('[Soru raporu] ' || r.word || ' — ' || replace(r.question, E'\n', ' '), 1000),
         'done', left(btrim(reply_text), 1000), now(), k
  from public.question_reports r
  where r.qkey = k and not exists (select 1 from public.feedback f where f.qkey = k and f.user_id = r.user_id);
  update public.question_reports set replied_at = now(), reply = left(btrim(reply_text), 1000) where qkey = k;
  select count(*) into n from public.question_reports where qkey = k;
  return n;
end $$;

-- Gönderilen yanıtı sil (kullanıcıların listesinden de kalkar)
create or replace function public.admin_delete_report_reply(k text)
returns void language plpgsql security definer set search_path = public as $$
begin
  if not public.is_admin() then raise exception 'not allowed'; end if;
  delete from public.feedback where qkey = k;
  update public.question_reports set replied_at = null, reply = null where qkey = k;
end $$;
revoke all on function public.admin_reply_report(text, text) from public, anon;
revoke all on function public.admin_delete_report_reply(text) from public, anon;
grant execute on function public.admin_reply_report(text, text) to authenticated;
grant execute on function public.admin_delete_report_reply(text) to authenticated;
