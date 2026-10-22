-- Dosya: supabase-dp-neg.sql
-- Kelime Defteri: günlük puan eksiye inebilsin (dereceli düello kaybı gibi kayıplar test çözmeden de günlük puandan düşsün).
-- SQL Editor'da bir kez çalıştır. (Önce supabase-scorefix.sql çalıştırılmış olmalı.)
-- Çalıştırmazsan uygulama eksi puanı sunucuya 0 olarak yazar, bir şey bozulmaz.

alter table public.scores drop constraint if exists scores_dp_check;
alter table public.scores add constraint scores_dp_check check (dp between -6000 and 6000);

-- Koruma tetikleyicisi: eksi puandan toparlanırken artış sınırı 0'dan hesaplanır.
create or replace function public.scores_guard() returns trigger
language plpgsql security definer set search_path = public as $$
declare
  isad boolean := exists(select 1 from public.admins where user_id = new.user_id);
  el numeric; nm text; n2 text; dmax numeric;
begin
  new.updated_at := now();   -- istemci saatine güvenilmez
  new.name := btrim(regexp_replace(new.name, '[\x01-\x1f\x7f\u200b-\u200f\u202a-\u202e\u2066-\u2069\ufeff]', '', 'g'));
  if char_length(new.name) < 2 then new.name := (select username from public.profiles where user_id = new.user_id); end if;
  if not isad then
    n2 := public.norm_name(new.name);
    if public.reserved_name(new.name)
       or exists(select 1 from public.admins a join public.profiles p on p.user_id = a.user_id
                 left join public.scores s on s.user_id = a.user_id
                 where public.norm_name(p.username) = n2 or public.norm_name(s.name) = n2) then
      insert into public.security_log(user_id, kind, detail) values (new.user_id, 'ad_taklidi', left(new.name, 40));
      new.name := (select username from public.profiles where user_id = new.user_id);
    end if;
  end if;
  if tg_op = 'INSERT' then
    if not isad and not exists (select 1 from public.scores s0 where s0.user_id = new.user_id)
       and (new.ap > 500 or new.ans > 1500 or new.lrn > 400 or new.st > 3) then
      insert into public.security_log(user_id, kind, detail) values (new.user_id, 'ilk_kayit_sinir', format('ap=%s ans=%s lrn=%s st=%s', new.ap, new.ans, new.lrn, new.st));
      new.ap := least(new.ap, 500); new.ans := least(new.ans, 1500); new.cor := least(new.cor, new.ans);
      new.lrn := least(new.lrn, 400); new.st := least(new.st, 3);
      new.dp := least(new.dp, 500); new.wp := least(new.wp, 500); new.da := least(new.da, 1500); new.dc := least(new.dc, new.da); new.wa := least(new.wa, 1500); new.wc := least(new.wc, new.wa);
    end if;
  elsif not isad then
    el := greatest(extract(epoch from (now() - old.updated_at)), 5);
    if new.ap - old.ap > 150 + el * 3 then
      dmax := old.ap + 150 + el * 3;
      insert into public.security_log(user_id, kind, detail) values (new.user_id, 'puan_sicramasi', format('ap %s -> %s (izin %s), %s sn', old.ap, new.ap, round(dmax), round(el)));
      new.ap := dmax;
    end if;
    if new.ans - old.ans > 60 + el * 3 then
      insert into public.security_log(user_id, kind, detail) values (new.user_id, 'soru_sicramasi', format('ans %s -> %s, %s sn', old.ans, new.ans, round(el)));
      new.ans := old.ans + (60 + el * 3)::int; new.cor := least(new.cor, new.ans);
    end if;
    if new.lrn - old.lrn > 40 + el then
      insert into public.security_log(user_id, kind, detail) values (new.user_id, 'ogrenme_sicramasi', format('lrn %s -> %s, %s sn', old.lrn, new.lrn, round(el)));
      new.lrn := old.lrn + (40 + el)::int;
    end if;
    if new.dp - (case when new.dk is not distinct from old.dk then greatest(old.dp, 0) else 0 end) > 150 + el * 3 then
      new.dp := (case when new.dk is not distinct from old.dk then greatest(old.dp, 0) else 0 end) + 150 + el * 3; end if;
    if new.wp - (case when new.wk is not distinct from old.wk then old.wp else 0 end) > 150 + el * 3 then
      new.wp := (case when new.wk is not distinct from old.wk then old.wp else 0 end) + 150 + el * 3; end if;
    if new.da - (case when new.dk is not distinct from old.dk then old.da else 0 end) > 60 + el * 3 then
      new.da := ((case when new.dk is not distinct from old.dk then old.da else 0 end) + 60 + el * 3)::int; new.dc := least(new.dc, new.da); end if;
    if new.wa - (case when new.wk is not distinct from old.wk then old.wa else 0 end) > 60 + el * 3 then
      new.wa := ((case when new.wk is not distinct from old.wk then old.wa else 0 end) + 60 + el * 3)::int; new.wc := least(new.wc, new.wa); end if;
    if new.st - old.st > 2 + el / 86400 then new.st := old.st + (2 + el / 86400)::int; end if;
  end if;
  return new;
end $$;
