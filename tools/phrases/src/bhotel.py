# Kalıplar: Otelde ve havalimanında (B1 seyahat). P(İngilizce, Türkçe, seviye, üslup, örnek İngilizce, örnek Türkçe, diyalog)
def P(en,tr,lv,reg,ex,extr,d):return {'en':en,'tr':tr,'lv':lv,'reg':reg,'ex':[ex,extr],'d':d}
import sys,os;sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'..'))
from ext_meta import fix
GROUP={'id':'bhotel','t':'Otel ve havalimanı','en':'At the hotel and the airport',
'ins':'Otelde giriş yapmak, hizmet sormak, odadaki sorunu bildirmek ve havalimanında uçuşla ilgili konuşmak için kalıplar.',
'sub':[
 {'k':'hcheck','t':'Otelde giriş ve hizmetler','en':'Checking in and asking about services','items':[
  P("I have a reservation for ...","... için rezervasyonum var","B1","","Good evening. I have a reservation for three nights.","İyi akşamlar. Üç gece için rezervasyonum var.",("Welcome to the Grand Hotel. How can I help you?","___ three nights, in the name of Demir.",["My flight has been delayed.","Could you send someone to fix it?"])),
  P("Is breakfast included?","Kahvaltı dahil mi?","B1","","Is breakfast included in the price?","Kahvaltı fiyata dahil mi?",("The room is 80 euros a night.","___ Or do we pay extra for it?",["I've missed my connection.","Where do I check in?"])),
  P("What time is check-out?","Odayı kaçta boşaltmamız gerekiyor?","B1","","What time is check-out tomorrow?","Yarın odayı kaçta boşaltmamız gerekiyor?",("Your room is number 212. Enjoy your stay.","Thank you. ___",["Could I have a window seat?","The air conditioning doesn't work."])),
  P("Could I have a wake-up call at ...?","Saat ...'de beni telefonla uyandırabilir misiniz?","B2","","Could I have a wake-up call at six thirty?","Saat altı buçukta beni telefonla uyandırabilir misiniz?",("My train leaves very early tomorrow.","___ six thirty, please?",["I'd like to change rooms.","My flight has been delayed."])),
  P("Is there a lift?","Asansör var mı?","A2","","Is there a lift? I have a lot of luggage.","Asansör var mı? Çok bagajım var.",("Your room is on the fifth floor.","___ I have two heavy suitcases.",["Where do I check in?","Is breakfast included?"])),
 ]},
 {'k':'hprob','t':'Odadaki sorunlar','en':'Reporting a problem','items':[
  P("There's a problem with ...","... ile ilgili bir sorun var","B1","","There's a problem with the shower in my room.","Odamdaki duşla ilgili bir sorun var.",("Reception. Can I help you?","Yes, ___ the shower in room 305.",["I've got a sore throat.","Could I try this on?"])),
  P("... doesn't work.","... çalışmıyor.","A2","","The air conditioning doesn't work.","Klima çalışmıyor.",("What seems to be the matter?","The air conditioning ___ It's very hot.",["Is breakfast included?","What time is check-out?"])),
  P("Could you send someone to fix it?","Birini gönderip düzelttirebilir misiniz?","B2","resmî","The lamp is broken. Could you send someone to fix it?","Lamba bozuk. Birini gönderip düzelttirebilir misiniz?",("I'm so sorry about the broken lamp.","___ as soon as possible?",["Is there a lift?","I'd like to check out, please."])),
  P("I'd like to change rooms.","Oda değiştirmek istiyorum.","B1","","The room is too noisy. I'd like to change rooms.","Oda çok gürültülü. Oda değiştirmek istiyorum.",("You can hear the street all night, can't you?","Yes, it's terrible. ___",["Is there a lift?","What time is check-out?"])),
  P("It's much too noisy.","Çok fazla gürültülü.","B1","","I can't sleep. It's much too noisy.","Uyuyamıyorum. Çok fazla gürültülü.",("Did you sleep well?","No. ___ there's a party next door.",["Is breakfast included?","Could I have a wake-up call at ...?"])),
 ]},
 {'k':'air','t':'Havalimanında','en':'At the airport','items':[
  P("Where do I check in?","Check-in'i nerede yaptırırım?","A2","","Excuse me, where do I check in for the flight to Rome?","Affedersiniz, Roma uçuşu için check-in'i nerede yaptırırım?",("I've just arrived at the airport.","___ for my flight to Rome?",["Is there a lift?","I'd like to change rooms."])),
  P("Which gate is the flight to ...?","... uçuşu hangi kapıda?","B1","","Which gate is the flight to Berlin?","Berlin uçuşu hangi kapıdan kalkıyor?",("The screen says boarding at nine.","Yes, but ___ Berlin?",["Is breakfast included?","I have a reservation for ..."])),
  P("My flight has been delayed.","Uçuşum rötar yaptı.","B1","","I'm sorry I'm late. My flight has been delayed.","Geç kaldığım için üzgünüm. Uçuşum rötar yaptı.",("Where are you? We've been waiting for an hour.","I'm still at the airport. ___",["Could I have a window seat?","The air conditioning doesn't work."])),
  P("I've missed my connection.","Aktarma uçuşumu kaçırdım.","B2","","My first plane was late, so I've missed my connection.","İlk uçağım rötar yaptığı için aktarma uçuşumu kaçırdım.",("Is there a problem, madam?","Yes. ___ to Madrid. What can I do?",["Is breakfast included?","What time is check-out?"])),
  P("Could I have a window seat?","Pencere kenarı bir koltuk alabilir miyim?","A2","","Could I have a window seat, please?","Pencere kenarı bir koltuk alabilir miyim, lütfen?",("Here are your boarding pass and passport.","Thanks. ___ I like looking at the clouds.",["I've missed my connection.","My flight has been delayed."])),
 ]},
]}
fix(GROUP)
