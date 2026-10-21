-- Dosya: supabase-duel-duzelt.sql
-- Tek seferlik düzeltme: BOZDOĞAN - ÇETİNER arasındaki SON dereceli maç iptal edilir, iki oyuncunun o maçtan gelen puanı geri alınır
-- (maç öncesi hale döner), sonra ikisine de 50 puan verilir. Kullanıcılar uygulamayı açınca puan düzeltmesi bildirimini görür.
-- Önce supabase-duel-ceza.sql ve supabase-duel-recalc.sql çalışmış olmalı. ÖNCE YEDEK ALIN. Yalnızca BİR KEZ çalıştırın.
-- Sonuç olarak tek satır döner (maç, durum, iki oyuncunun farkı). Maç bulunamazsa ya da isimler birden fazla kişiyle eşleşirse hata verir ve hiçbir şey değiştirmez.

alter table public.duel_recalc add column if not exists note text;

create or replace function public.duel_recalc_pull() returns jsonb
language sql stable security definer set search_path = public as $$
  select coalesce(jsonb_agg(jsonb_build_object('id', duel_id, 'delta', delta, 'done_at', done_at, 'note', note) order by created_at), '[]'::jsonb)
  from public.duel_recalc where user_id = auth.uid() and not acked
$$;
revoke all on function public.duel_recalc_pull() from public, anon;
grant execute on function public.duel_recalc_pull() to authenticated;

do $$
declare d public.duels; ua uuid; ub uuid; na text; nb text; cnt int;
        o1 numeric; o2 numeric; note1 text := 'Uygulamanın kapatılması sırasında bozulan dereceli maçın puanları geri alındı ve özür olarak 50 puan eklendi.';
begin
  select count(distinct s.user_id) into cnt from public.scores s where s.name ilike '%bozdo%';
  if cnt <> 1 then raise exception 'BOZDOĞAN % kişiyle eşleşti, işlem durduruldu', cnt; end if;
  select s.user_id, s.name into ua, na from public.scores s where s.name ilike '%bozdo%' limit 1;
  select count(distinct s.user_id) into cnt from public.scores s where s.name ilike '%et%' and s.name ilike '%ner%' and s.user_id <> ua
    and exists (select 1 from public.duels x where x.mode = 'ranked' and ((x.p1 = ua and x.p2 = s.user_id) or (x.p2 = ua and x.p1 = s.user_id)));
  if cnt <> 1 then raise exception 'ÇETİNER % kişiyle eşleşti, işlem durduruldu', cnt; end if;
  select s.user_id, s.name into ub, nb from public.scores s where s.name ilike '%et%' and s.name ilike '%ner%' and s.user_id <> ua
    and exists (select 1 from public.duels x where x.mode = 'ranked' and ((x.p1 = ua and x.p2 = s.user_id) or (x.p2 = ua and x.p1 = s.user_id))) limit 1;

  select * into d from public.duels
   where mode = 'ranked' and ((p1 = ua and p2 = ub) or (p1 = ub and p2 = ua))
   order by created_at desc limit 1 for update;
  if not found then raise exception 'maç bulunamadı'; end if;

  o1 := coalesce(d.dl1, 0); o2 := coalesce(d.dl2, 0);
  -- maçın puan etkisini sıfırla
  update public.duels set winner = null, dl1 = 0, dl2 = 0, pen1 = 0, pen2 = 0, pen_rf = true, pen_ack = coalesce(pen_ack, now()),
         status = case when status in ('done', 'void') then status else 'void' end,
         done_at = coalesce(done_at, now())
   where id = d.id;
  delete from public.duel_bans where user_id in (ua, ub);
  insert into public.duel_penalties(user_id, duel_id, kind, pts, note, by_user)
    select u, d.id, 'admin_refund', 0, 'Bozulan maç düzeltmesi', auth.uid() from unnest(array[ua, ub]) u where d.status = 'void';

  -- maçtan gelen puanı geri al
  if d.status in ('done', 'void') then
    if d.p1 = ua then
      insert into public.duel_recalc(duel_id, user_id, old_dl, new_dl, delta, done_at, note) values (d.id, d.p1, o1, 0, -o1, d.done_at, note1)
        on conflict (duel_id, user_id) do update set new_dl = 0, delta = case when public.duel_recalc.acked then -o1 else public.duel_recalc.delta - o1 end, acked = false, note = note1;
      insert into public.duel_recalc(duel_id, user_id, old_dl, new_dl, delta, done_at, note) values (d.id, d.p2, o2, 0, -o2, d.done_at, note1)
        on conflict (duel_id, user_id) do update set new_dl = 0, delta = case when public.duel_recalc.acked then -o2 else public.duel_recalc.delta - o2 end, acked = false, note = note1;
    else
      insert into public.duel_recalc(duel_id, user_id, old_dl, new_dl, delta, done_at, note) values (d.id, d.p1, o1, 0, -o1, d.done_at, note1)
        on conflict (duel_id, user_id) do update set new_dl = 0, delta = case when public.duel_recalc.acked then -o1 else public.duel_recalc.delta - o1 end, acked = false, note = note1;
      insert into public.duel_recalc(duel_id, user_id, old_dl, new_dl, delta, done_at, note) values (d.id, d.p2, o2, 0, -o2, d.done_at, note1)
        on conflict (duel_id, user_id) do update set new_dl = 0, delta = case when public.duel_recalc.acked then -o2 else public.duel_recalc.delta - o2 end, acked = false, note = note1;
    end if;
    delete from public.duel_recalc where duel_id = d.id and delta = 0;
  end if;

  -- ikisine de 50 puan (ayrı satır: maç işlenmiş olsun olmasın uygulanır)
  insert into public.duel_recalc(duel_id, user_id, old_dl, new_dl, delta, done_at, note)
    values (gen_random_uuid(), ua, 0, 50, 50, null, note1), (gen_random_uuid(), ub, 0, 50, 50, null, note1);

  raise notice 'Düzeltilen maç: % (% - %), önceki durum: %, önceki fark: % / %', d.id, na, nb, d.status, o1, o2;
end $$;

select d.id, d.status, d.dl1, d.dl2, d.winner,
       (select string_agg(r.delta::text, ' / ' order by r.created_at) from public.duel_recalc r where r.duel_id = d.id) as geri_alinan,
       (select count(*) from public.duel_recalc r where r.note like 'Uygulamanın kapatılması%' and r.delta = 50 and not r.acked) as bekleyen_50
from public.duels d where d.mode = 'ranked' order by d.created_at desc limit 1;
