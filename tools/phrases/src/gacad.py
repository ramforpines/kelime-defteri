# Kalıplar: Akademik yazım kalıpları
def P(en,tr,lv,reg,ex,extr,d):return {'en':en,'tr':tr,'lv':lv,'reg':reg,'ex':[ex,extr],'d':d}
GROUP={'id':'gacad','t':'Akademik yazım kalıpları','en':'Academic writing patterns',
'ins':'Makale ve sınav yazılarında (IELTS, TOEFL, üniversite ödevleri) sık geçen kalıplar: veri anlatma, neden-sonuç, çekinceli ifade ve kaynak gösterme.',
'sub':[
 {'k':'atrend','t':'Veri ve eğilim anlatma','en':'Describing data and trends','items':[
  P("account for ...","... oranında olmak, ... -i oluşturmak","C1","resmî","Students account for 40% of all visitors.","Ziyaretçilerin %40'ını öğrenciler oluşturuyor.",("Who uses the library most?","Students ___ 40% of all visitors.",["lead to ...","it is generally accepted that ..."])),
  P("a significant increase in ...","... -de önemli bir artış","B2","resmî","The survey shows a significant increase in online shopping.","Anket, çevrimiçi alışverişte önemli bir artış gösteriyor.",("What does the survey show?","It shows ___ online shopping.",["tend to ...","according to ..."])),
  P("remain stable at ...","... düzeyinde sabit kalmak","B2","","Prices are expected to remain stable at this level.","Fiyatların bu düzeyde sabit kalması bekleniyor.",("What will happen to prices?","They are expected to ___ this level.",["give rise to ...","it is generally accepted that ..."])),
  P("fluctuate around ...","... civarında dalgalanmak","C1","","Sales fluctuate around 300 units a month.","Satışlar ayda 300 adet civarında dalgalanıyor.",("Are monthly sales steady?","No, they ___ 300 units a month.",["account for ...","relative to ..."])),
 ]},
 {'k':'acause','t':'Neden ve sonuç','en':'Cause and effect','items':[
  P("lead to ...","... -e yol açmak","B2","","Poor sleep can lead to health problems.","Kötü uyku sağlık sorunlarına yol açabilir.",("Why is sleep so important?","Poor sleep can ___ health problems.",["according to ...","tend to ..."])),
  P("give rise to ...","... -e neden olmak, ... -i doğurmak","C1","resmî","Rapid growth may give rise to new problems.","Hızlı büyüme yeni sorunlara yol açabilir.",("Is fast growth always good?","No, it may ___ new problems.",["account for ...","remain stable at ..."])),
  P("result from ...","... -den kaynaklanmak","B2","","Most accidents result from carelessness.","Kazaların çoğu dikkatsizlikten kaynaklanır.",("What causes most accidents?","Most of them ___ carelessness.",["a significant increase in ...","relative to ..."])),
  P("owing to ...","... nedeniyle","B2","resmî","The event was cancelled owing to bad weather.","Etkinlik kötü hava nedeniyle iptal edildi.",("Why was the event cancelled?","It was cancelled ___ bad weather.",["tend to ...","it is generally accepted that ..."])),
  P("contribute to ...","... -e katkıda bulunmak, ... -e yol açmak","B2","","Stress can contribute to heart disease.","Stres kalp hastalığına yol açabilir.",("Is stress really dangerous?","Yes, it can ___ heart disease.",["remain stable at ...","according to ..."])),
 ]},
 {'k':'ahedge','t':'Çekinceli ifade','en':'Hedging and generalising','items':[
  P("tend to ...","... eğiliminde olmak","B2","","Young people tend to prefer online news.","Gençler çevrimiçi haberleri tercih etme eğiliminde.",("Where do young people read the news?","They ___ prefer online news.",["lead to ...","account for ..."])),
  P("it is generally accepted that ...","... yaygın olarak kabul edilir","B2","resmî","It is generally accepted that exercise improves memory.","Egzersizin hafızayı geliştirdiği genel olarak kabul edilir.",("Does exercise help the brain?","___ exercise improves memory.",["owing to ...","fluctuate around ..."])),
  P("as a consequence of ...","... -in sonucu olarak","B2","","As a consequence of the storm, the school was closed.","Fırtınanın sonucu olarak okul kapatıldı.",("Why was the school closed?","___ the storm.",["according to ...","result from ..."])),
  P("it can be said that ...","... savunulabilir","C1","resmî","It can be said that the law is unfair.","Yasanın adaletsiz olduğu söylenebilir.",("Is the new law fair?","___ the law is unfair.",["give rise to ...","relative to ..."])),
 ]},
 {'k':'asource','t':'Kaynak ve karşılaştırma','en':'Sources and comparison','items':[
  P("according to ...","... -e göre","B1","","According to the report, crime is falling.","Rapora göre suç oranı düşüyor.",("Is crime going up?","___ the report, it is falling.",["tend to ...","lead to ..."])),
  P("relative to ...","... ile karşılaştırıldığında","C1","resmî","Relative to villages, cities attract many people.","Köylerle karşılaştırıldığında şehirler çok insanı çekiyor.",("Where do most people want to live?","___ villages, cities attract many people.",["owing to ...","a significant increase in ..."])),
  P("in contrast to ...","... ile karşılaştırıldığında, ... -in aksine","B2","resmî","In contrast to men, women live longer on average.","Erkeklerin aksine kadınlar ortalama daha uzun yaşıyor.",("Who lives longer?","___ men, women live longer on average.",["result from ...","remain stable at ..."])),
  P("the findings suggest that ...","bulgular ... olduğunu gösteriyor","C1","resmî","The findings suggest that sleep affects learning.","Bulgular uykunun öğrenmeyi etkilediğini gösteriyor.",("What did the study find?","___ sleep affects learning.",["account for ...","contribute to ..."])),
 ]},
]}
