"""Seviye düzeltme: tek kelimelik kayıtların CEFR seviyesi dış kaynaklardan alınır.
Öncelik: 1) Oxford 3000/5000 (Oxford Learner's Dictionaries; github.com/voothi/20260715190122-oxford-3000-5000, MIT)
         2) CEFR-J Vocabulary Profile 1.5 + Octanove C1/C2 (github.com/openlanguageprofiles/olp-en-cefrj)
Kaynaklarda olmayan kelimeler ve kalıplar/deyimler olduğu gibi kalır. Birden çok anlam/türde en düşük seviye alınır.
Kullanım: kaynak depoları /tmp/cefr/ox ve /tmp/cefr/cj altına klonla, sonra: python3 tools/level/apply.py"""
import json,os,sys,collections
H=os.path.dirname(os.path.abspath(__file__));ROOT=os.path.dirname(os.path.dirname(H));sys.path.insert(0,H)
from sources import load,look
OX,CJ=load()
ADM=json.load(open(os.path.join(H,'admin.json'),encoding='utf8'))   # yöneticinin uygulamada elle verdiği seviyeler (en yüksek öncelik)
s=open(os.path.join(ROOT,'words.js'),encoding='utf8').read();W=json.loads(s[len('window.WORDS='):-1])
from manual import MAN,PV   # kaynaklarda olmayanların elle gözden geçirilmiş seviyeleri
MAN.update({'amalgamation':'C1','budgetary':'C1','enlistment':'C1','incursion':'C1','inoculation':'C1','cerebral':'C1','societal':'C1','periodical':'B2','regularity':'B2','bursary':'B2','instalment':'B2','abbreviation':'B2'})
c=collections.Counter()
for w in W:
    if ' ' in w[0].strip():
        l=ADM.get(w[0].strip()) or PV.get(w[0].strip())
        if l and l!=w[7]:c[(w[7],l)]+=1;w[7]=l
        continue
    l=ADM.get(w[0].strip()) or MAN.get(w[0].strip()) or look(OX,w[0]) or look(CJ,w[0])
    if l and l!=w[7]:c[(w[7],l)]+=1;w[7]=l
open(os.path.join(ROOT,'words.js'),'w',encoding='utf8').write('window.WORDS='+json.dumps(W,ensure_ascii=False,separators=(',',':'))+';')
print('değişen',sum(c.values()));print(collections.Counter(w[7] for w in W))
