-- Kelime Defteri: güvenlik sertleştirmesi. SQL Editor'da bir kez çalıştır (tekrar çalıştırmak zararsızdır).
-- (supabase-admin.sql, supabase-chat.sql, supabase-theme.sql ve supabase-duel.sql çalıştırılmış olmalı.)

-- 0) Güvenlik kaydı: şüpheli işlemler burada tutulur, yönetici görür
create table if not exists public.security_log (
  id bigint generated always as identity primary key,
  user_id uuid references auth.users(id) on delete cascade,
  kind text not null,
  detail text not null default '',
  created_at timestamptz not null default now()
);
alter table public.security_log enable row level security;
revoke all on public.security_log from anon, authenticated;   -- yalnızca güvenli fonksiyonlar yazar/okur

-- 1) Kullanıcı adı: büyük/küçük harften bağımsız benzersiz + biçim + ayrılmış adlar
create unique index if not exists profiles_username_uq on public.profiles (lower(username));

create or replace function public.norm_name(s text) returns text
language sql immutable as $$
  select regexp_replace(translate(lower(coalesce(s, '')), 'ıöüşçğâîûİ', 'iousc' || 'gaiui'), '[^a-z0-9]', '', 'g')
$$;

create or replace function public.reserved_name(s text) returns boolean
language sql immutable as $$
  select public.norm_name(s) ~ '(admin|yonetic|yonetim|moderat|sistem|system|destek|support|kelimedefteri|official)'
$$;

create or replace function public.handle_new_user() returns trigger
language plpgsql security definer set search_path = public as $$
declare un text := split_part(new.email, '@', 1);
begin
  if un !~ '^[a-z0-9][a-z0-9_.-]{2,19}$' then raise exception 'invalid username'; end if;
  if public.reserved_name(un) then raise exception 'reserved username'; end if;
  insert into public.profiles(user_id, username, approved) values (new.id, un, false) on conflict do nothing;
  return new;
end $$;

-- 2) Görünen ad ve liderlik puanı denetimi
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
    if not isad and (new.ap > 500 or new.ans > 1500 or new.lrn > 400 or new.st > 3) then
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
drop trigger if exists scores_guard_trg on public.scores;
create trigger scores_guard_trg before insert or update on public.scores
  for each row execute function public.scores_guard();
-- sıra: önce koruma, sonra un/ad doldurma (alfabetik: scores_fill_un_trg < scores_guard_trg, ikisi de birbirinden bağımsız)

-- 3) Sohbet: özel mesaj taşkınlığı freni (dakikada 60), genel sohbet dakikada 5 aynı kalır
drop policy if exists "chat_insert" on public.chat_messages;
create policy "chat_insert" on public.chat_messages for insert to authenticated
  with check (
    user_id = auth.uid() and public.is_approved() and not public.is_blocked(auth.uid())
    and (
      (to_user is null and (select count(*) from public.chat_messages m
         where m.user_id = auth.uid() and m.to_user is null and m.created_at > now() - interval '1 minute') < 5)
      or
      (to_user is not null and public.chat_can_receive(to_user)
         and (select count(*) from public.chat_messages m
         where m.user_id = auth.uid() and m.to_user is not null and m.created_at > now() - interval '1 minute') < 60)
    )
  );

-- 4) Yardımcı fonksiyonlar anonim erişime kapatılır
revoke all on function public.is_admin() from public, anon;
revoke all on function public.is_approved() from public, anon;
revoke all on function public.is_blocked(uuid) from public, anon;
revoke all on function public.chat_can_receive(uuid) from public, anon;
grant execute on function public.is_admin() to authenticated;
grant execute on function public.is_approved() to authenticated;
grant execute on function public.is_blocked(uuid) to authenticated;
grant execute on function public.chat_can_receive(uuid) to authenticated;

-- 5) Yönetici: güvenlik kayıtları
create or replace function public.admin_security_log() returns table(id bigint, username text, kind text, detail text, created_at timestamptz)
language plpgsql security definer stable set search_path = public as $$
begin
  if not public.is_admin() then raise exception 'not allowed'; end if;
  return query select l.id, coalesce(p.username, '?'), l.kind, l.detail, l.created_at
    from public.security_log l left join public.profiles p on p.user_id = l.user_id
    order by l.id desc limit 60;
end $$;
revoke all on function public.admin_security_log() from public, anon;
grant execute on function public.admin_security_log() to authenticated;

create or replace function public.admin_clear_security_log() returns void
language plpgsql security definer set search_path = public as $$
begin
  if not public.is_admin() then raise exception 'not allowed'; end if;
  delete from public.security_log;
end $$;
revoke all on function public.admin_clear_security_log() from public, anon;
grant execute on function public.admin_clear_security_log() to authenticated;
