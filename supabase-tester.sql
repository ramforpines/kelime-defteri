-- Beta erişimi: yöneticiler ve "Test eden yapımcı" flaması (user_flags.flag = 'maker') olan kullanıcılar
-- normal adresten girince en güncel (beta/) sürüme yönlendirilir. Ayrı bir rol yok; yönetim panelinden flamayı vermek yeterli.
-- (Daha önce bu dosyanın eski hâlini çalıştırdıysan oluşan beta_testers tablosu aşağıda silinir.)
drop table if exists public.beta_testers;

create or replace function public.is_beta() returns boolean
language sql security definer stable set search_path = public as $$
  select exists(select 1 from public.admins where user_id = auth.uid())
      or exists(select 1 from public.user_flags where user_id = auth.uid() and flag = 'maker');
$$;
revoke all on function public.is_beta() from public, anon;
grant execute on function public.is_beta() to authenticated;

-- kontrol: beta sürümü görecek yönetici olmayan kullanıcılar
select p.username from public.user_flags f join public.profiles p on p.user_id = f.user_id where f.flag = 'maker';
