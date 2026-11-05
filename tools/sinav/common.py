"""Ortak yardımcılar: eski PET deneme bölümlerini genel sınav bölüm biçimine çevirir."""
import os,importlib.util
HERE=os.path.dirname(os.path.abspath(__file__))
def load(path,name='TEST'):
    spec=importlib.util.spec_from_file_location(os.path.basename(path)[:-3],path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
    return getattr(m,name)
PETDIR=os.path.join(HERE,'..','pet')
PN={'R1':'Kısa metinler','R2':'Eşleştirme','R3':'Uzun metin','R4':'Cümle yerleştirme','R5':'Çoktan seçmeli boşluk','R6':'Açık boşluk','L1':'Kısa kayıtlar','L2':'Kısa konuşmalar','L3':'Not tamamlama','L4':'Röportaj'}
def pet(p,pid=None):
    """PET bölümünü genel biçime çevir. pid: ses dosyası için bölüm kimliği."""
    k=p['k'];n=('Okuma ' if k[0]=='R' else 'Dinleme ')+k[1]+' · '+PN[k]
    b={'k':k,'nm':n,'ti':p['ti'],'ins':p['ins']}
    if k=='R1':b.update(ty='mc',q=p['q'])
    elif k=='R2':b.update(ty='match',pl='Metinler (A–H)',opts=[list(t) for t in p['texts']],q=[{'q':nm+': '+d,'a':p['a'][i],'tg':p['tg'][i] if isinstance(p['tg'][i],list) else [p['tg'][i]],'e':p['e'][i]} for i,(nm,d) in enumerate(p['people'])])
    elif k=='R3':b.update(ty='mc',title=p['title'],p=p['p'],q=p['q'])
    elif k=='R4':b.update(ty='gap',title=p['title'],p=p['p'],opts=[list(s) for s in p['s']],a=p['a'],tg=[[t] if isinstance(t,str) else t for t in p['tg']],e=p['e'])
    elif k=='R5':b.update(ty='cloze',title=p['title'],p=p['p'],o=[list(x) for x in p['o']],e=p['e'])
    elif k=='R6':b.update(ty='open',title=p['title'],p=p['p'],a=p['a'],tg=p['tg'],e=p['e'])
    elif k in('L1','L2'):b.update(ty='mc',q=p['q'])
    elif k=='L3':b.update(ty='open',id=p['id'],sc=p['sc'],title='Notlar',p=p['notes'],a=p['a'],tg=p['tg'],e=p['e'])
    elif k=='L4':b.update(ty='mc',id=p['id'],sc=p['sc'],q=p['q'])
    if pid:b['id']=pid
    return b
