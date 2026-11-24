# Kalıplar: Sohbet (hava, hafta sonu, aile) – B1. P(İngilizce, Türkçe, seviye, üslup, örnek İngilizce, örnek Türkçe, diyalog)
import sys,os;sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'..'))
from ext_meta import fix
def P(en,tr,lv,reg,ex,extr,d):return {'en':en,'tr':tr,'lv':lv,'reg':reg,'ex':[ex,extr],'d':d}
GROUP={'id':'bsmall','t':'Sohbet: hava, hafta sonu, aile','en':'Small talk',
'ins':'Tanımadığın ya da az tanıdığın biriyle hava durumu, hafta sonu ve aile hakkında kısa sohbetler için kalıplar.',
'sub':[
 {'k':'mweath','t':'Hava durumu','en':'Talking about the weather','items':[
  P("What awful weather!","Ne berbat hava!","A2","","What awful weather! It hasn't stopped raining all day.","Ne berbat hava! Bütün gün yağmur dinmedi.",("I forgot my umbrella.","___ You'll get wet."  ,["Did you have a good weekend?","How's your family?"])),
  P("It's supposed to ...","...-mesi bekleniyor","B2","","It's supposed to snow tomorrow.","Yarın kar yağması bekleniyor.",("Are we going on the picnic?","I'm not sure. ___ rain."  ,["Did you have a good weekend?","How's your family?"])),
  P("It's freezing today.","Bugün hava buz gibi.","B1","","It's freezing today. Don't forget your gloves.","Bugün hava buz gibi. Eldivenlerini unutma.",("Shall we walk to school?","___ Let's take the bus."  ,["Did you have a good weekend?","How's your family?"])),
  P("I hope it clears up.","Umarım hava açılır.","B1","","I hope it clears up before the match.","Umarım maçtan önce hava açılır.",("The forecast says cloudy all afternoon.","___ I want to go to the park."  ,["How's your family?","What are you up to this weekend?"])),
 ]},
 {'k':'mweek','t':'Hafta sonu ve planlar','en':'Weekends and plans','items':[
  P("Did you have a good weekend?","Hafta sonun güzel geçti mi?","A2","","Did you have a good weekend? What did you do?","Hafta sonun güzel geçti mi? Ne yaptın?",("Hi, Maria! Nice to see you.","Hi! ___ ?"  ,["I hope it clears up.","How's your family?"])),
  P("What are you up to this weekend?","Bu hafta sonu ne yapıyorsun?","B1","samimi","What are you up to this weekend? Any plans?","Bu hafta sonu ne yapıyorsun? Bir planın var mı?",("It's Friday at last!","Yes! ___ ?"  ,["What awful weather!","How's your family?"])),
  P("Nothing special.","Özel bir şey yok.","A2","","Nothing special. I'm just going to relax at home.","Özel bir şey yok. Sadece evde dinleneceğim.",("Are you doing anything exciting?","No, ___ I'm tired."  ,["It's freezing today.","How's your family?"])),
  P("I'm looking forward to ...","... için sabırsızlanıyorum","B1","","I'm looking forward to the summer holidays.","Yaz tatili için sabırsızlanıyorum.",("Are you excited about the trip?","Yes, ___ it."  ,["What awful weather!","It's freezing today."])),
 ]},
 {'k':'mfam','t':'Aile ve arkadaşlar','en':'Family and friends','items':[
  P("How's your family?","Ailen nasıl?","A2","","How's your family? I haven't seen them for ages.","Ailen nasıl? Onları uzun zamandır görmedim.",("Hello, Mr Brown! Nice to see you.","Hello, Anna! ___"  ,["What awful weather!","Nothing special."])),
  P("Give my regards to ...","... 'e selamlarımı ilet","B1","resmî","Give my regards to your parents.","Anne babana selamlarımı ilet.",("I have to go now. Bye!","Goodbye. ___"  ,["What awful weather!","Nothing special."])),
  P("I haven't seen you for ages.","Seni uzun zamandır görmedim.","B1","","I haven't seen you for ages! How are you?","Seni uzun zamandır görmedim! Nasılsın?",("Hello, Sara! Remember me?","Of course! ___"  ,["What awful weather!","Nothing special."])),
  P("We should meet up some time.","Bir ara buluşmalıyız.","B1","","It was great to chat. We should meet up some time.","Sohbet çok güzeldi. Bir ara buluşmalıyız.",("It was good to see you again.","Yes. ___"  ,["What awful weather!","It's freezing today."])),
 ]},
]}
fix(GROUP)
