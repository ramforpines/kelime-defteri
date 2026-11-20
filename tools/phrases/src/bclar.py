# Kalıplar: Nazikçe sözünü kesmek ve açıklama istemek (Berlitz 6 temasından esinlenilmiş, özgün) – B2
import sys,os;sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'..'))
from ext_meta import fix
def P(en,tr,lv,reg,ex,extr,d):return {'en':en,'tr':tr,'lv':lv,'reg':reg,'ex':[ex,extr],'d':d}
GROUP={'id':'bclar','t':'Sözü kesmek ve açıklama istemek','en':'Interrupting and clarifying',
'ins':'Toplantıda ve konuşmada nazikçe sözü kesmek, anlamadığın yeri sormak ve anladığını doğrulamak için kalıplar.',
'sub':[
 {'k':'qint','t':'Nazikçe sözü kesmek','en':'Interrupting politely','items':[
  P("Excuse me for cutting in, but ...","Sözünüzü keseceğim ama ...","B2","resmî","Excuse me for cutting in, but could I ask a question?","Sözünüzü keseceğim ama bir soru sorabilir miyim?",("As I was saying, the budget is limited.","___ may I ask something?"  ,["Could you clarify what you mean by ...?","As far as I understand, ..."])),
  P("May I just say something?","Bir şey söyleyebilir miyim?","B1","","May I just say something? I disagree.","Bir şey söyleyebilir miyim? Katılmıyorum.",("So we agree to cancel the trip.","___ I disagree."  ,["Could you clarify what you mean by ...?","As far as I understand, ..."])),
  P("Could I come in here?","Buraya katılabilir miyim?","B2","","Could I come in here? I have some information.","Buraya katılabilir miyim? Elimde bir bilgi var.",("...and then the second option is...","___ I have some information."  ,["Could you clarify what you mean by ...?","As far as I understand, ..."])),
 ]},
 {'k':'qclar','t':'Açıklama istemek','en':'Asking for clarification','items':[
  P("Could you clarify what you mean by ...?","... derken ne kastettiğinizi açıklar mısınız?","B2","resmî","Could you clarify what you mean by flexible hours?","Esnek saat derken ne kastettiğinizi açıklar mısınız?",("We offer flexible hours.","___ flexible hours?"  ,["Excuse me for cutting in, but ...","As far as I understand, ..."])),
  P("I didn't quite catch that.","Tam anlayamadım.","B1","","Sorry, I didn't quite catch that.","Pardon, tam anlayamadım.",("The meeting is on the fifteenth.","Sorry, ___ ."  ,["Excuse me for cutting in, but ...","As far as I understand, ..."])),
  P("Would you mind repeating that?","Tekrar eder misiniz?","B1","resmî","Would you mind repeating that more slowly?","Bunu daha yavaş tekrar eder misiniz?",("The code is 4-7-2-9-1.","___ more slowly?"  ,["Excuse me for cutting in, but ...","As far as I understand, ..."])),
 ]},
 {'k':'qcheck','t':'Anladığını doğrulamak','en':'Checking understanding','items':[
  P("As far as I understand, ...","Doğru anladıysam, ...","B2","","As far as I understand, the shop closes at six.","Doğru anladıysam, dükkân altıda kapanıyor.",("We close earlier on Saturdays.","___ the shop closes at six on Saturdays?"  ,["Excuse me for cutting in, but ...","Could you clarify what you mean by ...?"])),
  P("What you mean, then, is that ...","Yani demek istediğin şu: ...","B2","","What you mean, then, is that we should wait.","Yani demek istediğin şu: beklemeliyiz.",("It's too risky to decide now.","___ we should wait."  ,["Excuse me for cutting in, but ...","Could you clarify what you mean by ...?"])),
  P("Let me make sure I've got this right.","Doğru anladığımdan emin olayım.","B2","","Let me make sure I've got this right: it starts on Monday?","Doğru anladığımdan emin olayım: Pazartesi mi başlıyor?",("The course begins next week.","___ it starts on Monday?"  ,["Excuse me for cutting in, but ...","Could you clarify what you mean by ...?"])),
 ]},
]}
fix(GROUP)
