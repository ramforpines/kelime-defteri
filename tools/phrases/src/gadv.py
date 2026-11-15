# Kalıplar: Tavsiye ve uyarı (özgün örnekler)
def P(en,tr,lv,reg,ex,extr,d):return {'en':en,'tr':tr,'lv':lv,'reg':reg,'ex':[ex,extr],'d':d}
GROUP={'id':'gadv','t':'Tavsiye ve uyarı','en':'Advice and warnings',
'ins':'Tavsiye isterken, verirken ve uyarırken tonu doğru ayarlamak gerekir. "You must" sert kaçar; "It might be a good idea to" yumuşaktır, "I must warn you" ise ciddi bir uyarıdır.',
'sub':[
 {'k':'aask','t':'Tavsiye isteme','en':'Asking for advice','items':[
  P("Do you have any advice on ...","... konusunda tavsiyen var mı?","B2","","Do you have any advice on learning English quickly?","İngilizceyi hızlı öğrenme konusunda tavsiyen var mı?",("I want to improve my English.","___ learning English quickly?",["I'd strongly advise you to ...","Watch out for ..."])),
  P("What would you recommend for ...","... için ne önerirsin?","B2","","What would you recommend for a first-time visitor?","İlk kez gelen biri için ne önerirsin?",("I'm visiting Istanbul.","___ a first-time visitor?",["Be careful not to ...","You'd better not ..."])),
  P("I could use some advice about ...","... konusunda tavsiyeye ihtiyacım var","C1","","I could use some advice about changing careers.","Meslek değiştirme konusunda tavsiyeye ihtiyacım var.",("You look worried.","Yes, ___ changing careers.",["My advice would be to ...","I must warn you that ..."])),
  P("What do you think I should do about ...","... konusunda ne yapmam gerektiğini düşünüyorsun?","B2","","What do you think I should do about my noisy neighbours?","Gürültücü komşularım konusunda ne yapmam gerektiğini düşünüyorsun?",("My neighbours are very loud.","___ my noisy neighbours?",["It would be wise to ...","Make sure you don't ..."])),
  P("Any tips for ...","... için ipucu var mı?","B1","samimi","Any tips for passing the driving test?","Sürücü sınavını geçmek için ipucu var mı?",("I have my driving test tomorrow.","Great! ___ passing it?",["I'd strongly advise you to ...","Watch out for ..."])),
 ]},
 {'k':'agive','t':'Tavsiye verme','en':'Giving advice','items':[
  P("I'd strongly advise you to ...","Sana ... -meni şiddetle tavsiye ederim","C1","resmî","I'd strongly advise you to read the contract carefully.","Sözleşmeyi dikkatle okumanı şiddetle tavsiye ederim.",("Should I sign it now?","I'd say no. ___ read the contract carefully.",["Do you have any advice on ...","Be careful not to ..."])),
  P("It would be wise to ...","... -mek iyi bir fikir olabilir","B2","","It would be wise to book early.","Erken rezervasyon yapmak iyi bir fikir olabilir.",("The hotel fills quickly.","___ book early.",["Any tips for ...","You'd better not ..."])),
  P("My advice would be to ...","Tavsiyem ... -menizdir","B2","","My advice would be to save some money first.","Tavsiyem önce biraz para biriktirmeniz.",("Can I buy a car now?","___ save some money first.",["I could use some advice about ...","Make sure you don't ..."])),
  P("You had better ...","... -sen iyi olur (yalın fiil)","B2","","You had better see a doctor about that cough.","O öksürük için bir doktora görünsen iyi olur.",("I've been coughing for weeks.","___ see a doctor.",["What would you recommend for ...","I must warn you that ..."])),
  P("The best thing to do is to ...","Yapılacak en iyi şey ... -mektir","B2","","The best thing to do is to ask for help.","Yapılacak en iyi şey yardım istemektir.",("I'm stuck with this problem.","___ ask for help.",["Watch out for ...","Do you have any advice on ..."])),
 ]},
 {'k':'awarn','t':'Uyarma','en':'Warning someone','items':[
  P("Watch out for ...","... -e dikkat et","B2","","Watch out for icy roads tonight.","Bu gece buzlu yollara dikkat et.",("I'm driving home tonight.","Okay. ___ icy roads.",["It would be wise to ...","Any tips for ..."])),
  P("Be careful not to ...","... -memeye dikkat et","B2","","Be careful not to spill the coffee.","Kahveyi dökmemeye dikkat et.",("I'm carrying the hot cups.","___ spill the coffee.",["My advice would be to ...","What would you recommend for ..."])),
  P("Make sure you don't ...","... -mediğinden emin ol","B2","","Make sure you don't leave your bag on the train.","Çantanı trende bırakmadığından emin ol.",("I'm travelling by train tomorrow.","___ leave your bag.",["You had better ...","I could use some advice about ..."])),
  P("You'd better not ...","... -sen iyi olmaz (yalın fiil)","B2","","You'd better not touch that wire.","O kabloya dokunmasan iyi olur.",("Can I touch this?","Please, ___ touch that wire.",["The best thing to do is to ...","What do you think I should do about ..."])),
  P("I must warn you that ...","Sizi uyarmam gerek ...","C1","resmî","I must warn you that the exam is very difficult.","Sizi uyarmam gerek, sınav çok zor.",("Is the test easy?","Not at all. ___ it is very difficult.",["I'd strongly advise you to ...","Any tips for ..."])),
 ]},
]}
