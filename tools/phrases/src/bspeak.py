# Kalıplar: Konuşma sınavı (fotoğraf anlatma, kelime bulamama, ortak karar) – B1. P(İngilizce, Türkçe, seviye, üslup, örnek İngilizce, örnek Türkçe, diyalog)
import sys,os;sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'..'))
from ext_meta import fix
def P(en,tr,lv,reg,ex,extr,d):return {'en':en,'tr':tr,'lv':lv,'reg':reg,'ex':[ex,extr],'d':d}
GROUP={'id':'bspeak','t':'Konuşma sınavı','en':'The speaking test',
'ins':'Fotoğrafı anlatırken, kelime bulamadığında ve partnerinle karar verirken kullanabileceğin kalıplar.',
'sub':[
 {'k':'ppic','t':'Fotoğrafı anlatmak','en':'Describing a photograph','items':[
  P("In the foreground, there is ...","Ön planda ... var","B1","","In the foreground, there is a girl with a red bag.","Ön planda kırmızı çantalı bir kız var.",("Can you describe the picture?","Yes. ___ a girl with a red bag.",["What I mean is ...","Shall we start with the first idea?"])),
  P("In the background, you can see ...","Arka planda ... görebilirsiniz","B1","","In the background, you can see some mountains.","Arka planda bazı dağlar görebilirsiniz.",("What else is in the photo?","___ some mountains and a small village.",["Let me think for a moment.","Which one do you prefer?"])),
  P("On the left, there is ...","Solda ... var","A2","","On the left, there is an old man with a dog.","Solda köpekli yaşlı bir adam var.",("Who are the people in the picture?","___ an old man with a dog.",["It's a kind of ...","I'd go for the second idea."])),
  P("I would imagine that ...","... gibi görünüyor","B1","","I would imagine that it is a market.","Bana öyle geliyor ki burası bir pazar.",("What kind of place is this?","___ it is a market.",["I can't think of the word.","Shall we start with the first idea?"])),
  P("They seem to be ...","... gibiler","B1","","They seem to be having a great time.","Çok iyi vakit geçiriyor gibiler.",("How do the people feel?","___ having a great time.",["Let me think for a moment.","I'd go for the second idea."])),
 ]},
 {'k':'pgap','t':'Kelime bulamamak, zaman kazanmak','en':'When you cannot find the word','items':[
  P("I can't think of the word.","Kelimeyi hatırlayamıyorum.","B1","","I can't think of the word, but it's a kind of bird.","Kelimeyi hatırlayamıyorum ama bir tür kuş.",("What is the man holding?","___ but you use it to catch fish.",["On the left, there is ...","They seem to be ..."])),
  P("It's something you use for ...","... için kullandığın bir şey","B1","","It's something you use for cutting paper.","Kâğıt kesmek için kullandığın bir şey.",("What are scissors?","___ cutting paper.",["I'd go for the second idea.","In the background, you can see ..."])),
  P("Let me think for a moment.","Bir an düşüneyim.","B1","","Let me think for a moment. I haven't decided yet.","Bir an düşüneyim. Henüz karar vermedim.",("Which place would you choose?","___ Both are good.",["It looks as if ...","On the left, there is ..."])),
  P("In other words, ...","Başka bir deyişle ...","B1","","In other words, it's too expensive for students.","Başka bir deyişle, öğrenciler için çok pahalı.",("I don't understand why you don't like it.","___ the price is too high.",["They seem to be ...","In the foreground, there is ..."])),
  P("Could you say that again, please?","Lütfen tekrar eder misiniz?","A2","","Could you say that again, please?","Lütfen tekrar eder misiniz?",("What are your hobbies?","Sorry, ___",["It looks as if ...","I'd go for the second idea."])),
 ]},
 {'k':'pdisc','t':'Partnerle karar vermek','en':'Discussing options with a partner','items':[
  P("Shall we start with ...?","... ile başlayalım mı?","B1","","Shall we start with the first idea?","İlk fikirle başlayalım mı?",("We have five ideas to talk about.","OK. ___ the cinema?",["It looks as if ...","Let me think for a moment."])),
  P("Which one do you prefer?","Hangisini tercih edersin?","B1","","There are two choices. Which one do you prefer?","İki seçenek var. Hangisini tercih edersin?",("The park is nice, but the museum is interesting too.","___ ?",["It's a kind of ...","They seem to be ..."])),
  P("My choice would be ...","Benim seçimim ... olurdu","B1","","My choice would be the second idea, because it's cheaper.","Benim seçimim ikinci fikir olurdu, çünkü daha ucuz.",("So, what's your final decision?","___ the picnic.",["In the background, you can see ...","What I mean is ..."])),
  P("That's a good point.","Bu iyi bir nokta.","B1","","That's a good point. I hadn't thought of that.","Bu iyi bir nokta. Bunu düşünmemiştim.",("A picnic could be a problem if it rains.","___ Maybe we need a plan B.",["Which one do you prefer?","It's a kind of ..."])),
  P("You've got a point, but ...","Haklısın ama ...","B2","","You've got a point, but I think a film is more fun.","Haklısın ama bence film daha eğlenceli.",("A museum is more educational.","___ I think a film is more fun.",["On the left, there is ...","Let me think for a moment."])),
 ]},
]}
fix(GROUP)
