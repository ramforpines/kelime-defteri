"""Kullanım kalıpları: src.txt -> pat.js. Satır: kelime | kalıp | Türkçe | örnek {doğru|yanlış|yanlış|yanlış}"""
import json,os,re
H=os.path.dirname(os.path.abspath(__file__));ROOT=os.path.dirname(os.path.dirname(H))
P={}
for i,l in enumerate(open(os.path.join(H,'src.txt'),encoding='utf8')):
    l=l.strip()
    if not l or l.startswith('#'):continue
    w,pat,tr,ex=[x.strip() for x in l.split('|',3)]
    m=re.search(r'\{([^}]*)\}',ex);assert m and ex.count('{')==1,('örnek',i+1,l)
    o=m.group(1).split('|');assert len(o)==4 and len(set(o))==4,('şık',i+1,l)
    P.setdefault(w,[]).append([pat,tr,ex])
open(os.path.join(ROOT,'pat.js'),'w',encoding='utf8').write('/* Kullanım kalıpları. tools/pat/build.py ile üretilir (kaynak: tools/pat/src.txt). Örnekte {doğru|yanlış|yanlış|yanlış}. */\nwindow.PAT='+json.dumps(P,ensure_ascii=False,separators=(',',':'))+';\n')
print(len(P),'kelime',sum(len(v) for v in P.values()),'kalıp')
