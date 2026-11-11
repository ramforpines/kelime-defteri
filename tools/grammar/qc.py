#!/usr/bin/env python3
"""Gramer sorularında kalite kontrolü (grammar.js üzerinde): kapsam, çeldirici/yanıt sorunları, olası çift doğru.
Kullanım: python3 tools/grammar/qc.py [--lt]   (--lt: LanguageTool ile 'yanlış şık da doğru görünüyor mu' denetimi, yavaş)"""
import json,re,sys,os,subprocess,collections
ROOT=os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','..'))
js="global.window={};require(process.argv[1]+'/grammar.js');process.stdout.write(JSON.stringify(window.GRAMMAR))"
G=json.loads(subprocess.run(['node','-e',js,ROOT],capture_output=True,check=True).stdout)
rows=[]
for t in G:
    for k,q in enumerate(t['quiz']):rows.append((t['id'],'quiz',k,q))
    for k,q in enumerate(t.get('dq',[])):rows.append((t['id'],'dq',k,q))
n=len(rows);withn=sum(1 for r in rows if r[3].get('n'));
print('toplam %d soru; şık açıklamalı %d (%.0f%%)'%(n,withn,100*withn/n))
short=[r for r in rows if len(r[3]['w'])<45 and not r[3].get('n')]
print('kısa açıklamalı ve şık notu olmayan:',len(short))
by=collections.Counter(r[0] for r in rows if not r[3].get('n'))
print('açıklaması eksik soru sayısı (konu başına):',dict(by.most_common(60)))
bad=0
for P,src,k,q in rows:
    o=q['o']
    if len(set(x.lower() for x in o))!=len(o):print('YİNELENEN ŞIK',P,src,k,o);bad+=1
    if not 0<=q['a']<len(o):print('A DIŞI',P,src,k);bad+=1
    L=[len(x) for x in o];
    if L[q['a']]>max(l for i,l in enumerate(L) if i!=q['a'])+8:print('doğru şık çok uzun',P,src,k,q['q'][:50]);bad+=1
print('sorun:',bad)
pos=collections.Counter(q['a'] for _,_,_,q in rows);print('doğru şık konumu:',dict(pos))
if '--lt' in sys.argv:
    import language_tool_python as lt
    tool=lt.LanguageTool('en-US');TR=re.compile(r'[çğıöşüÇĞİÖŞÜ]|saat|cümle|doğru|hangi',re.I);amb=0
    cats=('GRAMMAR','TYPOS','PUNCTUATION','CASING','CONFUSED_WORDS')
    def ok(s):return not [m for m in tool.check(s) if m.category in cats and m.rule_id!='MORFOLOGIK_RULE_EN_US']
    for P,src,k,q in rows:
        if '___' not in q['q'] or TR.search(q['q']):continue
        for j,o in enumerate(q['o']):
            if j==q['a']:continue
            s=re.sub(r'\s+',' ',q['q'].replace('___',o).replace('*','')).strip()
            if ok(s):amb+=1;print('OLASI ÇİFT DOĞRU %s.%s[%d]: %s'%(P,src,k,s))
    print('olası çift doğru:',amb)
