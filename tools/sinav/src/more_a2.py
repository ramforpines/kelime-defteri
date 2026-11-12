# A2 Key: ek Use of English çalışma parçaları (özgün metin)
def mk(k,id,t,ty,nm,ins,**o):
    d={'k':k,'id':id,'t':t,'ty':ty,'nm':nm,'ti':'Reading Part '+k[1],'ins':ins};d.update(o);return d
MORE={'R':[
mk('R4','a2r4b','Çoktan seçmeli boşluk: Hafta sonum','cloze','Okuma 4 · Çoktan seçmeli boşluk','Metni oku ve her boşluk için en uygun kelimeyi (A, B ya da C) seç.',title='My weekend',
 p='On Saturday I (1) ______ up late because I was tired. After breakfast, I went to the park (2) ______ my friends. We played football for two hours, and then we (3) ______ ice cream. In the evening, I stayed at home and (4) ______ a film. It was (5) ______ than the last one I saw. On Sunday, I\'m going (6) ______ my grandmother\'s house.',
 o=[(['got','get','getting'],0,['past-simple']),(['with','at','for'],0,['prepositions-in-on-at']),(['had','have','having'],0,['past-simple']),(['watching','watched','watch'],1,['past-simple']),(['good','better','best'],1,['comparatives-superlatives']),(['at','to','in'],1,['prepositions-in-on-at'])],
 e=['Saturday: geçmiş, got up (Past Simple).','with my friends: arkadaşlarımla.','geçmiş olay: we had ice cream.','stayed ... and watched: iki geçmiş fiil.','than ile karşılaştırma: better.','go to + yer: to.']),
mk('R5','a2r5b','Açık boşluk: Yeni okul','open','Okuma 5 · Açık boşluk','Metni oku ve her boşluğa TEK kelime yaz.',title='A message about school',one=True,
 p='Hi Lena, I\'m writing (1) ______ tell you about my new school. It is big, and there (2) ______ a lot of students. My favourite lesson (3) ______ English because the teacher is very kind. I usually go home (4) ______ bus, but today my dad picked me up. What (5) ______ you doing on Friday? Do you want (6) ______ come to the cinema with me?',
 a=[['to'],['are'],['is'],['by'],['are'],['to']],
 tg=[['gerund-infinitive'],['there-is-are'],['to-be'],['prepositions-in-on-at'],['to-be'],['gerund-infinitive']],
 e=['amaç: write to tell.','there are + çoğul.','my favourite lesson is: tekil özne.','by bus: otobüsle.','What are you doing: Present Continuous sorusu.','want to + yalın fiil.']),
]}
