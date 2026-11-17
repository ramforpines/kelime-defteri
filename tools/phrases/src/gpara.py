# Kalıplar: Başka sözcüklerle anlatma (özgün örnekler)
def P(en,tr,lv,reg,ex,extr,d):return {'en':en,'tr':tr,'lv':lv,'reg':reg,'ex':[ex,extr],'d':d}
GROUP={'id':'gpara','t':'Başka sözcüklerle anlatma','en':'Paraphrasing and explaining',
'ins':'Konuşurken bir kelimeyi hatırlayamadığında susma, başka sözcüklerle anlat. Bu hem konuşmayı sürdürür hem de speaking sınavlarında kelime bilginin geniş olduğunu gösterir. Üç yol var: kelimeyi sormak, aynı şeyi başka türlü söylemek ve yaklaşık anlatmak.',
'sub':[
 {'k':'wnoword','t':'Kelimeyi bulamama','en':'When you cannot find the word','items':[
  P("I can't think of the word for ...","... in kelimesi aklıma gelmiyor","B2","","I can't think of the word for this tool.","Bu aletin kelimesi aklıma gelmiyor.",("What do you call that thing?","Sorry, ___ it.",["In other words ...","Roughly speaking ..."])),
  P("What's the word for ...","... in kelimesi nedir?","B2","","What's the word for a person who repairs shoes?","Ayakkabı tamir eden kişiye ne denir?",("I need a repairman.","Wait, ___ a person who fixes shoes?",["That is to say ...","It looks a bit like ..."])),
  P("It's a kind of ...","Bir tür ...","B1","","It's a kind of bird that lives near the sea.","Deniz kenarında yaşayan bir tür kuş.",("What is a gull?","___ bird.",["What I mean is ...","Sort of ..."])),
  P("It's something you use to ...","... için kullandığın bir şey","B2","","It's something you use to cut paper.","Kâğıt kesmek için kullandığın bir şey.",("What is that object?","___ cut paper.",["To put it simply ...","Or rather ..."])),
  P("It looks a bit like ...","Biraz ... a benziyor","B2","","It looks a bit like a small umbrella.","Biraz küçük bir şemsiyeye benziyor.",("Can you describe it?","___ a small umbrella.",["Let me put it another way ...","In other words ..."])),
 ]},
 {'k':'wrephrase','t':'Aynı şeyi başka türlü söyleme','en':'Rephrasing what you said','items':[
  P("In other words ...","Başka bir deyişle ...","B2","","In other words, we do not have enough money.","Başka bir deyişle yeterli paramız yok.",("Why did you say the budget is tight?","___ we do not have enough money.",["I can't think of the word for ...","Sort of ..."])),
  P("What I mean is ...","Demek istediğim şu ...","B2","","What I mean is that the plan is too risky.","Demek istediğim, planın çok riskli olduğu.",("Did you say you dislike the plan?","Not exactly. ___ it is too risky.",["It's a kind of ...","Or rather ..."])),
  P("Let me put it another way ...","Başka türlü anlatayım ...","C1","","Let me put it another way: we cannot afford it.","Başka türlü anlatayım: buna gücümüz yetmez.",("I don't follow you.","___ we cannot afford it.",["It looks a bit like ...","Roughly speaking ..."])),
  P("To put it simply ...","Basitçe söylemek gerekirse ...","C1","","To put it simply, prices are rising faster than wages.","Basitçe söylemek gerekirse fiyatlar ücretlerden hızlı artıyor.",("Can you make it clear?","___ prices rise faster than wages.",["What's the word for ...","It's something you use to ..."])),
  P("That is to say ...","Yani, başka bir ifadeyle ...","C1","resmî","The report is incomplete, that is to say we need more data.","Rapor eksik, yani daha fazla veriye ihtiyacımız var.",("Is the report ready?","No, ___ we need more data.",["Sort of ...","It's a kind of ..."])),
 ]},
 {'k':'wexample','t':'Yaklaşık anlatma','en':'Giving an approximate idea','items':[
  P("Roughly speaking ...","Kabaca söylersek ...","C1","","Roughly speaking, it takes about an hour.","Kabaca söylersek yaklaşık bir saat sürer.",("How long is the trip?","___ it takes an hour.",["In other words ...","What's the word for ..."])),
  P("Or rather ...","Ya da daha doğrusu ...","C1","","He is a teacher, or rather a university lecturer.","O bir öğretmen, ya da daha doğrusu üniversitede öğretim görevlisi.",("Is he a teacher?","Yes, ___ a lecturer.",["It looks a bit like ...","What I mean is ..."])),
  P("Sort of ...","Bir nevi ... gibi bir şey","B2","samimi","It's sort of a small restaurant.","Bir nevi küçük bir restoran gibi.",("What is that place?","___ a small restaurant.",["To put it simply ...","That is to say ..."])),
  P("Something along the lines of ...","... benzeri bir şey","C1","","He said something along the lines of \"I'll think about it\".","\"Düşüneceğim\" gibi bir şey söyledi.",("What did he reply?","He said ___ 'I'll think about it'.",["Let me put it another way ...","It's something you use to ..."])),
  P("More or less ...","Aşağı yukarı ... , kabaca ...","B2","","More or less, the project is finished.","Aşağı yukarı proje bitti.",("Is the project done?","___ finished.",["I can't think of the word for ...","What I mean is ..."])),
 ]},
]}
