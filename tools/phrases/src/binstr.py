# Kalıplar: Talimat vermek ve uyarmak – B1. P(İngilizce, Türkçe, seviye, üslup, örnek İngilizce, örnek Türkçe, diyalog)
import sys,os;sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'..'))
from ext_meta import fix
def P(en,tr,lv,reg,ex,extr,d):return {'en':en,'tr':tr,'lv':lv,'reg':reg,'ex':[ex,extr],'d':d}
GROUP={'id':'binstr','t':'Talimat vermek ve uyarmak','en':'Giving instructions and warnings',
'ins':'Bir şeyin nasıl yapıldığını adım adım anlatmak, uyarmak ve anlaşıldığını kontrol etmek için kalıplar.',
'sub':[
 {'k':'istep','t':'Adım adım anlatmak','en':'Step by step','items':[
  P("It's very easy.","Çok kolay.","A2","","Don't worry. It's very easy.","Endişelenme. Çok kolay.",("Is it difficult to use?","No, ___"  ,["Make sure you ...","Is that clear?"])),
  P("Let's do it together.","Hadi birlikte yapalım.","A2","","Let's do it together. I'll show you.","Hadi birlikte yapalım. Sana göstereceğim.",("I've never done this before.","___ I'll show you."  ,["Make sure you ...","Is that clear?"])),
  P("First of all, ...","Her şeyden önce, ...","B1","","First of all, wash your hands.","Her şeyden önce ellerini yıka.",("How do I make the sauce?","___ chop the onions."  ,["Make sure you ...","Is that clear?"])),
  P("After that, ...","Bundan sonra, ...","A2","","After that, add the tomatoes.","Bundan sonra domatesleri ekle.",("And then?","___ add the tomatoes."  ,["Take care not to ...","Is that clear?"])),
  P("Once you've done that, ...","Bunu yaptıktan sonra, ...","B1","","Once you've done that, turn off the heat.","Bunu yaptıktan sonra ocağı kapat.",("I've finished mixing it.","___ turn off the heat."  ,["Make sure you ...","Is that clear?"])),
  P("Finally, ...","Son olarak, ...","A2","","Finally, serve it with rice.","Son olarak pilavla servis et.",("Is that all?","Almost. ___ serve it with rice."  ,["Take care not to ...","Is that clear?"])),
 ]},
 {'k':'iwarn','t':'Uyarmak ve hatırlatmak','en':'Warnings and reminders','items':[
  P("Make sure you ...","... olduğundan emin ol","B1","","Make sure you lock the door when you leave.","Çıkarken kapıyı kilitlediğinden emin ol.",("I'm going out now.","OK. ___ lock the door."  ,["First of all, ...","Is that clear?"])),
  P("Take care not to ...","... -memeye dikkat et","B1","","Take care not to drop the plates.","Tabakları düşürmemeye dikkat et.",("Can I carry these?","Yes, but ___ drop them."  ,["First of all, ...","Is that clear?"])),
  P("Mind your step.","Adımına dikkat et.","B1","","Mind your step. The floor is wet.","Adımına dikkat et. Zemin ıslak.",("Why is there a sign?","___ The floor is wet."  ,["First of all, ...","Is that clear?"])),
  P("Better safe than sorry.","İhtiyatlı olmakta fayda var.","B2","","Take an umbrella. Better safe than sorry.","Şemsiye al. İhtiyatlı olmakta fayda var.",("It isn't raining now.","True, but take one. ___"  ,["First of all, ...","Is that clear?"])),
  P("Don't forget to ...","... -meyi unutma","A2","","Don't forget to take your keys.","Anahtarlarını almayı unutma.",("See you later!","Bye! ___ take your keys."  ,["After that, ...","Is that clear?"])),
  P("Whatever you do, don't ...","Ne yaparsan yap, ... -me","B2","","Whatever you do, don't touch the red button.","Ne yaparsan yap, kırmızı düğmeye dokunma.",("Can I press anything?","___ touch the red button."  ,["First of all, ...","Is that clear?"])),
 ]},
 {'k':'ichk','t':'Anlaşıldığını kontrol etmek','en':'Checking understanding','items':[
  P("Is that clear?","Anlaşıldı mı?","A2","","You press this button first. Is that clear?","Önce bu düğmeye basarsın. Anlaşıldı mı?",("So you open the file and save it.","Yes. ___"  ,["First of all, ...","Make sure you ..."])),
  P("Do you see what I mean?","Ne demek istediğimi anlıyor musun?","B1","","You have to hold it like this. Do you see what I mean?","Bunu böyle tutman gerekiyor. Ne demek istediğimi anlıyor musun?",("Like this?","Exactly. ___"  ,["After that, ...","Take care not to ..."])),
  P("Let me know if you get stuck.","Takılırsan haber ver.","B1","","Let me know if you get stuck.","Takılırsan haber ver.",("I think I can do it myself.","OK. ___"  ,["First of all, ...","Take care not to ..."])),
  P("Can you repeat that, please?","Tekrar eder misin lütfen?","A2","","Can you repeat that, please? I missed the last step.","Tekrar eder misin lütfen? Son adımı kaçırdım.",("Then turn it off and unplug it.","Sorry, ___"  ,["Finally, ...","Make sure you ..."])),
 ]},
]}
fix(GROUP)
