-- Yönetici için sohbet hız sınırı yok (genel dakikada 5, özel dakikada 60 sınırı yalnızca yönetici olmayanlara uygulanır).
-- supabase-security.sql çalıştırılmış olmalı (is_admin, chat_can_receive). SQL Editor'da bir kez çalıştırın.
drop policy if exists "chat_insert" on public.chat_messages;
create policy "chat_insert" on public.chat_messages for insert to authenticated
  with check (
    user_id = auth.uid() and public.is_approved() and not public.is_blocked(auth.uid())
    and (
      (to_user is null and (public.is_admin() or (select count(*) from public.chat_messages m
         where m.user_id = auth.uid() and m.to_user is null and m.created_at > now() - interval '1 minute') < 5))
      or
      (to_user is not null and public.chat_can_receive(to_user)
         and (public.is_admin() or (select count(*) from public.chat_messages m
         where m.user_id = auth.uid() and m.to_user is not null and m.created_at > now() - interval '1 minute') < 60))
    )
  );
