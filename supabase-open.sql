-- Kelime Defteri: "liderlik tablosundan çıkarma" özelliği tamamen kaldırıldı + sohbette kullanıcı adıyla arama.
-- SQL Editor'a yapıştırıp bir kez çalıştır. (supabase-admin.sql, supabase-chat.sql ve supabase-theme.sql çalıştırılmış olmalı.)

-- 1) Tablodan çıkarılmış ya da gizlenmiş herkes geri alınır
update public.profiles set lb_blocked = false where lb_blocked;
update public.scores set hide = false where hide;

-- 2) Liderlik tablosunu onaylı herkes eksiksiz görür (gizleme/engelleme kuralı yok)
drop policy if exists "scores_select" on public.scores;
create policy "scores_select" on public.scores for select to authenticated
  using (public.is_approved());

-- 3) Yönetici "tablodan çıkar" fonksiyonu kaldırılır
drop function if exists public.admin_set_blocked(uuid, boolean);

-- 4) Sohbet kullanıcı araması: kullanıcı adına ve görünen ada göre, tüm onaylı kullanıcılar arasında
create or replace function public.chat_find_users(q text)
returns table(user_id uuid, username text, name text, color int, av int, fr text, ad boolean)
language plpgsql security definer stable set search_path = public as $$
declare k text := lower(btrim(replace(replace(coalesce(q, ''), '%', ''), '_', '\_')));
begin
  if not public.is_approved() then raise exception 'not allowed'; end if;
  if length(k) < 1 then return; end if;
  return query
    select p.user_id, p.username, coalesce(s.name, p.username)::text, coalesce(s.color, 0)::int, coalesce(s.av, 0)::int,
           coalesce(s.fr, '')::text, exists(select 1 from public.admins a where a.user_id = p.user_id)
    from public.profiles p
    left join public.scores s on s.user_id = p.user_id
    where p.user_id <> auth.uid()
      and (p.approved or exists(select 1 from public.admins a2 where a2.user_id = p.user_id))
      and (lower(p.username) like '%' || k || '%' or lower(coalesce(s.name, '')) like '%' || k || '%')
    order by (lower(p.username) = k) desc, p.username
    limit 15;
end $$;
revoke all on function public.chat_find_users(text) from public, anon;
grant execute on function public.chat_find_users(text) to authenticated;
