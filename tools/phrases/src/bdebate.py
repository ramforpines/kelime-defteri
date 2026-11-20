# Kalıplar: Tartışma (B2). P(İngilizce, Türkçe, seviye, üslup, örnek İngilizce, örnek Türkçe, diyalog)
import sys,os;sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'..'))
from ext_meta import fix
def P(en,tr,lv,reg,ex,extr,d):return {'en':en,'tr':tr,'lv':lv,'reg':reg,'ex':[ex,extr],'d':d}
GROUP={'id':'bdebate','t':'Tartışmada karşı çıkmak ve vurgulamak','en':'Debating: conceding, emphasising and challenging',
'ins':'Karşı tarafın haklı yanını kabul etmek, kendi noktanı vurgulamak ve karşı görüşe nazikçe itiraz etmek için kalıplar.',
'sub':[
 {'k':'dconc','t':'Haklı yanını kabul etmek','en':'Conceding a point','items':[
  P("I see your point, but ...","Dediğini anlıyorum ama ...","B2","","I see your point, but I still think it's too expensive.","Dediğini anlıyorum ama yine de çok pahalı olduğunu düşünüyorum.",("Cycling is cheaper than driving.","___ not everyone lives near a bike path.",["That's exactly what I mean.","Surely you don't believe that?"])),
  P("That's true up to a point.","Bir noktaya kadar doğru.","B2","","That's true up to a point, but there are exceptions.","Bir noktaya kadar doğru, ama istisnalar var.",("Young people spend too much time online.","___ but many use it to study."  ,["Without a doubt.","I'd go even further."])),
  P("Point taken.","Haklısın / Not aldım.","B1","samimi","Point taken. I hadn't thought about the cost.","Haklısın. Maliyeti düşünmemiştim.",("Tickets cost twice as much in summer.","___ I'll go in spring."  ,["Surely you don't believe that?","I'd go even further."])),
  P("You may be right about that.","Bu konuda haklı olabilirsin.","B1","","You may be right about that, but I'd like to check the facts.","Bu konuda haklı olabilirsin ama gerçekleri kontrol etmek isterim.",("Most students prefer online lessons.","___ but I'd like to see the numbers."  ,["That's exactly what I mean.","I'd go even further."])),
 ]},
 {'k':'dstress','t':'Vurgulamak','en':'Emphasising your point','items':[
  P("That's exactly what I mean.","Tam olarak demek istediğim bu.","B1","","That's exactly what I mean. We need more public parks.","Tam olarak demek istediğim bu. Daha fazla halk parkına ihtiyacımız var.",("So you want cities to be greener?","Yes! ___"  ,["I see your point, but ...","Surely you don't believe that?"])),
  P("Without a doubt.","Kuşkusuz.","B2","","Without a doubt, education is the most important issue.","Kuşkusuz, eğitim en önemli konu.",("Is health care important for a country?","___ It's the most important thing."  ,["Fair enough.","You may be right about that."])),
  P("I'd go even further.","Hatta daha da ileri giderim.","B2","","I'd go even further and say that it should be free for everyone.","Hatta daha da ileri gidip herkes için ücretsiz olması gerektiğini söylerim.",("Public transport should be cheaper.","___ and make it free."  ,["That's true up to a point.","Surely you don't believe that?"])),
  P("The point I'm trying to make is ...","Anlatmaya çalıştığım şey şu: ...","B2","","The point I'm trying to make is that small changes can have a big effect.","Anlatmaya çalıştığım şey şu: küçük değişiklikler büyük etki yapabilir.",("I'm not sure I follow you.","___ small changes matter."  ,["Fair enough.","You may be right about that."])),
 ]},
 {'k':'dchall','t':'Karşı görüşe itiraz etmek','en':'Challenging politely','items':[
  P("Surely you don't believe that?","Buna gerçekten inanmıyorsun, değil mi?","B2","","Surely you don't believe that? The figures say the opposite.","Buna gerçekten inanmıyorsun, değil mi? Rakamlar tam tersini söylüyor.",("Homework has no effect on exam results.","___ Studies show it helps."  ,["Without a doubt.","Fair enough."])),
  P("Where is the evidence for that?","Bunun kanıtı nerede?","B2","","That's a strong claim. Where is the evidence for that?","Bu güçlü bir iddia. Bunun kanıtı nerede?",("Everybody knows that electric cars are cleaner.","Do they? ___"  ,["I'd go even further.","Fair enough."])),
  P("I'm afraid I can't agree.","Maalesef katılamıyorum.","B1","resmî","I'm afraid I can't agree with that statement.","Maalesef bu ifadeye katılamıyorum.",("School uniforms should be banned.","___ They help students feel equal."  ,["Without a doubt.","That's exactly what I mean."])),
  P("Have you considered ...?","... düşündün mü?","B2","","Have you considered the cost for poorer families?","Daha az varlıklı aileler için maliyeti düşündün mü?",("Everyone should have a private car.","___ the cost of petrol?"  ,["That's exactly what I mean.","Fair enough."])),
 ]},
]}
fix(GROUP)
