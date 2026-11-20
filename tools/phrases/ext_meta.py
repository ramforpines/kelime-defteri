# Yeni kalıp grupları için yakın alt grup ve işlev açıklamaları (build.py okur)
NEAR_X={'hcheck':['hprob','air'],'hprob':['hcheck','air'],'air':['hcheck','hprob'],
 'dsym':['hdoc','dpharm'],'hdoc':['dsym','dpharm'],'dpharm':['dsym','hdoc'],
 'sfit':['sret','sprice'],'sret':['sfit','sprice'],'sprice':['sfit','sret'],
 'ppic':['pgap','pdisc'],'pgap':['ppic','pdisc'],'pdisc':['ppic','pgap'],
 'wmail':['wstory','wart'],'wstory':['wmail','wart'],'wart':['wmail','wstory']}
FUNC_X={'hcheck':'checking in at a hotel and asking about services','hprob':'reporting a problem in a hotel room','air':'travelling by plane and talking at the airport',
 'dsym':'describing symptoms to a doctor','hdoc':'the questions and advice a doctor gives','dpharm':'asking for medicine in a pharmacy',
 'sfit':'trying on clothes and asking about sizes','sret':'returning or changing something you bought','sprice':'asking about prices and discounts',
 'ppic':'describing a photograph in a speaking test','pgap':'managing when you cannot find a word or need time to think','pdisc':'discussing options with a partner in a speaking test',
 'wmail':'writing informal emails and messages','wstory':'telling a story in writing','wart':'giving opinions and reasons in an article or essay'}
import random
def fix(G):
    """Diyalog çeldiricilerini aynı gruptaki başka alt gruplardan (açık uçlu olmayan) seçer."""
    allp=[(s['k'],p) for s in G['sub'] for p in s['items']]
    for k,p in allp:
        pool=[q['en'] for k2,q in allp if k2!=k and '...' not in q['en']]
        if len(pool)<6:pool+=[q['en'] for k2,q in allp if k2!=k and '...' in q['en']]
        d=p['d'];p['d']=(d[0],d[1],random.Random(p['en']).sample(pool,2))
    return G
