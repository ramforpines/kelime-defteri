-- Dosya: supabase-sync.sql
-- Kelime Defteri: ilerleme eşitleme güvenliği. SQL Editor'da bir kez çalıştır.
-- user_state tablosu üzerine yazılırken, daha büyük (daha çok ilerleme içeren) önceki durum "prev" sütununda saklanır.
-- Böylece bir cihaz yanlışlıkla boş/eski veri gönderse bile son iyi durum kurtarılabilir.
alter table public.user_state add column if not exists prev jsonb;
alter table public.user_state add column if not exists prev_at timestamptz;

create or replace function public.user_state_keep() returns trigger
language plpgsql security definer set search_path = public as $$
begin
  if new.state is distinct from old.state then
    if new.prev is null or length(old.state::text) >= length(new.prev::text) or coalesce(new.prev_at, '-infinity') < now() - interval '14 days' then
      new.prev := old.state;
      new.prev_at := coalesce(old.updated_at, now());
    end if;
  end if;
  return new;
end $$;
drop trigger if exists user_state_keep_trg on public.user_state;
create trigger user_state_keep_trg before update on public.user_state
  for each row execute function public.user_state_keep();

-- Kullanıcı tablodan okurken "prev" görünmesin diye istemci yalnızca "state" ister; yine de kendi satırını okuyabilir.
-- Bir kullanıcının son iyi durumunu geri yüklemek için (örnek: kullanıcı adı ramazan_1):
--   update public.user_state set state = prev, updated_at = now()
--   where user_id = (select user_id from public.profiles where username = 'ramazan_1') and prev is not null;
