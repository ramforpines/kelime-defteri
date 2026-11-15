# Kalıplar: Telefon ve e-posta (özgün örnekler)
def P(en,tr,lv,reg,ex,extr,d):return {'en':en,'tr':tr,'lv':lv,'reg':reg,'ex':[ex,extr],'d':d}
GROUP={'id':'gtel','t':'Telefon ve e-posta','en':'Phone calls and emails',
'ins':'Telefonda ve e-postada kullanılan kalıplar sabittir; bunları olduğu gibi öğrenmek profesyonel görünmeni sağlar. Resmî e-postalarda "I am writing to", telefonda "Could I speak to" gibi kalıplar neredeyse zorunludur.',
'sub':[
 {'k':'tcall','t':'Telefonu açma ve arama','en':'Starting a phone call','items':[
  P("Could I speak to ...","... ile görüşebilir miyim?","B1","resmî","Could I speak to the manager, please?","Müdürle görüşebilir miyim lütfen?",("Who do you want to talk to?","___ the manager, please?",["I'll pass on the message to ...","Please find attached ..."])),
  P("I'm calling about ...","... hakkında arıyorum","B1","","I'm calling about the apartment you advertised.","İlan verdiğiniz daire hakkında arıyorum.",("Why are you calling?","___ the apartment you advertised.",["Thank you for calling ...","I am writing to ..."])),
  P("I'm returning your call about ...","... hakkındaki aramanıza geri dönüyorum","C1","resmî","I'm returning your call about the invoice.","Fatura hakkındaki aramanıza geri dönüyorum.",("You left a message earlier.","Yes, ___ the invoice.",["Could you ask him to call me back ...","I would be grateful if you could ..."])),
  P("Could you put me through to ...","Beni ... a bağlayabilir misiniz?","B2","resmî","Could you put me through to the sales department?","Beni satış departmanına bağlayabilir misiniz?",("I need to reach sales.","___ the sales department?",["I'm afraid he's not available ...","Further to ..."])),
  P("Could you hold on ...","... biraz bekler misiniz?","B1","","Could you hold on a moment, please?","Bir dakika bekler misiniz lütfen?",("He is in another office.","___ a moment, please?",["Can I take a message ...","Further to ..."])),
 ]},
 {'k':'tmsg','t':'Mesaj bırakma ve görüşmeyi bitirme','en':'Taking messages and ending a call','items':[
  P("Can I take a message ...","Mesaj alabilir miyim?","B1","","Can I take a message for her?","Onun için mesaj alabilir miyim?",("She is not in.","___ for her?",["Could I speak to ...","I am writing to ..."])),
  P("Could you ask him to call me back ...","Beni geri aramasını söyler misiniz?","B2","","Could you ask him to call me back this afternoon?","Öğleden sonra beni geri aramasını söyler misiniz?",("He's not available.","___ this afternoon?",["I'm calling about ...","Please find attached ..."])),
  P("I'll pass on the message to ...","Mesajı ... -e iletirim","B2","","I'll pass on the message to Mr Brown.","Mesajı Bay Brown'a iletirim.",("Can you tell him I called?","Of course, ___ Mr Brown.",["Could you hold on ...","I would be grateful if you could ..."])),
  P("I'm afraid he's not available ...","Maalesef kendisi şu an müsait değil ...","B2","resmî","I'm afraid he's not available at the moment.","Maalesef kendisi şu an müsait değil.",("Can I speak to Mr Smith?","Sorry, ___ at the moment.",["Could you put me through to ...","Further to ..."])),
  P("Thank you for calling ...","Aradığınız için teşekkürler","B1","resmî","Thank you for calling our customer service.","Müşteri hizmetlerimizi aradığınız için teşekkürler.",("How does the operator end the call?","___ our customer service.",["I'm returning your call about ...","I look forward to hearing from you ..."])),
 ]},
 {'k':'temail','t':'E-posta açılış ve kapanış','en':'Starting and ending emails','items':[
  P("I am writing to ...","... -mek için yazıyorum","B2","resmî","I am writing to apply for the position of manager.","Müdürlük pozisyonuna başvurmak için yazıyorum.",("How do you begin a formal email?","___ apply for the position.",["Could I speak to ...","Can I take a message ..."])),
  P("Please find attached ...","Ekte ... bulabilirsiniz","B2","resmî","Please find attached my CV.","Ekte özgeçmişimi bulabilirsiniz.",("Where is the file you promised?","___ my CV.",["I'm calling about ...","Could you hold on ..."])),
  P("I would be grateful if you could ...","... -ebilirseniz minnettar olurum","C1","resmî","I would be grateful if you could confirm the date.","Tarihi onaylayabilirseniz minnettar olurum.",("What do you ask the client?","___ confirm the date.",["Could you put me through to ...","I'll pass on the message to ..."])),
  P("Further to ...","... ile ilgili olarak (devamında)","C1","resmî","Further to our phone call, I am sending the details.","Telefon görüşmemizin devamında ayrıntıları gönderiyorum.",("Why are you emailing him?","___ our phone call, here are the details.",["I'm afraid he's not available ...","Thank you for calling ..."])),
  P("I look forward to hearing from you ...","Sizden haber bekliyorum","B2","resmî","I look forward to hearing from you soon.","Yakında sizden haber bekliyorum.",("How do you close the email?","___ soon.",["Could you ask him to call me back ...","I'm returning your call about ..."])),
 ]},
]}
