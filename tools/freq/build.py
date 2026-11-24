"""Sözlük sıklık puanı: wordfreq (altyazı, haber, Wikipedia, kitap, web birleşik; günlük ve akademik dil birlikte).
Tek kelime: Zipf sıklığı. Kalıp/deyim: içerik kelimelerinin en seyreği (yalnız edatlar sık görünmesin) − 0,8.
Çıktı: freq.js -> window.FREQ={kelime: puan×100}"""
import json,os,re,subprocess
from wordfreq import zipf_frequency as Z
ROOT=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
W=json.loads(subprocess.check_output(['node','-e',"global.window={};require('%s/words.js');process.stdout.write(JSON.stringify(window.WORDS.map(w=>w[0])))"%ROOT]))
STOP=set('a an the to of in on at by for with up down out off over about into onto away back around through be do have get go make take come put set one someone something somebody sb sth yourself oneself your his her their its it so as that what not like'.split())
def score(w):
    k=re.sub(r'\(.*?\)','',w).strip()
    if re.fullmatch(r"-?[A-Za-z][A-Za-z'’]*-?",k):
        k=k.strip('-');v=Z(k,'en')
        if w.strip().startswith('-') or w.strip().endswith('-'):v=min(v,4.0)   # ön/son ek kayıtları
        return v
    t=[x for x in re.findall(r"[a-z']+",k.lower().replace('/',' ')) if x not in STOP]
    v=min(Z(x,'en') for x in t) if t else min(4.5,Z(k,'en')-1.5)   # yalnız edat/zamirden oluşan kalıplar (on and off) üste çıkmasın
    if '-' in k and ' ' not in k:v=Z(k,'en')-1.0
    return min(v,5.2)-0.8
F={}
for w in W:
    if w in F:continue
    F[w]=int(round(score(w)*100))
open(os.path.join(ROOT,'freq.js'),'w',encoding='utf8').write('/* Sözlük sıklık puanları (Zipf×100). tools/freq/build.py ile üretilir. */\nwindow.FREQ='+json.dumps(F,ensure_ascii=False,separators=(',',':'))+';\n')
top=sorted(F,key=lambda x:-F[x])
print(len(F),'ilk 40:',', '.join(top[:40]))
print('akademik örnek:',[(x,F.get(x)) for x in ['analysis','hypothesis','significant','data','research','methodology','furthermore','approach','concept','theory']])
