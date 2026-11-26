-- Dosya: supabase-pl.sql
-- Kelime Defteri: seviye tespit sınavı sonuçları (soruların zorluğunu gerçek cevaplarla ayarlamak için). SQL Editor'da bir kez çalıştır.
create table if not exists public.pl_runs(
  user_id uuid not null default auth.uid(),
  rid text not null,                       -- sınav kimliği
  data jsonb not null,                     -- cevaplar (soru kimliği, doğru/yanlış), sonuç, bildirilen gerçek seviye
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  primary key (user_id, rid)
);
alter table public.pl_runs enable row level security;
drop policy if exists pl_runs_ins on public.pl_runs;
create policy pl_runs_ins on public.pl_runs for insert to authenticated with check (user_id = auth.uid());
drop policy if exists pl_runs_upd on public.pl_runs;
create policy pl_runs_upd on public.pl_runs for update to authenticated using (user_id = auth.uid()) with check (user_id = auth.uid());
drop policy if exists pl_runs_sel on public.pl_runs;
create policy pl_runs_sel on public.pl_runs for select to authenticated using (user_id = auth.uid() or public.is_admin());

-- yönetici: tüm sınavları tek seferde al (kalibrasyon için Claude'a yapıştırılır)
create or replace function public.admin_pl_runs()
returns jsonb language plpgsql security definer set search_path = public as $$
begin
  if not public.is_admin() then raise exception 'not allowed'; end if;
  return coalesce((select jsonb_agg(jsonb_build_object('u', left(md5(user_id::text), 8), 'rid', rid, 'at', created_at, 'd', data) order by created_at) from public.pl_runs), '[]'::jsonb);
end $$;
grant execute on function public.admin_pl_runs() to authenticated;
