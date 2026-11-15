# Kalıplar: Rica ve izin (özgün örnekler)
def P(en,tr,lv,reg,ex,extr,d):return {'en':en,'tr':tr,'lv':lv,'reg':reg,'ex':[ex,extr],'d':d}
GROUP={'id':'greq','t':'Rica ve izin','en':'Requests and permission',
'ins':'Rica ederken ve izin isterken doğrudan "Give me" ya da "Can I" demek çoğu ortamda sert kaçar. Daha kibar kalıplar ricayı yumuşatır; cevap verirken de reddetmenin kibar yolları vardır.',
'sub':[
 {'k':'qreq','t':'Rica etme','en':'Making a request','items':[
  P("Could you possibly ...","Mümkünse ... -ebilir misiniz?","B2","resmî","Could you possibly send me the file today?","Mümkünse dosyayı bugün bana gönderebilir misiniz?",("What do you need from her?","___ send me the file today?",["Do you mind if I ...","Feel free to ..."])),
  P("Would you mind ...","... -meniz mümkün mü?","B2","","Would you mind opening the window?","Pencereyi açmanız mümkün mü?",("It's very hot in here.","___ opening the window?",["May I ...","I'm afraid I can't ..."])),
  P("I was wondering if you could ...","... -ebilir misiniz diye merak ediyordum","C1","resmî","I was wondering if you could help me with this form.","Bu formda bana yardım edebilir misiniz diye merak ediyordum.",("How do you ask the clerk for help?","___ help me with this form.",["Is it all right if I ...","By all means ..."])),
  P("Would it be possible to ...","... -mek mümkün olur mu?","C1","resmî","Would it be possible to change my appointment?","Randevumu değiştirmek mümkün olur mu?",("The date doesn't suit me.","___ change my appointment?",["I'd rather you didn't ...","Would it be okay if I ..."])),
  P("I'd really appreciate it if you could ...","... -ebilirseniz çok memnun olurum","C1","resmî","I'd really appreciate it if you could reply soon.","Yakında yanıt verebilirseniz çok memnun olurum.",("How do you end the polite email?","___ reply soon.",["Do you mind if I ...","I'm afraid it's not possible to ..."])),
 ]},
 {'k':'qperm','t':'İzin isteme','en':'Asking for permission','items':[
  P("May I ...","... -ebilir miyim?","B1","resmî","May I borrow your pen for a moment?","Kalemini bir an ödünç alabilir miyim?",("You want a pen.","___ borrow your pen?",["Would you mind ...","Feel free to ..."])),
  P("Is it all right if I ...","... -mem sorun olur mu?","B2","","Is it all right if I sit here?","Buraya oturmam sorun olur mu?",("The seat looks free.","___ sit here?",["Could you possibly ...","I'd rather you didn't ..."])),
  P("Do you mind if I ...","... -mamın bir sakıncası var mı?","B2","","Do you mind if I open the window?","Pencereyi açmamın bir sakıncası var mı?",("It's stuffy in the room.","___ open the window?",["I was wondering if you could ...","By all means ..."])),
  P("Would it be okay if I ...","... -sam uygun olur mu?","B2","","Would it be okay if I came a bit late?","Biraz geç gelsem uygun olur mu?",("Can you arrive on time?","___ came a bit late?",["Would it be possible to ...","I'm afraid I can't ..."])),
  P("I was wondering whether I could ...","... -ebilir miyim diye merak ediyordum","C1","resmî","I was wondering whether I could leave early today.","Bugün erken çıkabilir miyim diye merak ediyordum.",("How do you ask your boss politely?","___ leave early today.",["I'd really appreciate it if you could ...","Feel free to ..."])),
 ]},
 {'k':'qrep','t':'İzin verme ve reddetme','en':'Granting or refusing','items':[
  P("Feel free to ...","Çekinmeden ... -ebilirsin","B2","","Feel free to use my desk.","Çekinmeden masamı kullanabilirsin.",("May I use your desk?","Of course. ___ use it.",["I'm afraid I can't ...","Could you possibly ..."])),
  P("By all means ...","Elbette, buyurun ...","C1","resmî","By all means, take a seat.","Elbette, oturun.",("May I sit down?","___ take a seat.",["I'd rather you didn't ...","Do you mind if I ..."])),
  P("I'm afraid I can't ...","Maalesef ... -emem","B2","","I'm afraid I can't lend you the car today.","Maalesef sana bugün arabayı veremem.",("Can I borrow your car?","Sorry, ___ lend it today.",["Feel free to ...","Would you mind ..."])),
  P("I'd rather you didn't ...","... -mamanı tercih ederim","C1","","I'd rather you didn't smoke in here.","Burada sigara içmemeni tercih ederim.",("Do you mind if I smoke?","Actually, ___ smoke in here.",["By all means ...","May I ..."])),
  P("I'm afraid it's not possible to ...","Maalesef ... mümkün değil","C1","resmî","I'm afraid it's not possible to change the booking.","Maalesef rezervasyonu değiştirmek mümkün değil.",("Can I move my reservation?","Sorry, ___ change the booking.",["Would it be okay if I ...","I was wondering if you could ..."])),
 ]},
]}
