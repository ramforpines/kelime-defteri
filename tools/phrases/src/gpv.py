# Kalıplar: Phrasal verb çerçeveleri. P(İngilizce, Türkçe, seviye, üslup, örnek İngilizce, örnek Türkçe, diyalog)
def P(en,tr,lv,reg,ex,extr,d):return {'en':en,'tr':tr,'lv':lv,'reg':reg,'ex':[ex,extr],'d':d}
I1,I2="turn up","carry on"
GROUP={'id':'gpv','t':'Phrasal verb çerçeveleri','en':'Phrasal verbs in patterns',
'ins':'Phrasal verb\'leri tek tek ezberlemek yerine nesneyle birlikte çerçeve olarak öğren: hangileri nesne alır (get along with ...), hangileri almaz (turn up).',
'sub':[
 {'k':'pvrel','t':'İlişkiler ve duygular','en':'Relationships and feelings','items':[
  P("get along with ...","... ile iyi geçinmek","B1","","I get along with my neighbours.","Komşularımla iyi geçinirim.",("Do you like your new colleagues?","Yes, I ___ all of them.",[I1,I2])),
  P("fall out with ...","... ile arası bozulmak","B2","","I don't want to fall out with my best friend.","En yakın arkadaşımla arayı bozmak istemiyorum.",("Why don't you talk to Jim any more?","I don't want to ___ him again.",[I1,I2])),
  P("look up to ...","... -e saygı duymak, ... -i örnek almak","B2","","I look up to my older brother.","Ağabeyimi örnek alıyorum.",("Who is your role model?","I really ___ my older brother.",[I1,I2])),
  P("put up with ...","... -e katlanmak","B2","","I can't put up with the noise any more.","Gürültüye daha fazla katlanamıyorum.",("Why are you moving out?","I can't ___ the noise any more.",[I1,I2])),
  P("get over ...","... -i atlatmak","B2","","It took her months to get over the shock.","Şoku atlatması aylar sürdü.",("Is she feeling better now?","Yes, she's finally ___ the shock.",[I1,I2])),
  P("break up with ...","... ile ayrılmak","B1","","He didn't want to break up with his girlfriend.","Kız arkadaşından ayrılmak istemedi.",("Why is he so sad?","He had to ___ his girlfriend.",[I1,I2])),
 ]},
 {'k':'pvplan','t':'Plan ve zaman','en':'Plans, delays and running out','items':[
  P("put off ...","... -i ertelemek","B1","","Don't put off your homework until tomorrow.","Ödevini yarına erteleme.",("When will you start your project?","I know I shouldn't ___ it any longer.",[I1,I2])),
  P("call off ...","... -i iptal etmek","B2","","They had to call off the match.","Maçı iptal etmek zorunda kaldılar.",("Is the match still on?","No, they had to ___ the match.",[I1,I2])),
  P("carry on","devam etmek","B1","","Please carry on with your work.","Lütfen işine devam et.",("Should I stop now?","No, please ___ with your work.",[I1,"break down"])),
  P("set up ...","... -i kurmak","B2","","We decided to set up a small business.","Küçük bir iş kurmaya karar verdik.",("What are your plans?","We want to ___ a small business.",[I1,I2])),
  P("run out of ...","... -i bitirmek, ... -i kalmamak","B1","","We've run out of milk.","Sütümüz bitti.",("Can I have some milk?","Sorry, we've ___ milk.",[I1,I2])),
  P("turn up","ortaya çıkmak, gelmek","B1","","He didn't turn up for the meeting.","Toplantıya gelmedi.",("Was Tom at the meeting?","No, he didn't ___.",["look up to ...","run out of ..."])),
 ]},
 {'k':'pvlearn','t':'Öğrenme ve anlama','en':'Finding out and understanding','items':[
  P("find out ...","... -i öğrenmek, ... -i keşfetmek","B1","","I need to find out what time the train leaves.","Trenin kaçta kalktığını öğrenmem gerek.",("Do you know when the train leaves?","No, I need to ___ what time it leaves.",[I1,I2])),
  P("work out ...","... -i çözmek, ... -i hesaplamak","B2","","I can't work out how much it costs.","Ne kadar tuttuğunu hesaplayamıyorum.",("Is the maths problem difficult?","Yes, I can't ___ the answer.",[I1,I2])),
  P("look up ...","... -i (sözlükte) aramak","B1","","I'll look up the word in a dictionary.","Kelimeye sözlükten bakacağım.",("What does this word mean?","I don't know. I'll ___ it in the dictionary.",[I1,I2])),
  P("point out ...","... -i belirtmek, ... -e dikkat çekmek","B2","","Please point out any mistakes in my report.","Lütfen raporumdaki hataları belirt.",("Can I show you my essay?","Sure, and I'll ___ any mistakes.",[I1,I2])),
  P("go over ...","... -i gözden geçirmek","B2","","Let's go over the notes before the exam.","Sınavdan önce notları gözden geçirelim.",("How should we prepare for the exam?","Let's ___ the notes together.",[I1,I2])),
 ]},
 {'k':'pvdaily','t':'Günlük işler','en':'Everyday actions','items':[
  P("pick up ...","... -i almak, ... -i yoldan almak","B1","","Can you pick up the children from school?","Çocukları okuldan alabilir misin?",("Who is collecting the kids today?","Can you ___ them from school?",[I1,I2])),
  P("give up ...","... -i bırakmak, vazgeçmek","B1","","You should give up smoking.","Sigarayı bırakmalısın.",("Does he still smoke?","No, he decided to ___ smoking.",[I1,I2])),
  P("take off","havalanmak, (giysiyi) çıkarmak","B1","","The plane will take off at six.","Uçak altıda kalkacak.",("What time does the flight leave?","It will ___ at six.",["look up ...","put off ..."])),
  P("look after ...","... -e bakmak","A2","","Who will look after the dog?","Köpeğe kim bakacak?",("Who is taking care of the dog?","My sister will ___ it this weekend.",[I1,I2])),
  P("turn down ...","... -i reddetmek, ... -in sesini kısmak","B2","","I'm going to turn down the job offer.","İş teklifini reddedeceğim.",("Did she accept the job?","Not yet, but I'm going to ___ the offer.",[I1,I2])),
  P("break down","bozulmak, arızalanmak","B1","","I hope our car doesn't break down.","Umarım arabamız bozulmaz.",("Why are you so nervous?","I'm afraid our car will ___ on the motorway.",["pick up ...","look after ..."])),
 ]},
]}
