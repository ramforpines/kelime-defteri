# Kalıplar: Olay anlatmak – B1. P(İngilizce, Türkçe, seviye, üslup, örnek İngilizce, örnek Türkçe, diyalog)
import sys,os;sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'..'))
from ext_meta import fix
def P(en,tr,lv,reg,ex,extr,d):return {'en':en,'tr':tr,'lv':lv,'reg':reg,'ex':[ex,extr],'d':d}
GROUP={'id':'bnarr','t':'Olay anlatmak','en':'Telling a story',
'ins':'Konuşmada bir olayı anlatmaya başlamak, sürdürmek ve bitirmek için kalıplar.',
'sub':[
 {'k':'nopen','t':'Anlatıya başlamak','en':'Starting','items':[
  P("Guess what happened!","Ne oldu tahmin et!","B1","samimi","Guess what happened! I met my favourite singer.","Ne oldu tahmin et! En sevdiğim şarkıcıyla tanıştım.",("You look so happy today.","Yes! ___ I met my favourite singer."  ,["Anyway, ...","Luckily, ..."])),
  P("You won't believe this, but ...","İnanmayacaksın ama ...","B1","samimi","You won't believe this, but I found a wallet full of money.","İnanmayacaksın ama içi para dolu bir cüzdan buldum.",("What's the news?","___ I found a wallet full of money."  ,["Anyway, ...","What a relief!"])),
  P("I'll never forget the time ...","... zamanı asla unutmam","B1","","I'll never forget the time we got lost in Rome.","Roma'da kaybolduğumuz zamanı asla unutmam.",("Do you remember our holiday?","Of course! ___ we got lost in Rome."  ,["Luckily, ...","In the end, ..."])),
  P("Listen to this!","Şunu dinle!","B1","samimi","Listen to this! My neighbour won the lottery.","Şunu dinle! Komşum piyangoyu kazandı.",("Do you have any news?","Yes! ___ My neighbour won the lottery."  ,["Anyway, ...","What a relief!"])),
  P("Did I tell you about ...?","... hakkında sana anlattım mı?","B1","samimi","Did I tell you about my trip to Italy?","İtalya gezimi sana anlattım mı?",("Guess what I did in July.","Wait. ___ my trip to Italy?"  ,["Anyway, ...","What a relief!"])),
 ]},
 {'k':'nmid','t':'Anlatıyı sürdürmek','en':'Keeping the story going','items':[
  P("Apparently, ...","Anlaşılan ...","B2","","Apparently, the shop had been closed for a week.","Anlaşılan dükkân bir haftadır kapalıymış.",("Why was nobody there?","___ the shop had been closed for a week."  ,["Guess what happened!","What a relief!"])),
  P("As it turned out, ...","Sonradan anlaşıldı ki ...","B2","","As it turned out, the key had been in my pocket.","Sonradan anlaşıldı ki anahtar cebimdeymiş.",("Did you find the key?","Yes. ___ it was in my pocket."  ,["Guess what happened!","What a relief!"])),
  P("The next thing I knew, ...","Bir de baktım ki ...","B2","","The next thing I knew, the lights had gone out.","Bir de baktım ki ışıklar sönmüştü.",("What happened at the cinema?","I was watching the film, and ___ the lights were out."  ,["Guess what happened!","Anyway, ..."])),
  P("Meanwhile, ...","Bu arada ...","B1","","Meanwhile, my sister was waiting at the station.","Bu arada kız kardeşim istasyonda bekliyordu.",("I was in the shop for an hour.","And ___ my sister was waiting outside."  ,["Guess what happened!","What a relief!"])),
 ]},
 {'k':'nend','t':'Anlatıyı bitirmek','en':'Finishing','items':[
  P("Luckily, ...","Neyse ki ...","B1","","Luckily, nobody was hurt.","Neyse ki kimse yaralanmadı.",("Was the accident serious?","No. ___ nobody was hurt."  ,["Did I tell you about ...?","Apparently, ..."])),
  P("Thank goodness for that!","Çok şükür!","B1","","Thank goodness for that! I thought I had lost it.","Çok şükür! Kaybettiğimi sandım.",("I found your phone.","___ I thought I had lost it."  ,["Guess what happened!","Apparently, ..."])),
  P("It was a close call.","Kıl payı kurtuldum.","B2","","It was a close call. The train nearly hit the car.","Kıl payı kurtuldum. Tren neredeyse arabaya çarpıyordu.",("Were you in danger?","Yes. ___"  ,["Guess what happened!","Apparently, ..."])),
  P("What a relief!","Ne büyük rahatlık!","B1","","The exam is over. What a relief!","Sınav bitti. Ne büyük rahatlık!",("The results are good!","___"  ,["Did I tell you about ...?","Apparently, ..."])),
  P("Anyway, ...","Neyse, ...","B1","samimi","Anyway, that's enough about me. How are you?","Neyse, benden bu kadar. Sen nasılsın?",("... and then the bus left without me.","Oh no! ___ you made it in the end."  ,["Did I tell you about ...?","Apparently, ..."])),
  P("To cut a long story short, ...","Uzun lafın kısası, ...","B2","","To cut a long story short, we missed the plane.","Uzun lafın kısası, uçağı kaçırdık.",("What happened at the airport?","Well, ___ we missed the plane."  ,["Did I tell you about ...?","Apparently, ..."])),
 ]},
]}
fix(GROUP)
