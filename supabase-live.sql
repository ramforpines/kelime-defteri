-- Dosya: supabase-live.sql
-- Kelime Defteri: anlık duyuru (her ekranda açılan pencere). Yönetici Ben → Anlık duyuru sekmesinden yayınlar.
-- (Önce supabase-admin.sql çalıştırılmış olmalı.)
create table if not exists public.live_announcement (
  id int primary key default 1 check (id = 1),
  body text not null default '',
  updated_at timestamptz not null default now()
);
insert into public.live_announcement(id, body) values (1, '') on conflict do nothing;
alter table public.live_announcement enable row level security;
drop policy if exists "live_select" on public.live_announcement;
create policy "live_select" on public.live_announcement for select to authenticated using (public.is_approved());
revoke all on public.live_announcement from anon;

-- Yalnızca yönetici yazar. Her yayında updated_at yenilenir; böylece aynı metin tekrar yayınlanırsa herkese yeniden açılır.
create or replace function public.admin_set_live_announcement(msg text)
returns void language plpgsql security definer set search_path = public as $$
begin
  if not public.is_admin() then raise exception 'not allowed'; end if;
  update public.live_announcement set body = left(btrim(coalesce(msg, '')), 1500), updated_at = now() where id = 1;
end $$;
revoke all on function public.admin_set_live_announcement(text) from public, anon;
grant execute on function public.admin_set_live_announcement(text) to authenticated;
