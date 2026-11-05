#!/usr/bin/env python3
"""Kalıplar bölümünü doğrular ve ../../phrases.js dosyasını yazar. Kullanım: python3 build.py"""
import os,json,glob,importlib.util,random
HERE=os.path.dirname(os.path.abspath(__file__));ROOT=os.path.abspath(os.path.join(HERE,'..','..'))
LV=['A1','A2','B1','B2','C1','C2'];REG={'','resmî','samimi'};errs=[];groups=[]
for f in sorted(glob.glob(os.path.join(HERE,'src','*.py'))):
    sp=importlib.util.spec_from_file_location(os.path.basename(f)[:-3],f);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m);G=m.GROUP
    seen=set();cnt={l:0 for l in LV}
    for s in G['sub']:
        for p in s['items']:
            if p['lv'] not in LV:errs.append('seviye '+p['en'])
            if p['reg'] not in REG:errs.append('üslup '+p['en'])
            if p['en'].lower() in seen:errs.append('tekrar '+p['en'])
            seen.add(p['en'].lower());cnt[p['lv']]+=1
            if not p['tr'] or not all(p['ex']):errs.append('eksik '+p['en'])
    print(G['id'],sum(cnt.values()),'kalıp',cnt)
    q=[]
    for i,(sit,ok,wr,why,lv) in enumerate(G['quiz']):
        o=[ok]+wr;random.Random(G['id']+str(i)).shuffle(o)
        if len(set(o))!=len(o):errs.append('şık tekrarı '+sit)
        q.append({'q':sit,'o':o,'a':o.index(ok),'e':why,'lv':lv})
    G['quiz']=q;groups.append(G)
if errs:print('\n'.join('HATA: '+e for e in errs));raise SystemExit(1)
PLAN=['Öneri yapma','Rica ve izin','Teşekkür ve özür','Konuşmayı yönetme','Açıklama isteme','Karşılaştırma ve zıtlık','Tahmin ve olasılık','Tavsiye ve uyarı','Duygu belirtme','Tebrik ve iyi dilekler','Telefon ve e-posta','Yazmada sonuç cümleleri']
open(os.path.join(ROOT,'phrases.js'),'w',encoding='utf8').write('/* Kalıplar (beta). tools/phrases/build.py ile üretilir; elle düzenleme. */\nwindow.PHRASES='+json.dumps(groups,ensure_ascii=False,separators=(',',':'))+';\nwindow.PHRASES_PLAN='+json.dumps(PLAN,ensure_ascii=False)+';\n')
print('tamam')
