#!/usr/bin/env python3
"""Gramer verisini doğrular ve ../../grammar.js dosyasını üretir. Kullanım: python3 build.py [--lt]"""
import json,os,re,random,sys,importlib.util,glob
HERE=os.path.dirname(os.path.abspath(__file__));ROOT=os.path.abspath(os.path.join(HERE,'..','..'))
sys.path.insert(0,HERE)
LEVELS=['A1','A2','B1','B2','C1','C2']
errs=[];warn=[]
def E(m):errs.append(m)
def W(m):warn.append(m)
def _words():
    f='/tmp/gram/words.json'
    if os.path.exists(f):return json.load(open(f))
    import subprocess;os.makedirs('/tmp/gram',exist_ok=True)   # taze oturumda words.js'den üret
    subprocess.check_call(['node','-e',"global.window={};eval(require('fs').readFileSync('%s/words.js','utf8'));const W=window.WORDS||window.W||Object.values(window).find(Array.isArray);require('fs').writeFileSync('%s',JSON.stringify(W))"%(ROOT,f)])
    return json.load(open(f))
words={w[0].lower() for w in _words()}
topics=json.load(open(os.path.join(HERE,'existing.json')))
for f in sorted(glob.glob(os.path.join(HERE,'src','*.py'))):
    spec=importlib.util.spec_from_file_location(os.path.basename(f)[:-3],f);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
    topics+=m.TOPICS
# bugünün testi için ek gramer soruları: dq/<konu id>.py içinde DQ=[{lv,t,stem,right,wrongs,why},...] (konu mini testinden FARKLI sorular)
DQ={}
for f in sorted(glob.glob(os.path.join(HERE,'dq','*.py'))):
    spec=importlib.util.spec_from_file_location('dq_'+os.path.basename(f)[:-3],f);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
    DQ[os.path.basename(f)[:-3]]=m.DQ
SAFE=re.compile(r'<(?!/?(b|i|br)\b)[^>]*>')
def conv_quiz(t):
    if t['quiz'] and 'stem' in t['quiz'][0]:
        out=[]
        for seed in range(400):
            rng=random.Random('%s|%d'%(t['id'],seed));out=[]
            for q in t['quiz']:
                o=[q['right']]+q['wrongs'];rng.shuffle(o)
                out.append(dict(lv=q['lv'],t=q['t'],q=q['stem'],o=o,a=o.index(q['right']),w=q['why']))
            cnt=[0,0,0,0]
            for q in out:cnt[q['a']]+=1
            nopt=len(out[0]['o']);need=len(out)//nopt-2
            if all(c>=need for c in cnt[:nopt]) and max(cnt[:nopt])<=len(out)//nopt+2:break
        t['quiz']=out
    return t
def S(path,s,raw=False):
    if not isinstance(s,str) or not s.strip():E('%s: boş metin'%path);return
    if s.count('*')%2:E('%s: * eşleşmiyor: %s'%(path,s))
    if raw:
        if SAFE.search(s):E('%s: izinsiz etiket: %s'%(path,s))
    elif re.search(r'[<>]',s):E('%s: HTML olmamalı: %s'%(path,s))
def pairs(path,L,minn=1):
    if not isinstance(L,list) or len(L)<minn:E('%s: en az %d örnek gerekli'%(path,minn));return
    for k,e in enumerate(L):
        if not(isinstance(e,(list,tuple)) and len(e)==2):E('%s[%d]: [en,tr] olmalı'%(path,k));continue
        S('%s[%d].en'%(path,k),e[0]);S('%s[%d].tr'%(path,k),e[1])
        if '*' not in e[0]:W('%s[%d]: vurgu yok: %s'%(path,k,e[0]))
ids=set();EN=[];  # (yol, cümle) — İngilizce denetim için
def addEN(path,s):EN.append((path,s.replace('*','')))
for t in topics:
    t=conv_quiz(t);P=t.get('id','?')
    if P in ids:E('yinelenen id '+P)
    ids.add(P)
    for k in['id','lv','title','form_name','intro','form','uses','mistakes','tip','vocab','quiz','dialogues']:
        if k not in t:E('%s: eksik alan %s'%(P,k))
    if t.get('lv') not in LEVELS:E('%s: seviye'%P)
    for k,s in enumerate(t.get('intro',[])):S('%s.intro[%d]'%(P,k),s,True)
    for k,f in enumerate(t.get('form',[])):
        S('%s.form[%d].k'%(P,k),f['k']);S('%s.form[%d].p'%(P,k),f['p']);pairs('%s.form[%d].e'%(P,k),[f['e']]);addEN('%s.form[%d]'%(P,k),f['e'][0])
    if len(t.get('form',[]))<3:E('%s: form < 3'%P)
    if t.get('formnote'):
        n=t['formnote'];S(P+'.formnote.h',n['h']);S(P+'.formnote.body',n['body'],True);pairs(P+'.formnote.ex',n.get('ex',[]),0)
    def inl(path,L):
        for k,n in enumerate(L or []):
            S('%s[%d].h'%(path,k),n['h']);S('%s[%d].body'%(path,k),n['body'],True);pairs('%s[%d].ex'%(path,k),n.get('ex',[]),0)
            for e in n.get('ex',[]):addEN('%s[%d]'%(path,k),e[0])
    if len(t.get('uses',[]))<3:E('%s: kullanım < 3'%P)
    for k,u in enumerate(t.get('uses',[])):
        S('%s.uses[%d].h'%(P,k),u['h']);S('%s.uses[%d].why'%(P,k),u['why'],True);pairs('%s.uses[%d].ex'%(P,k),u['ex'],3)
        for e in u['ex']:addEN('%s.uses[%d]'%(P,k),e[0])
        if u.get('note'):S('%s.uses[%d].note'%(P,k),u['note'],True)
        inl('%s.uses[%d].inl'%(P,k),u.get('inl'))
    for k2 in('timesTitle','timesNote','verbsTitle','verbsNote'):
        if k2 in t:S(P+'.'+k2,t[k2])
    for g in('times','verbs'):
        for k,x in enumerate(t.get(g,[])):
            S('%s.%s[%d].h'%(P,g,k),x['h']);S('%s.%s[%d].say'%(P,g,k),x['say'],True);pairs('%s.%s[%d].ex'%(P,g,k),x['ex'],2)
            for e in x['ex']:addEN('%s.%s[%d]'%(P,g,k),e[0])
            for L in (x['lists'] if g=='times' else [{'l':'','w':x['l']}]):
                pairs0=[(a[0],a[1]) for a in L['w']]
                for a in pairs0:
                    if not a[0] or not a[1]:E('%s.%s: boş kelime çifti'%(P,g))
            if g=='times':inl('%s.times[%d].inl'%(P,k),x.get('inl'))
    for k,r in enumerate(t.get('patterns',[])):
        S('%s.patterns[%d]'%(P,k),r[0]);S('%s.patterns[%d].ex'%(P,k),r[1]);S('%s.patterns[%d].tr'%(P,k),r[2]);addEN('%s.patterns[%d]'%(P,k),r[1])
    for k,d in enumerate(t.get('dialogues',[])):
        S('%s.dlg[%d].h'%(P,k),d['h'])
        if len(d['lines'])<4:E('%s: diyalog çok kısa'%P)
        for j,l in enumerate(d['lines']):
            S('%s.dlg[%d][%d]'%(P,k,j),l[1]);S('%s.dlg[%d][%d].tr'%(P,k,j),l[2]);addEN('%s.dlg[%d][%d]'%(P,k,j),l[1])
        if d.get('note'):S('%s.dlg[%d].note'%(P,k),d['note'],True)
    if t.get('vs2'):
        for k,r in enumerate(t['vs2']):
            for j in(0,1,2,3):S('%s.vs2[%d][%d]'%(P,k,j),r[j])
            addEN('%s.vs2[%d]'%(P,k),r[0]);addEN('%s.vs2[%d]'%(P,k),r[2])
    if len(t.get('mistakes',[]))<4:E('%s: hata < 4'%P)
    for k,m in enumerate(t.get('mistakes',[])):
        for f in('bad','good','why'):S('%s.mistakes[%d].%s'%(P,k,f),m[f])
        addEN('%s.mistakes[%d].good'%(P,k),m['good'])
    S(P+'.tip',t.get('tip'))
    v=t.get('vocab',[])
    if len(v)<6:E('%s: kelime < 6'%P)
    for w in v:
        if w.lower() not in words:E('%s: sözlükte olmayan kelime: %s'%(P,w))
    for k,w in enumerate(t.get('irr',[])):pass
    # test
    qz=t.get('quiz',[])
    if len(qz)!=20:E('%s: test %d soru (20 olmalı)'%(P,len(qz)))
    d=[q['lv'] for q in qz]
    if [d.count(i) for i in(1,2,3,4)]!=[6,6,5,3] or d!=sorted(d):E('%s: zorluk dağılımı 6/6/5/3 ve artan olmalı: %s'%(P,d))
    seen=set()
    for k,q in enumerate(qz):
        pth='%s.quiz[%d]'%(P,k);S(pth+'.q',q['q']);S(pth+'.w',q['w']);S(pth+'.t',q['t'])
        if len(set(q['o']))!=len(q['o']):E(pth+': yinelenen şık')
        if not(0<=q['a']<len(q['o'])):E(pth+': a aralık dışı')
        key=(q['q'],q['o'][q['a']])
        if key in seen:E(pth+': yinelenen soru')
        seen.add(key)
        if '___' in q['q'] or '?' in q['q']:pass
        for o in q['o']:
            if len(o)>60:W(pth+': uzun şık')
    cnt=[sum(1 for q in qz if q['a']==i) for i in range(3)]
    if min(cnt[:2])<4:W('%s: cevap konumu dağılımı %s'%(P,cnt))
    t['_n']=len(qz)
    # ek sorular (dq)
    if P in DQ:
        dq=conv_quiz({'id':P+'|dq','quiz':[dict(q) for q in DQ[P]]})['quiz']
        qkeys={(q['q'],q['o'][q['a']]) for q in qz}
        for k,q in enumerate(dq):
            pth='%s.dq[%d]'%(P,k);S(pth+'.q',q['q']);S(pth+'.w',q['w']);S(pth+'.t',q['t'])
            if len(set(q['o']))!=len(q['o']):E(pth+': yinelenen şık')
            if (q['q'],q['o'][q['a']]) in qkeys:E(pth+': mini testte zaten var')
            qkeys.add((q['q'],q['o'][q['a']]))
            L=[len(o) for o in q['o']];c=L[q['a']];d=[x for i,x in enumerate(L) if i!=q['a']]
            if c>max(d)+3:W(pth+': doğru şık belirgin biçimde en uzun')
            if '___' in q['q']:addEN(pth,q['q'].replace('___',q['o'][q['a']]))
        t['dq']=dq
    # LT için doğru cümleler
    for k,q in enumerate(qz):
        if '___' in q['q']:
            addEN('%s.quiz[%d]'%(P,k),q['q'].replace('___',q['o'][q['a']]))
        elif q['q'].startswith('Hangi') or q['q'].startswith('Which'):pass
    topics[topics.index(next(x for x in topics if x.get('id')==P))]=t
topics.sort(key=lambda t:(LEVELS.index(t['lv']),t.get('ord',50)))
if '--lt' in sys.argv:
    import language_tool_python as lt
    tool=lt.LanguageTool('en-US');bad=0
    NAMES={'Ayşe','Ali','Mert','Elif','Tom','Mehmet','Ahmet','Zeynep','Deniz','Can','Selin','Kaan','Emre','Ece','Burak','Izmir','İzmir','Ankara','Fatma','Sara','Anna','Mia','Leo','Ben','Lily','Jack','Emma','Sam'}
    TR=re.compile(r'\(saat|cümle|doğru|anlam|hangi|şu |gelir')
    def chk(s):
        r=[]
        for m in tool.check(s):
            if m.category not in('GRAMMAR','TYPOS','PUNCTUATION','CASING','CONFUSED_WORDS'):continue
            tok=s[m.offset:m.offset+m.error_length]
            if m.rule_id=='MORFOLOGIK_RULE_EN_US' and (tok in NAMES or tok.strip("'s") in NAMES):continue
            r.append(m)
        return r
    for path,s in EN:
        if not s.strip() or len(s)<4 or TR.search(s):continue
        for m in chk(s):
            bad+=1;print('LT %s | %s | %s -> %s'%(path,s,m.rule_id,m.message[:90]))
    print('LT bulgu:',bad)
    amb=0
    for t in (topics if '--amb' in sys.argv else []):
        for k,q in enumerate(t['quiz']):
            if '___' not in q['q'] or TR.search(q['q']):continue
            for j,o in enumerate(q['o']):
                if j==q['a']:continue
                if not chk(q['q'].replace('___',o)):
                    amb+=1;print('OLASI ÇİFT DOĞRU %s.quiz[%d]: %s  [%s]'%(t['id'],k,q['q'].replace('___',o),o))
    print('olası çift doğru:',amb)
for t in topics:t.pop('_n',None)
for w in warn[:60]:print('uyarı:',w)
if len(warn)>60:print('... %d uyarı daha'%(len(warn)-60))
if errs:
    for e in errs:print('HATA:',e)
    print('%d hata'%len(errs));sys.exit(1)
PLAN={'B1':['-ed / -ing sıfatlar ve sıfat sırası','Sıfat + edat kalıpları','Ön ekler ve son ekler'],'C1':['Mixed conditionals','Advanced passive and reporting'],'C2':['İnce anlam farkları ve üslup']}
out='/* Gramer konu anlatımları (beta). Bu dosya tools/grammar/build.py ile üretilir; elle düzenleme. *...* = vurgulanan gramer parçası. */\nwindow.GRAMMAR='+json.dumps(topics,ensure_ascii=False,separators=(',',':'))+';\nwindow.GRAMMAR_PLAN='+json.dumps(PLAN,ensure_ascii=False,separators=(',',':'))+';\n'
open(os.path.join(ROOT,'grammar.js'),'w',encoding='utf8').write(out)
print('tamam: %d konu, %d KB'%(len(topics),len(out)//1024))
