-- Dosya: supabase-reports5.sql
-- Kelime Defteri: raporlar her zaman önce yöneticiye düşer; yanıt yalnızca henüz yanıtlanmamış (yeni) raporlayanlara gider; eski yanıtlar ayrı gösterilir, düzenlenir, silinir.
-- supabase-reports3.sql ve supabase-reports4.sql'in yerine geçer (ayrıca çalıştırmak gerekmez).
-- (Önce supabase-reports.sql ve supabase-feedback.sql çalıştırılmış olmalı.)
alter table public.question_reports add column if not exists replied_at timestamptz;
alter table public.question_reports add column if not exists reply text;
alter table public.question_reports add column if not exists fb_id bigint;
alter table public.feedback add column if not exists qkey text;
create index if not exists feedback_qkey_idx on public.feedback(qkey) where qkey is not null;

-- Daha önce gönderilmiş yanıtları satır bazında bağla
update public.feedback f set qkey = r.qkey
from public.question_reports r
where f.qkey is null and f.user_id = r.user_id and f.reply is not null
  and f.body = left('[Soru raporu] ' || r.word || ' — ' || replace(r.question, E'\n', ' '), 1000);
update public.question_reports r set fb_id = x.id, reply = coalesce(r.reply, x.reply), replied_at = coalesce(r.replied_at, x.replied_at)
from (select distinct on (qkey, user_id) id, qkey, user_id, reply, replied_at from public.feedback
      where qkey is not null and reply is not null order by qkey, user_id, id desc) x
where x.qkey = r.qkey and x.user_id = r.user_id and r.fb_id is null;

-- Aynı kullanıcı aynı soruyu yeniden bildirirse bu yeni bir rapordur: yanıt bilgisi sıfırlanır, rapor açık olur
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
    picked = excluded.picked, status = 'open', created_at = now(), reply = null, replied_at = null, fb_id = null;
end $$;
revoke all on function public.report_question(text,text,text,jsonb,text,text,text,text) from public, anon;
grant execute on function public.report_question(text,text,text,jsonb,text,text,text,text) to authenticated;

drop function if exists public.admin_list_reports();
create or replace function public.admin_list_reports()
returns table(qkey text, word text, feat text, question text, options jsonb, correct text, status text,
              cnt bigint, reasons jsonb, notes jsonb, last_at timestamptz, reporters jsonb, pending bigint, answers jsonb)
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
                                        'picked', r.picked, 'at', r.created_at, 'replied', r.reply is not null) order by r.created_at desc),
           count(*) filter (where r.reply is null),
           (select coalesce(jsonb_agg(jsonb_build_object('reply', a.reply, 'n', a.n, 'at', a.at) order by a.at desc), '[]'::jsonb)
              from (select r3.reply, count(*) n, max(r3.replied_at) at from public.question_reports r3
                    where r3.qkey = r.qkey and r3.reply is not null group by r3.reply) a)
    from public.question_reports r
    left join public.profiles p on p.user_id = r.user_id
    left join public.scores s on s.user_id = r.user_id
    group by r.qkey
    order by (case when bool_or(r.status = 'open') then 0 else 1 end), count(*) desc, max(r.created_at) desc
    limit 300;
end $$;
revoke all on function public.admin_list_reports() from public, anon;
grant execute on function public.admin_list_reports() to authenticated;

-- Yanıt: yalnızca henüz yanıtlanmamış (yeni) raporlayanlara gider. Eski yanıtlara dokunmaz.
create or replace function public.admin_reply_report(k text, reply_text text)
returns int language plpgsql security definer set search_path = public as $$
declare n int := 0; r record; fid bigint; t text;
begin
  if not public.is_admin() then raise exception 'not allowed'; end if;
  if reply_text is null or char_length(btrim(reply_text)) < 2 then raise exception 'empty'; end if;
  t := left(btrim(reply_text), 1000);
  for r in select id, user_id, word, question from public.question_reports where qkey = k and reply is null loop
    insert into public.feedback(user_id, kind, body, status, reply, replied_at, qkey)
    values (r.user_id, 'hata', left('[Soru raporu] ' || r.word || ' — ' || replace(r.question, E'\n', ' '), 1000), 'done', t, now(), k)
    returning id into fid;
    update public.question_reports set reply = t, replied_at = now(), fb_id = fid where id = r.id;
    n := n + 1;
  end loop;
  return n;
end $$;

-- Gönderilmiş bir yanıtı (metnine göre) düzenle
create or replace function public.admin_edit_report_reply(k text, old_reply text, new_reply text)
returns int language plpgsql security definer set search_path = public as $$
declare n int; t text;
begin
  if not public.is_admin() then raise exception 'not allowed'; end if;
  if new_reply is null or char_length(btrim(new_reply)) < 2 then raise exception 'empty'; end if;
  t := left(btrim(new_reply), 1000);
  update public.feedback set reply = t, replied_at = now()
    where id in (select fb_id from public.question_reports where qkey = k and reply = old_reply and fb_id is not null);
  update public.question_reports set reply = t, replied_at = now() where qkey = k and reply = old_reply;
  get diagnostics n = row_count;
  return n;
end $$;

-- Gönderilmiş bir yanıtı sil (kullanıcıların listesinden kalkar; o raporlar yeniden "yanıtlanmamış" olur)
drop function if exists public.admin_delete_report_reply(text);
create or replace function public.admin_delete_report_reply(k text, old_reply text)
returns void language plpgsql security definer set search_path = public as $$
begin
  if not public.is_admin() then raise exception 'not allowed'; end if;
  delete from public.feedback where id in (select fb_id from public.question_reports where qkey = k and reply = old_reply and fb_id is not null);
  update public.question_reports set reply = null, replied_at = null, fb_id = null where qkey = k and reply = old_reply;
end $$;

revoke all on function public.admin_reply_report(text, text) from public, anon;
revoke all on function public.admin_edit_report_reply(text, text, text) from public, anon;
revoke all on function public.admin_delete_report_reply(text, text) from public, anon;
grant execute on function public.admin_reply_report(text, text) to authenticated;
grant execute on function public.admin_edit_report_reply(text, text, text) to authenticated;
grant execute on function public.admin_delete_report_reply(text, text) to authenticated;
