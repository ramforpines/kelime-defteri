#!/usr/bin/env python3
"""PET denemelerini doğrular, dinleme seslerini üretir (kokoro-onnx) ve ../../pet.js dosyasını yazar.
Kullanım: python3 build.py [--no-audio]
Ses: konuşma metni değişmediyse mevcut mp3 yeniden üretilmez (metin özeti dosya adında değil, .sig dosyasında tutulur)."""
import os,sys,json,glob,importlib.util,hashlib,re,subprocess,tempfile
HERE=os.path.dirname(os.path.abspath(__file__));ROOT=os.path.abspath(os.path.join(HERE,'..','..'))
TTS=os.environ.get('KD_TTS','/tmp/claude-0/tts')
VOICE={'M':'bm_george','F':'bf_emma'}
errs=[]
def E(m):errs.append(m)

gr=open(os.path.join(ROOT,'grammar.js'),encoding='utf8').read()
GIDS=set(re.findall(r'"id":"([a-z0-9-]+)","lv"',gr))
SKILL={'gist','detail','inference','attitude','purpose','vocab','spelling','reference','coherence'}
PARTS=['R1','R2','R3','R4','R5','R6','L1','L2','L3','L4']
NQ={'R1':5,'R2':5,'R3':5,'R4':5,'R5':6,'R6':6,'L1':7,'L2':6,'L3':6,'L4':6}

def tags(t,P):
    if not t:E(P+': etiket yok')
    for x in t:
        if x not in SKILL and x not in GIDS:E(P+': bilinmeyen etiket '+x)

tests=[]
for f in sorted(glob.glob(os.path.join(HERE,'src','*.py'))):
    spec=importlib.util.spec_from_file_location(os.path.basename(f)[:-3],f);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
    tests.append(m.TEST)

audio_jobs=[]
for T in tests:
    ks=[p['k'] for p in T['parts']]
    if ks!=PARTS:E(T['id']+': bölüm sırası '+str(ks))
    for p in T['parts']:
        P=T['id']+'.'+p['k'];k=p['k']
        if k in('R1','L1','L2'):
            if len(p['q'])!=NQ[k]:E(P+': soru sayısı %d'%len(p['q']))
            for i,q in enumerate(p['q']):
                n=3 if k!='R3' else 4
                if len(q['o'])!=n or len(set(q['o']))!=n:E(P+'[%d]: şık sayısı'%i)
                if not 0<=q['a']<n:E(P+'[%d]: cevap'%i)
                tags(q.get('tg'),P+'[%d]'%i)
                if not q.get('e'):E(P+'[%d]: açıklama yok'%i)
                if k!='R1':audio_jobs.append((T['id']+'-'+q['id'],q['sc']))
        elif k in('R3','L4'):
            if len(p['q'])!=NQ[k]:E(P+': soru sayısı')
            n=4 if k=='R3' else 3
            for i,q in enumerate(p['q']):
                if len(q['o'])!=n or len(set(q['o']))!=n:E(P+'[%d]: şık sayısı'%i)
                if not 0<=q['a']<n:E(P+'[%d]: cevap'%i)
                tags(q.get('tg'),P+'[%d]'%i)
            if k=='L4':audio_jobs.append((T['id']+'-'+p['id'],p['sc']))
        elif k=='R2':
            L=[t[0] for t in p['texts']]
            if len(p['people'])!=5 or len(L)!=8:E(P+': kişi/metin sayısı')
            if len(set(p['a']))!=5 or any(a not in L for a in p['a']):E(P+': cevaplar')
            for i,t in enumerate(p['tg']):tags(t if isinstance(t,list) else [t],P+'[%d]'%i)
        elif k=='R4':
            L=[s[0] for s in p['s']]
            if len(L)!=8 or len(set(p['a']))!=5 or any(a not in L for a in p['a']):E(P+': cümle/cevap')
            for i in range(1,6):
                if '(%d) ______'%i not in p['p']:E(P+': boşluk %d yok'%i)
        elif k=='R5':
            if len(p['o'])!=6:E(P+': 6 boşluk olmalı')
            for i,(o,a,t) in enumerate(p['o']):
                if '(%d) ______'%(i+1) not in p['p']:E(P+': boşluk %d yok'%(i+1))
                if len(o)!=4 or len(set(o))!=4 or not 0<=a<4:E(P+'[%d]: şık'%i)
                tags(t,P+'[%d]'%i)
        elif k in('R6','L3'):
            src=p['p'] if k=='R6' else p['notes']
            if len(p['a'])!=6:E(P+': 6 cevap olmalı')
            for i,a in enumerate(p['a']):
                if '(%d) ______'%(i+1) not in src:E(P+': boşluk %d yok'%(i+1))
                if not a or any(not x.strip() for x in a):E(P+'[%d]: cevap boş'%i)
                tags(p['tg'][i],P+'[%d]'%i)
            if k=='R6':
                for i,a in enumerate(p['a']):
                    if any(' ' in x for x in a if x not in('a lot',)):E(P+'[%d]: tek kelime olmalı'%i)
            if k=='L3':audio_jobs.append((T['id']+'-'+p['id'],p['sc']))
        if 'e' in p and isinstance(p['e'],list):
            nn=len(p.get('a') or p.get('o') or [])
            if len(p['e'])!=nn:E(P+': açıklama sayısı')

if errs:
    print('\n'.join('HATA: '+e for e in errs));sys.exit(1)

# ses
AD=os.path.join(ROOT,'audio','pet');os.makedirs(AD,exist_ok=True)
if '--no-audio' not in sys.argv and audio_jobs:
    k=None
    for name,sc in audio_jobs:
        sig=hashlib.sha1(json.dumps(sc,ensure_ascii=False).encode()).hexdigest()[:16]
        mp3=os.path.join(AD,name+'.mp3');sg=mp3+'.sig'
        if os.path.exists(mp3) and os.path.exists(sg) and open(sg).read()==sig:continue
        if k is None:
            from kokoro_onnx import Kokoro
            import numpy as np,soundfile as sf
            k=Kokoro(os.path.join(TTS,'kokoro-v1.0.int8.onnx'),os.path.join(TTS,'voices-v1.0.bin'))
        parts=[];sr=24000
        for sp,line in sc:
            s,sr=k.create(line,voice=VOICE[sp],speed=0.85,lang='en-gb');parts.append(s);parts.append(np.zeros(int(sr*0.45),dtype=s.dtype))
        wav=tempfile.mktemp(suffix='.wav');sf.write(wav,np.concatenate(parts),sr)
        subprocess.run(['ffmpeg','-y','-loglevel','error','-i',wav,'-ac','1','-ar','22050','-b:a','40k',mp3],check=True);os.remove(wav)
        open(sg,'w').write(sig);print('ses:',name)

out='/* PET (B1 Preliminary) formatında denemeler (beta). tools/pet/build.py ile üretilir; elle düzenleme. */\nwindow.PET='+json.dumps(tests,ensure_ascii=False,separators=(',',':'))+';\n'
open(os.path.join(ROOT,'pet.js'),'w',encoding='utf8').write(out)
print('tamam: %d deneme, %d ses, %d KB'%(len(tests),len(audio_jobs),len(out)//1024))
