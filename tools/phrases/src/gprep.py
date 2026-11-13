# Kalıplar: Edat kalıpları. P(İngilizce, Türkçe, seviye, üslup, örnek İngilizce, örnek Türkçe, diyalog)
def P(en,tr,lv,reg,ex,extr,d):return {'en':en,'tr':tr,'lv':lv,'reg':reg,'ex':[ex,extr],'d':d}
GROUP={'id':'gprep','t':'Edat kalıpları','en':'Prepositions that go with words',
'ins':'Bazı sıfat, fiil ve isimler belli bir edatla birlikte kullanılır. Bu edatları sözcükle birlikte, kalıp olarak öğren; çoğu zaman Türkçeden tahmin edilemez.',
'sub':[
 {'k':'pfeel','t':'Duygu ve yetenek (sıfat + edat)','en':'Feelings and abilities','items':[
  P("afraid of ...","... -den korkan","A2","","I'm afraid of spiders.","Örümceklerden korkarım.",("Why won't you touch it?","I'm ___ spiders.",["depend on ...","a reason for ..."])),
  P("good at ...","... konusunda iyi","A2","","She is good at maths.","Matematikte iyidir.",("Why does everyone ask Sara for help with homework?","She's ___ maths.",["belong to ...","an increase in ..."])),
  P("interested in ...","... ile ilgilenen","A2","","He's interested in history.","Tarihle ilgileniyor.",("Why does he go to the museum so often?","He's really ___ history.",["succeed in ...","a lack of ..."])),
  P("keen on ...","... -e meraklı, ... -i seven","B1","","My sister is keen on climbing.","Kız kardeşim dağcılığa meraklı.",("Does your sister like sport?","Yes, she's ___ climbing.",["believe in ...","a demand for ..."])),
  P("proud of ...","... ile gurur duyan","B1","","I'm proud of my daughter.","Kızımla gurur duyuyorum.",("How do you feel about her exam result?","I'm so ___ her.",["rely on ...","the key to ..."])),
  P("fond of ...","... -i seven, ... -e düşkün","B2","","She's very fond of her grandmother.","Büyükannesini çok sever.",("Are they close?","Yes, she's very ___ her grandmother.",["complain about ...","a solution to ..."])),
  P("tired of ...","... -den bıkmış","B1","","I'm tired of waiting.","Beklemekten bıktım.",("Why are you leaving?","I'm ___ waiting.",["ask for ...","a reason for ..."])),
 ]},
 {'k':'pdep','t':'Güven ve inanç (fiil + edat)','en':'Depending on, believing in and belonging to','items':[
  P("depend on ...","... -e bağlı olmak, ... -e güvenmek","B1","","You can depend on me.","Bana güvenebilirsin.",("Will you help me move?","Of course. You can ___ me.",["afraid of ...","an increase in ..."])),
  P("rely on ...","... -e güvenmek, ... -e bel bağlamak","B2","","You can rely on her to be on time.","Zamanında geleceğine güvenebilirsin.",("Is she a good manager?","Yes, you can ___ her to be on time.",["interested in ...","a lack of ..."])),
  P("believe in ...","... -e inanmak","B1","","I believe in hard work.","Çok çalışmaya inanırım.",("What's your secret to success?","I ___ hard work.",["proud of ...","a demand for ..."])),
  P("belong to ...","... -e ait olmak","B1","","Does this jacket belong to you?","Bu ceket senin mi?",("Is this your jacket?","No, it doesn't ___ me.",["good at ...","a lack of ..."])),
  P("succeed in ...","... -de başarılı olmak","B2","","I hope to succeed in getting the job.","İşi almayı başarmayı umuyorum.",("What are your goals this year?","I hope to ___ getting a better job.",["tired of ...","a reason for ..."])),
 ]},
 {'k':'pcomm','t':'Özür, şikâyet ve rica','en':'Apologising, complaining and asking','items':[
  P("apologise for ...","... için özür dilemek","B1","","I must apologise for being late.","Geç kaldığım için özür dilemeliyim.",("You're twenty minutes late!","I'm so sorry. I must ___ being late.",["fond of ...","a lack of ..."])),
  P("complain about ...","... hakkında şikâyet etmek","B1","","Please don't complain about the food.","Lütfen yemekten şikâyet etme.",("What's wrong with the soup?","Nothing. Please don't ___ it.",["keen on ...","a solution to ..."])),
  P("ask for ...","... istemek","A2","","You can ask for help at any time.","İstediğin zaman yardım isteyebilirsin.",("I don't understand this exercise.","You can ___ help at any time.",["proud of ...","a lack of ..."])),
  P("grateful for ...","... için minnettar","B2","","I'm grateful for your support.","Desteğin için minnettarım.",("Thank you so much for everything.","I'm really ___ your support.",["succeed in ...","an increase in ..."])),
 ]},
 {'k':'pnoun','t':'İsim + edat','en':'Nouns with prepositions','items':[
  P("a reason for ...","... için bir neden","B1","","Is there a reason for this delay?","Bu gecikmenin bir nedeni var mı?",("The train has stopped again.","Is there ___ this delay?",["afraid of ...","rely on ..."])),
  P("an increase in ...","... -de artış","B2","","There has been an increase in prices.","Fiyatlarda artış oldu.",("Why is everyone complaining?","There has been ___ prices.",["good at ...","depend on ..."])),
  P("a solution to ...","... -in çözümü","B2","","We need a solution to this problem.","Bu soruna bir çözüm bulmalıyız.",("The printer is broken again.","We need ___ this problem.",["interested in ...","believe in ..."])),
  P("a lack of ...","... eksikliği","B2","","The project failed because of a lack of money.","Proje para eksikliği yüzünden başarısız oldu.",("Why did the project fail?","It failed because of ___ money.",["proud of ...","rely on ..."])),
  P("a demand for ...","... -e talep","B2","","There is a demand for electric cars.","Elektrikli araçlara talep var.",("Why are more factories making electric cars?","Because there is ___ electric cars.",["keen on ...","apologise for ..."])),
  P("the key to ...","... -in anahtarı","B2","","Practice is the key to success.","Pratik, başarının anahtarıdır.",("How can I speak better English?","Practice is ___ success.",["believe in ...","ask for ..."])),
 ]},
 {'k':'pfix','t':'Sabit edatlı öbekler','en':'Fixed prepositional phrases','items':[
  P("in charge of ...","... -den sorumlu","B1","","Who is in charge of this project?","Bu projeden kim sorumlu?",("I have a question about the project.","Ask Anna. She's ___ it.",["afraid of ...","a demand for ..."])),
  P("on behalf of ...","... adına","B2","resmî","I'm writing on behalf of the whole team.","Tüm ekip adına yazıyorum.",("Who is this email from?","I'm writing ___ the whole team.",["afraid of ...","rely on ..."])),
  P("in terms of ...","... açısından","C1","resmî","In terms of price, this phone is the best.","Fiyat açısından bu telefon en iyisi.",("Which phone should I buy?","___ price, this one is the best.",["good at ...","depend on ..."])),
  P("as a result of ...","... sonucunda","B2","","As a result of the storm, the match was cancelled.","Fırtına sonucunda maç iptal edildi.",("Why was the match cancelled?","___ the storm.",["keen on ...","apologise for ..."])),
  P("in addition to ...","... -in yanı sıra","B2","","In addition to English, she speaks German.","İngilizcenin yanı sıra Almanca da konuşuyor.",("Does she speak other languages?","___ English, she speaks German.",["afraid of ...","complain about ..."])),
 ]},
]}
