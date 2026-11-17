# Kalıplar: Beğeni ve tercih (özgün örnekler)
def P(en,tr,lv,reg,ex,extr,d):return {'en':en,'tr':tr,'lv':lv,'reg':reg,'ex':[ex,extr],'d':d}
GROUP={'id':'glike','t':'Beğeni ve tercih','en':'Likes, dislikes and preferences',
'ins':'Sevdiğin şeyi ve tercihini anlatırken "like" ve "prefer" ile yetinme. Kalıplar hem konuşmanı doğal yapar hem de speaking sınavlarında seviyeni gösterir. Kalıbın ardından isim ya da -ing gelir.',
'sub':[
 {'k':'llike','t':'Beğenme ve sevme','en':'Saying what you like','items':[
  P("I'm really into ...","... çok ilgimi çekiyor, ... a bayılıyorum","B2","samimi","I'm really into photography these days.","Bu aralar fotoğrafçılığa bayılıyorum.",("What do you do in your free time?","___ photography these days.",["I can't stand ...","I'd much rather ..."])),
  P("I'm fond of ...","... -i severim, ... e düşkünüm","B2","","I'm fond of long walks by the sea.","Deniz kenarında uzun yürüyüşleri severim.",("Do you enjoy the seaside?","Yes, ___ long walks there.",["I'm fed up with ...","I'd opt for ..."])),
  P("I can't get enough of ...","... -e doyamıyorum","C1","samimi","I can't get enough of this song.","Bu şarkıya doyamıyorum.",("Why are you playing it again?","Because ___ this song.",["I have no interest in ...","I'm not a big fan of ..."])),
  P("I have a soft spot for ...","... -e zaafım var","C1","","I have a soft spot for old black-and-white films.","Eski siyah beyaz filmlere zaafım var.",("Do you like classic movies?","Yes, ___ old films.",["I find it rather boring to ...","I'd sooner ..."])),
  P("I'm keen on ...","... -e meraklıyım, ... -i çok severim","B2","","I'm keen on trying new restaurants.","Yeni restoranlar denemeye meraklıyım.",("What do you enjoy about travel?","___ trying local food.",["I can't stand ...","I'm more of a ..."])),
 ]},
 {'k':'ldis','t':'Sevmeme ve hoşlanmama','en':'Saying what you dislike','items':[
  P("I can't stand ...","... -e katlanamam","B2","","I can't stand waiting in long queues.","Uzun kuyruklarda beklemeye katlanamam.",("Why do you avoid the post office?","Because ___ long queues.",["I'm really into ...","I'm fond of ..."])),
  P("I'm not a big fan of ...","... in pek hayranı değilim","B2","samimi","I'm not a big fan of horror films.","Korku filmlerinin pek hayranı değilim.",("Shall we watch a horror film?","Hmm, ___ horror films.",["I'm keen on ...","I have a soft spot for ..."])),
  P("I'm fed up with ...","... den bıktım","B2","samimi","I'm fed up with this noisy neighbourhood.","Bu gürültülü mahalleden bıktım.",("Why do you want to move?","Because ___ the noise.",["I can't get enough of ...","I'd opt for ..."])),
  P("I find it rather boring to ...","... -mek bence oldukça sıkıcı","C1","","I find it rather boring to listen to long speeches.","Uzun konuşmaları dinlemeyi oldukça sıkıcı buluyorum.",("Did you enjoy the lecture?","No, ___ listen to lectures.",["I'm really into ...","I'm more of a ..."])),
  P("I have no interest in ...","... a hiç ilgim yok","C1","resmî","I have no interest in sports at all.","Spora hiç ilgim yok.",("Will you watch the match with us?","No, ___ football.",["I'm fond of ...","I'd much rather ..."])),
 ]},
 {'k':'lpref','t':'Tercih belirtme','en':'Saying what you prefer','items':[
  P("I'd much rather ...","... -meyi tercih ederim (yalın fiil)","B2","","I'd much rather stay at home tonight.","Bu akşam evde kalmayı tercih ederim.",("Do you want to go out tonight?","No, ___ stay in.",["I can't stand ...","I'm really into ..."])),
  P("I'm more of a ...","Ben daha çok ... tipiyim","B2","","I'm more of a tea person than a coffee person.","Ben kahveden çok çay tipiyim.",("Would you like coffee?","No, thanks. ___ tea person.",["I'm fed up with ...","I have no interest in ..."])),
  P("I'd sooner ...","... -meyi daha çok isterim (yalın fiil)","C1","","I'd sooner walk than wait for the bus.","Otobüsü beklemektense yürümeyi tercih ederim.",("Shall we take the bus?","I'd rather not. ___ walk.",["I find it rather boring to ...","I'm keen on ..."])),
  P("I'd opt for ...","... -i seçerdim","B2","","I'd opt for the blue one.","Ben maviyi seçerdim.",("Which jacket looks better?","Well, ___ the blue one.",["I can't get enough of ...","I'm not a big fan of ..."])),
  P("I lean towards ...","... a yöneliyorum, ... -i tercih ediyorum","C1","","I lean towards quiet cafés when I study.","Çalışırken sessiz kafeleri tercih ediyorum.",("Where do you usually study?","___ quiet cafés.",["I'm fed up with ...","I have a soft spot for ..."])),
 ]},
]}
