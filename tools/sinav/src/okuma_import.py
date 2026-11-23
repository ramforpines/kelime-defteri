# Okuma sekmesindeki parçaları sınav çalışma bölümüne uzun metin (çoktan seçmeli) olarak aktarır.
import json,os,re
H=os.path.dirname(os.path.abspath(__file__))
D=json.load(open(os.path.join(H,'okuma_import.json'),encoding='utf-8'))
def tag(q):
    s=q.lower()
    if re.search(r'\bmean|word\b|phrase|refers? to|expression',s):return ['vocab']
    if re.search(r'main idea|mainly about|best title|best summary|passage is about|text is about|purpose',s):return ['gist']
    if re.search(r'attitude|opinion|feel|think|believe|writer|author|view',s):return ['attitude']
    if re.search(r'suggest|imply|infer|likely|probably|why does|why did|why is|why do',s):return ['inference']
    return ['detail']
def part(r):
    lv=r['lv'];k='R3' if lv in('A2','B1') else 'R5'
    big=lv in('B2','C1','C2')
    return {'k':k,'id':'okr_'+r['id'],'t':'Uzun metin: '+r['t'],'ty':'mc',
     'nm':'Okuma %s · Uzun metin'%k[1],
     'ti':('Reading and Use of English Part ' if big else 'Reading Part ')+k[1],
     'ins':'Metni oku ve soruları cevapla.','title':r['t'],'p':r['p'],
     'q':[{'q':x['q'],'o':x['o'],'a':x['a'],'tg':tag(x['q']),'e':x.get('e') or 'Metinde cevabı bul.'} for x in r['q']]}
BY={}
for r in D:
    lv='C1' if r['lv']=='C2' else r['lv']
    BY.setdefault(lv,[]).append(part(r))
TITLES={'okr_'+r['id']:r['t'] for r in D}
