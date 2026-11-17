# Kalıplar: Konuşmayı yönetme (özgün örnekler)
def P(en,tr,lv,reg,ex,extr,d):return {'en':en,'tr':tr,'lv':lv,'reg':reg,'ex':[ex,extr],'d':d}
GROUP={'id':'gconv','t':'Konuşmayı yönetme','en':'Managing a conversation',
'ins':'Toplantıda ve sohbette konuşmanın akışını yönetmek, söz kesmeyi kibarca yapmayı, konu değiştirmeyi ve ana konuya dönmeyi bilmek demektir. Bu kalıplar konuşmayı bozmadan söz almanı ve yön vermeni sağlar.',
'sub':[
 {'k':'cint','t':'Söz kesme ve söz alma','en':'Interrupting politely','items':[
  P("Sorry to interrupt, but ...","Sözünüzü keserek özür dilerim ama ...","B2","","Sorry to interrupt, but I have a quick question.","Sözünüzü keserek özür dilerim ama kısa bir sorum var.",("How do you speak up in a meeting?","___ I have a quick question.",["By the way, ...","As I was saying, ..."])),
  P("Can I just say ...","Şunu söyleyebilir miyim ...","B2","","Can I just say that I agree with Maria?","Maria ile aynı fikirde olduğumu söyleyebilir miyim?",("Do you want to add something?","Yes, ___ that I agree with Maria.",["Speaking of ...","I'll get back to you on ..."])),
  P("If I could just add ...","Şunu da ekleyebilirsem ...","C1","resmî","If I could just add one more point, the cost is too high.","Bir noktayı daha ekleyebilirsem, maliyet çok yüksek.",("Can you comment before we move on?","___ one more point.",["Going back to ...","Let me finish what I was saying ..."])),
  P("Before you go on, ...","Devam etmeden önce ...","C1","","Before you go on, could you explain that term?","Devam etmeden önce bu terimi açıklar mısınız?",("I don't understand this word.","Then ask: '___, could you explain it?'",["That reminds me of ...","We seem to be going off topic ..."])),
  P("Excuse me for cutting in, ...","Lafınızı kestiğim için kusura bakmayın, ...","C1","resmî","Excuse me for cutting in, but the time is up.","Lafınızı kestiğim için kusura bakmayın ama süre doldu.",("The speaker is over time.","___ but the time is up.",["As I was saying, ...","By the way, ..."])),
 ]},
 {'k':'cchange','t':'Konu değiştirme','en':'Changing the subject','items':[
  P("By the way, ...","Bu arada, ...","B1","","By the way, have you seen Ahmet today?","Bu arada, bugün Ahmet'i gördün mü?",("How do you switch to another topic?","___ have you seen Ahmet today?",["Sorry to interrupt, but ...","I'll get back to you on ..."])),
  P("Speaking of ...","... demişken","B2","","Speaking of holidays, where are you going this year?","Tatilden söz açılmışken bu yıl nereye gidiyorsun?",("We were talking about holidays.","Yes, ___ holidays, where are you going?",["Can I just say ...","Let me finish what I was saying ..."])),
  P("That reminds me of ...","Bu bana ... -i hatırlattı","B2","","That reminds me of a funny story.","Bu bana komik bir hikâyeyi hatırlattı.",("Why are you smiling?","___ a funny story.",["If I could just add ...","As I was saying, ..."])),
  P("Going back to ...","... konusuna dönersek","C1","","Going back to your earlier question, the answer is yes.","Önceki sorunuza dönersek cevap evet.",("You asked something before.","___ your earlier question, the answer is yes.",["Before you go on, ...","Speaking of ..."])),
  P("Can we come back to ...","... konusuna geri dönebilir miyiz?","C1","","Can we come back to this point after lunch?","Bu konuya öğle yemeğinden sonra geri dönebilir miyiz?",("Time is short.","___ this point later?",["Excuse me for cutting in, ...","That reminds me of ..."])),
 ]},
 {'k':'cturn','t':'Konuşmayı yönlendirme','en':'Keeping the conversation on track','items':[
  P("As I was saying, ...","Dediğim gibi, ...","B2","","As I was saying, the plan needs more time.","Dediğim gibi, planın daha çok zamana ihtiyacı var.",("You were cut off.","___ the plan needs more time.",["By the way, ...","Sorry to interrupt, but ..."])),
  P("Let me finish what I was saying ...","Söylediğimi bitirmeme izin ver ...","C1","","Let me finish what I was saying about the budget.","Bütçe hakkında söylediğimi bitirmeme izin ver.",("Someone interrupted you.","Please ___ about the budget.",["Speaking of ...","Can I just say ..."])),
  P("We seem to be going off topic ...","Konudan uzaklaşıyor gibiyiz ...","C1","","We seem to be going off topic, so let's return to the agenda.","Konudan uzaklaşıyor gibiyiz, gündeme dönelim.",("The meeting is drifting.","___ let's return to the agenda.",["That reminds me of ...","If I could just add ..."])),
  P("I'll get back to you on ...","... konusunda size geri döneceğim","B2","","I'll get back to you on the price by Friday.","Fiyat konusunda Cuma gününe kadar size döneceğim.",("What is the price?","I don't know yet. ___ it by Friday.",["Going back to ...","Before you go on, ..."])),
  P("Let's stick to the point ...","Konuya bağlı kalalım ...","C1","","Let's stick to the point and finish on time.","Konuya bağlı kalalım ve zamanında bitirelim.",("People are chatting off-topic.","___ and finish on time.",["Excuse me for cutting in, ...","Can we come back to ..."])),
 ]},
]}
