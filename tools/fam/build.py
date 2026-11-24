"""Kelime aileleri: sözlükteki tek kelimelik kayıtlar arasında türetme bağları (care → careful → carefully, careless...).
Güvenli eklerde bağ doğrudan kurulur; riskli eklerde (−y, −ive, −er, −al, −ion, −ed/−ing) Türkçe karşılık ya da İngilizce tanım örtüşmesi aranır.
Çıktı: fam.js -> window.FAM={kelime:[aile üyeleri...]} (yalnız 2+ üyeli aileler; üyeler seviye ve uzunluğa göre sıralı)."""
import json,os,re,subprocess
ROOT=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
W=json.loads(subprocess.check_output(['node','-e',"global.window={};require('%s/words.js');process.stdout.write(JSON.stringify(window.WORDS))"%ROOT]))
_ix=open(os.path.join(ROOT,'index.html'),encoding='utf8').read()
RMX=set(json.loads(re.search(r'const RMX=new Set\((\[.*?\])\)',_ix).group(1)));RMW=set(json.loads(re.search(r'const RMW=new Set\((\[.*?\])\)',_ix).group(1)))
W=[w for w in W if not ((w[7] in('A1','A2') and w[0] in RMW) or (w[0] in RMX and w[7] in('B1','B2','C1')))]
E={}
for w in W:
    k=w[0].strip()
    if re.fullmatch(r"[a-z]{3,}",k) and k not in E:E[k]=w
TRS=lambda w:{t[:5] for t in re.findall(r'[a-zçğıöşü]{4,}',re.sub(r'\(.*?\)','',w[2].lower()))}
def defhas(d,b):   # türev tanımında kök (ya da kökün ilk 4+ harfi) geçiyor mu
    s=d[1].lower();r=b[:max(4,len(b)-2)]
    return re.search(r'\b'+re.escape(r),s) is not None
POS=lambda w:w[3].lower()
# (ek, kökten türeve dönüşüm fonksiyonları, türevin beklenen türü, güvenli mi)
def V(*f):return f
RULES=[
 ('ly',V(lambda b:b+'ly',lambda b:b[:-1]+'ily' if b.endswith('y') else None,lambda b:b[:-1]+'y' if b.endswith('le') else None,lambda b:b+'ally' if b.endswith('ic') else None),'adverb',True),
 ('ness',V(lambda b:b+'ness',lambda b:b[:-1]+'iness' if b.endswith('y') else None),'noun',True),
 ('ment',V(lambda b:b+'ment',),'noun',True),
 ('ity',V(lambda b:b+'ity',lambda b:b[:-1]+'ity' if b.endswith('e') else None,lambda b:b[:-2]+'ility' if b.endswith('le') else None,lambda b:b+'ity' if b.endswith('al') else None),'noun',True),
 ('ation',V(lambda b:b+'ation',lambda b:b[:-1]+'ation' if b.endswith('e') else None,lambda b:b[:-3]+'ation' if b[-3:] in('ize','ise') else None,lambda b:b[:-1]+'ication' if b.endswith('fy') else None),'noun',True),
 ('ion',V(lambda b:b+'ion',lambda b:b[:-1]+'ion' if b.endswith('e') else None,lambda b:b[:-2]+'sion' if b.endswith('de') else None,lambda b:b[:-1]+'ssion' if b.endswith('t') and b.endswith('mit') else None,lambda b:b[:-4]+'ception' if b.endswith('ceive') else None,lambda b:b[:-3]+'ption' if b.endswith('ume') else None,lambda b:b[:-2]+'ption' if b.endswith('be') else None),'noun',False),
 ('ful',V(lambda b:b+'ful',lambda b:b[:-1]+'iful' if b.endswith('y') else None),'adjective',True),
 ('less',V(lambda b:b+'less',),'adjective',True),
 ('able',V(lambda b:b+'able',lambda b:b[:-1]+'able' if b.endswith('e') and not b.endswith('ee') else None,),"adjective",True),
 ("ible",V(lambda b:b+"ible",lambda b:b[:-1]+"ible" if b.endswith("e") else None),"adjective",False),
 ('ive',V(lambda b:b+'ive',lambda b:b[:-1]+'ive' if b.endswith('e') else None,lambda b:b[:-2]+'sive' if b.endswith('de') else None,lambda b:b[:-3]+'ive' if b.endswith('ion') else None),'adjective',False),
 ('ous',V(lambda b:b+'ous',lambda b:b[:-1]+'ious' if b.endswith('y') else None,lambda b:b[:-1]+'ous' if b.endswith('e') else None),'adjective',False),
 ('al',V(lambda b:b+'al',lambda b:b[:-1]+'al' if b.endswith('e') else None),'adjective',False),
 ('ize',V(lambda b:b+'ize',lambda b:b+'ise',lambda b:b[:-1]+'ize' if b.endswith('e') else None,lambda b:b[:-1]+'ise' if b.endswith('e') else None),'verb',True),
 ('ence',V(lambda b:b[:-1]+'ce' if b.endswith('nt') else None,),'noun',True),
 ('er',V(lambda b:b+'er',lambda b:b+'r' if b.endswith('e') else None,lambda b:b+b[-1]+'er' if re.search(r'[^aeiou][aeiou][bdgmnpt]$',b) else None,lambda b:b+'or',lambda b:b[:-1]+'or' if b.endswith('e') else None),'noun',False),
 ('y',V(lambda b:b+'y' if len(b)>=4 else None,lambda b:b[:-1]+'y' if b.endswith('e') and len(b)>=5 else None),'adjective',False),
 ('ed',V(lambda b:b+'ed',lambda b:b+'d' if b.endswith('e') else None),'adjective',False),
 ('ing',V(lambda b:b+'ing',lambda b:b[:-1]+'ing' if b.endswith('e') else None),'adjective',False),
]
PREF=[('un',True),('dis',True),('in',True),('im',True),('il',True),('ir',True),('mis',True)]
par={x:x for x in E}
def find(x):
    while par.get(x,x)!=x:par[x]=par.get(par[x],par[x]);x=par[x]
    return x
def union(a,b):par[find(a)]=find(b)
links=[]
def ok(b,d,safe,exp,suf=''):
    if exp not in POS(E[d]):return False
    if safe and suf in('ly','ness','less','ful'):return True   # bu eklerde anlam neredeyse hep korunur
    return bool(TRS(E[b])&TRS(E[d])) or defhas(E[d],b)
for b in E:
    for suf,fs,exp,safe in RULES:
        for f in fs:
            d=f(b)
            if d and d!=b and d in E and ok(b,d,safe,exp,suf):links.append((b,d,suf))
    for p,safe in PREF:
        d=p+b
        if d in E and (POS(E[b]).split(',')[0].strip().split(' ')[0] in POS(E[d])) and ('not' in E[d][1].lower() or 'bad' in E[d][1].lower() or 'wrong' in E[d][1].lower() or 'opposite' in E[d][1].lower() or bool(TRS(E[b])&TRS(E[d]))):
            links.append((b,d,p+'-'))
BAD={('appoint','disappoint'),('appointment','disappointment'),('different','indifferent'),('lay','mislay'),('solve','dissolve'),('take','mistake'),('migrate','immigrate'),('migrant','immigrant'),('famous','infamous'),('apart','apartment'),('universe','university'),('content','discontent'),('credible','incredible'),('curious','incurious'),('moving','unmoving'),('flammable','inflammable'),('ease','unease'),('leg','legible'),('advert','advertise'),('constant','inconstant'),('lead','mislead'),('leading','misleading'),('use','misuse'),('mean','meanly'),('show','showy'),('organ','organize'),('organ','organise'),('organ','organism'),('organ','organic'),('gent','gentle'),('gent','gently')}   # anlamı kopmuş / yanıltıcı bağlar
links=[l for l in links if (l[0],l[1]) not in BAD]
for b,d,s in links:union(b,d)
G={}
for x in E:
    if x in par:G.setdefault(find(x),[]).append(x)
LV={'A1':0,'A2':1,'B1':2,'B2':3,'C1':4,'C2':5}
fam={};big=[]
for r,m in G.items():
    if len(m)<2:continue
    if len(m)>14:big.append(sorted(m));continue
    m=sorted(m,key=lambda x:(len(x),LV.get(E[x][7],9),x))
    for x in m:fam[x]=m
open(os.path.join(ROOT,'fam.js'),'w',encoding='utf8').write('/* Kelime aileleri. tools/fam/build.py ile üretilir; elle düzenleme. */\nwindow.FAM='+json.dumps({k:[x for x in v] for k,v in fam.items()},ensure_ascii=False,separators=(',',':'))+';\n')
fams={tuple(v) for v in fam.values()}
print('aile',len(fams),'kelime',len(fam),'çok büyük (atlandı)',len(big))
if __name__=='__main__':
    import random;random.seed(3)
    for f in random.sample(sorted(fams),70):print(' · '.join(f))
    for b in big[:5]:print('BÜYÜK',len(b),b[:20])
