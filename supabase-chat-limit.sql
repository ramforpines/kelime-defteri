-- Dosya: supabase-chat-limit.sql
-- Kelime Defteri: sohbet hız sınırı + özel mesajda yöneticiye ve diğer kullanıcılara gönderme düzeltmesi. Genel sohbet: dakikada en fazla 5 mesaj. Özel mesajlarda sınır yok.
-- (supabase-chat.sql çalıştırılmış olmalı.) SQL Editor'da bir kez çalıştır.
-- Alıcı onaylı kullanıcı ya da yönetici mi? (profiles tablosu RLS ile gizli olduğu için güvenli fonksiyonla bakılır)
create or replace function public.chat_can_receive(uid uuid) returns boolean
language sql security definer stable set search_path = public as $$
  select coalesce((select approved from public.profiles where user_id = uid), false)
         or exists(select 1 from public.admins where user_id = uid)
$$;
grant execute on function public.chat_can_receive(uuid) to authenticated;

drop policy if exists "chat_insert" on public.chat_messages;
create policy "chat_insert" on public.chat_messages for insert to authenticated
  with check (
    user_id = auth.uid() and public.is_approved() and not public.is_blocked(auth.uid())
    and (
      (to_user is null and (select count(*) from public.chat_messages m
         where m.user_id = auth.uid() and m.to_user is null and m.created_at > now() - interval '1 minute') < 5)
      or
      (to_user is not null and public.chat_can_receive(to_user))
    )
  );
