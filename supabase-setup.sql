-- Kelime Defteri: Supabase kurulum betiği. SQL Editor'da bir kez çalıştır.

-- 1) Kullanıcının kendi ilerlemesi (yalnızca kendisi okur/yazar)
create table if not exists public.user_state (
  user_id uuid primary key references auth.users(id) on delete cascade,
  state jsonb not null,
  updated_at timestamptz not null default now()
);

-- 2) Liderlik tablosu puanları (herkes okur, herkes yalnızca kendi satırını yazar)
create table if not exists public.scores (
  user_id uuid primary key references auth.users(id) on delete cascade,
  name text not null check (char_length(name) between 2 and 24),
  color int not null default 0 check (color between 0 and 7),
  hide boolean not null default false,
  dk text, da int not null default 0 check (da between 0 and 3000),
  dc int not null default 0 check (dc between 0 and 3000),
  dp numeric not null default 0 check (dp between 0 and 6000),
  wk text, wa int not null default 0 check (wa between 0 and 21000),
  wc int not null default 0 check (wc between 0 and 21000),
  wp numeric not null default 0 check (wp between 0 and 42000),
  ans int not null default 0 check (ans >= 0),
  cor int not null default 0 check (cor >= 0),
  ap numeric not null default 0 check (ap >= 0),
  lrn int not null default 0 check (lrn between 0 and 20000),
  st int not null default 0 check (st between 0 and 5000),
  sd text,
  updated_at timestamptz not null default now()
);

alter table public.user_state enable row level security;
alter table public.scores enable row level security;

drop policy if exists "state_select_own" on public.user_state;
drop policy if exists "state_insert_own" on public.user_state;
drop policy if exists "state_update_own" on public.user_state;
create policy "state_select_own" on public.user_state for select to authenticated using (auth.uid() = user_id);
create policy "state_insert_own" on public.user_state for insert to authenticated with check (auth.uid() = user_id);
create policy "state_update_own" on public.user_state for update to authenticated using (auth.uid() = user_id) with check (auth.uid() = user_id);

drop policy if exists "scores_select" on public.scores;
drop policy if exists "scores_insert_own" on public.scores;
drop policy if exists "scores_update_own" on public.scores;
create policy "scores_select" on public.scores for select to authenticated using (hide = false or auth.uid() = user_id);
create policy "scores_insert_own" on public.scores for insert to authenticated with check (auth.uid() = user_id);
create policy "scores_update_own" on public.scores for update to authenticated using (auth.uid() = user_id) with check (auth.uid() = user_id);

-- Anonim (giriş yapmamış) kullanıcılar hiçbir şey göremez ve yazamaz.
revoke all on public.user_state from anon;
revoke all on public.scores from anon;
