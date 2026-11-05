#!/usr/bin/env python3
"""Kalıplar bölümünü doğrular, her kalıp için test soruları üretir ve ../../phrases.js dosyasını yazar.
Kullanım: python3 build.py
Kaynak: src/<grup>.py (GROUP) ve src/<grup>_dlg.py (D: her kalıp için diyalog).
Her kalıba 5–6 soru: 0 anlam (İng→Tr), 1 Tr→İng, 2 tutum, 3 örnek cümlede boşluk, 4 diyalog, 5 üslup (resmî / samimi kalıplarda).
Yanlış şıklar, anlamca yakın gruplardan (ör. tamamen ↔ kısmen katılma) ve seviyesi yakın kalıplardan seçilir."""
import os,re,json,glob,importlib.util,random
HERE=os.path.dirname(os.path.abspath(__file__));ROOT=os.path.abspath(os.path.join(HERE,'..','..'))
LV=['A1','A2','B1','B2','C1','C2'];REG={'','resmî','samimi'};errs=[];groups=[]
def load(f,name):
    sp=importlib.util.spec_from_file_location(os.path.basename(f)[:-3],f);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m);return getattr(m,name)
# anlamca yakın gruplar (çeldirici kaynağı)
NEAR={'give':['ask','unsure','partly'],'ask':['give','unsure'],'agree':['partly','unsure','polite'],'partly':['agree','polite','unsure'],
      'polite':['partly','unsure','agree'],'strong':['agree','unsure','partly'],'unsure':['agree','ask']}
FUNC={'give':'Fikrini söylemek','ask':'Karşındakinin fikrini sormak','agree':'Tamamen katılmak','partly':'Kısmen katılmak','polite':'Kibarca katılmamak','strong':'Kesinlikle katılmamak','unsure':'Kararsız olmak'}
def core(en):
    c=re.sub(r'\(([^)]*)\)',r'\1',en).replace('...','').strip()
    c=re.sub(r'\s+',' ',c).strip()
    return c
def fill(line,en):
    c=core(en)
    if en.strip().endswith('...') or en.strip().endswith('...?'):c=c.rstrip('?').strip()
    return line.replace('___',c)
def opts(rng,right,pool,k=2):
    pool=[x for x in pool if x!=right];rng.shuffle(pool);out=[]
    for x in pool:
        if x not in out:out.append(x)
        if len(out)==k:break
    o=[right]+out;rng.shuffle(o);return o
for f in sorted(glob.glob(os.path.join(HERE,'src','*.py'))):
    if f.endswith('_dlg.py'):continue
    G=load(f,'GROUP');dlg=load(f[:-3]+'_dlg.py','D')
    allp=[];seen=set()
    for s in G['sub']:
        for p in s['items']:
            p['cat']=s['k']
            if p['lv'] not in LV:errs.append('seviye '+p['en'])
            if p['reg'] not in REG:errs.append('üslup '+p['en'])
            if p['en'].lower() in seen:errs.append('tekrar '+p['en'])
            seen.add(p['en'].lower());allp.append(p)
    by={}
    for p in allp:by.setdefault(p['cat'],[]).append(p)
    nq=0
    for i,p in enumerate(allp):
        rng=random.Random(G['id']+'|'+p['en']);li=LV.index(p['lv'])
        near=[q for c in NEAR[p['cat']] for q in by[c]]
        near.sort(key=lambda q:(abs(LV.index(q['lv'])-li),rng.random()))
        cand=near[:8]
        isopen=lambda q:'...' in q['en']
        same=[q for q in near if isopen(q)==isopen(p)][:8]
        if isopen(p) and p['cat'] in('partly','polite'):
            # "..., but" ve "With all due respect," kalıplarında görüş bildiren açık kalıplar da cümleye uyabilir; çift doğruyu önlemek için soru kalıpları kullanılır
            same=sorted([q for q in by['ask'] if isopen(q)],key=lambda q:(abs(LV.index(q['lv'])-li),rng.random()))
        elif len(same)<4:
            same=sorted([q for q in allp if isopen(q)==isopen(p) and q['cat']!=p['cat']],key=lambda q:(abs(LV.index(q['lv'])-li),rng.random()))[:8]
        Q=[]
        # 0 anlam
        o=opts(rng,p['tr'],[q['tr'] for q in cand]);Q.append({'f':0,'q':'“%s” ne anlama gelir?'%p['en'],'o':o,'a':o.index(p['tr']),'e':'“%s” = %s'%(p['en'],p['tr'])})
        # 1 Türkçeden İngilizceye
        o=opts(rng,p['en'],[q['en'] for q in cand]);Q.append({'f':1,'q':'“%s” demek için hangisini kullanırsın?'%p['tr'],'o':o,'a':o.index(p['en']),'e':'“%s” = %s'%(p['en'],p['tr'])})
        # 2 tutum
        fs=[FUNC[c] for c in NEAR[p['cat']]];o=opts(rng,FUNC[p['cat']],fs);Q.append({'f':2,'q':'“%s” diyen kişi ne yapıyor?'%p['en'],'o':o,'a':o.index(FUNC[p['cat']]),'e':'“%s”: %s.'%(p['en'],FUNC[p['cat']].lower())})
        # 3 örnek cümlede boşluk (Türkçesi ipucu)
        c=core(p['en']).rstrip('?.!');ex=p['ex'][0];m=re.search(re.escape(c),ex,re.I)
        if m:
            sent=ex[:m.start()]+'___'+ex[m.end():]
            cc=[core(q['en']).rstrip('?.!') for q in same if core(q['en']).rstrip('?.!').lower()!=c.lower()]
            if m.start()>0 and re.search(r'[a-z,] $',ex[:m.start()]):cc=[x[0].lower()+x[1:] if not x.startswith('I ') and not x.startswith("I'") else x for x in cc]
            right=ex[m.start():m.end()];o=opts(rng,right,cc)
            Q.append({'f':3,'q':'Boşluğa hangisi gelir?\n%s\n(Türkçesi: %s)'%(sent,p['ex'][1]),'o':o,'a':o.index(right),'e':'%s → %s'%(ex,p['ex'][1])})
        else:errs.append('örnekte kalıp yok: '+p['en']+' | '+ex)
        # 4 diyalog
        d=dlg.get(p['en'])
        if not d:errs.append('diyalog yok: '+p['en'])
        else:
            a,b=d;right=fill('___',p['en'])
            co=[fill('___',q['en']) for q in same]
            text='A: %s\nB: %s'%(a,b);o=opts(rng,right,co)
            Q.append({'f':4,'q':'Diyalogda boşluğa hangisi gelir?\n'+text,'o':o,'a':o.index(right),'e':'A: %s\nB: %s'%(fill(a,p['en']) if '___' in a else a,fill(b,p['en']) if '___' in b else b)})
        # 5 üslup
        if p['reg']:
            other=[q for q in by[p['cat']]+cand if q['reg']!=p['reg'] and q['en']!=p['en']]
            o=opts(rng,p['en'],[q['en'] for q in other])
            soru='Hangisi daha resmî bir ifadedir (iş, toplantı, yazı)?' if p['reg']=='resmî' else 'Hangisi arkadaşlar arasında kullanılan samimi bir ifadedir?'
            Q.append({'f':5,'q':soru,'o':o,'a':o.index(p['en']),'e':'“%s” %s bir ifadedir.'%(p['en'],p['reg'])})
        for q in Q:
            if len(set(q['o']))!=len(q['o']) or len(q['o'])<3:errs.append('şık sorunu: %s f%d %s'%(p['en'],q['f'],q['o']))
        p['qs']=Q;nq+=len(Q)
    print(G['id'],len(allp),'kalıp',nq,'soru')
    q=[]
    for i,(sit,ok,wr,why,lv) in enumerate(G['quiz']):
        o=[ok]+wr;random.Random(G['id']+str(i)).shuffle(o)
        q.append({'q':sit,'o':o,'a':o.index(ok),'e':why,'lv':lv})
    G['quiz']=q;groups.append(G)
if errs:print('\n'.join('HATA: '+e for e in errs));raise SystemExit(1)
PLAN=['Öneri yapma','Rica ve izin','Teşekkür ve özür','Konuşmayı yönetme','Açıklama isteme','Karşılaştırma ve zıtlık','Tahmin ve olasılık','Tavsiye ve uyarı','Duygu belirtme','Tebrik ve iyi dilekler','Telefon ve e-posta','Yazmada sonuç cümleleri']
open(os.path.join(ROOT,'phrases.js'),'w',encoding='utf8').write('/* Kalıplar (beta). tools/phrases/build.py ile üretilir; elle düzenleme. */\nwindow.PHRASES='+json.dumps(groups,ensure_ascii=False,separators=(',',':'))+';\nwindow.PHRASES_PLAN='+json.dumps(PLAN,ensure_ascii=False)+';\n')
print('tamam')
