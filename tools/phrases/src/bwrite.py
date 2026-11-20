# Kalıplar: Yazma sınavı (e-posta, hikâye, makale) – B1. P(İngilizce, Türkçe, seviye, üslup, örnek İngilizce, örnek Türkçe, diyalog)
import sys,os;sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'..'))
from ext_meta import fix
def P(en,tr,lv,reg,ex,extr,d):return {'en':en,'tr':tr,'lv':lv,'reg':reg,'ex':[ex,extr],'d':d}
GROUP={'id':'bwrite','t':'Yazma sınavı','en':'The writing test',
'ins':'E-posta, hikâye ve makale yazarken cümleleri bağlamak, olay anlatmak ve görüş bildirmek için kalıplar.',
'sub':[
 {'k':'wmail','t':'E-posta ve mesaj','en':'Informal emails','items':[
  P("Thanks for your email.","E-postan için teşekkürler.","A2","","Hi Anna, thanks for your email.","Merhaba Anna, e-postan için teşekkürler.",("Dear Ali, I'm happy to hear from you again.","Hi Sara, ___ It was great to hear from you.",["Suddenly, ...","In my opinion, ..."])),
  P("Sorry I haven't written for ages.","Uzun zamandır yazmadığım için üzgünüm.","B1","","Sorry I haven't written for ages, but I've been very busy.","Uzun zamandır yazmadığım için üzgünüm ama çok meşguldüm.",("Where have you been? I haven't heard from you for months.","Hi Mia, ___ I've had so many exams.",["To my surprise, ...","On the other hand, ..."])),
  P("I'm writing to ask ...","... sormak için yazıyorum","B1","","I'm writing to ask if you would like to come to my party.","Partime gelmek ister misin diye sormak için yazıyorum.",("What is your email about?","___ if you can help me with my homework.",["It all started when ...","Not only ... but also ..."])),
  P("Write back soon.","Çabuk cevap yaz.","A2","samimi","I'd love to hear your news. Write back soon!","Haberlerini duymak isterim. Çabuk cevap yaz!",("I'll tell you everything in my next email.","Great! ___",["Suddenly, ...","In the end, ..."])),
  P("Give my love to ...","... 'e sevgilerimi ilet","B1","","Give my love to your parents.","Anne babana sevgilerimi ilet.",("Say hello to your family from me.","Of course. ___ your sister, too.",["Thanks for your email.","Suddenly, ..."])),
 ]},
 {'k':'wstory','t':'Hikâye anlatmak','en':'Telling a story','items':[
  P("It all started when ...","Her şey ... ile başladı","B1","","It all started when I missed the last bus.","Her şey son otobüsü kaçırmamla başladı.",("How did the adventure begin?","___ I lost my phone.",["I'm writing to ask ...","Write back soon."])),
  P("Suddenly, ...","Birdenbire ...","A2","","Suddenly, the lights went out.","Birdenbire ışıklar söndü.",("Everything was quiet in the house.","___ we heard a loud noise.",["Thanks for your email.","I'm writing to ask ..."])),
  P("To my surprise, ...","Şaşırarak gördüm ki ...","B1","","To my surprise, the door was open.","Şaşırarak gördüm ki kapı açıktı.",("Did you find the key?","No, but ___ the door was already open.",["Not only ... but also ...","Write back soon."])),
  P("In the end, ...","Sonunda ...","A2","","In the end, we found the dog in the park.","Sonunda köpeği parkta bulduk.",("Was everything OK after all that?","Yes. ___ everybody was safe.",["Thanks for your email.","I'd like to argue that ..."])),
  P("It was a dark and stormy night.","Karanlık ve fırtınalı bir geceydi.","B2","","It was a dark and stormy night. Nobody was on the street.","Karanlık ve fırtınalı bir geceydi. Sokakta kimse yoktu.",("How does your story begin?","___ Nobody was on the street.",["x","y"])),
  P("I couldn't believe my eyes.","Gözlerime inanamadım.","B1","","I couldn't believe my eyes when I saw the box.","Kutuyu görünce gözlerime inanamadım.",("What did you feel when you saw it?","___ It was full of money.",["x","y"])),
  P("I will never forget ...","... asla unutmayacağım","B1","","I will never forget the day we got lost in the forest.","Ormanda kaybolduğumuz günü asla unutmayacağım.",("That was an exciting summer, wasn't it?","Yes! ___ the night we spent in the tent.",["It all started when ...","Give my love to ..."])),
 ]},
 {'k':'wart','t':'Makale: görüş ve neden','en':'Opinions and reasons in an article','items':[
  P("Personally, I feel that ...","Bana kalırsa ...","A2","","Personally, I feel that homework should be shorter.","Bana kalırsa ev ödevleri daha kısa olmalı.",("Do you think homework is useful?","___ it takes too much time.",["Suddenly, ...","Sorry I haven't written for ages."])),
  P("Another reason is that ...","Bir başka neden ...","B1","","Another reason is that cycling is good for your health.","Bir başka neden, bisikletin sağlığa iyi gelmesi.",("Why do you like cycling?","It's cheap. ___ it's healthy.",["To my surprise, ...","Write back soon."])),
  P("All the same, ...","Buna rağmen ...","B1","","Cars are convenient. All the same, they cause pollution.","Arabalar rahattır. Buna rağmen kirliliğe neden olurlar.",("Cars are fast and comfortable.","Yes, but ___ they cause a lot of pollution.",["It all started when ...","I will never forget ..."])),
  P("For example, ...","Örneğin ...","A2","","Sport is good for you. For example, it keeps your heart strong.","Spor sana iyi gelir. Örneğin kalbini güçlü tutar.",("Why do you think sport is so important?","___ it keeps your heart strong.",["Suddenly, ...","Give my love to ..."])),
  P("There are several reasons for this.","Bunun birkaç nedeni var.","B1","","Many students feel tired. There are several reasons for this.","Birçok öğrenci yorgun hissediyor. Bunun birkaç nedeni var.",("Why are students so tired?","___ They sleep late and study a lot.",["x","y"])),
  P("That is why I agree.","İşte bu yüzden katılıyorum.","B1","","Sport is good for the body. That is why I agree.","Spor vücut için iyi. İşte bu yüzden katılıyorum.",("Do you agree that sport is important?","Yes. ___",["x","y"])),
  P("I'd like to argue that ...","Şunu savunmak isterim: ...","B2","resmî","I'd like to argue that young people need more free time.","Şunu savunmak isterim: gençlerin daha çok boş zamana ihtiyacı var.",("What is the main idea of your essay?","___ young people need more free time.",["In the end, ...","Write back soon."])),
 ]},
]}
fix(GROUP)
