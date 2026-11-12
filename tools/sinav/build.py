#!/usr/bin/env python3
"""Seviye sınavlarını (A2 Key, B1 Preliminary, B2 First, C1 Advanced) ve çalışma bölümünü doğrular,
dinleme seslerini üretir (kokoro-onnx) ve ../../sinav.js dosyasını yazar.
Kullanım: python3 build.py [--no-audio]
Kaynak: src/<seviye>.py dosyaları EXAMS (liste) ve PRAC (sözlük: R, L, W, S listeleri) tanımlar.

Bölüm türleri (ty):
  mc     çoktan seçmeli. q:[{x? kısa metin, sc? ses, q, o, a, tg, e}], p? ortak metin (paragraf listesi), sc? ortak ses
  match  eşleştirme. opts:[[harf, başlık, metin?]], q:[{q, a:harf, tg, e}], p? ortak metin, sc? ortak ses
  gap    cümle/paragraf yerleştirme. p: '(1) ______' boşluklu metin, opts:[[harf, cümle]], a:[harf], tg, e
  cloze  çoktan seçmeli boşluk. p, o:[[seçenekler, doğru, tg]], e
  open   açık boşluk / not tamamlama / kelime türetme. p, a:[[kabul edilenler]], tg, e, st? (kök kelimeler), sc? ses
  kwt    anahtar kelimeyle dönüştürme. q:[{s1, key, s2 ('______' içerir), a:[...], tg, e}]
Yazma görevi: id, part, kind, t, in, mail, pts, min, max, model. Sınavda W.tasks: [görev, {'choice':[görev, görev, ...]}]
Konuşma bölümü: id, p, t, ins, img? [[emoji sahnesi, Türkçe açıklama]], opts? [seçenekler], q:[[soru, saniye, kalıplar, örnek cevap]]"""
import os,sys,json,glob,hashlib,re,subprocess,tempfile,importlib.util
HERE=os.path.dirname(os.path.abspath(__file__));ROOT=os.path.abspath(os.path.join(HERE,'..','..'))
sys.path.insert(0,HERE)
TTS=os.environ.get('KD_TTS','/tmp/claude-0/tts')
VOICE={'M':'bm_george','F':'bf_emma','M2':'bm_lewis','F2':'bf_isabella'}
errs=[];warn=[]
def E(m):errs.append(m)
gr=open(os.path.join(ROOT,'grammar.js'),encoding='utf8').read()
GIDS=set(re.findall(r'"id":"([a-z0-9-]+)","lv"',gr))
SKILL={'gist','detail','inference','attitude','purpose','vocab','spelling','reference','coherence','collocation','word-formation','transformation'}
def tags(t,P):
    if not t:E(P+': etiket yok');return
    for x in t:
        if x not in SKILL and x not in GIDS:E(P+': bilinmeyen etiket '+x)
audio=[]
def aud(owner,pid,sc,P):
    if not pid:E(P+': ses kimliği yok');return
    if not sc or any(len(x)!=2 or x[0] not in VOICE or not x[1].strip() for x in sc):E(P+': ses metni hatalı')
    audio.append((owner+'-'+pid,sc))
def gaps(txt,n,P):
    for i in range(1,n+1):
        if '(%d) ______'%i not in txt:E(P+': boşluk %d yok'%i)
    if '(%d) ______'%(n+1) in txt:E(P+': fazla boşluk')
def part(p,owner,P):
    ty=p.get('ty');P=P+'.'+str(p.get('k') or p.get('id'))
    for f in('k','nm','ins'):
        if not p.get(f):E(P+': '+f+' yok')
    txt=p.get('p');txt='\n'.join(txt) if isinstance(txt,list) else (txt or '')
    if p.get('sc') and not p.get('noaud'):aud(owner,p.get('id'),p['sc'],P)
    if ty=='mc':
        for i,q in enumerate(p['q']):
            n=len(q['o'])
            if n not in(3,4) or len(set(q['o']))!=n:E(P+'[%d]: şık'%i)
            if not 0<=q['a']<n:E(P+'[%d]: cevap'%i)
            tags(q.get('tg'),P+'[%d]'%i)
            if not q.get('e'):E(P+'[%d]: açıklama yok'%i)
            if q.get('sc'):aud(owner,q.get('id'),q['sc'],P+'[%d]'%i)
    elif ty=='match':
        L=[o[0] for o in p['opts']]
        if len(set(L))!=len(L):E(P+': harf tekrarı')
        for i,q in enumerate(p['q']):
            if q['a'] not in L:E(P+'[%d]: cevap'%i)
            tags(q.get('tg'),P+'[%d]'%i)
            if not q.get('e'):E(P+'[%d]: açıklama yok'%i)
        if p.get('uniq') and len(set(q['a'] for q in p['q']))!=len(p['q']):E(P+': cevaplar tekrar etmemeli')
    elif ty=='gap':
        L=[o[0] for o in p['opts']];n=len(p['a'])
        gaps(txt,n,P)
        if len(set(p['a']))!=n or any(a not in L for a in p['a']):E(P+': cevaplar')
        if len(p['tg'])!=n or len(p['e'])!=n:E(P+': tg/e sayısı')
        for i,t in enumerate(p['tg']):tags(t,P+'[%d]'%i)
    elif ty=='cloze':
        n=len(p['o']);gaps(txt,n,P)
        if len(p['e'])!=n:E(P+': açıklama sayısı')
        for i,(o,a,t) in enumerate(p['o']):
            if len(o) not in(3,4) or len(set(o))!=len(o) or not 0<=a<len(o):E(P+'[%d]: şık'%i)
            tags(t,P+'[%d]'%i)
    elif ty=='open':
        n=len(p['a']);gaps(txt,n,P)
        if len(p['tg'])!=n or len(p['e'])!=n:E(P+': tg/e sayısı')
        if p.get('st') and len(p['st'])!=n:E(P+': kök sayısı')
        for i,a in enumerate(p['a']):
            if not a or any(not x.strip() for x in a):E(P+'[%d]: cevap boş'%i)
            tags(p['tg'][i],P+'[%d]'%i)
            if p.get('one') and any(' ' in x for x in a):E(P+'[%d]: tek kelime olmalı'%i)
    elif ty=='kwt':
        for i,q in enumerate(p['q']):
            if '______' not in q['s2'] or not q['a'] or not q['key']:E(P+'[%d]: kwt'%i)
            for a in q['a']:
                if q['key'].lower() not in a.lower():E(P+'[%d]: cevap anahtar kelimeyi içermeli: '%i+a)
                wn=len(a.split())
                if not(2<=wn<=q.get('mx',5)):E(P+'[%d]: kelime sayısı %d'%(i,wn))
            tags(q.get('tg'),P+'[%d]'%i)
    else:E(P+': bilinmeyen tür '+str(ty))
def wtask(w,P):
    P=P+'.'+w.get('id','?')
    for lb,tx in w.get('more',[]):
        n=len(tx.split())
        if not(w['min']<=n<=w['max']+25):warn.append(P+': ek örnek %d kelime'%n)
    for f in('id','part','t','in','mail','pts','min','max','model'):
        if f not in w:E(P+': '+f+' yok')
    if w.get('min',0)>=w.get('max',0):E(P+': min/max')
    n=len(w.get('model','').split())
    if not(w['min']<=n<=w['max']+25):warn.append(P+': örnek cevap %d kelime'%n)
def spart(s,P):
    P=P+'.'+s.get('id','?')
    for f in('id','t','ins','q'):
        if not s.get(f):E(P+': '+f+' yok')
    for q in s['q']:
        if len(q)!=4 or q[1]<10 or not q[3]:E(P+': soru biçimi')
        for a in (q[3] if isinstance(q[3],list) else [q[3]]):
            n=len(a.split()); r={'a2':1.5,'b1':1.8,'b2':2.0,'c1':2.1}.get(s['id'][:2],1.8)
            if isinstance(q[3],list) and not(q[1]*r*0.6<=n<=q[1]*r*1.45):warn.append(P+': konuşma örneği %d kelime (%d sn)'%(n,q[1]))
sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'src'))
LV=['A2','B1','B2','C1'];NAME={'A2':'A2 Key','B1':'B1 Preliminary','B2':'B2 First','C1':'C1 Advanced'}
exams=[];prac={}
ONLY=[x for x in os.environ.get('KD_LV','').split(',') if x]   # örn. KD_LV=A2,B1: yalnızca bu seviyeler (sesi hazır olmayanları yayına almamak için)
for lv in LV:
    if ONLY and lv not in ONLY:continue
    f=os.path.join(HERE,'src',lv.lower()+'.py')
    if not os.path.exists(f):continue
    spec=importlib.util.spec_from_file_location(lv.lower(),f);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
    for X in m.EXAMS:
        X.setdefault('lv',lv);X.setdefault('name',NAME[lv]);P=X['id']
        for sk in('R','L','W','S'):
            if sk not in X['sec']:E(P+': bölüm yok '+sk)
        for p in X['sec']['R']['parts']+X['sec']['L']['parts']:part(p,X['id'],P)
        for t in X['sec']['W']['tasks']:
            for w in (t['choice'] if 'choice' in t else [t]):wtask(w,P)
        for s in X['sec']['S']['parts']:spart(s,P)
        exams.append(X)
    pr=m.PRAC;P='prac-'+lv
    mf=os.path.join(HERE,'src','more_'+lv.lower()+'.py')   # ek çalışma parçaları (özgün Use of English alıştırmaları)
    if os.path.exists(mf):
        sp0=importlib.util.spec_from_file_location('more'+lv,mf);mm=importlib.util.module_from_spec(sp0);sp0.loader.exec_module(mm)
        for sk,L in mm.MORE.items():pr.setdefault(sk,[]).extend(L)
    try:
        import importlib;_of=importlib.import_module('opt_fix') if True else None
    except Exception:_of=None
    if _of:_of.apply(pr,warn);_of.apply_gap(pr)
    xf=os.path.join(HERE,'src','extra_'+lv.lower()+'.py')   # ek örnek cevaplar
    if os.path.exists(xf):
        sp=importlib.util.spec_from_file_location('x'+lv,xf);xm=importlib.util.module_from_spec(sp);sp.loader.exec_module(xm)
        for w in pr.get('W',[]):
            if w['id'] in xm.W:w['more']=[list(x) for x in xm.W[w['id']]]
            else:warn.append(P+': ek yazma örneği yok '+w['id'])
        for t in pr.get('S',[]):
            if t['id'] not in xm.S:warn.append(P+': ek konuşma örneği yok '+t['id']);continue
            ms=xm.S[t['id']]
            if len(ms)!=len(t['q']):E(P+'.'+t['id']+': ek örnek sayısı soru sayısıyla uyuşmuyor');continue
            t['q']=[[q[0],q[1],q[2],list(m2)] for q,m2 in zip(t['q'],ms)]
    for sk in('R','L','W','S'):
        if len(pr.get(sk,[]))<5:warn.append(P+': %s çalışma sayısı %d'%(sk,len(pr.get(sk,[]))))
    ids=[x['id'] for sk in 'RLWS' for x in pr.get(sk,[])]
    if len(ids)!=len(set(ids)):E(P+': kimlik tekrarı')
    for p in pr.get('R',[])+pr.get('L',[]):
        if not p.get('t'):E(P+'.'+p['id']+': başlık (t) yok')
        part(p,'p'+lv.lower(),P)
    for w in pr.get('W',[]):wtask(w,P)
    for s in pr.get('S',[]):spart(s,P)
    prac[lv]=pr
XF=os.path.join(HERE,'src','extra_exam.py')   # sınav sonuç ekranı için ek örnek cevaplar
if os.path.exists(XF):
    sp=importlib.util.spec_from_file_location('xexam',XF);xm=importlib.util.module_from_spec(sp);sp.loader.exec_module(xm)
    for X in exams:
        for t in X['sec']['W']['tasks']:
            for w in (t['choice'] if 'choice' in t else [t]):
                if w['id'] in xm.W:w['more']=[list(x) for x in xm.W[w['id']]];wtask(w,X['id'])
                else:warn.append(X['id']+': ek yazma örneği yok '+w['id'])
        for sp_ in X['sec']['S']['parts']:
            if sp_['id'] not in xm.S:warn.append(X['id']+': ek konuşma örneği yok '+sp_['id']);continue
            ms=xm.S[sp_['id']]
            if len(ms)!=len(sp_['q']):E(X['id']+'.'+sp_['id']+': ek örnek sayısı');continue
            sp_['q']=[[q[0],q[1],q[2],list(m2)] for q,m2 in zip(sp_['q'],ms)];spart(sp_,X['id'])
_tt=importlib.util.spec_from_file_location('titles',os.path.join(HERE,'src','titles.py'));_tm=importlib.util.module_from_spec(_tt);_tt.loader.exec_module(_tm)
for lv,pr in prac.items():
    for k in 'RLWS':
        for x in pr.get(k,[]):
            if x['id'] in _tm.T:x['t']=_tm.T[x['id']]
            else:warn.append('İngilizce başlık yok: '+x['id'])
def _imgcap(parts):
    for t in parts:
        for im in t.get('img',[]):
            if len(im)>=3:
                if im[2] not in _tm.IMG:E('İngilizce resim açıklaması yok: '+im[2])
                else:im[:]=im[:3]+[_tm.IMG[im[2]]]
for X in exams:_imgcap(X['sec']['S']['parts'])
for lv,pr in prac.items():_imgcap(pr.get('S',[]))
names=[a[0] for a in audio]
if len(names)!=len(set(names)):E('ses adı tekrarı: '+str([n for n in names if names.count(n)>1]))
for w in warn:print('UYARI:',w)
if errs:
    print('\n'.join('HATA: '+e for e in errs));sys.exit(1)
AD=os.path.join(ROOT,'audio','sx');os.makedirs(AD,exist_ok=True)
if '--no-audio' not in sys.argv:
    k=None;todo=[]
    for name,sc in audio:
        sig=hashlib.sha1(json.dumps(sc,ensure_ascii=False).encode()).hexdigest()[:16]
        mp3=os.path.join(AD,name+'.mp3');sg=mp3+'.sig'
        if os.path.exists(mp3) and os.path.exists(sg) and open(sg).read()==sig:continue
        todo.append((name,sc,mp3,sg,sig))
    for name,sc,mp3,sg,sig in todo:
        if k is None:
            from kokoro_onnx import Kokoro
            import numpy as np,soundfile as sf
            k=Kokoro(os.path.join(TTS,'kokoro-v1.0.int8.onnx'),os.path.join(TTS,'voices-v1.0.bin'))
        parts=[];sr=24000
        for sp,line in sc:
            if line.startswith('#'):  # '#2' gibi: sessizlik (saniye)
                parts.append(np.zeros(int(sr*float(line[1:])),dtype=np.float32));continue
            s,sr=k.create(line,voice=VOICE[sp],speed=0.85 if name[:2] in('a2','b1') or name[1:3] in('a2','b1') else 0.92,lang='en-gb');parts.append(s);parts.append(np.zeros(int(sr*0.45),dtype=s.dtype))
        wav=tempfile.mktemp(suffix='.wav');sf.write(wav,np.concatenate(parts),sr)
        subprocess.run(['ffmpeg','-y','-loglevel','error','-i',wav,'-ac','1','-ar','22050','-b:a','40k',mp3],check=True);os.remove(wav)
        open(sg,'w').write(sig);print('ses:',name,flush=True)
    keep=set(n+'.mp3' for n in names)|set(n+'.mp3.sig' for n in names)
    for f in ([] if ONLY else os.listdir(AD)):
        if f not in keep:os.remove(os.path.join(AD,f));print('silindi:',f)
out='/* Seviye sınavları ve çalışma bölümü (beta). tools/sinav/build.py ile üretilir; elle düzenleme. */\nwindow.SINAV='+json.dumps({'exams':exams,'prac':prac},ensure_ascii=False,separators=(',',':'))+';\n'
open(os.path.join(ROOT,'sinav.js'),'w',encoding='utf8').write(out)
print('tamam: %d sınav, %d ses, %d KB'%(len(exams),len(audio),len(out)//1024))
