# Kalıplar: Şikâyet etmek ve cevap vermek (Berlitz 5/6 "complaint" hedeflerinden esinlenilmiş, özgün) – B1/B2
import sys,os;sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'..'))
from ext_meta import fix
def P(en,tr,lv,reg,ex,extr,d):return {'en':en,'tr':tr,'lv':lv,'reg':reg,'ex':[ex,extr],'d':d}
GROUP={'id':'bcomp','t':'Şikâyet etmek ve çözüm istemek','en':'Making a complaint',
'ins':'Restoranda, mağazada veya çevrimiçi bir hizmette sorun yaşadığında kibarca ama net şikâyet etmek için kalıplar.',
'sub':[
 {'k':'cmp1','t':'Şikâyete başlamak','en':'Starting a complaint','items':[
  P("I'm afraid there's a problem with ...","Maalesef ... ile ilgili bir sorun var","B1","","I'm afraid there's a problem with my order.","Maalesef siparişimle ilgili bir sorun var.",("Hello, how can I help?","___ my order."  ,["I'd like a refund, please.","I expect a reply by Friday."])),
  P("I'd like to make a complaint.","Bir şikâyette bulunmak istiyorum.","B1","resmî","I'd like to make a complaint about the service.","Hizmetle ilgili bir şikâyette bulunmak istiyorum.",("Can I help you?","Yes. ___ about the service."  ,["I'd like a refund, please.","I expect a reply by Friday."])),
  P("I'm writing to complain about ...","... hakkında şikâyet etmek için yazıyorum","B2","","I'm writing to complain about the late delivery.","Geç teslimat hakkında şikâyet etmek için yazıyorum.",("How do you start your email?","___ the late delivery."  ,["I'd like a refund, please.","I expect a reply by Friday."])),
  P("This is not what I ordered.","Sipariş ettiğim bu değil.","B1","","Excuse me, this is not what I ordered.","Pardon, sipariş ettiğim bu değil.",("Here is your meal, sir.","Excuse me, ___"  ,["I'd like a refund, please.","I expect a reply by Friday."])),
 ]},
 {'k':'cmp2','t':'Sorunu açıklamak','en':'Describing the problem','items':[
  P("It stopped working after ...","... sonra çalışmayı bıraktı","B1","","It stopped working after two days.","İki gün sonra çalışmayı bıraktı.",("What's wrong with the kettle?","___ two days."  ,["I'd like a refund, please.","Could you look into it?"])),
  P("The food was cold when it arrived.","Yemek geldiğinde soğuktu.","B1","","The food was cold when it arrived, and the waiter was rude.","Yemek geldiğinde soğuktu ve garson kabaydı.",("What was the problem?","___ and the waiter was rude."  ,["I'd like a refund, please.","Could you look into it?"])),
  P("I've been waiting for over an hour.","Bir saatten fazladır bekliyorum.","B1","","I've been waiting for over an hour, and nobody has helped me.","Bir saatten fazladır bekliyorum ve kimse yardım etmedi.",("Why are you upset?","___ and nobody has helped me."  ,["I'd like a refund, please.","Could you look into it?"])),
  P("It's not as described on the website.","Web sitesinde anlatıldığı gibi değil.","B2","","It's not as described on the website. I expected a sea view.","Web sitesinde anlatıldığı gibi değil. Deniz manzarası bekliyordum.",("Is the room okay?","No. ___ I expected a sea view."  ,["I'd like a refund, please.","Could you look into it?"])),
 ]},
 {'k':'cmp3','t':'Çözüm istemek','en':'Asking for a solution','items':[
  P("I'd like a refund, please.","Para iadesi istiyorum.","B1","","The shirt is damaged, so I'd like a refund, please.","Gömlek hasarlı, bu yüzden para iadesi istiyorum.",("The shirt is damaged.","Then ___"  ,["I'm afraid there's a problem with ...","It stopped working after ..."])),
  P("Could you look into it?","Bunu araştırabilir misiniz?","B1","","My account is wrong. Could you look into it?","Hesabım yanlış. Bunu araştırabilir misiniz?",("My account shows two payments.","___"  ,["I'm afraid there's a problem with ...","It stopped working after ..."])),
  P("I expect a reply by ...","... tarihine kadar bir cevap bekliyorum","B2","resmî","I expect a reply by Friday.","Cuma gününe kadar bir cevap bekliyorum.",("What do you want from us?","___ Friday."  ,["I'm afraid there's a problem with ...","It stopped working after ..."])),
  P("I'm sorry for the inconvenience.","Yaşattığımız rahatsızlık için özür dileriz.","B2","resmî","I'm sorry for the inconvenience. We'll replace it today.","Yaşattığımız rahatsızlık için özür dileriz. Bugün değiştireceğiz.",("The vacuum cleaner doesn't work.","___ We'll replace it today."  ,["I'm afraid there's a problem with ...","It stopped working after ..."])),
 ]},
]}
fix(GROUP)
