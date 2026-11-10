#!/usr/bin/env python3
"""Kalıplar bölümünü doğrular, her kalıp için test soruları üretir ve ../../phrases.js dosyasını yazar.
Kullanım: python3 build.py
Kaynak: src/<grup>.py (GROUP) ve src/<grup>_dlg.py (D: her kalıp için diyalog).
Her kalıba 5–6 İngilizce soru: 0 diyalog, 1 işlev etiketiyle boşluk, 2 işlev → kalıp, 3 kalıp → işlev, 4 yakın anlamlı kalıp, 5 üslup (resmî / samimi kalıplarda).
Yanlış şıklar, anlamca yakın gruplardan (ör. tamamen ↔ kısmen katılma) ve seviyesi yakın kalıplardan seçilir."""
import os,re,json,glob,importlib.util,random
HERE=os.path.dirname(os.path.abspath(__file__));ROOT=os.path.abspath(os.path.join(HERE,'..','..'))
LV=['A1','A2','B1','B2','C1','C2'];REG={'','resmî','samimi'};errs=[];groups=[];gseen=set()
def load(f,name):
    sp=importlib.util.spec_from_file_location(os.path.basename(f)[:-3],f);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m);return getattr(m,name)
# anlamca yakın gruplar (çeldirici kaynağı)
NEAR={'give':['ask','unsure','partly'],'ask':['give','unsure'],'agree':['partly','unsure','polite'],'partly':['agree','polite','unsure'],
      'polite':['partly','unsure','agree'],'strong':['agree','unsure','partly'],'unsure':['agree','ask'],
      'make':['accept','decline'],'accept':['decline','make'],'decline':['accept','make'],
      'sim':['con','deg','pre'],'con':['sim','deg','pre'],'deg':['sim','con','pre'],'pre':['sim','con','deg'],
      'cert':['poss','unlik'],'prob':['poss','unlik'],'poss':['cert','unlik'],'unlik':['cert','poss'],'guess':['cert','unlik'],
      'dask':['dgive','dcheck','dland'],'dgive':['dland','dask','dcheck'],'dland':['dgive','dask','dcheck'],'dcheck':['dask','dgive','dland'],
      'off':['offyes','offno','prom'],'offyes':['offno','off','prom'],'offno':['offyes','off','prom'],'prom':['off','offyes','offno']}
NOF1={'guess':['unlik'],'prob':['unlik']}  # boşluk sorusunda gramer olarak da uyabilecek çeldiricileri önler
FUNC_EN={'give':'giving an opinion','ask':'asking for an opinion','agree':'complete agreement','partly':'partial agreement','polite':'polite disagreement','strong':'strong disagreement','unsure':'being undecided',
        'make':'making a suggestion','accept':'accepting a suggestion','decline':'turning down a suggestion',
        'sim':'showing similarity','con':'showing contrast','deg':'comparing things','pre':'saying what you prefer',
        'cert':'being almost sure','prob':'saying something is probably true','poss':'saying something is only possible (not likely)','unlik':'saying something is unlikely','guess':'guessing from what you can see',
        'dask':'asking the way','dgive':'giving directions','dland':'describing where a place is','dcheck':'checking you understood the directions',
        'off':'offering to help','offyes':'accepting an offer','offno':'refusing an offer politely','prom':'making a promise'}
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
ORDER=['opinion','suggest','speculate','contrast','directions','offers']
for f in sorted(glob.glob(os.path.join(HERE,'src','*.py')),key=lambda x:ORDER.index(os.path.basename(x)[:-3]) if os.path.basename(x)[:-3] in ORDER else 99):
    if f.endswith('_dlg.py'):continue
    G=load(f,'GROUP');dlg=load(f[:-3]+'_dlg.py','D') if os.path.exists(f[:-3]+'_dlg.py') else {}
    allp=[];seen=set()
    for s in G['sub']:
        for p in s['items']:
            p['cat']=s['k']
            if p['lv'] not in LV:errs.append('seviye '+p['en'])
            if p['reg'] not in REG:errs.append('üslup '+p['en'])
            if p['en'].lower() in seen:errs.append('tekrar '+p['en'])
            if p['en'].lower() in gseen:errs.append('gruplar arası tekrar '+p['en'])
            gseen.add(p['en'].lower());seen.add(p['en'].lower());allp.append(p)
    var={}
    for p in allp:
        for v in (p['en'],core(p['en']),core(p['en']).rstrip('?.!').strip()):var[v.lower()]=p['en']
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
        if p['cat'] in NOF1:same=[q for c in NOF1[p['cat']] for q in by[c] if isopen(q)==isopen(p)][:8]
        if isopen(p) and p['cat'] in('partly','polite'):
            # "..., but" ve "With all due respect," kalıplarında görüş bildiren açık kalıplar da cümleye uyabilir; çift doğruyu önlemek için soru kalıpları kullanılır
            same=sorted([q for q in by['ask'] if isopen(q)],key=lambda q:(abs(LV.index(q['lv'])-li),rng.random()))
        elif len(same)<4:
            same=sorted([q for q in allp if isopen(q)==isopen(p) and q['cat']!=p['cat']],key=lambda q:(abs(LV.index(q['lv'])-li),rng.random()))[:8]
        Q=[]
        def add(f,q,o,right,e):Q.append({'f':f,'q':q,'o':o,'a':o.index(right),'e':e})
        # 0 diyalog
        d=p.get('d') or dlg.get(p['en'])
        if not d:errs.append('diyalog yok: '+p['en'])
        else:
            a,b=d[0],d[1];right=fill('___',p['en'])
            if len(d)==3:
                bad=[w for w in d[2] if w.lower() not in var]
                if bad:errs.append('diyalog çeldirici yok: %s | %s'%(p['en'],bad))
                pool=[fill('___',var[w.lower()]) for w in d[2] if w.lower() in var];o=[right]+pool;rng.shuffle(o)
            else:o=opts(rng,right,[fill('___',q['en']) for q in same])
            add(0,'Complete the dialogue.\nA: %s\nB: %s'%(a,b),o,right,'A: %s\nB: %s'%(fill(a,p['en']) if '___' in a else a,fill(b,p['en']) if '___' in b else b))
        # 1 örnek cümlede boşluk + işlev etiketi (İngilizce)
        c=core(p['en']).rstrip('?.!').strip();ex=p['ex'][0];m=re.search(re.escape(c),ex,re.I)
        if m:
            sent=ex[:m.start()]+'___'+ex[m.end():]
            cc=[core(q['en']).rstrip('?.!').strip() for q in same if core(q['en']).rstrip('?.!').lower()!=c.lower()]
            if m.start()>0 and re.search(r'[a-z,] $',ex[:m.start()]):cc=[x[0].lower()+x[1:] if not x.startswith('I ') and not x.startswith("I'") else x for x in cc]
            right=ex[m.start():m.end()];o=opts(rng,right,cc)
            add(1,'Complete the sentence (%s).\n%s'%(FUNC_EN[p['cat']],sent),o,right,ex)
        else:errs.append('örnekte kalıp yok: '+p['en']+' | '+ex)
        # 2 işlev → kalıp
        o=opts(rng,p['en'],[q['en'] for q in cand])
        add(2,'Which phrase do you use for %s?'%FUNC_EN[p['cat']],o,p['en'],'“%s” is used for %s.'%(p['en'],FUNC_EN[p['cat']]))
        # 3 kalıp → işlev
        fs=[FUNC_EN[c2] for c2 in NEAR[p['cat']]];o=opts(rng,FUNC_EN[p['cat']],fs)
        add(3,'What does “%s” express?'%p['en'],o,FUNC_EN[p['cat']],'“%s” is used for %s.'%(p['en'],FUNC_EN[p['cat']]))
        # 4 yakın anlam: aynı gruptan başka bir kalıp
        sib=[q for q in by[p['cat']] if q['en']!=p['en']];sib.sort(key=lambda q:(isopen(q)!=isopen(p),abs(LV.index(q['lv'])-li),rng.random()))
        if sib:
            right=sib[0]['en'];o=opts(rng,right,[q['en'] for q in cand if q['cat']!=p['cat']])
            add(4,'Which phrase is closest in meaning to “%s”?'%p['en'],o,right,'Both “%s” and “%s” are used for %s.'%(p['en'],right,FUNC_EN[p['cat']]))
        # 5 üslup
        if p['reg']:
            other=[q for q in by[p['cat']]+cand if q['reg']!=p['reg'] and q['en']!=p['en']]
            o=opts(rng,p['en'],[q['en'] for q in other])
            add(5,'Which phrase is the most formal?' if p['reg']=='resmî' else 'Which phrase is the most informal (used with friends)?',o,p['en'],'“%s” is %s.'%(p['en'],'formal' if p['reg']=='resmî' else 'informal'))
        for q in Q:
            if len(set(q['o']))!=len(q['o']) or len(q['o'])<3:errs.append('şık sorunu: %s f%d %s'%(p['en'],q['f'],q['o']))
        p['qs']=Q;nq+=len(Q)
    print(G['id'],len(allp),'kalıp',nq,'soru')
    q=[]
    for i,(sit,ok,wr,why,lv) in enumerate(G.get('quiz',[])):
        o=[ok]+wr;random.Random(G['id']+str(i)).shuffle(o)
        q.append({'q':sit,'o':o,'a':o.index(ok),'e':why,'lv':lv})
    G['quiz']=q;groups.append(G)
if errs:print('\n'.join('HATA: '+e for e in errs));raise SystemExit(1)
PLAN=['Restoranda sipariş','Plan yapma ve buluşma','Beğeni ve tercih','İlgi gösterme ve tepki','Başka sözcüklerle anlatma','Rica ve izin','Teşekkür ve özür','Konuşmayı yönetme','Açıklama isteme','Tavsiye ve uyarı','Duygu belirtme','Tebrik ve iyi dilekler','Telefon ve e-posta','Yazmada sonuç cümleleri']
open(os.path.join(ROOT,'phrases.js'),'w',encoding='utf8').write('/* Kalıplar (beta). tools/phrases/build.py ile üretilir; elle düzenleme. */\nwindow.PHRASES='+json.dumps(groups,ensure_ascii=False,separators=(',',':'))+';\nwindow.PHRASES_PLAN='+json.dumps(PLAN,ensure_ascii=False)+';\n')
print('tamam')
