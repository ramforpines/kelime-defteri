-- Dosya: supabase-levels.sql
-- Kelime Defteri: yöneticinin kelime seviyesini elle değiştirmesi. SQL Editor'da bir kez çalıştır.
-- Herkes okur (uygulama açılışta uygular), yalnız yönetici yazar.
create table if not exists public.word_levels(
  word text primary key,
  level text not null check (level in ('A1','A2','B1','B2','C1','C2')),
  updated_at timestamptz not null default now(),
  updated_by uuid
);
alter table public.word_levels enable row level security;
drop policy if exists word_levels_read on public.word_levels;
create policy word_levels_read on public.word_levels for select to authenticated using (true);

create or replace function public.admin_set_word_level(p_word text, p_level text)
returns void language plpgsql security definer set search_path = public as $$
begin
  if not public.is_admin() then raise exception 'not allowed'; end if;
  if p_level is null or p_level = '' then
    delete from public.word_levels where word = p_word;   -- varsayılana dön
  else
    insert into public.word_levels(word, level, updated_at, updated_by) values (p_word, p_level, now(), auth.uid())
    on conflict (word) do update set level = excluded.level, updated_at = now(), updated_by = auth.uid();
  end if;
end $$;
grant execute on function public.admin_set_word_level(text, text) to authenticated;
