#!/usr/bin/env python3
"""Parçalı, içerik adresli veri dosyaları üretir (d/ klasörü) ve index.html'deki betik bloğunu günceller.
Amaç: güncellemede kullanıcı yalnızca DEĞİŞEN parçaları indirsin. Dosya adı içeriğin özetini taşır (d/w03-1a2b3c4d.js);
içerik değişmezse ad da değişmez ve service worker onu önbellekten verir (ağa hiç gitmez).
- words.js: sırası korunarak 1000'er satırlık parçalara bölünür (yeni kelimeler sona eklendiği için çoğu zaman yalnız son parça değişir).
- examples.js / senses.js / extr.js: anahtarın özetine göre 16 kovaya bölünür (bir kelimenin değişmesi yalnız kendi kovasını etkiler).
- Diğer betikler (grammar, reading..., phrases, sinav) özetli adla kopyalanır.
Kaynak dosyalar (words.js vb.) olduğu gibi kalır; araçlar onları düzenlemeye devam eder. Kullanım: python3 tools/release/assets.py"""
import os,re,json,hashlib,glob
ROOT=os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','..'));D=os.path.join(ROOT,'d')
os.makedirs(D,exist_ok=True)
H=lambda b:hashlib.sha1(b).hexdigest()[:10]
made=[]
def put(stem,text):
    b=text.encode('utf8');name='%s-%s.js'%(stem,H(b));p=os.path.join(D,name)
    if not os.path.exists(p):open(p,'wb').write(b)
    made.append(name);return 'd/'+name
import subprocess
def load_globals():   # kaynakları index.html'deki sırayla node'da çalıştırıp pencere nesnelerini al (examples.js EXTR'ye de ekler)
    js="global.window={};for(const f of ['words.js','extr.js','examples.js','senses.js'])require(process.argv[1]+'/'+f);process.stdout.write(JSON.stringify({W:window.WORDS,X:window.EXTR,E:window.EXS,S:window.SENSES}))"
    return json.loads(subprocess.run(['node','-e',js,ROOT],capture_output=True,check=True).stdout)
G=load_globals()
tags=[]
# 1) kelimeler: sıra korunur
W=G['W'];N=1000
for i in range(0,len(W),N):
    tags.append(put('w%02d'%(i//N),'(window.WORDS=window.WORDS||[]).push.apply(window.WORDS,'+json.dumps(W[i:i+N],ensure_ascii=False,separators=(',',':'))+');\n'))
# 2) sözlük tipindeki veriler: 16 kova
def buckets(o,var,stem,k=16):
    B=[dict() for _ in range(k)]
    for key,v in o.items():B[int(hashlib.md5(key.encode('utf8')).hexdigest(),16)%k][key]=v
    return [put('%s%02d'%(stem,i),'Object.assign(window.%s=window.%s||{},%s);\n'%(var,var,json.dumps(b,ensure_ascii=False,separators=(',',':')))) for i,b in enumerate(B)]
# 3) betikleri özetli adla kopyala
def copy(path):return put(os.path.basename(path)[:-3],open(os.path.join(ROOT,path),encoding='utf8').read())
ORDER=['grammar.js','extr.js','examples.js','senses.js','reading.js','reading-tr.js','reading2.js','reading3.js','reading4.js','reading-fix.js','gloss.js','exam.js','mock.js','supabase.js']
for f in ORDER:
    if f=='extr.js':tags+=buckets(G['X'],'EXTR','x')   # extr.js + examples.js içindeki ek EXTR girdileri birleşik
    elif f=='examples.js':tags+=buckets(G['E'],'EXS','e')
    elif f=='senses.js':tags+=buckets(G['S'],'SENSES','s')
    else:tags.append(copy(f))
lazy={f:copy(f) for f in ['phrases.js','sinav.js']}
# eski parçaları sil (kaynaklar duruyor; bunlar yeniden üretilebilir kopyalardır)
for p in glob.glob(os.path.join(D,'*.js')):
    if os.path.basename(p) not in made:os.remove(p)
blk='<!--ASSETS: tools/release/assets.py üretir, elle düzenleme-->\n'+''.join('<script src="%s"></script>\n'%t for t in tags)+'<script>window.ASSET=%s;</script>\n<!--/ASSETS-->'%json.dumps(lazy)
ip=os.path.join(ROOT,'index.html');s=open(ip,encoding='utf8').read()
if '<!--ASSETS' in s:s=re.sub(r'<!--ASSETS.*?<!--/ASSETS-->',lambda m:blk,s,flags=re.S)
else:
    a=s.index('<script src="words.js"></script>');b=s.index('<script src="supabase.js"></script>')+len('<script src="supabase.js"></script>')
    s=s[:a]+blk+s[b:]
open(ip,'w',encoding='utf8').write(s)
tot=sum(os.path.getsize(os.path.join(D,n)) for n in made)
print('parça: %d dosya, %d KB'%(len(made),tot//1024))
