# Kalıplar: Gramer kalıpları (günlük konuşmada sık kullanılan yapılar). P(İngilizce, Türkçe, seviye, üslup, örnek İngilizce, örnek Türkçe, diyalog)
def P(en,tr,lv,reg,ex,extr,d):return {'en':en,'tr':tr,'lv':lv,'reg':reg,'ex':[ex,extr],'d':d}
W1,W2="I wish I had ...","I'm used to ..."
GROUP={'id':'gframes','t':'Gramer kalıpları','en':'Useful grammar patterns',
'ins':'Konuşmada ve yazıda sık kullanılan gramer yapıları: dilek ve pişmanlık, koşul ve varsayım, alışkanlık ve alışma, zorunluluk ve izin. Her kalıbın ardından hangi fiil biçiminin geldiğine dikkat et.',
'sub':[
 {'k':'gwish','t':'Dilek ve pişmanlık','en':'Wishes and regrets','items':[
  P("I wish I had ...","Keşke ... olsaydı","B1","","I wish I had more free time.","Keşke daha çok boş zamanım olsaydı.",("You look tired all the time.","Yes, ___ more free time.",["I used to ...","You'd better ..."])),
  P("If only I ...","Keşke ... (şimdiki ya da geçmiş pişmanlık)","B2","","If only I knew the answer!","Keşke cevabı bilseydim!",("The exam question was so hard.","___ knew the answer!",["You'd better ...",W2])),
  P("I should have ...","... -meliydim (yapmadım)","B1","","I should have studied harder.","Daha çok çalışmalıydım.",("You failed the test.","I know. ___ studied harder.",["I used to ...","I'm supposed to ..."])),
  P("I'd rather you ...","Keşke sen ... (yapma/yapsan) tercih ederim","B2","","I'd rather you didn't smoke here.","Burada sigara içmemeni tercih ederim.",("Do you mind if I smoke in here?","Actually, ___ didn't.",[W1,W2])),
  P("It's time we ...","... -mamızın zamanı geldi","B2","","It's time we left.","Gitme zamanımız geldi.",("It's almost midnight.","___ left. We have work tomorrow.",[W2,"I'd rather you ..."])),
  P("I regret ...","... -diğime pişmanım","B2","","I regret not telling her the truth.","Ona gerçeği söylemediğime pişmanım.",("Did you tell her about the problem?","No, and ___ not telling her.",[W2,"I tend to ..."])),
 ]},
 {'k':'gcond','t':'Koşul ve varsayım','en':'Conditions and suppositions','items':[
  P("If I were in your position, I'd ...","Senin durumunda olsam ... yapardım","B1","","If I were in your position, I'd take the job.","Senin yerinde olsam o işi kabul ederdim.",("Should I accept this offer?","___ take it.",[W1,W2])),
  P("Unless ...","... -mediği sürece / ... -medikçe","B1","","Unless you hurry, you'll miss the bus.","Acele etmezsen otobüsü kaçırırsın.",("Will we catch the bus?","___ we hurry, we'll miss it.",["If only I ...","I'd rather you ..."])),
  P("As long as ...","... -mek koşuluyla","B1","","You can borrow it as long as you return it.","Geri verdiğin sürece ödünç alabilirsin.",("Can I borrow your car?","Yes, ___ you drive carefully.",["If only I ...","I'd rather you ..."])),
  P("What if ...?","... olursa ne olur?","B1","","What if it rains tomorrow?","Yarın yağmur yağarsa ne olur?",("The picnic is tomorrow.","But ___ it rains?",["It's time we ...","I'd rather you ..."])),
  P("Provided that ...","... şartıyla","B2","resmî","You can go out provided that you finish your homework.","Ödevini bitirmen şartıyla dışarı çıkabilirsin.",("Can I go to the party?","Yes, ___ you're back by ten.",["If only I ...","I'd rather you ..."])),
  P("Had I known, ...","Bilseydim ... (resmî)","C1","resmî","Had I known, I would have helped.","Bilseydim yardım ederdim.",("Why didn't you help us?","___ I would have.",["As long as ...","Unless ..."])),
 ]},
 {'k':'ghabit','t':'Alışkanlık ve alışma','en':'Habits and getting used to things','items':[
  P("I used to ...","Eskiden ... yapardım (artık yapmıyorum)","A2","","I used to play tennis every week when I was a student.","Öğrenciyken her hafta tenis oynardım.",("Do you still play tennis?","No, ___ play every week, but not now.",[W2,W1])),
  P("I'm used to ...","... -meye alışkınım","B1","","I'm used to getting up early.","Erken kalkmaya alışkınım.",("Doesn't the early start bother you?","Not at all. ___ getting up early.",["I used to ...",W1])),
  P("I'm getting used to ...","... -meye alışıyorum","B1","","I'm getting used to the cold weather.","Soğuk havaya alışıyorum.",("How do you like your new city?","It's hard, but ___ the cold weather.",["I used to ...","I'd rather you ..."])),
  P("I tend to ...","... eğilimim var / genellikle ... yaparım","B2","","I tend to wake up early.","Genellikle erken uyanırım.",("Are you a morning person?","Yes, ___ wake up before six.",[W2,W1])),
  P("I'm in the habit of ...","... alışkanlığım var","C1","resmî","I'm in the habit of reading before bed.","Yatmadan önce okuma alışkanlığım var.",("Do you read at night?","Yes, ___ reading before bed.",["I used to ...","I tend to ..."])),
  P("I would often ...","Sık sık ... yapardım (geçmişte)","B2","","When I was little, I would often visit my grandma.","Küçükken sık sık büyükannemi ziyaret ederdim.",("What did you do in summer as a child?","___ visit my grandparents.",[W2,"I'm getting used to ..."])),
 ]},
 {'k':'gobl','t':'Zorunluluk ve izin','en':'Obligation, permission and advice','items':[
  P("You'd better ...","... yapsan iyi olur","B1","","You'd better take an umbrella.","Şemsiye alsan iyi olur.",("It looks like rain.","___ take an umbrella.",["I used to ...",W1])),
  P("You don't have to ...","... zorunda değilsin","A2","","You don't have to wait for me.","Beni beklemek zorunda değilsin.",("Should I wait for you?","No, ___ wait for me.",["I used to ...",W1])),
  P("You're not allowed to ...","... yapmana izin yok","B1","","You're not allowed to smoke here.","Burada sigara içmen yasak.",("Can I smoke in here?","No, ___ smoke in here.",[W2,W1])),
  P("I'm supposed to ...","... yapmam gerekiyor (plan ya da kural gereği)","B2","","I'm supposed to meet her at six.","Onunla altıda buluşmam gerekiyor.",("Why are you leaving so early?","___ meet my sister at six.",[W2,W1])),
  P("I have to ...","... yapmak zorundayım","A2","","I have to finish this report today.","Bu raporu bugün bitirmek zorundayım.",("Why can't you come out tonight?","Sorry, ___ finish this report.",[W2,W1])),
  P("You needn't ...","... yapmana gerek yok","B2","","You needn't have bought flowers.","Çiçek almana gerek yoktu.",("Should I bring anything?","No, ___ bring anything.",[W2,W1])),
  P("You are required to ...","... yapmanız zorunludur","C1","resmî","You are required to wear a helmet.","Kask takmanız zorunludur.",("What do the rules say?","___ wear a helmet.",[W2,W1])),
 ]},
]}
