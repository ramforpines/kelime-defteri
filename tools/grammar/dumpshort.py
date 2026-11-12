#!/usr/bin/env python3
"""Kısa (<32 karakter) şık notlarını listeler: python3 dumpshort.py <konu id> [üst sınır]"""
import json,subprocess,sys,os
ROOT=os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','..'))
js="global.window={};require(process.argv[1]+'/grammar.js');process.stdout.write(JSON.stringify(window.GRAMMAR))"
G=json.loads(subprocess.run(['node','-e',js,ROOT],capture_output=True,check=True).stdout)
t=[x for x in G if x['id']==sys.argv[1]][0]
for q in t['quiz']+t.get('dq',[]):
    if not q.get('n') or q['q'].startswith('Bu cümlede hatalı'):continue
    sh=[(q['o'][i],x) for i,x in enumerate(q['n']) if i!=q['a'] and x and x!='Doğru.' and len(x)<32]
    if sh:print(json.dumps(q['q'],ensure_ascii=False),'=>',json.dumps(q['o'][q['a']],ensure_ascii=False),'|',json.dumps(q['w'][:90],ensure_ascii=False),'|',json.dumps(sh,ensure_ascii=False))
