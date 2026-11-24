# Kalıplar: Doktorda ve eczanede (B1). P(İngilizce, Türkçe, seviye, üslup, örnek İngilizce, örnek Türkçe, diyalog)
def P(en,tr,lv,reg,ex,extr,d):return {'en':en,'tr':tr,'lv':lv,'reg':reg,'ex':[ex,extr],'d':d}
import sys,os;sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'..'))
from ext_meta import fix
GROUP={'id':'bhealth','t':'Doktor ve eczane','en':'At the doctor\'s and the pharmacy',
'ins':'Belirtileri anlatmak, doktorun sorularını ve önerilerini anlamak, eczanede ilaç istemek için kalıplar.',
'sub':[
 {'k':'dsym','t':'Belirtileri anlatmak','en':'Describing symptoms','items':[
  P("I've got a ...","... var / ... oldum","A2","","I've got a headache and a sore throat.","Başım ağrıyor ve boğazım yanıyor.",("What seems to be the problem?","___ terrible headache.",["You should stay in bed.","Do you have anything for a cough?"])),
  P("I feel dizzy.","Başım dönüyor.","B1","","I feel dizzy when I stand up quickly.","Hızlı ayağa kalkınca başım dönüyor.",("Are you all right? You look pale.","Not really. ___ and a bit sick.",["Take it twice a day.","Do I need a prescription?"])),
  P("It hurts when I ...","... yaptığımda acıyor","B1","","It hurts when I breathe in deeply.","Derin nefes aldığımda acıyor.",("Where exactly is the pain?","In my chest. ___ breathe in.",["How long have you had it?","You should stay in bed."])),
  P("I've had it for ...","... süredir böyle","B1","","I've had it for three days now.","Üç gündür böyle.",("How long have you had the cough?","___ about a week.",["Take it twice a day.","Do I need a prescription?"])),
  P("I think I've caught a cold.","Sanırım üşütmüşüm.","A2","","I think I've caught a cold. I keep sneezing.","Sanırım üşütmüşüm. Sürekli hapşırıyorum.",("Why are you sneezing so much?","___ after the rain yesterday.",["How long have you had it?","Take it twice a day."])),
 ]},
 {'k':'hdoc','t':'Doktorun soruları ve önerileri','en':'What the doctor says','items':[
  P("How long have you had ...?","... ne zamandır var?","B1","","How long have you had this cough?","Bu öksürük ne zamandır var?",("I've been coughing a lot.","___ it?",["I feel dizzy.","Do you have anything for a cough?"])),
  P("You should ...","... yapmalısınız","A2","","You should drink plenty of water and rest.","Bol su içip dinlenmelisiniz.",("I feel weak all the time.","___ rest more and eat well.",["I've got a ...","Do I need a prescription?"])),
  P("Take it twice a day.","Günde iki kez alın.","B1","","Take it twice a day after meals.","Günde iki kez, yemeklerden sonra alın.",("How should I take this medicine?","___ after meals.",["It hurts when I ...","I've had it for ..."])),
  P("Come back if you don't feel better.","İyileşmezseniz tekrar gelin.","B1","","Come back if you don't feel better in a week.","Bir hafta içinde iyileşmezseniz tekrar gelin.",("Thank you, doctor. Is that all?","Yes. ___ in a week.",["I've got a ...","I feel dizzy."])),
  P("It's nothing serious.","Ciddi bir şey değil.","B1","","Don't worry. It's nothing serious.","Endişelenme. Ciddi bir şey değil.",("Doctor, am I seriously ill?","No. ___ You just need some rest.",["It hurts when I ...","I've had it for ..."])),
 ]},
 {'k':'dpharm','t':'Eczanede','en':'At the pharmacy','items':[
  P("Do you have anything for ...?","... için bir şeyiniz var mı?","B1","","Do you have anything for a headache?","Baş ağrısı için bir şeyiniz var mı?",("Good morning. Can I help you?","I have a bad cough. ___ it?",["It hurts when I ...","You should ..."])),
  P("Do I need a prescription?","Reçete gerekiyor mu?","B1","","Do I need a prescription for these tablets?","Bu haplar için reçete gerekiyor mu?",("These are quite strong tablets.","Really? ___ ?",["I've had it for ...","How long have you had ...?"])),
  P("Is it safe to take with ...?","... ile birlikte almak güvenli mi?","B2","","Is it safe to take with my other medicine?","Diğer ilacımla birlikte almak güvenli mi?",("This syrup is very good for sore throats.","I'm already taking antibiotics. ___ them?",["I feel dizzy.","It's nothing serious."])),
  P("Does it have any side effects?","Yan etkisi var mı?","B2","","Does it have any side effects?","Yan etkisi var mı?",("Take one tablet before bed.","___ I have to drive tomorrow.",["Come back if you don't feel better.","Take it twice a day."])),
 ]},
]}
fix(GROUP)
