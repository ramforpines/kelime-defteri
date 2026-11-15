# Kalıplar: Açıklama isteme (özgün örnekler)
def P(en,tr,lv,reg,ex,extr,d):return {'en':en,'tr':tr,'lv':lv,'reg':reg,'ex':[ex,extr],'d':d}
GROUP={'id':'gclar','t':'Açıklama isteme','en':'Asking for clarification',
'ins':'Anlamadığında susmak yerine kibarca tekrar ya da açıklama iste. Üç adım vardır: duymadığını söylemek, anladığını doğrulamak ve ayrıntı istemek. Bu kalıplar özellikle toplantıda ve derste çok işe yarar.',
'sub':[
 {'k':'kmiss','t':'Duyamama ve tekrar isteme','en':'When you did not hear or understand','items':[
  P("Sorry, I didn't catch ...","Pardon, ... -i duyamadım","B1","","Sorry, I didn't catch your name.","Pardon, adını duyamadım.",("You introduced yourself.","Sorry, ___ your name.",["Just to be clear, ...","What exactly do you mean by ..."])),
  P("Could you repeat ...","... -i tekrar eder misiniz?","B1","","Could you repeat the last sentence?","Son cümleyi tekrar eder misiniz?",("The line was noisy.","Could you ___ the last sentence?",["Do you mean that ...","Can you be more specific about ..."])),
  P("I'm afraid I didn't quite hear ...","Maalesef ... -i tam duyamadım","C1","resmî","I'm afraid I didn't quite hear the last question.","Maalesef son soruyu tam duyamadım.",("Did you get the last question?","___ the last question.",["If I understand correctly, ...","Could you give me an example of ..."])),
  P("Could you speak a little more ...","Biraz daha ... konuşabilir misiniz?","B2","","Could you speak a little more slowly?","Biraz daha yavaş konuşabilir misiniz?",("He talks very fast.","Please ask: '___ slowly?'",["So what you're saying is ...","I'm not sure I understand why ..."])),
  P("I missed the part about ...","... kısmını kaçırdım","B2","","I missed the part about the deadline.","Teslim tarihi kısmını kaçırdım.",("Did you hear everything?","No, ___ the deadline.",["Am I right in thinking that ...","Could you explain what you mean by ..."])),
 ]},
 {'k':'kconfirm','t':'Anladığını doğrulama','en':'Checking that you understood','items':[
  P("So what you're saying is ...","Yani demek istediğin ...","B2","","So what you're saying is that we should wait.","Yani demek istediğin, beklememiz gerektiği.",("Do you want to delay the launch?","Yes. ___ that we should wait?",["Sorry, I didn't catch ...","Could you repeat ..."])),
  P("Do you mean that ...","... demek mi istiyorsun?","B1","","Do you mean that the shop is closed?","Dükkânın kapalı olduğunu mu demek istiyorsun?",("The shop's lights are off.","___ the shop is closed?",["I missed the part about ...","I'm afraid I didn't quite hear ..."])),
  P("If I understand correctly, ...","Doğru anladıysam, ...","C1","resmî","If I understand correctly, the meeting has moved to Friday.","Doğru anladıysam, toplantı Cuma gününe alındı.",("Let me check the new plan.","___ the meeting is on Friday.",["Could you speak a little more ...","What exactly do you mean by ..."])),
  P("Just to be clear, ...","Anlaşılır olsun diye, ...","B2","","Just to be clear, I will send the report tomorrow.","Anlaşılır olsun diye, raporu yarın göndereceğim.",("Who sends the report and when?","___ I will send it tomorrow.",["Can you be more specific about ...","Sorry, I didn't catch ..."])),
  P("Am I right in thinking that ...","... diye düşünmekte haklı mıyım?","C1","resmî","Am I right in thinking that the fee is included?","Ücretin dahil olduğunu düşünmekte haklı mıyım?",("Is breakfast free?","___ the fee is included?",["I'm not sure I understand why ...","Could you give me an example of ..."])),
 ]},
 {'k':'kmore','t':'Ayrıntı ve örnek isteme','en':'Asking for more detail','items':[
  P("Could you explain what you mean by ...","... ile neyi kastettiğinizi açıklar mısınız?","C1","","Could you explain what you mean by 'flexible hours'?","'Esnek saatler' ile neyi kastettiğinizi açıklar mısınız?",("The term is unclear.","___ 'flexible hours'?",["Do you mean that ...","I missed the part about ..."])),
  P("What exactly do you mean by ...","... ile tam olarak neyi kastediyorsun?","B2","","What exactly do you mean by 'soon'?","'Yakında' ile tam olarak neyi kastediyorsun?",("He said it would be ready soon.","But ___ 'soon'?",["So what you're saying is ...","Could you repeat ..."])),
  P("Could you give me an example of ...","... ile ilgili bir örnek verir misiniz?","B2","","Could you give me an example of a good answer?","İyi bir cevaba örnek verir misiniz?",("I don't see how to answer.","___ a good answer?",["Just to be clear, ...","Sorry, I didn't catch ..."])),
  P("Can you be more specific about ...","... konusunda daha net olabilir misiniz?","C1","","Can you be more specific about the dates?","Tarihler konusunda daha net olabilir misiniz?",("He only said 'next month'.","___ the dates?",["If I understand correctly, ...","I'm afraid I didn't quite hear ..."])),
  P("I'm not sure I understand why ...","Neden ... olduğunu tam anlamadım","C1","","I'm not sure I understand why the price changed.","Fiyatın neden değiştiğini tam anlamadım.",("The price went up.","___ the price changed.",["Could you speak a little more ...","Am I right in thinking that ..."])),
 ]},
]}
