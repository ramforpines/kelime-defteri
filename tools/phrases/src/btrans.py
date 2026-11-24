# Kalıplar: Ulaşım (bilet, saat, taksi) – B1. P(İngilizce, Türkçe, seviye, üslup, örnek İngilizce, örnek Türkçe, diyalog)
import sys,os;sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'..'))
from ext_meta import fix
def P(en,tr,lv,reg,ex,extr,d):return {'en':en,'tr':tr,'lv':lv,'reg':reg,'ex':[ex,extr],'d':d}
GROUP={'id':'btrans','t':'Ulaşım: bilet, saat ve taksi','en':'Transport: tickets, times and taxis',
'ins':'Tren ve otobüs bileti almak, saat ve peron sormak, taksiye binmek için kalıplar.',
'sub':[
 {'k':'ttick','t':'Bilet almak','en':'Buying tickets','items':[
  P("Could I have a return ticket to ...?","... için gidiş-dönüş bilet alabilir miyim?","A2","","Could I have a return ticket to Manchester?","Manchester için gidiş-dönüş bilet alabilir miyim?",("Good morning. Where to?","___ How much is it?",["Which platform does it leave from?","Please drop me off at the corner."])),
  P("Is there a cheaper ticket?","Daha ucuz bir bilet var mı?","B1","","Is there a cheaper ticket for students?","Öğrenciler için daha ucuz bir bilet var mı?",("That's thirty pounds.","___ I'm a student."  ,["What time does the next train leave?","Please drop me off at the corner."])),
  P("Do I have to book in advance?","Önceden rezervasyon yaptırmam gerekiyor mu?","B1","","Do I have to book in advance for this train?","Bu tren için önceden rezervasyon yaptırmam gerekiyor mu?",("This is a very popular route.","Really? ___ ?"  ,["Which platform does it leave from?","Please keep the rest."])),
  P("Can I pay by card?","Kartla ödeyebilir miyim?","A2","","Can I pay by card at the ticket machine?","Bilet makinesinde kartla ödeyebilir miyim?",("That will be fifteen euros.","___ I haven't got any cash."  ,["What time does the next train leave?","Please drop me off at the corner."])),
 ]},
 {'k':'tinfo','t':'Saat, peron ve aktarma','en':'Times, platforms and changes','items':[
  P("What time does the next train leave?","Bir sonraki tren kaçta kalkıyor?","A2","","What time does the next train leave for Bristol?","Bristol'a bir sonraki tren kaçta kalkıyor?",("I have to be in Bristol by noon.","___ for Bristol?"  ,["A return ticket to ..., please.","Please keep the rest."])),
  P("Which platform does it leave from?","Hangi perondan kalkıyor?","A2","","Which platform does it leave from? I am late.","Hangi perondan kalkıyor? Geç kaldım.",("I've got my ticket for Leeds.","Great. ___ ?"  ,["Is there a cheaper ticket?","Please keep the rest."])),
  P("Do I have to change?","Aktarma yapmam gerekiyor mu?","B1","","Do I have to change at Reading?","Reading'de aktarma yapmam gerekiyor mu?",("This train goes to Cardiff.","___ ?"  ,["Is there a cheaper ticket?","Please keep the rest."])),
  P("How long does it take to get to ...?","... yere gitmek ne kadar sürer?","B1","","How long does it take to get to the museum?","Müzeye gitmek ne kadar sürer?",("I want to see the museum today.","___ by bus?"  ,["Please keep the rest.","Is there a cheaper ticket?"])),
  P("How long does the journey take?","Yolculuk ne kadar sürüyor?","B1","","How long does the journey take by bus?","Otobüsle yolculuk ne kadar sürüyor?",("I'm thinking of going to London by coach.","___ ?"  ,["Can I pay by card?","Please keep the rest."])),
 ]},
 {'k':'ttaxi','t':'Taksi ve yolda','en':'In a taxi','items':[
  P("Could you take me to ...?","Beni ...'e götürür müsünüz?","A2","","Could you take me to the airport, please?","Beni havalimanına götürür müsünüz, lütfen?",("Where would you like to go?","___ the station, please?"  ,["Is there a cheaper ticket?","Do I have to change?"])),
  P("Please drop me off at ...","Lütfen beni ...'de bırakın","B1","","Please drop me off at the corner of the street.","Lütfen beni sokağın köşesinde bırakın.",("We're almost at your house.","___ the corner, please."  ,["Which platform does it leave from?","How long does the journey take?"])),
  P("Please keep the rest.","Üstü kalsın.","B1","","That's ten pounds. Please keep the rest.","On pound. Üstü kalsın.",("That's nine pounds fifty.","Here's ten. ___"  ,["Do I have to change?","What time does the next train leave?"])),
  P("How much will it cost?","Ne kadar tutar?","A2","","How much will it cost to get to the airport?","Havalimanına gitmek ne kadar tutar?",("I need a taxi to the airport.","___ ?"  ,["Which platform does it leave from?","Do I have to change?"])),
 ]},
]}
fix(GROUP)
