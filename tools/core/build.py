"""Çekirdek liste (Odak modu): B1–B2 ağırlıklı ~3.500 kayıt.
Ölçütler: wordfreq sıklığı, sınav metinlerinde geçme, kelime ailesi (türev tekrarını at), AmE/BrE çiftleri.
Çıktı: core.js -> window.CORE=[kelime,...] (sıra = öğrenme sırası)."""
import json,os,re,subprocess
from wordfreq import zipf_frequency as Z
ROOT=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
W=json.loads(subprocess.check_output(['node','-e',"global.window={};require('%s/words.js');process.stdout.write(JSON.stringify(window.WORDS))"%ROOT]))
def z(s):
    s=re.sub(r'\(.*?\)|\.\.\.|…|/\S+','',s).strip()
    v=Z(s,'en')
    if '-' in s:v-=1.2   # tireli birleşikler parçalarının sıklığını alır; olduğundan sık görünmesin
    return v
STOPP=set('a an the to of in on at by for with up down out off over about into onto away back around through be do have get go make take come put set one someone something yourself oneself sb sth it its your so as that what not like after see know time'.split())
def zm(s):   # kalıp sıklığı: içerik kelimelerinin en seyreği (kalıbı 'on to' gibi yalnız edatlar sık göstermesin)
    t=[x for x in re.findall(r"[a-z']+",re.sub(r'\(.*?\)','',s.lower())) if x not in STOPP]
    return min(Z(x,'en') for x in t) if t else 2.0
_ix=open(os.path.join(ROOT,'index.html'),encoding='utf8').read()   # uygulamanın sözlükten çıkardığı kelimeler (RMX: uluslararası/tanıdık, RMW: çok basit) çekirdeğe girmez
RMX=set(json.loads(re.search(r'const RMX=new Set\((\[.*?\])\)',_ix).group(1)));RMW=set(json.loads(re.search(r'const RMW=new Set\((\[.*?\])\)',_ix).group(1)))
W=[w for w in W if not ((w[7] in('A1','A2') and w[0] in RMW) or (w[0] in RMX and w[7] in('B1','B2','C1')))]
low={w[0].lower():w for w in W}
# sınav metinleri
st=open(os.path.join(ROOT,'sinav.js'),encoding='utf8').read()
SN={}
for t in re.findall(r"[A-Za-z][a-z]{2,}",st):t=t.lower();SN[t]=SN.get(t,0)+1
def insinav(w):
    if ' ' in w:return False
    forms=[w,w+'s',w+'es',w+'ed',w+'d',w+'ing',w[:-1]+'ing',w[:-1]+'ies' if w.endswith('y') else w]
    return sum(SN.get(f,0) for f in forms)>=2
# kelime ailesi / varyant: türev ya da çekimli biçimse ve kökü sözlükte daha düşük/aynı seviyedeyse at
LV=['A1','A2','B1','B2','C1','C2']
def base_of(w):
    c=[]
    if w.endswith('ly'):c+= [w[:-2],w[:-3]+'y' if w.endswith('ily') else None,w[:-2]+'e',w[:-4]+'le' if w.endswith('ably') or w.endswith('ibly') else None, w[:-4] if w.endswith('ally') else None]
    if w.endswith('ness'):c+=[w[:-4],w[:-5]+'y' if w.endswith('iness') else None]
    if w.endswith('ize'):c+=[w[:-3]+'ise']
    if w.endswith('ization'):c+=[w[:-7]+'isation']
    if w.endswith('or') and not w.endswith('ior'):c+=[w[:-2]+'our']
    if w.endswith('er') and len(w)>4:c+=[w[:-2]+'re'] if w[-3] in 'tb' else []
    return [x for x in c if x and len(x)>=4 and x in low and x!=w]
FORMS={}
for k in list(low):
    if ' ' in k:continue
    for suf,b in(('ing',''),('ing','e'),('ed',''),('ed','e'),('d','')):
        if k.endswith(suf) and len(k)>=len(suf)+2:
            r=k[:-len(suf)]+b
            if r in low and r!=k and ' ' not in r and len(r)>=(3 if b else 4):FORMS.setdefault(k,r)
for a,b in(('known','know'),('given','give'),('taken','take'),('done','do'),('gone','go'),('children','child'),('people','person'),('men','man'),('women','woman')):FORMS[a]=b
AME={'trash':'rubbish','garbage':'rubbish','elevator':'lift','apartment':'flat','truck':'lorry','gasoline':'petrol','faucet':'tap','drugstore':'chemist','candy':'sweets','cookie':'biscuit','sidewalk':'pavement','restroom':'toilet','railroad':'railway','zipper':'zip','closet':'wardrobe','someplace':'somewhere','mall':'shopping centre','vacation':'holiday','subway':'underground'}
def skip(w):
    k=w[0].lower()
    if k in AME and AME[k] in low:return 'ame'
    if re.search(r'^[-]|[-]$',k):return 'affix'
    if Z(k,'en')>=6.0:return 'temel'   # 'as, but, if, know' gibi en temel sözcükler zaten biliniyor
    if k in FORMS and FORMS[k] in low and low[FORMS[k]][7] in('A1','A2') and Z(k,'en')>=4.5 and not re.search(r'preposition|conjunction',str(w[3])):return 'form:'+FORMS[k]   # 'called, using, known': temel fiilin biçimi
    if k in FORMS and FORMS[k] in low and not re.search(r'adjective|noun|preposition|conjunction',str(w[3])) and k not in ('grind','bind','feed'):return 'form:'+FORMS[k]   # -ed/-ing sıfatları (bored, amazing) kalır
    for b in (base_of(k) if Z(k,'en')<3.8 or k.endswith('ly') else []):   # sık kullanılan -ness/-ize sözcükleri (awareness, weakness) kendi başına öğrenilir
        if LV.index(low[b][7])<=LV.index(w[7]):return 'family:'+b
    return None
single=[w for w in W if ' ' not in w[0].strip() and w[7] in('B1','B2','C1')]
picked=[];why={}
for lv,n,cut in(('B1',1290,None),('B2',1270,None),('C1',350,None)):
    L=[w for w in single if w[7]==lv and not skip(w)]
    L.sort(key=lambda w:-(z(w[0])+(0.6 if insinav(w[0].lower()) else 0)))
    top=L[:n]
    extra=[w for w in L[n:] if insinav(w[0].lower()) and lv!='C1'][:150]
    for w in top+extra:picked.append(w)
# kalıplar: B1–B2 phrasal verb / kolokasyon / kalıp; atasözü ve C1 deyim yok
MT={'phrasal verb':0.5,'collocation':0.2,'phrase':0.2,'idiom':-0.3,'preposition phrase':0.1,'adverb phrase':0.1,'adjective phrase':0.1}
multi=[w for w in W if ' ' in w[0].strip() and w[7] in('B1','B2') and w[3] in MT]
multi=[w for w in multi if zm(w[0])>2.0]
multi.sort(key=lambda w:-(zm(w[0])+MT[w[3]]+(0.5 if w[7]=='B1' else 0)))
picked+=multi[:600]
# sıra: B1 → B2 → C1, her seviyede tek kelimeler önce sık olan, kalıplar araya serpiştirilir
order={'B1':0,'B2':1,'C1':2}
seen=set();out=[]
for lv in('B1','B2','C1'):   # her seviyede kelimeler sıklığa göre, kalıplar orantılı aralıklarla serpiştirilir
    ws=sorted({w[0]:w for w in picked if w[7]==lv and ' ' not in w[0].strip()}.values(),key=lambda w:-z(w[0]))
    ps=sorted({w[0]:w for w in picked if w[7]==lv and ' ' in w[0].strip()}.values(),key=lambda w:-zm(w[0]))
    tot=len(ws)+len(ps);i=j=0
    for k in range(tot):
        if j<len(ps) and (i>=len(ws) or (j+1)/len(ps)<=(k+1)/tot):w=ps[j];j+=1
        else:w=ws[i];i+=1
        if w[0] not in seen:seen.add(w[0]);out.append(w[0])
open(os.path.join(ROOT,'core.js'),'w',encoding='utf8').write('/* Çekirdek liste (Odak modu). tools/core/build.py ile üretilir; elle düzenleme. */\nwindow.CORE='+json.dumps(out,ensure_ascii=False,separators=(',',':'))+';\n')
import collections
c=collections.Counter((low[x.lower()][7],' ' in x) for x in out)
print(len(out),dict(c))
