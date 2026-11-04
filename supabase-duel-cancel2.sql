-- Düello aramasından güvenli çıkış (4.152.2)
-- Sorun: kullanıcı "bot ile oyna"ya bastığında ya da arama süresi dolup lobiye döndüğünde,
-- aynı anda karşı taraf onu eşleştirmişse sunucuda gerçek maç kuruluyor ama bu kullanıcı
-- botla oynuyor / lobide kalıyordu (karşı taraf boş rakiple oynuyordu).
-- Çözüm: sıradan çıkarken, bu arada kurulmuş aktif maç varsa onun id'si döner; uygulama oyuncuyu o maça alır.
-- Eşleştirme kuyruk satırını "for update" ile kilitlediği için silme işlemi eşleştirmeyle sıraya girer:
-- ya eşleşme önce biter (maç id'si döner) ya da kullanıcı kuyruktan çıkar (bir daha eşleşmez).

create or replace function public.duel_cancel2() returns uuid
language plpgsql security definer set search_path = public as $$
declare uid uuid := auth.uid(); did uuid;
begin
  if uid is null then return null; end if;
  delete from public.duel_queue where user_id = uid;
  select id into did from public.duels
   where status = 'active' and (p1 = uid or p2 = uid)
   order by created_at desc limit 1;
  return did;
end $$;
revoke all on function public.duel_cancel2() from public, anon;
grant execute on function public.duel_cancel2() to authenticated;
