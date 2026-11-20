# Kalıplar: Kitap, film, haber ve yorum (Berlitz 5/6 temalarından esinlenilmiş, özgün) – B1/B2
import sys,os;sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'..'))
from ext_meta import fix
def P(en,tr,lv,reg,ex,extr,d):return {'en':en,'tr':tr,'lv':lv,'reg':reg,'ex':[ex,extr],'d':d}
GROUP={'id':'bmedia','t':'Kitap, film, haber ve çevrimiçi yorum','en':'Books, films, news and comments',
'ins':'Bir filmin veya kitabın konusunu özetlemek, bir habere tepki vermek ve internette yorum yazmak için kalıplar.',
'sub':[
 {'k':'md1','t':'Konuyu özetlemek','en':'Summarising a plot','items':[
  P("It's about ...","... hakkında","B1","","It's about a girl who finds a magic key.","Sihirli bir anahtar bulan bir kızı anlatıyor.",("What's the film about?","___ a girl who finds a magic key."  ,["Have you heard the news?","I couldn't agree more with you."])),
  P("The story is set in ...","Hikâye ...'da geçiyor","B1","","The story is set in Paris in the 1920s.","Hikâye 1920'lerin Paris'inde geçiyor.",("Where does it take place?","___ Paris in the 1920s."  ,["Have you heard the news?","I couldn't agree more with you."])),
  P("At the very end, ...","En sonunda, ...","B1","","At the very end, they find the treasure.","En sonunda hazineyi buluyorlar.",("How does it finish?","___ they find the treasure."  ,["Have you heard the news?","I couldn't agree more with you."])),
  P("The main character is ...","Ana karakter ...","B1","","The main character is a young detective.","Ana karakter genç bir dedektif.",("Who is the hero?","___ a young detective."  ,["Have you heard the news?","I couldn't agree more with you."])),
 ]},
 {'k':'md2','t':'Habere ve dedikoduya tepki','en':'Reacting to news and rumours','items':[
  P("Have you heard the news?","Haberi duydun mu?","B1","","Have you heard the news? Sam is moving to Berlin.","Haberi duydun mu? Sam Berlin'e taşınıyor.",("Hi! What's up?","___ Sam is moving to Berlin."  ,["It's about ...","Great post! I totally agree."])),
  P("I heard a rumour that ...","... diye bir söylenti duydum","B2","","I heard a rumour that the shop is closing.","Dükkânın kapanacağı yönünde bir söylenti duydum.",("Is it true?","I don't know. ___ the shop is closing."  ,["It's about ...","Great post! I totally agree."])),
  P("I wouldn't believe everything I read.","Okuduğum her şeye inanmazdım.","B2","","I wouldn't believe everything I read online.","İnternette okuduğum her şeye inanmazdım.",("The article says it's all true.","Hmm. ___ online."  ,["It's about ...","Great post! I totally agree."])),
  P("That's hard to believe!","İnanması zor!","B1","","He won the lottery twice? That's hard to believe!","İki kez piyango mu kazandı? İnanması zor!",("He won the lottery twice.","___"  ,["It's about ...","Great post! I totally agree."])),
 ]},
 {'k':'md3','t':'Çevrimiçi yorum yazmak','en':'Leaving an online comment','items':[
  P("Great post! I totally agree.","Harika yazı! Tamamen katılıyorum.","B1","","Great post! I totally agree about the pollution.","Harika yazı! Kirlilik konusunda tamamen katılıyorum.",("What did you write under the article?","___ about the pollution."  ,["It's about ...","Have you heard the news?"])),
  P("With respect, I see it differently.","Saygımla, ben farklı görüyorum.","B2","","With respect, I see it differently. Prices aren't the issue.","Saygımla, ben farklı görüyorum. Sorun fiyatlar değil.",("Everyone says prices are the problem.","___ Prices aren't the issue."  ,["It's about ...","Have you heard the news?"])),
  P("Thanks for sharing this.","Bunu paylaştığın için teşekkürler.","B1","","Thanks for sharing this. It was really useful.","Bunu paylaştığın için teşekkürler. Gerçekten işe yaradı.",("I posted a travel guide.","___ It was really useful."  ,["It's about ...","Have you heard the news?"])),
  P("I'd recommend it to anyone who ...","... olan herkese tavsiye ederim","B2","","I'd recommend it to anyone who loves history.","Tarihi sevenlere tavsiye ederim.",("Is the book worth reading?","Yes. ___ loves history."  ,["It's about ...","Have you heard the news?"])),
 ]},
]}
fix(GROUP)
