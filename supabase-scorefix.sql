-- Dosya: supabase-scorefix.sql
-- Kelime Defteri: liderlik tablosunda 500 puanda takılma hatasının düzeltilmesi. SQL Editor'da bir kez çalıştır.
-- Hata: puan kaydı "upsert" ile yazıldığı için, satır zaten varken bile "ilk kayıt sınırı" (puan 500, soru 1500, öğrenilen 400, seri 3) her seferinde uygulanıyordu.
-- Yönetici bu sınırdan muaf olduğu için fark edilmemişti. Düzeltme: ilk kayıt sınırı yalnızca gerçekten yeni satırda uygulanır.
-- (Önce supabase-security.sql çalıştırılmış olmalı.)

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
    if new.dp - (case when new.dk is not distinct from old.dk then old.dp else 0 end) > 150 + el * 3 then
      new.dp := (case when new.dk is not distinct from old.dk then old.dp else 0 end) + 150 + el * 3; end if;
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

-- Onarım: bugüne kadar kısılmış puanları kullanıcıların kendi kayıtlı ilerlemesinden (user_state) yeniden hesapla.
-- Öğrenilen kelime ve seri sayıları, kullanıcı uygulamayı kullandıkça birkaç kayıt içinde kendiliğinden düzelir.
alter table public.scores disable trigger scores_guard_trg;
update public.scores s set
  ap = greatest(0, coalesce((u.state ->> 'tp')::numeric, s.ap)),
  ans = greatest(s.ans, coalesce((select sum((v ->> 0)::int + (v ->> 1)::int) from jsonb_each(u.state -> 'lv') x(k, v)), 0)::int),
  cor = greatest(s.cor, coalesce((select sum((v ->> 0)::int) from jsonb_each(u.state -> 'lv') x(k, v)), 0)::int),
  dp = greatest(s.dp, coalesce(((u.state -> 'days') -> s.dk ->> 'p')::numeric, 0)),
  da = greatest(s.da, coalesce(((u.state -> 'days') -> s.dk ->> 'a')::int, 0)),
  dc = greatest(s.dc, coalesce(((u.state -> 'days') -> s.dk ->> 'c')::int, 0)),
  wp = greatest(s.wp, coalesce((select sum((v ->> 'p')::numeric) from jsonb_each(u.state -> 'days') d(k, v) where d.k >= s.wk and d.k < to_char(s.wk::date + 7, 'YYYY-MM-DD')), 0)),
  wa = greatest(s.wa, coalesce((select sum((v ->> 'a')::int) from jsonb_each(u.state -> 'days') d(k, v) where d.k >= s.wk and d.k < to_char(s.wk::date + 7, 'YYYY-MM-DD')), 0)::int),
  wc = greatest(s.wc, coalesce((select sum((v ->> 'c')::int) from jsonb_each(u.state -> 'days') d(k, v) where d.k >= s.wk and d.k < to_char(s.wk::date + 7, 'YYYY-MM-DD')), 0)::int)
from public.user_state u
where u.user_id = s.user_id and jsonb_typeof(u.state) = 'object'
  and s.dk is not null and s.wk is not null
  and (s.ap = 500 or s.dp = 500 or s.wp = 500 or s.ans = 1500)
  and not exists (select 1 from public.admins a where a.user_id = s.user_id);
alter table public.scores enable trigger scores_guard_trg;
