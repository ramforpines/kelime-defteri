#!/usr/bin/env python3
"""b1_src.py -> ../../reading5.js (okuma parçaları + Türkçe çeviriler). Doğru şık konumları sırayla döndürülür."""
import json,os,re,sys
H=os.path.dirname(os.path.abspath(__file__));ROOT=os.path.abspath(os.path.join(H,'..','..'))
sys.path.insert(0,H)
from b1_src import R
A=[];T={};errs=[]
ids=set()
for r_i,r in enumerate(R):
    i=r['id']
    if i in ids:errs.append('tekrar '+i)
    ids.add(i)
    if len(r['p'])!=len(r['ptr']):errs.append(i+': paragraf çevirisi')
    if not 5<=len(r['g'])<=8:errs.append(i+': kelime')
    qs=[];tq=[]
    for k,(q,o,e,qt,ot) in enumerate(r['q']):
        if len(o)!=4 or len(set(o))!=4 or len(ot)!=4:errs.append('%s q%d şık'%(i,k))
        pos=(r_i*3+k*2+1)%4
        oo=o[1:];oo.insert(pos,o[0]);ot2=ot[1:];ot2.insert(pos,ot[0])
        qs.append({'q':q,'o':oo,'a':pos,'e':e});tq.append({'q':qt,'o':ot2})
    A.append({'id':i,'t':r['t'],'lv':'B1','g':[list(x) for x in r['g']],'p':r['p'],'q':qs})
    T[i]={'p':r['ptr'],'q':tq}
if errs:print('\n'.join(errs));sys.exit(1)
js='/* Kelime Defteri: ek B1 okuma parçaları (tools/reading/b1.py üretir). */\n(function(){var A='+json.dumps(A,ensure_ascii=False)+';var T='+json.dumps(T,ensure_ascii=False)+';window.READINGS=(window.READINGS||[]).concat(A);window.READINGS_TR=Object.assign(window.READINGS_TR||{},T)})();\n'
open(os.path.join(ROOT,'reading5.js'),'w',encoding='utf8').write(js);print('reading5.js',len(js),len(A),'parça')
