import csv,json,subprocess,re,collections
LV=['A1','A2','B1','B2','C1','C2']
def load():
    OX={};CJ={}
    for f in ['/tmp/cefr/ox/20260715160822-oxford-3000.en.tsv','/tmp/cefr/ox/20260715165539-oxford-5000-expanded.en.tsv']:
        for r in csv.DictReader(open(f,encoding='utf8'),delimiter='\t'):
            w=r['Word'].strip().lower()
            for l in re.findall(r'[ABC][12]',r['Level']):
                if w not in OX or LV.index(l)<LV.index(OX[w]):OX[w]=l
    for f in ['/tmp/cefr/cj/cefrj-vocabulary-profile-1.5.csv','/tmp/cefr/cj/octanove-vocabulary-profile-c1c2-1.0.csv']:
        for r in csv.DictReader(open(f,encoding='utf8')):
            l=r['CEFR'].strip()[:2]
            if l not in LV:continue
            for w in r['headword'].split('/'):
                w=w.strip().lower()
                if w and (w not in CJ or LV.index(l)<LV.index(CJ[w])):CJ[w]=l
    return OX,CJ
def var(k):
    k=k.lower();return [k,re.sub(r'ise$','ize',k),re.sub(r'ised$','ized',k),re.sub(r'isation$','ization',k),re.sub(r'our$','or',k),re.sub(r're$','er',k),re.sub(r'yse$','yze',k)]
def look(D,k):
    for c in var(k):
        if c in D:return D[c]
