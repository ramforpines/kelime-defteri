-- Yük azaltma: app_stats sonucunu 30 sn önbellekle (her kullanıcı için tüm tabloları taramasın) + sık kullanılan sorgulara indeks.
-- Güvenle birden çok kez çalıştırılabilir.

-- 1) İndeksler
create index if not exists duels_winner_idx on public.duels (winner) where winner is not null;
create index if not exists duels_created_idx on public.duels (created_at);
create index if not exists scores_dk_idx on public.scores (dk);
create index if not exists profiles_last_seen_idx on public.profiles (last_seen);
create index if not exists chat_pub_idx on public.chat_messages (created_at) where to_user is null;

-- 2) Önbellek tablosu
create table if not exists public.app_stats_cache (id int primary key, at timestamptz not null default now(), data jsonb);
alter table public.app_stats_cache enable row level security;
revoke all on public.app_stats_cache from anon, authenticated;

-- 3) Eski hesaplama fonksiyonu (varsa) app_stats_calc adıyla saklanır
do $$
begin
  if exists (select 1 from pg_proc p join pg_namespace n on n.oid = p.pronamespace where n.nspname = 'public' and p.proname = 'app_stats')
     and not exists (select 1 from pg_proc p join pg_namespace n on n.oid = p.pronamespace where n.nspname = 'public' and p.proname = 'app_stats_calc') then
    alter function public.app_stats() rename to app_stats_calc;
  end if;
end $$;
revoke all on function public.app_stats_calc() from public, anon, authenticated;

-- 4) app_stats artık önbellekten döner; 30 sn'den eskiyse yeniden hesaplar
create or replace function public.app_stats() returns jsonb
language plpgsql security definer set search_path = public as $$
declare c public.app_stats_cache; r jsonb;
begin
  if not public.is_approved() then raise exception 'not allowed'; end if;
  select * into c from public.app_stats_cache where id = 1;
  if found and c.at > now() - interval '30 seconds' and c.data is not null then return c.data; end if;
  r := public.app_stats_calc();
  insert into public.app_stats_cache(id, at, data) values (1, now(), r)
    on conflict (id) do update set at = excluded.at, data = excluded.data;
  return r;
end $$;
revoke all on function public.app_stats() from public, anon;
grant execute on function public.app_stats() to authenticated;
