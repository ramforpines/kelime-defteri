# Kalıplar: Kolokasyonlar (iş, ekonomi, hukuk)
def P(en,tr,lv,reg,ex,extr,d):return {'en':en,'tr':tr,'lv':lv,'reg':reg,'ex':[ex,extr],'d':d}
GROUP={'id':'gcoll','t':'Kolokasyonlar: iş, ekonomi ve hukuk','en':'Collocations for business, the economy and the law',
'ins':'Kolokasyon, birlikte sık kullanılan sözcük çiftleridir. "Güçlü rekabet" için strong değil fierce competition denir. Bunları çiftler halinde öğrenmek yazı ve konuşmayı doğallaştırır.',
'sub':[
 {'k':'cbiz','t':'İş ve pazarlama','en':'Work and marketing','items':[
  P("fierce competition","sert rekabet","C1","","The company faces fierce competition from overseas.","Şirket yurtdışından sert rekabetle karşılaşıyor.",("Why are prices so low?","There is ___ between the shops.",["serve a sentence","commit a crime"])),
  P("launch a product","bir ürünü piyasaya sürmek","B2","","We plan to launch a product in spring.","Baharda bir ürünü piyasaya sürmeyi planlıyoruz.",("What is the company doing this year?","It will ___ in spring.",["curb inflation","serve a sentence"])),
  P("meet a deadline","son teslim tarihine yetişmek","B2","","She worked all night to meet a deadline.","Bir teslim tarihine yetişmek için bütün gece çalıştı.",("Why is she still at the office?","She must ___ tomorrow.",["serve a sentence","hold a trial"])),
  P("a growing market","büyüyen pazar","B2","","Electric bikes are a growing market.","Elektrikli bisikletler büyüyen bir pazar.",("Why do investors like bikes?","It is ___.",["a rising crime rate","heavy taxation"])),
  P("customer loyalty","müşteri sadakati","C1","","Good service builds customer loyalty.","İyi hizmet müşteri sadakati yaratır.",("How can a shop keep its regular buyers?","By building ___.",["serve a sentence","an economic slowdown"])),
 ]},
 {'k':'cecon','t':'Ekonomi','en':'The economy','items':[
  P("curb inflation","enflasyonu dizginlemek","C1","resmî","The bank raised rates to curb inflation.","Merkez bankası enflasyonu dizginlemek için faizi artırdı.",("Why did the bank raise interest rates?","To ___.",["launch a product","commit a crime"])),
  P("an economic slowdown","ekonomik yavaşlama","C1","resmî","The country is facing an economic slowdown.","Ülke ekonomik bir yavaşlamayla karşı karşıya.",("What worries the experts?","Mostly ___.",["customer loyalty","a fair trial"])),
  P("rising unemployment","artan işsizlik","B2","","Rising unemployment worries young people.","Artan işsizlik gençleri endişelendiriyor.",("What is the biggest problem for graduates?","___.",["fierce competition","a fair trial"])),
  P("heavy taxation","ağır vergilendirme","C1","resmî","Heavy taxation discourages small firms.","Ağır vergilendirme küçük firmaları caydırıyor.",("Why are small firms closing?","They suffer from ___.",["a growing market","serve a sentence"])),
  P("balance the budget","bütçeyi dengelemek","C1","resmî","The government must balance the budget.","Hükümet bütçeyi dengelemek zorunda.",("What is the minister's main task?","To ___.",["meet a deadline","hold a trial"])),
 ]},
 {'k':'cjust','t':'Hukuk ve suç','en':'Crime and the law','items':[
  P("commit a crime","suç işlemek","B2","","He was arrested for planning to commit a crime.","Suç işlemeyi planladığı için tutuklandı.",("Why was he arrested?","He is accused of trying to ___.",["curb inflation","launch a product"])),
  P("a fair trial","adil yargılama","C1","","Everyone has the right to a fair trial.","Herkesin adil yargılanma hakkı vardır.",("What does the law promise?","The right to ___.",["heavy taxation","a growing market"])),
  P("serve a sentence","cezasını çekmek","C1","resmî","He had to serve a sentence of five years.","Beş yıllık cezasını çekmek zorunda kaldı.",("Is he free now?","No, he must ___ of two more years.",["meet a deadline","balance the budget"])),
  P("a rising crime rate","artan suç oranı","C1","","A rising crime rate worries the residents.","Artan suç oranı sakinleri endişelendiriyor.",("Why do people feel unsafe?","Because of ___.",["customer loyalty","an economic slowdown"])),
  P("hold a trial","dava görmek, yargılama yapmak","C1","resmî","The court will hold a trial next month.","Mahkeme gelecek ay yargılama yapacak.",("When will the case be heard?","They will ___ next month.",["launch a product","curb inflation"])),
 ]},
]}
