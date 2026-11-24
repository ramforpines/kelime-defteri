# Kalıplar: Davet ve buluşma – B1. P(İngilizce, Türkçe, seviye, üslup, örnek İngilizce, örnek Türkçe, diyalog)
import sys,os;sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'..'))
from ext_meta import fix
def P(en,tr,lv,reg,ex,extr,d):return {'en':en,'tr':tr,'lv':lv,'reg':reg,'ex':[ex,extr],'d':d}
GROUP={'id':'binvite','t':'Davet etmek ve buluşmak','en':'Invitations and arrangements',
'ins':'Birini davet etmek, daveti kabul ya da reddetmek, buluşma saatini ve yerini ayarlamak için kalıplar.',
'sub':[
 {'k':'iinv','t':'Davet etmek','en':'Inviting someone','items':[
  P("Would you like to come to ...?","... gelmek ister misin?","B1","","Would you like to come to my birthday party?","Doğum günü partime gelmek ister misin?",("I'm having a party on Saturday.","___ ?"  ,["Sorry, I won't be able to come.","Shall we meet outside the cinema?"])),
  P("I'd like to invite you to ...","... ister misin diye düşünüyordum","B2","","I'd like to invite you to dinner on Friday.","Seni cuma günü akşam yemeğine davet etmek istiyorum.",("Are you free on Friday evening?","Yes. Why?  ___ dinner?"  ,["Sorry, I won't be able to come.","What time shall we meet?"])),
  P("Are you doing anything on ...?","... günü bir şey yapıyor musun?","A2","","Are you doing anything on Sunday afternoon?","Pazar öğleden sonra bir şey yapıyor musun?",("I'd like to see you soon.","___ Sunday?"  ,["I'd love to, thanks.","Let's make it six o'clock."])),
  P("Why don't you join us?","Neden bize katılmıyorsun?","B1","","We're going for a picnic. Why don't you join us?","Pikniğe gidiyoruz. Neden bize katılmıyorsun?",("What are you doing this weekend?","We're going for a picnic. ___"  ,["Sorry, I won't be able to come.","Let's make it six o'clock."])),
 ]},
 {'k':'iacc','t':'Kabul etmek ve reddetmek','en':'Accepting and declining','items':[
  P("I'd love to, thanks.","Çok isterim, teşekkürler.","A2","","I'd love to, thanks. What time?","Çok isterim, teşekkürler. Saat kaçta?",("Would you like to come to the cinema?","___ What time?"  ,["Why don't you join us?","Let's make it six o'clock."])),
  P("Sorry, I won't be able to come.","Maalesef gelemeyeceğim.","B1","","Sorry, I won't be able to come on Saturday.","Maalesef cumartesi gelemeyeceğim.",("Are you coming to the party?","___ I have to work."  ,["Why don't you join us?","Shall we meet outside the cinema?"])),
  P("That sounds like fun.","Kulağa harika geliyor.","A2","","That sounds like fun. I'll bring some drinks.","Kulağa harika geliyor. İçecek getiririm.",("We're going to the beach tomorrow.","___ Can I bring anything?"  ,["Are you doing anything on ...?","What time shall we meet?"])),
  P("Perhaps some other time.","Belki başka zaman.","B1","","Thanks for asking, but perhaps some other time.","Sorduğun için teşekkürler ama belki başka zaman.",("Do you want to go bowling tonight?","I'm tired. ___"  ,["That sounds like fun.","Why don't you join us?"])),
 ]},
 {'k':'iarr','t':'Buluşma saati ve yeri','en':'Arranging a time and place','items':[
  P("What time shall we meet?","Saat kaçta buluşalım?","A2","","What time shall we meet tomorrow?","Yarın saat kaçta buluşalım?",("OK, the cinema it is.","___ ?"  ,["Sorry, I won't be able to come.","Perhaps some other time."])),
  P("Let's make it ...","... olsun / ... yapalım","B1","","Let's make it six o'clock at the station.","Saat altıda istasyonda buluşalım.",("Is five too early for you?","A bit. ___ six o'clock."  ,["Perhaps some other time.","That sounds like fun."])),
  P("Shall we meet outside ...?","... önünde buluşalım mı?","B1","","Shall we meet outside the cinema?","Sinemanın önünde buluşalım mı?",("Where should we meet?","___ ?"  ,["I'd love to, thanks.","Are you doing anything on ...?"])),
  P("See you there.","Orada görüşürüz.","A2","samimi","OK, six o'clock. See you there!","Tamam, saat altı. Orada görüşürüz!",("So we'll meet at the cinema at six.","Yes. ___"  ,["Perhaps some other time.","Sorry, I won't be able to come."])),
 ]},
]}
fix(GROUP)
