-- Kelime Defteri: sohbet hız sınırı. Genel sohbet: dakikada en fazla 5 mesaj. Özel mesajlarda sınır yok.
-- (supabase-chat.sql çalıştırılmış olmalı.) SQL Editor'da bir kez çalıştır.
drop policy if exists "chat_insert" on public.chat_messages;
create policy "chat_insert" on public.chat_messages for insert to authenticated
  with check (
    user_id = auth.uid() and public.is_approved() and not public.is_blocked(auth.uid())
    and (
      (to_user is null and (select count(*) from public.chat_messages m
         where m.user_id = auth.uid() and m.to_user is null and m.created_at > now() - interval '1 minute') < 5)
      or
      (to_user is not null and exists(select 1 from public.profiles p where p.user_id = to_user and p.approved))
    )
  );
