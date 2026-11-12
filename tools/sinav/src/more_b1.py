# B1 Preliminary: ek Use of English çalışma parçaları (özgün metin)
def mk(k,id,t,ty,nm,ins,**o):
    d={'k':k,'id':id,'t':t,'ty':ty,'nm':nm,'ti':'Reading Part '+k[1],'ins':ins};d.update(o);return d
MORE={'R':[
mk('R5','b1r5c','Çoktan seçmeli boşluk: Pazar yeri','cloze','Okuma 5 · Çoktan seçmeli boşluk','Metni oku ve her boşluk için en uygun kelimeyi (A, B ya da C) seç.',title='A morning at the market',
 p='Every Saturday morning, my grandfather takes me to the old market in our town. We always (1) ______ early because the best stalls are busy by nine. He likes buying fresh bread and olives, and he never forgets to ask the sellers about their families. Last week, we saw a man (2) ______ shoes from a small van. My grandfather bought a pair, although he (3) ______ already got three at home! "You can never have (4) ______ shoes," he joked. On the way home, it (5) ______ heavily, so we shared one umbrella. I think it was the best part of the day.',
 o=[(['arrive','arrived','arrives'],0,['present-simple']),(['sells','selling','sold'],1,['gerund-infinitive']),(['has','have','is'],0,['present-perfect']),(['too many','too much','so much'],0,['countable-uncountable']),(['was raining','rains','has rained'],0,['past-continuous'])],
 e=['We always + yalın fiil: alışkanlık (Present Simple).','saw a man + -ing: bir adamın ... -diğini gördük.','he has already got: has + V3 (Present Perfect).','shoes sayılabilir çoğul: too many. much sayılamayanlarla kullanılır.','geçmişte süren olay: it was raining.']),
mk('R6','b1r6c','Açık boşluk: Yeni daire','open','Okuma 6 · Açık boşluk','Metni oku ve her boşluğa TEK kelime yaz.',title='A new flat',one=True,
 p='My sister has just moved (1) ______ a new flat near the city centre. It is much smaller (2) ______ her old one, but she says she loves it. The flat is on the third floor, and there (3) ______ a lift, which is useful when she goes shopping. She has lived there (4) ______ two weeks and has already met most of her neighbours. Next weekend she is going to have a party, so she asked me (5) ______ I could help her cook. I told her I would, as long (6) ______ she let me choose the music.',
 a=[['into','to'],['than'],['is'],['for'],['if','whether'],['as']],
 tg=[['prepositions-in-on-at'],['comparatives-superlatives'],['there-is-are'],['present-perfect'],['reported-speech'],['first-conditional']],
 e=['move into a flat: daireye taşınmak.','smaller than: -den daha küçük.','there is a lift: asansör var (tekil).','for two weeks: iki haftadır (süre).','asked me if I could help: evet/hayır sorusunun aktarımı.','as long as: -mek koşuluyla.']),
]}
