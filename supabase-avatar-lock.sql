-- Kilitli avatarlar için sunucu doğrulaması.
-- 49 = yönetici F-16, 50 = Düello Ejderi (1 dereceli galibiyet), 51-56 = lig miğferleri (Platin, Zümrüt, Elmas, Ustalık, Büyükustalık, Şampiyonluk).
-- Gereken: supabase-duel-elg.sql (duel_wincount) çalıştırılmış olmalı. SQL Editor'da bir kez çalıştırın.

create or replace function public.avatar_allowed(u uuid, a int) returns boolean
language plpgsql stable security definer set search_path = public as $$
declare v_ap numeric; w int; rk int;
begin
  if a is null or a < 49 or a > 56 then return true; end if;
  if exists(select 1 from public.admins where user_id = u) then return true; end if;
  if a = 49 then return false; end if;
  w := public.duel_wincount(u);
  if a = 50 then return w >= 1; end if;
  v_ap := coalesce((select s.ap from public.scores s where s.user_id = u), 0);
  rk := 1 + (select count(*) from public.scores s where s.ap > v_ap)::int;
  return case a
    when 51 then v_ap >= 2000  and w >= 20
    when 52 then v_ap >= 3500  and w >= 50
    when 53 then v_ap >= 6000  and w >= 100
    when 54 then v_ap >= 10000 and w >= 200
    when 55 then w >= 200 and (v_ap >= 16000 or (v_ap >= 10000 and rk <= 30))
    when 56 then w >= 200 and (v_ap >= 25000 or (v_ap >= 10000 and rk <= 10))
    else false end;
end $$;
revoke all on function public.avatar_allowed(uuid, int) from public, anon, authenticated;

create or replace function public.scores_av_lock() returns trigger
language plpgsql security definer set search_path = public as $$
begin
  if new.av between 49 and 56 and (tg_op = 'INSERT' or new.av is distinct from old.av) then
    if not public.avatar_allowed(new.user_id, new.av) then
      new.av := case when tg_op = 'UPDATE' and public.avatar_allowed(new.user_id, old.av) then old.av else 0 end;   -- uygunsuz seçim: eski (geçerliyse) avatara dön
    end if;
  end if;
  return new;
end $$;
drop trigger if exists scores_av_lock_trg on public.scores;
create trigger scores_av_lock_trg before insert or update on public.scores
  for each row execute function public.scores_av_lock();

-- Şu an uygunsuz miğfer seçmiş olanları (varsa) harf avatarına döndür
update public.scores s set av = 0 where s.av between 51 and 56 and not public.avatar_allowed(s.user_id, s.av);
