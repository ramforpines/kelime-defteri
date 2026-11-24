"""Karıştırılan kelimeler (G) ve yalancı eşdeğerler (F): src.txt -> conf.js"""
import json,os,re,subprocess
H=os.path.dirname(os.path.abspath(__file__));ROOT=os.path.dirname(os.path.dirname(H))
have=set(json.loads(subprocess.check_output(['node','-e',"global.window={};require('%s/words.js');process.stdout.write(JSON.stringify(window.WORDS.map(w=>w[0])))"%ROOT])))
G=[];F={};miss=[]
for i,l in enumerate(open(os.path.join(H,'src.txt'),encoding='utf8')):
    l=l.strip()
    if not l or l.startswith('#'):continue
    p=[x.strip() for x in l.split('|')]
    if p[0]=='G':
        ws=[x.strip() for x in p[1].split(',')];ss=[x.strip() for x in '|'.join(p[3:]).split(';') if x.strip()]
        for s in ss:
            m=re.search(r'\{([^}]*)\}',s);assert m and s.count('{')==1,(i+1,s)
            o=m.group(1).split('|');assert 2<=len(o)<=4 and len(set(o))==len(o),(i+1,s)
        G.append({'w':ws,'e':p[2],'s':ss});miss+=[w for w in ws if w not in have]
    elif p[0]=='F':
        F[p[1]]={'t':p[2],'x':[x.strip() for x in p[3].split(';')],'n':p[4] if len(p)>4 else ''};miss+=[p[1]] if p[1] not in have else []
open(os.path.join(ROOT,'conf.js'),'w',encoding='utf8').write('/* Karıştırılan kelimeler ve yalancı eşdeğerler. tools/conf/build.py ile üretilir (kaynak: src.txt). */\nwindow.CONF='+json.dumps({'g':G,'f':F},ensure_ascii=False,separators=(',',':'))+';\n')
print('grup',len(G),'cümle',sum(len(g['s']) for g in G),'yalancı eşdeğer',len(F),'sözlükte yok:',sorted(set(miss)))
