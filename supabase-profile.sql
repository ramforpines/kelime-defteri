-- Dosya: supabase-profile.sql
-- Kelime Defteri: avatar, çerçeve ve rozetlerin liderlik tablosunda görünmesi. SQL Editor'da bir kez çalıştır.
alter table public.scores add column if not exists av int not null default 0 check (av between 0 and 99);
alter table public.scores add column if not exists fr text not null default '' check (char_length(fr) <= 12);
alter table public.scores add column if not exists bd text not null default '' check (char_length(bd) <= 300);
