# Kalıplar: get, take, go, come, keep ile phrasal verb'ler
def P(en,tr,lv,reg,ex,extr,d):return {'en':en,'tr':tr,'lv':lv,'reg':reg,'ex':[ex,extr],'d':d}
GROUP={'id':'gpv2','t':'Phrasal verb: get, take, go, come, keep','en':'Phrasal verbs with get, take, go, come and keep',
'ins':'Bu beş fiil, günlük İngilizcede en çok phrasal verb kuran fiillerdir. Aynı fiil, edatına göre bambaşka anlamlar kazanır (get over, get away, get across), bu yüzden hep birlikte öğren.',
'sub':[
 {'k':'vget','t':'get ile','en':'Phrasal verbs with get','items':[
  P("get away with ...","... -in cezasını çekmeden kurtulmak","C1","","He will not get away with cheating on the test.","Sınavda kopya çekip yırtamayacak.",("Did the teacher notice his cheating?","No, he got ___ it.",["take after ...","keep up with ..."])),
  P("get across ...","... -i anlatabilmek, karşıya geçirmek","C1","","I want to get across my point to him.","Fikrimi ona anlatmak istiyorum.",("Why was the meeting so difficult?","I tried to ___ my point.",["go through with ...","come up with ..."])),
  P("get round to ...","... -e sıra gelmek, ... -e vakit bulmak","C1","","I hope to get round to answering that email.","O e-postayı yanıtlamaya vakit bulmayı umuyorum.",("Did you reply to her?","Not yet. I hope to ___ it.",["take up ...","keep on ..."])),
  P("get by on ...","... ile idare etmek, geçinmek","B2","","I can get by on a small salary.","Küçük bir maaşla idare edebilirim.",("Is life expensive there?","A little, but we can ___ one income.",["come across ...","go off ..."])),
  P("get through to ...","... -e ulaşmak, ... -e derdini anlatmak","C1","","I tried to call, but I couldn't get through to him.","Aradım ama ona ulaşamadım.",("Why didn't you talk to the manager?","I couldn't ___ him on the phone.",["take over ...","keep up with ..."])),
 ]},
 {'k':'vtake','t':'take ile','en':'Phrasal verbs with take','items':[
  P("take after ...","... -e çekmek, ... -e benzemek","B2","","I want to take after my mother.","Annem gibi olmak istiyorum.",("Does she look like her father?","No, she wants to ___ her mother.",["get away with ...","come up with ..."])),
  P("take over ...","... -i devralmak","B2","","A new manager will take over the project.","Yeni bir yönetici projeyi devralacak.",("Who is running the team next year?","A new manager will ___ it.",["go off ...","keep on ..."])),
  P("take up ...","... -e başlamak (hobi), ... -i kaplamak","B2","","I decided to take up painting.","Resme başlamaya karar verdim.",("What are you doing in your free time?","I want to ___ painting.",["get by on ...","go through with ..."])),
  P("take in ...","... -i kavramak, ... -i kandırmak","C1","","Don't let him take in the old man.","Yaşlı adamı kandırmasına izin verme.",("Why was the old man so upset?","He lost money when someone tried to ___ him.",["come across ...","keep up with ..."])),
  P("take to ...","... -den hoşlanmaya başlamak","C1","","I hope to take to my new neighbours.","Yeni komşularımdan hoşlanmayı umuyorum.",("Do you like the new people?","Not yet, but I hope to ___ them.",["go off ...","get round to ..."])),
 ]},
 {'k':'vgo','t':'go ile','en':'Phrasal verbs with go and come','items':[
  P("go through with ...","... -i sonuna kadar götürmek","C1","","She will go through with the operation.","Ameliyatı sonuna kadar götürecek.",("Was she nervous about the operation?","Yes, but she will ___ it.",["take to ...","get by on ..."])),
  P("go off ...","... -den soğumak, bozulmak","C1","","I might go off coffee soon.","Yakında kahveden soğuyabilirim.",("Do you still drink coffee?","Not really. I might ___ it soon.",["take up ...","come up with ..."])),
  P("come up with ...","... -i bulmak, ... -i akıl etmek","B2","","Can you come up with a better plan?","Daha iyi bir plan bulabilir misin?",("Did anyone have a solution?","No. Can you ___ a better plan?",["take over ...","go through with ..."])),
  P("come across ...","... -e rastlamak","B2","","I might come across my old diary.","Eski günlüğüme rastlayabilirim.",("Do you know where your old diary is?","Not yet. I might ___ it in a drawer.",["get across ...","keep on ..."])),
  P("come down with ...","(hastalığa) yakalanmak","C1","","I hope I won't come down with flu.","Umarım gribe yakalanmam.",("Why are you wearing a scarf?","I hope I won't ___ flu.",["take after ...","get away with ..."])),
 ]},
 {'k':'vkeep','t':'keep ile','en':'Phrasal verbs with keep','items':[
  P("keep up with ...","... -e ayak uydurmak","B2","","It is hard to keep up with the news.","Haberlere ayak uydurmak zor.",("Why are you always on your phone?","I'm trying to ___ the news.",["take over ...","come across ..."])),
  P("keep on ...","... -e devam etmek","B2","","Please keep on talking despite the noise.","Lütfen gürültüye rağmen konuşmaya devam et.",("Should I stop when the music starts?","No, please ___ talking.",["go off ...","take in ..."])),
  P("keep from ...","... -den kendini alıkoymak","C1","","I couldn't keep from laughing.","Gülmekten kendimi alamadım.",("Was the film funny?","I couldn't ___ laughing.",["get through to ...","come down with ..."])),
  P("keep out of ...","... -e karışmamak, uzak durmak","C1","","Please keep out of my business.","Lütfen işime karışma.",("Can I give you some advice?","Please ___ my business.",["go through with ...","take up ..."])),
  P("keep back ...","... -i saklamak, geri tutmak","C1","","The company may keep back some of his pay.","Şirket maaşının bir kısmını tutabilir.",("Did he receive his full salary?","No, they may ___ part of it.",["get round to ...","come up with ..."])),
 ]},
]}
