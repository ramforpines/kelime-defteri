# Kalıplar: Sunum yapma (özgün örnekler)
def P(en,tr,lv,reg,ex,extr,d):return {'en':en,'tr':tr,'lv':lv,'reg':reg,'ex':[ex,extr],'d':d}
GROUP={'id':'gpres','t':'Sunum yapma','en':'Giving a presentation',
'ins':'İyi bir sunum üç bölümden oluşur: başlangıç, bölümler arası geçiş ve kapanış. Her bölümün hazır kalıpları vardır; dinleyiciyi yönlendirdikleri için bunları aynen kullanmak sunumu akıcı ve profesyonel yapar.',
'sub':[
 {'k':'pstart','t':'Sunuma başlama','en':'Starting a presentation','items':[
  P("I'd like to start by ...","... ile başlamak istiyorum","B2","resmî","I'd like to start by thanking you all for coming.","Geldiğiniz için hepinize teşekkür ederek başlamak istiyorum.",("How will you open the talk?","___ thanking everyone.",["Moving on to ...","To sum up ..."])),
  P("Today I'm going to talk about ...","Bugün ... hakkında konuşacağım","B2","","Today I'm going to talk about online learning.","Bugün çevrimiçi öğrenme hakkında konuşacağım.",("What is your topic?","___ climate change.",["This brings me to ...","In conclusion ..."])),
  P("The aim of this talk is to ...","Bu konuşmanın amacı ... -mektir","C1","resmî","The aim of this talk is to explain our new plan.","Bu konuşmanın amacı yeni planımızı açıklamaktır.",("Why are you giving this talk?","___ explain our plan.",["Let's turn to ...","That brings me to the end of ..."])),
  P("I've divided my talk into ...","Konuşmamı ... bölüme ayırdım","C1","resmî","I've divided my talk into three parts.","Konuşmamı üç bölüme ayırdım.",("How is the presentation organised?","___ three parts.",["To sum up ...","Thank you for listening to ..."])),
  P("Feel free to interrupt if ...","... durumunda sözümü kesmekten çekinmeyin","C1","","Feel free to interrupt if you have any questions.","Sorunuz olursa sözümü kesmekten çekinmeyin.",("Can I ask something during the talk?","Of course. ___ you have a question.",["In conclusion ...","Moving on to ..."])),
 ]},
 {'k':'pmove','t':'Bölümler arası geçiş','en':'Moving to the next point','items':[
  P("Moving on to ...","... konusuna geçersek","B2","","Moving on to the next slide, you can see the results.","Sonraki slayta geçersek sonuçları görebilirsiniz.",("What is on the next slide?","___ the results, we see growth.",["I'd like to start by ...","In conclusion ..."])),
  P("Let's turn to ...","Şimdi ... konusuna dönelim","B2","","Let's turn to the second part of the talk.","Şimdi konuşmanın ikinci bölümüne dönelim.",("What comes after the introduction?","___ the main findings.",["Today I'm going to talk about ...","To sum up ..."])),
  P("This brings me to ...","Bu da beni ... konusuna getiriyor","C1","","This brings me to my next point: cost.","Bu da beni bir sonraki noktama, maliyete getiriyor.",("Why are you speaking about costs now?","Well, ___ my next point.",["The aim of this talk is to ...","Feel free to interrupt if ..."])),
  P("I'd now like to look at ...","Şimdi ... konusuna bakmak istiyorum","C1","resmî","I'd now like to look at the data in more detail.","Şimdi verilere daha ayrıntılı bakmak istiyorum.",("What will you discuss next?","___ the data in detail.",["I've divided my talk into ...","This brings me to ..."])),
  P("As you can see from this chart, ...","Bu grafikten de görebileceğiniz gibi, ...","B2","","As you can see from this chart, sales have risen.","Bu grafikten de görebileceğiniz gibi satışlar arttı.",("What does the chart show?","___ sales have risen.",["Let's turn to ...","In conclusion ..."])),
 ]},
 {'k':'pend','t':'Sunumu bitirme','en':'Concluding a presentation','items':[
  P("To sum up ...","Özetlemek gerekirse ...","B2","","To sum up, we need to act quickly.","Özetlemek gerekirse hızlı hareket etmemiz gerekiyor.",("How do you end the talk?","___ we need to act now.",["Moving on to ...","I'd like to start by ..."])),
  P("In conclusion ...","Sonuç olarak ...","B2","resmî","In conclusion, the project was a success.","Sonuç olarak proje başarılıydı.",("What is your final point?","___ the plan works.",["This brings me to ...","Let's turn to ..."])),
  P("That brings me to the end of ...","Bu da ... bölümünün sonuna geldiğimiz anlamına geliyor","C1","resmî","That brings me to the end of my presentation.","Bu da sunumumun sonuna geldiğimiz anlamına geliyor.",("Is the talk over?","Yes. ___ my talk.",["I'd now like to look at ...","The aim of this talk is to ..."])),
  P("Thank you for listening to ...","... dinlediğiniz için teşekkürler","B2","","Thank you for listening to my talk, and I'm happy to answer questions.","Dinlediğiniz için teşekkürler, sorularınızı yanıtlamaktan memnuniyet duyarım.",("How do you close the talk?","I say, '___ my talk.'",["Today I'm going to talk about ...","As you can see from this chart, ..."])),
  P("I'd be happy to answer ...","... yanıtlamaktan memnuniyet duyarım","C1","resmî","I'd be happy to answer any questions you may have.","Sorularınızı yanıtlamaktan memnuniyet duyarım.",("What happens after the talk?","___ any questions now.",["Feel free to interrupt if ...","Moving on to ..."])),
 ]},
]}
