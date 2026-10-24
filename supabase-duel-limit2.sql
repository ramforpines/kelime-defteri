-- Dosya: supabase-duel-limit2.sql
-- Kelime Defteri: aynı rakiple 24 saatlik dereceli maç sınırı GERÇEK (etkin) lige göre.
-- Önceki sürüm yalnızca puan ligine bakıyordu: dereceli galibiyet şartını sağlamayan (gerçek ligi altın olan) ama puanı platin olan biri platin sınırına (2) takılıyordu.
-- Şimdi her iki oyuncunun etkin ligi (puan ligi ile galibiyet şartının düşüğü, duel_elg) alınır, yükseği geçerlidir:
--   Altın ve altı: 3 maç, Platin ve Zümrüt: 2 maç, Elmas ve üstü: 1 maç.
-- SQL Editor'da bir kez çalıştırın (tekrar çalıştırmak zararsızdır). Önce supabase-duel-limit.sql çalıştırılmış olmalı.

create or replace function public.duel_pair_ok(a uuid, b uuid) returns boolean language sql stable security definer set search_path = public as $$
  select count(*) < (
    case
      when greatest(public.duel_elg(a), public.duel_elg(b)) >= 6 then 1
      when greatest(public.duel_elg(a), public.duel_elg(b)) >= 4 then 2
      else 3 end)
  from public.duels d
  where d.mode = 'ranked' and d.status in ('active', 'done') and d.created_at > now() - interval '24 hours'
    and ((d.p1 = a and d.p2 = b) or (d.p1 = b and d.p2 = a))
$$;
revoke all on function public.duel_pair_ok(uuid, uuid) from public, anon, authenticated;
