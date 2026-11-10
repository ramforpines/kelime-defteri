/* Kelime Defteri service worker.
   d/ klasöründeki parçalar içerik adreslidir (adında içeriğin özeti var): bir kez indirilir, sonra hep önbellekten gelir (ağa gidilmez).
   Güncellemede yalnızca adı değişen (içeriği değişen) parçalar indirilir; sayfa güncel listeyi gönderince eskiler silinir.
   Diğer dosyalar (index.html vb.): önce ağ, olmazsa önbellek. */
const CACHE='kd-cache-v1',DCACHE='kd-data-v1';
const CORE=['./','index.html','manifest.webmanifest','icon-192.png','duel-swords.svg','duel-nav.svg','icon-512.png','apple-touch-icon.png'];
self.addEventListener('install',e=>{
  e.waitUntil(caches.open(CACHE).then(c=>c.addAll(CORE)).catch(()=>{}).then(()=>self.skipWaiting()));
});
self.addEventListener('activate',e=>{
  e.waitUntil(caches.keys().then(ks=>Promise.all(ks.filter(k=>k!==CACHE&&k!==DCACHE).map(k=>caches.delete(k)))).then(()=>caches.open(CACHE)).then(c=>c.keys().then(rs=>Promise.all(rs.filter(r=>/\.js(\?|$)/.test(r.url)&&!/\/sw\.js/.test(r.url)).map(r=>c.delete(r))))).then(()=>self.clients.claim()));   // eski tam boy veri dosyalarını önbellekten çıkar
});
self.addEventListener('message',e=>{
  const keep=e.data&&e.data.keep;if(!Array.isArray(keep)||!keep.length)return;
  const K=new Set(keep);
  e.waitUntil(caches.open(DCACHE).then(c=>c.keys().then(rs=>Promise.all(rs.filter(r=>!K.has(r.url)).map(r=>c.delete(r))))));
});
self.addEventListener('fetch',e=>{
  const req=e.request;
  if(req.method!=='GET')return;
  const url=new URL(req.url);
  const sameOrigin=url.origin===location.origin;
  const font=/fonts\.(googleapis|gstatic)\.com$/.test(url.hostname);
  if(!sameOrigin&&!font)return;   // Supabase istekleri doğrudan ağa gider
  if(font||(sameOrigin&&/\/d\/[^/]+-[0-9a-f]{10}\.js$/.test(url.pathname))){   // değişmez dosyalar: önce önbellek
    const C=font?CACHE:DCACHE;
    e.respondWith(caches.open(C).then(c=>c.match(req).then(hit=>hit||fetch(req).then(res=>{if(res&&res.ok)c.put(req,res.clone());return res}))));
    return;
  }
  e.respondWith(
    fetch(req,{cache:'no-cache'}).then(res=>{
      if(res&&res.ok){const cp=res.clone();caches.open(CACHE).then(c=>c.put(req,cp))}
      return res;
    }).catch(()=>caches.match(req).then(hit=>hit||caches.match('index.html')))
  );
});
