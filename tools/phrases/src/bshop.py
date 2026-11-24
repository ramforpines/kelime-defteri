# Kalıplar: Alışveriş (beden, iade, fiyat) – B1. P(İngilizce, Türkçe, seviye, üslup, örnek İngilizce, örnek Türkçe, diyalog)
import sys,os;sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'..'))
from ext_meta import fix
def P(en,tr,lv,reg,ex,extr,d):return {'en':en,'tr':tr,'lv':lv,'reg':reg,'ex':[ex,extr],'d':d}
GROUP={'id':'bshop','t':'Alışverişte beden, iade ve fiyat','en':'Shopping: sizes, returns and prices',
'ins':'Mağazada denemek, beden sormak, aldığın şeyi iade ya da değiştirmek ve fiyat pazarlığı yapmak için kalıplar.',
'sub':[
 {'k':'sfit','t':'Deneme ve beden','en':'Trying on and sizes','items':[
  P("Can I try this on?","Bunu deneyebilir miyim?","A2","","Can I try this on, please?","Bunu deneyebilir miyim, lütfen?",("What do you think of this jacket?","It's lovely. ___",["I'd like to return this.","Is there a discount?"])),
  P("Where are the fitting rooms?","Deneme kabinleri nerede?","A2","","Excuse me, where are the fitting rooms?","Affedersiniz, deneme kabinleri nerede?",("I'd like to try on these two shirts.","Of course. ___ ?",["Do you have the receipt?","It's too expensive."])),
  P("Have you got this in a bigger size?","Bunun daha büyük bedeni var mı?","B1","","Have you got this in a bigger size?","Bunun daha büyük bedeni var mı?",("How does it feel?","It's too tight. ___",["Can I have a refund?","I'm just looking, thanks."])),
  P("It doesn't fit.","Olmadı, üstüme oturmuyor.","B1","","I'm afraid it doesn't fit.","Maalesef üstüme oturmuyor.",("Does the dress look good?","No. ___ It's too long.",["How much does it cost?","Do you take cards?"])),
  P("It suits you.","Sana yakışıyor.","B1","","Red is your colour. It suits you.","Kırmızı senin rengin. Sana yakışıyor.",("What about this blue scarf?","___ It matches your eyes.",["Can I have a refund?","Is there a discount?"])),
 ]},
 {'k':'sret','t':'İade ve değişim','en':'Returning and changing things','items':[
  P("I'd like to return this.","Bunu iade etmek istiyorum.","B1","","I'd like to return this. It's the wrong size.","Bunu iade etmek istiyorum. Yanlış beden.",("Can I help you?","Yes. ___ I bought it yesterday.",["Can I try this on?","It suits you."])),
  P("Can I have a refund?","Param iade edilebilir mi?","B1","","This phone is broken. Can I have a refund?","Bu telefon bozuk. Param iade edilebilir mi?",("I'm afraid we don't have another one.","Then ___ ?",["Where are the fitting rooms?","I'm just looking, thanks."])),
  P("Can I exchange it, please?","Bunu değiştirebilir miyim, lütfen?","B2","","Can I exchange it, please? It is too small.","Bunu değiştirebilir miyim, lütfen? Çok küçük.",("These shoes are too big for me.","___ I need a smaller pair.",["Do you take cards?","It's too expensive."])),
  P("Do you have the receipt?","Fişiniz var mı?","B1","resmî","I'm sorry, but do you have the receipt?","Üzgünüm, ama fişiniz var mı?",("I'd like to return this jumper.","Of course. ___",["It suits you.","How much does it cost?"])),
 ]},
 {'k':'sprice','t':'Fiyat ve ödeme','en':'Prices and paying','items':[
  P("How much does it cost?","Ne kadar?","A2","","How much does it cost to send this parcel?","Bu paketi göndermek ne kadar tutar?",("I like this bag.","___ ?",["Can I try this on?","I'd like to return this."])),
  P("It's too expensive.","Çok pahalı.","A2","","It's too expensive for me.","Benim için çok pahalı.",("This coat is 200 euros.","Oh dear, ___",["Can I try this on?","It doesn't fit."])),
  P("Is there a discount?","İndirim var mı?","B1","","Is there a discount for students?","Öğrenciler için indirim var mı?",("The ticket costs 20 euros.","___ for students?",["It suits you.","It doesn't fit."])),
  P("I'm just looking, thanks.","Sadece bakıyorum, teşekkürler.","A2","","I'm just looking, thanks.","Sadece bakıyorum, teşekkürler.",("Can I help you with anything?","No, ___",["Can I have a refund?","Do you have the receipt?"])),
  P("Could I pay by card?","Kartla ödeyebilir miyim?","B1","","Could I pay by card, please?","Kartla ödeyebilir miyim, lütfen?",("That's 45 euros altogether.","___ I don't have any cash.",["It doesn't fit.","Where are the fitting rooms?"])),
 ]},
]}
fix(GROUP)
