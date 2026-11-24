# Kalıplar: Misafir ağırlamak ve yemek önermek (Berlitz 5 temalarından esinlenilmiş, özgün) – B1
import sys,os;sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'..'))
from ext_meta import fix
def P(en,tr,lv,reg,ex,extr,d):return {'en':en,'tr':tr,'lv':lv,'reg':reg,'ex':[ex,extr],'d':d}
GROUP={'id':'bhosp','t':'Misafir ağırlamak ve teşekkür notu yazmak','en':'Hosting a visitor',
'ins':'Eve gelen misafiri rahat ettirmek, yemek ve içecek önermek, sonra da teşekkür notu yazmak için kalıplar.',
'sub':[
 {'k':'hs1','t':'Misafiri karşılamak','en':'Welcoming a visitor','items':[
  P("Make yourself at home.","Kendi evinde gibi rahat ol.","B1","","Come in and make yourself at home.","İçeri gel ve kendi evinde gibi rahat ol.",("Thanks for inviting me.","Come in. ___"  ,["Would you like some tea?","Thank you for having me."])),
  P("Let me show you around.","Sana etrafı göstereyim.","B1","","Let me show you around the flat.","Sana daireyi gezdireyim.",("What a lovely place!","Thanks. ___ the flat."  ,["Would you like some tea?","Thank you for having me."])),
  P("Did you have a good journey?","Yolculuk nasıldı?","B1","","Did you have a good journey? You must be tired.","Yolculuk nasıldı? Yorgun olmalısın.",("Hello! Welcome!","Hi. ___ You must be tired."  ,["Would you like some tea?","Thank you for having me."])),
  P("Go ahead and ...","Çekinme, ...","B1","","Go ahead and use the shower.","Çekinme, duşu kullan.",("Is it okay if I wash up?","Of course. ___ use the shower."  ,["Would you like some tea?","Thank you for having me."])),
 ]},
 {'k':'hs2','t':'Yemek ve içecek önermek','en':'Offering food and drink','items':[
  P("Would you like some more ...?","Biraz daha ... ister misin?","B1","","Would you like some more soup?","Biraz daha çorba ister misin?",("This is delicious.","I'm glad. ___ soup?"  ,["Make yourself at home.","Thank you for having me."])),
  P("Help yourself to ...","İstediğin kadar ... al","B1","","Help yourself to some salad.","İstediğin kadar salata al.",("Is the food ready?","Yes. ___ some salad."  ,["Make yourself at home.","Thank you for having me."])),
  P("It's a local speciality.","Bu yöreye özgü bir yemek.","B2","","It's a local speciality. You should try it.","Bu yöreye özgü bir yemek. Denemelisin.",("What's this dish?","___ You should try it."  ,["Make yourself at home.","Thank you for having me."])),
  P("Let's try the local place.","Yerel lokantayı deneyelim.","B1","","Let's try the local place near the harbour.","Limanın yanındaki yerel lokantayı deneyelim.",("Where shall we eat tonight?","___ near the harbour."  ,["Make yourself at home.","Thank you for having me."])),
 ]},
 {'k':'hs3','t':'Teşekkür notu yazmak','en':'Writing a thank-you note','items':[
  P("Thank you for having me.","Beni ağırladığın için teşekkürler.","B1","","Thank you for having me. I had a wonderful time.","Beni ağırladığın için teşekkürler. Harika vakit geçirdim.",("It was great to see you.","Same here. ___ I had a wonderful time."  ,["Make yourself at home.","Help yourself to ..."])),
  P("I'm truly grateful for ...","... için gerçekten minnettarım","B1","","I'm truly grateful for your kindness.","Nazik davranışın için gerçekten minnettarım.",("What do you want to say in the note?","___ your kindness."  ,["Make yourself at home.","Help yourself to ..."])),
  P("It meant a lot to me.","Benim için çok anlamlıydı.","B1","","It meant a lot to me. Thank you for the gift.","Benim için çok anlamlıydı. Hediye için teşekkürler.",("Did you like the gift?","Yes, ___ Thank you for the gift."  ,["Make yourself at home.","Help yourself to ..."])),
  P("I hope we can do it again soon.","Umarım yakında yine yapabiliriz.","B1","","It was a lovely evening. I hope we can do it again soon.","Çok güzel bir akşamdı. Umarım yakında yine yapabiliriz.",("How do you end the note?","It was a lovely evening. ___"  ,["Make yourself at home.","Help yourself to ..."])),
 ]},
]}
fix(GROUP)
