-- Dosya: supabase-core.sql
-- Kelime Defteri: yöneticinin Odak listesine eklediği/çıkardığı kelimeler herkese uygulanır. SQL Editor'da bir kez çalıştır.
create table if not exists public.core_edits(
  word text primary key,
  op smallint not null check (op in (1,-1)),   -- 1: listeye ekle, -1: listeden çıkar
  updated_at timestamptz not null default now(),
  updated_by uuid
);
alter table public.core_edits enable row level security;
drop policy if exists core_edits_read on public.core_edits;
create policy core_edits_read on public.core_edits for select to authenticated using (true);

create or replace function public.admin_set_core(p_word text, p_op int)
returns void language plpgsql security definer set search_path = public as $$
begin
  if not public.is_admin() then raise exception 'not allowed'; end if;
  if p_op is null or p_op = 0 then
    delete from public.core_edits where word = p_word;   -- varsayılana dön
  else
    insert into public.core_edits(word, op, updated_at, updated_by) values (p_word, sign(p_op), now(), auth.uid())
    on conflict (word) do update set op = excluded.op, updated_at = now(), updated_by = auth.uid();
  end if;
end $$;
grant execute on function public.admin_set_core(text, int) to authenticated;
