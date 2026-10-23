/* Kelime Defteri service worker: önce ağ, olmazsa önbellek. Yeni sürüm yüklenince kullanıcılar bir sonraki açılışta güncel dosyaları alır. */
const CACHE='kd-cache-v1';
const CORE=['./','index.html','words.js','extr.js','senses.js','gloss.js','reading.js','reading-tr.js','reading2.js','reading3.js','exam.js','mock.js','supabase.js','manifest.webmanifest','icon-192.png','duel-swords.svg','duel-nav.svg','icon-512.png','apple-touch-icon.png'];
self.addEventListener('install',e=>{
  e.waitUntil(caches.open(CACHE).then(c=>c.addAll(CORE)).then(()=>self.skipWaiting()));
});
self.addEventListener('activate',e=>{
  e.waitUntil(caches.keys().then(ks=>Promise.all(ks.filter(k=>k!==CACHE).map(k=>caches.delete(k)))).then(()=>self.clients.claim()));
});
self.addEventListener('fetch',e=>{
  const req=e.request;
  if(req.method!=='GET')return;
  const url=new URL(req.url);
  const sameOrigin=url.origin===location.origin;
  const font=/fonts\.(googleapis|gstatic)\.com$/.test(url.hostname);
  if(!sameOrigin&&!font)return;   // Supabase istekleri doğrudan ağa gider
  if(font){
    e.respondWith(caches.match(req).then(hit=>hit||fetch(req).then(res=>{const cp=res.clone();caches.open(CACHE).then(c=>c.put(req,cp));return res}).catch(()=>hit)));
    return;
  }
  e.respondWith(
    fetch(req,{cache:'no-cache'}).then(res=>{
      if(res&&res.ok){const cp=res.clone();caches.open(CACHE).then(c=>c.put(req,cp))}
      return res;
    }).catch(()=>caches.match(req).then(hit=>hit||caches.match('index.html')))
  );
});
