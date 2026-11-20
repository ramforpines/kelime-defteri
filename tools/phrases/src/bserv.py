# Kalıplar: Teknik sorun, tamir ve sipariş takibi (Berlitz 6 temalarından esinlenilmiş, özgün) – B1/B2
import sys,os;sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'..'))
from ext_meta import fix
def P(en,tr,lv,reg,ex,extr,d):return {'en':en,'tr':tr,'lv':lv,'reg':reg,'ex':[ex,extr],'d':d}
GROUP={'id':'bserv','t':'Teknik sorun, tamir ve sipariş takibi','en':'Repairs, orders and services',
'ins':'Bozulan bir cihazı anlatmak, tamirci çağırmak, kargo ve posta işlerini sormak için kalıplar.',
'sub':[
 {'k':'sv1','t':'Teknik sorunu anlatmak','en':'Describing a technical problem','items':[
  P("It keeps crashing.","Sürekli donuyor.","B1","","It keeps crashing every time I open it.","Her açışımda sürekli donuyor.",("What's wrong with your app?","___ every time I open it."  ,["Could you send someone to ...?","Where's my parcel?"])),
  P("It won't turn on.","Açılmıyor.","B1","","It won't turn on, even when I charge it.","Şarj etsem de açılmıyor.",("Is the laptop working?","No. ___ even when I charge it."  ,["Could you send someone to ...?","Where's my parcel?"])),
  P("I can't connect to the internet.","İnternete bağlanamıyorum.","B1","","I can't connect to the internet since this morning.","Bu sabahtan beri internete bağlanamıyorum.",("Why can't you send the email?","Because ___ since this morning."  ,["Could you send someone to ...?","Where's my parcel?"])),
  P("I'm having trouble with ...","... ile sorun yaşıyorum","B1","","I'm having trouble with the printer.","Yazıcıyla sorun yaşıyorum.",("What's the problem?","___ the printer."  ,["Could you send someone to ...?","Where's my parcel?"])),
  P("Something seems to be wrong with ...","... ile ilgili bir sorun var gibi","B2","","Something seems to be wrong with the heating.","Isıtmayla ilgili bir sorun var gibi.",("Is it cold in here?","Yes. ___ the heating."  ,["Could you send someone to ...?","Where's my parcel?"])),
 ]},
 {'k':'sv2','t':'Tamirci çağırmak','en':'Calling a repair service','items':[
  P("Could you send someone to ...?","... için birini gönderebilir misiniz?","B1","","Could you send someone to look at the boiler?","Kombiye bakması için birini gönderebilir misiniz?",("What can we do for you?","___ look at the boiler?"  ,["It keeps crashing.","Where's my parcel?"])),
  P("When can you come out?","Ne zaman gelebilirsiniz?","B1","","When can you come out? It's urgent.","Ne zaman gelebilirsiniz? Acil.",("We'll send an engineer.","Great. ___ It's urgent."  ,["It keeps crashing.","Where's my parcel?"])),
  P("What's the estimated cost?","Tahmini maliyet nedir?","B2","","What's the estimated cost of the repair?","Tamirin tahmini maliyeti nedir?",("We can fix it tomorrow.","___ of the repair?"  ,["It keeps crashing.","Where's my parcel?"])),
  P("Is it covered by the warranty?","Garanti kapsamında mı?","B2","","Is it covered by the warranty?","Garanti kapsamında mı?",("The fridge is two years old.","___"  ,["It keeps crashing.","Where's my parcel?"])),
 ]},
 {'k':'sv3','t':'Sipariş ve posta işleri','en':'Orders and the post office','items':[
  P("I'm getting in touch about ...","... konusunda iletişime geçiyorum","B2","","I'm getting in touch about my parcel.","Paketim konusunda iletişime geçiyorum.",("Customer service, can I help?","___ my parcel."  ,["It keeps crashing.","Could you send someone to ...?"])),
  P("Where's my parcel?","Paketim nerede?","B1","","I ordered it last week. Where's my parcel?","Geçen hafta sipariş verdim. Paketim nerede?",("How can I help?","I ordered it last week. ___"  ,["It keeps crashing.","Could you send someone to ...?"])),
  P("I'd like to track my order.","Siparişimi takip etmek istiyorum.","B1","","I'd like to track my order. The number is 4521.","Siparişimi takip etmek istiyorum. Numara 4521.",("What's your question?","___ The number is 4521."  ,["It keeps crashing.","Could you send someone to ...?"])),
  P("How long will it take to arrive?","Ulaşması ne kadar sürer?","B1","","How long will it take to arrive in Canada?","Kanada'ya ulaşması ne kadar sürer?",("I'd like to send this parcel.","___ in Canada?"  ,["It keeps crashing.","Could you send someone to ...?"])),
  P("I'd like to send this by registered post.","Bunu taahhütlü göndermek istiyorum.","B2","","I'd like to send this by registered post, please.","Bunu taahhütlü göndermek istiyorum.",("How would you like to send it?","___"  ,["It keeps crashing.","Could you send someone to ...?"])),
 ]},
]}
fix(GROUP)
