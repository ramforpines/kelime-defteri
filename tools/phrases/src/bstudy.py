# Kalıplar: Okulda ve derste (B1). P(İngilizce, Türkçe, seviye, üslup, örnek İngilizce, örnek Türkçe, diyalog)
import sys,os;sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'..'))
from ext_meta import fix
def P(en,tr,lv,reg,ex,extr,d):return {'en':en,'tr':tr,'lv':lv,'reg':reg,'ex':[ex,extr],'d':d}
GROUP={'id':'bstudy','t':'Derste ve ödevlerde','en':'In class and with assignments',
'ins':'Öğretmenden açıklama istemek, teslim tarihleri hakkında konuşmak ve sınıf arkadaşlarıyla yardımlaşmak için kalıplar.',
'sub':[
 {'k':'scls','t':'Öğretmenden açıklama istemek','en':'Asking the teacher to clarify','items':[
  P("Could you explain that again, please?","Bunu tekrar açıklayabilir misiniz?","B1","","Could you explain that again, please? I didn't understand the last part.","Bunu tekrar açıklayabilir misiniz? Son kısmı anlamadım.",("Is everything clear?","Not really. ___"  ,["When is the deadline?","Could I borrow your notes?"])),
  P("What do you mean by ...?","... derken neyi kastediyorsunuz?","A2","","What do you mean by \"deadline\"?","\"Deadline\" derken neyi kastediyorsunuz?",("Please finish the task before the deadline.","Sorry, ___ \"deadline\"?"  ,["Shall we do it together?","I'll send you the file."])),
  P("How do you spell ...?","... nasıl yazılır?","A2","","How do you spell \"necessary\"?","\"Necessary\" nasıl yazılır?",("Write down this word: necessary.","Excuse me, ___ ?"  ,["I'm running out of time.","I'll send you the file."])),
  P("Could you give us an example?","Bize bir örnek verebilir misiniz?","B1","","Could you give us an example of a passive sentence?","Bize pasif bir cümle örneği verebilir misiniz?",("This rule is a bit difficult.","I agree. ___"  ,["When is the deadline?","Could I borrow your notes?"])),
 ]},
 {'k':'sdead','t':'Teslim tarihleri ve ödevler','en':'Deadlines and assignments','items':[
  P("When is the deadline?","Son teslim tarihi ne zaman?","B1","","When is the deadline for the project?","Projenin son teslim tarihi ne zaman?",("We have to finish the report.","___ ?"  ,["How do you spell ...?","Could you give us an example?"])),
  P("I'm running out of time.","Zamanım azalıyor.","B1","","I'm running out of time, so I can't finish it today.","Zamanım azalıyor, bu yüzden bugün bitiremem.",("Are you nearly finished?","No, ___ The deadline is tomorrow."  ,["Could I borrow your notes?","Shall we do it together?"])),
  P("Could I hand it in tomorrow?","Yarın teslim edebilir miyim?","B1","","Could I hand it in tomorrow instead of today?","Bugün yerine yarın teslim edebilir miyim?",("I know the essay is due today.","I'm sorry, ___ ?"  ,["What do you mean by ...?","I'll send you the file."])),
  P("I'll send you the file.","Dosyayı sana göndereceğim.","B1","","I'll send you the file as soon as I finish.","Bitirir bitirmez dosyayı sana göndereceğim.",("Can I see your presentation?","Of course. ___ tonight."  ,["How do you spell ...?","What do you mean by ...?"])),
 ]},
 {'k':'shelp','t':'Arkadaşlardan yardım istemek ve yardım etmek','en':'Asking classmates for help','items':[
  P("Could I borrow your notes?","Notlarını ödünç alabilir miyim?","B1","","I was ill yesterday. Could I borrow your notes?","Dün hastaydım. Notlarını ödünç alabilir miyim?",("Why weren't you in class?","I was ill. ___ ?"  ,["When is the deadline?","How do you spell ...?"])),
  P("Do you know how to ...?","Nasıl ... bilir misin?","B1","","Do you know how to do question six?","Altıncı soruyu nasıl yapacağını biliyor musun?",("I can't solve this problem.","___ do question six?"  ,["When is the deadline?","How do you spell ...?"])),
  P("Shall we do it together?","Birlikte yapalım mı?","B1","","The project is big. Shall we do it together?","Proje büyük. Birlikte yapalım mı?",("This is too much work for one person.","Yes. ___ ?"  ,["What do you mean by ...?","I'm running out of time."])),
  P("Would you mind checking my answers?","Cevaplarımı kontrol etmeyi kabul eder misin?","B2","","Would you mind checking my answers before I hand them in?","Teslim etmeden önce cevaplarımı kontrol etmeyi kabul eder misin?",("I've finished the exercise.","Great. ___ ?"  ,["When is the deadline?","How do you spell ...?"])),
  P("I'm stuck on question ...","... numaralı soruda takıldım","B1","","I'm stuck on question five. Can you help me?","Beşinci soruda takıldım. Bana yardım edebilir misin?",("How is the homework going?","Not well. ___ five."  ,["Could I hand it in tomorrow?","Shall we do it together?"])),
 ]},
]}
fix(GROUP)
