# Kalıplar: Özür dilemek ve cevap vermek (Berlitz 6 temasından esinlenilmiş, özgün) – B1
import sys,os;sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'..'))
from ext_meta import fix
def P(en,tr,lv,reg,ex,extr,d):return {'en':en,'tr':tr,'lv':lv,'reg':reg,'ex':[ex,extr],'d':d}
GROUP={'id':'bapol','t':'Özür dilemek ve özre cevap vermek','en':'Apologising and responding',
'ins':'Arkadaşına özür dilemek, ne olduğunu açıklamak ve gelen özre cevap vermek için kalıplar.',
'sub':[
 {'k':'zsorry','t':'Özür dilemek','en':'Apologising','items':[
  P("I'm really sorry about ...","... için gerçekten üzgünüm","B1","","I'm really sorry about yesterday.","Dün için gerçekten üzgünüm.",("You look upset.","I feel bad. ___ yesterday."  ,["It was a misunderstanding.","Don't worry about it."])),
  P("I owe you an apology.","Sana bir özür borçluyum.","B2","","I owe you an apology. I shouldn't have shouted.","Sana bir özür borçluyum. Bağırmamalıydım.",("What's this about?","___ I shouldn't have shouted."  ,["It was a misunderstanding.","Forget about it."])),
  P("It was all my fault.","Hepsi benim suçumdu.","B1","","It was all my fault. I forgot to call you.","Hepsi benim suçumdu. Seni aramayı unuttum.",("Why were you late?","___ I forgot to set my alarm."  ,["It was a misunderstanding.","Don't worry about it."])),
  P("I didn't mean to ...","... -mek istemedim","B1","","I didn't mean to hurt your feelings.","Seni kırmak istemedim.",("That comment really hurt.","I'm sorry. ___ hurt your feelings."  ,["It was a misunderstanding.","Forget about it."])),
 ]},
 {'k':'zexc','t':'Neyin yanlış gittiğini açıklamak','en':'Explaining','items':[
  P("It was a misunderstanding.","Bu bir yanlış anlaşılmaydı.","B1","","I'm sure it was a misunderstanding.","Eminim bu bir yanlış anlaşılmaydı.",("You said you'd come at six!","No, I said seven. ___"  ,["I owe you an apology.","Don't worry about it."])),
  P("I never realised that ...","... olduğundan haberim yoktu","B1","","I never realised that you were waiting.","Beklediğini bilmiyordum.",("I waited for an hour!","I'm sorry. ___ you were waiting."  ,["I owe you an apology.","Forget about it."])),
  P("What happened was that ...","Olan şuydu: ...","B2","","What happened was that my phone died.","Olan şuydu: telefonum kapandı.",("Why didn't you answer my calls?","Well, ___ my phone died."  ,["I owe you an apology.","Don't worry about it."])),
 ]},
 {'k':'zresp','t':'Özre cevap vermek','en':'Responding to an apology','items':[
  P("Don't worry about it.","Boş ver / Önemli değil.","A2","","Don't worry about it. These things happen.","Boş ver. Böyle şeyler olur.",("I'm so sorry I'm late.","___ These things happen."  ,["I owe you an apology.","It was a misunderstanding."])),
  P("Forget about it.","Unut gitsin.","B1","samimi","Forget about it. It's no big deal.","Unut gitsin. Büyütülecek bir şey yok.",("I'm sorry I broke your cup.","___ It's no big deal."  ,["I owe you an apology.","I didn't mean to ..."])),
  P("Apology accepted.","Özrün kabul.","B1","","Apology accepted. Let's start again.","Özrün kabul. Baştan başlayalım.",("I'm really sorry. Can you forgive me?","Of course. ___ Let's start again."  ,["It was all my fault.","It was a misunderstanding."])),
 ]},
]}
fix(GROUP)
