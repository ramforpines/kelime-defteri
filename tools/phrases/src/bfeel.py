# Kalıplar: Duygu ve tepki – B1. P(İngilizce, Türkçe, seviye, üslup, örnek İngilizce, örnek Türkçe, diyalog)
import sys,os;sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'..'))
from ext_meta import fix
def P(en,tr,lv,reg,ex,extr,d):return {'en':en,'tr':tr,'lv':lv,'reg':reg,'ex':[ex,extr],'d':d}
GROUP={'id':'bfeel','t':'Duygu ve tepki','en':'Feelings and reactions',
'ins':'Sevinç, sıkıntı ve hayal kırıklığını ifade etmek ve birinin anlattığına tepki vermek için kalıplar.',
'sub':[
 {'k':'xpos','t':'Olumlu duygular','en':'Positive feelings','items':[
  P("I can't wait to ...","... için sabırsızlanıyorum","B1","","I can't wait to see you again.","Seni tekrar görmek için sabırsızlanıyorum.",("The holiday starts tomorrow.","I know! ___ get on the plane."  ,["I've had enough of ...","What a pity!"])),
  P("I'm thrilled that ...","... -mesine çok sevindim","B2","","I'm thrilled that you passed the exam.","Sınavı geçmene çok sevindim.",("I got the job!","Congratulations! ___ you got it."  ,["I've had enough of ...","What a pity!"])),
  P("That's the best news I've heard all week.","Bu, bu hafta duyduğum en iyi haber.","B2","","That's the best news I've heard all week.","Bu, bu hafta duyduğum en iyi haber.",("We're going to have a baby!","Wow, ___ ."  ,["I've had enough of ...","What a pity!"])),
 ]},
 {'k':'xneg','t':'Sıkıntı ve hayal kırıklığı','en':'Annoyance and disappointment','items':[
  P("I've had enough of ...","... -den bıktım","B1","","I've had enough of this weather.","Bu havadan bıktım.",("It has rained for a week.","I know. ___ it."  ,["I can't wait to ...","That's the best news I've heard all week."])),
  P("It's so annoying when ...","... olması çok sinir bozucu","B1","","It's so annoying when people talk during a film.","İnsanların film sırasında konuşması çok sinir bozucu.",("Why are you angry?","___ people talk during a film."  ,["I can't wait to ...","That's the best news I've heard all week."])),
  P("What a pity!","Ne yazık!","B1","","You can't come? What a pity!","Gelemiyor musun? Ne yazık!",("Sorry, I can't come to your party.","Oh no, ___"  ,["I can't wait to ...","I'm thrilled that ..."])),
  P("I was really disappointed with ...","... beni gerçekten hayal kırıklığına uğrattı","B1","","I was really disappointed with the ending.","Son beni gerçekten hayal kırıklığına uğrattı.",("Did you like the film?","Not really. ___ the ending."  ,["I can't wait to ...","That's the best news I've heard all week."])),
 ]},
 {'k':'xreact','t':'Birinin anlattığına tepki vermek','en':'Reacting to news','items':[
  P("Really? How awful!","Gerçekten mi? Ne korkunç!","B1","","Really? How awful! Are you all right?","Gerçekten mi? Ne korkunç! İyi misin?",("I missed my train and my bag was stolen.","___ Are you all right?"  ,["I can't wait to ...","I've had enough of ..."])),
  P("That must have been awful.","Bu berbat olmuş olmalı.","B2","","You lost your keys at night? That must have been awful.","Anahtarlarını gece mi kaybettin? Bu berbat olmuş olmalı.",("I spent three hours in the cold.","___"  ,["I'm thrilled that ...","I can't wait to ..."])),
  P("I'm so sorry to hear that.","Bunu duyduğuma çok üzüldüm.","B1","","I'm so sorry to hear that your grandfather is ill.","Büyükbabanın hasta olduğunu duyduğuma çok üzüldüm.",("My grandfather is in hospital.","___"  ,["I can't wait to ...","I've had enough of ..."])),
  P("Good for you!","Aferin sana!","B1","samimi","You passed your driving test? Good for you!","Ehliyet sınavını mı geçtin? Aferin sana!",("I've finally passed my driving test.","___"  ,["I've had enough of ...","What a pity!"])),
 ]},
]}
fix(GROUP)
