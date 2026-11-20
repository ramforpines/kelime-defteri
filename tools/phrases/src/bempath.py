# Kalıplar: Teselli ve empati (Berlitz 5 temasından esinlenilmiş, özgün) – B1/B2
import sys,os;sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'..'))
from ext_meta import fix
def P(en,tr,lv,reg,ex,extr,d):return {'en':en,'tr':tr,'lv':lv,'reg':reg,'ex':[ex,extr],'d':d}
GROUP={'id':'bempath','t':'Teselli ve empati','en':'Comforting and empathising',
'ins':'Memleket özlemi çeken ya da üzgün birine destek olmak, öneri vermek ve kendi deneyimini paylaşmak için kalıplar.',
'sub':[
 {'k':'ycomf','t':'Teselli etmek','en':'Comforting','items':[
  P("I know how you feel.","Ne hissettiğini biliyorum.","B1","","I know how you feel. I missed my family too.","Ne hissettiğini biliyorum. Ben de ailemi özlemiştim.",("I miss my family so much.","___ It gets easier."  ,["What you need is a hobby.","Have you tried joining a club?"])),
  P("That must be really hard for you.","Bu senin için gerçekten zor olmalı.","B1","","That must be really hard for you. You live alone abroad.","Yurtdışında tek başına yaşamak senin için gerçekten zor olmalı.",("I've been feeling lonely here.","___"  ,["Have you tried joining a club?","I went through the same thing."])),
  P("It's perfectly natural to feel that way.","Böyle hissetmen çok doğal.","B2","","It's perfectly natural to feel that way at first.","Başta böyle hissetmen çok doğal.",("Is it normal to feel so sad?","Yes, ___"  ,["What you need is a hobby.","I went through the same thing."])),
  P("Don't be too hard on yourself.","Kendine fazla yüklenme.","B1","","Don't be too hard on yourself. You're doing your best.","Kendine fazla yüklenme. Elinden gelenin en iyisini yapıyorsun.",("I failed my first exam here.","Oh dear. ___"  ,["Have you tried joining a club?","I went through the same thing."])),
 ]},
 {'k':'yadv','t':'Öneri vermek','en':'Suggesting ways to feel better','items':[
  P("What you need is ...","İhtiyacın olan şey ...","B2","","What you need is a good night's sleep.","İhtiyacın olan şey iyi bir gece uykusu.",("I feel terrible.","Honestly, ___ a good night's sleep."  ,["I know how you feel.","I went through the same thing."])),
  P("Have you tried ...?","... denedin mi?","B1","","Have you tried joining a sports club?","Bir spor kulübüne katılmayı denedin mi?",("I don't know anybody here.","___ joining a club?"  ,["I know how you feel.","It's perfectly natural to feel that way."])),
  P("It might help to ...","... -mek yardımcı olabilir","B2","","It might help to call your family less often.","Ailenle daha az sık konuşmak yardımcı olabilir.",("I always feel sadder after we talk.","___ call them less often."  ,["I know how you feel.","I went through the same thing."])),
  P("Try to see it as ...","Bunu ... olarak görmeye çalış","B2","","Try to see it as a chance to learn.","Bunu öğrenme fırsatı olarak görmeye çalış.",("I made so many mistakes today.","___ a chance to learn."  ,["I know how you feel.","I went through the same thing."])),
  P("It's worth trying.","Denemeye değer.","B2","","It's worth trying. Nothing is lost.","Denemeye değer. Kaybedecek bir şey yok.",("Should I speak to the teacher?","Yes, ___ Nothing is lost."  ,["I know how you feel.","I went through the same thing."])),
  P("Why not give it a try?","Neden bir deneme yapmıyorsun?","B1","","Why not give it a try? You have nothing to lose.","Neden bir deneme yapmıyorsun? Kaybedecek bir şeyin yok.",("Do you think I should join the choir?","___ You have nothing to lose."  ,["I know how you feel.","It's perfectly natural to feel that way."])),
 ]},
 {'k':'yshare','t':'Kendi deneyimini paylaşmak','en':'Sharing your experience','items':[
  P("I went through the same thing.","Ben de aynı şeyi yaşadım.","B1","","I went through the same thing when I moved to London.","Londra'ya taşındığımda ben de aynı şeyi yaşadım.",("I'm so homesick.","___ when I moved to London."  ,["What you need is ...","Have you tried ...?"])),
  P("It took me a while to get used to ...","Alışmam biraz zaman aldı.","B2","","It took me a while to get used to the food.","Yemeklere alışmam biraz zaman aldı.",("Do you like it here now?","Yes. ___ the food."  ,["I know how you feel.","Don't be too hard on yourself."])),
  P("I remember feeling ...","... hissettiğimi hatırlıyorum","B1","","I remember feeling lost on my first day.","İlk gün kendimi kaybolmuş hissettiğimi hatırlıyorum.",("How was your first day at school?","___ lost on my first day, too."  ,["What you need is ...","Have you tried ...?"])),
  P("If I were you, I would try to ...","Ben olsam ... denerdim","B2","","If I were you, I would try to join a club.","Ben olsam bir kulübe katılmayı denerdim.",("What should I do to meet people?","___ join a club."  ,["I know how you feel.","It's perfectly natural to feel that way."])),
  P("Things will get better, I promise.","İşler düzelecek, söz veriyorum.","B1","","Things will get better, I promise. Give it time.","İşler düzelecek, söz veriyorum. Zamana zaman tanı.",("I want to go home.","I understand. ___ Give it time."  ,["What you need is ...","Have you tried ...?"])),
 ]},
]}
fix(GROUP)
