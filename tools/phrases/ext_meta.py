# Yeni kalıp grupları için yakın alt grup ve işlev açıklamaları (build.py okur)
NEAR_X={'nopen':['nmid','nend'],'nmid':['nopen','nend'],'nend':['nopen','nmid'],
 'istep':['iwarn','ichk'],'iwarn':['istep','ichk'],'ichk':['istep','iwarn'],
 'xpos':['xneg','xreact'],'xneg':['xpos','xreact'],'xreact':['xpos','xneg'],
 'ttick':['tinfo','ttaxi'],'tinfo':['ttick','ttaxi'],'ttaxi':['ttick','tinfo'],
 'iinv':['iacc','iarr'],'iacc':['iinv','iarr'],'iarr':['iinv','iacc'],
 'mweath':['mweek','mfam'],'mweek':['mweath','mfam'],'mfam':['mweath','mweek'],
 'jcv':['jint','jask'],'jint':['jcv','jask'],'jask':['jcv','jint'],
 'dconc':['dstress','dchall'],'dstress':['dconc','dchall'],'dchall':['dconc','dstress'],
 'scls':['sdead','shelp'],'sdead':['scls','shelp'],'shelp':['scls','sdead'],
 'hcheck':['hprob','air'],'hprob':['hcheck','air'],'air':['hcheck','hprob'],
 'dsym':['hdoc','dpharm'],'hdoc':['dsym','dpharm'],'dpharm':['dsym','hdoc'],
 'sfit':['sret','sprice'],'sret':['sfit','sprice'],'sprice':['sfit','sret'],
 'ppic':['pgap','pdisc'],'pgap':['ppic','pdisc'],'pdisc':['ppic','pgap'],
 'wmail':['wstory','wart'],'wstory':['wmail','wart'],'wart':['wmail','wstory']}
FUNC_X={'nopen':'starting to tell a story or news','nmid':'keeping a story going','nend':'finishing a story',
 'istep':'giving instructions step by step','iwarn':'warning someone and giving reminders','ichk':'checking understanding of instructions',
 'xpos':'expressing positive feelings','xneg':'expressing annoyance and disappointment','xreact':'reacting to what someone tells you',
 'ttick':'buying tickets','tinfo':'asking about times and platforms','ttaxi':'taking a taxi or asking for directions on the way',
 'iinv':'inviting someone','iacc':'accepting or declining an invitation','iarr':'arranging a time and place to meet',
 'mweath':'talking about the weather','mweek':'asking about someone\'s weekend or plans','mfam':'talking about family and friends',
 'jcv':'writing a job application','jint':'answering questions in a job interview','jask':'asking questions at the end of an interview',
 'dconc':'conceding a point in a debate','dstress':'emphasising your point','dchall':'challenging someone\'s argument politely',
 'scls':'asking your teacher or lecturer for clarification','sdead':'talking about deadlines and assignments','shelp':'asking classmates for help and offering it',
 'hcheck':'checking in at a hotel and asking about services','hprob':'reporting a problem in a hotel room','air':'travelling by plane and talking at the airport',
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
