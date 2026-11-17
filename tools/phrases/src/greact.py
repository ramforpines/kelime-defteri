# Kalıplar: İlgi gösterme ve tepki (özgün örnekler)
def P(en,tr,lv,reg,ex,extr,d):return {'en':en,'tr':tr,'lv':lv,'reg':reg,'ex':[ex,extr],'d':d}
GROUP={'id':'greact','t':'İlgi gösterme ve tepki','en':'Showing interest and reacting',
'ins':'Sohbette iyi bir dinleyici olmak, doğru zamanda doğru tepkiyi vermekle olur. Merak, şaşkınlık ve anlayış kalıpları konuşmayı sürdürür ve karşındakine ilgi gösterdiğini belli eder.',
'sub':[
 {'k':'rint','t':'İlgi ve merak gösterme','en':'Showing interest','items':[
  P("Tell me more about ...","Bana ... hakkında daha fazla anlat","B2","","Tell me more about your trip to Japan.","Bana Japonya gezinden biraz daha anlat.",("I just got back from Japan.","Really? ___ your trip.",["I can't believe ...","I'm sorry to hear about ..."])),
  P("I'd love to hear more about ...","... hakkında daha fazlasını duymak isterim","B2","","I'd love to hear more about your new job.","Yeni işin hakkında daha fazlasını duymak isterim.",("I started a new job last week.","Great! ___ it.",["I had no idea that ...","I can imagine how ..."])),
  P("How did you get into ...","... e nasıl başladın?","C1","","How did you get into rock climbing?","Kaya tırmanışına nasıl başladın?",("I love climbing.","Interesting! ___ it?",["I'm amazed that ...","That must have been ..."])),
  P("I'm curious about ...","... merak ediyorum","B2","","I'm curious about how the machine works.","Makinenin nasıl çalıştığını merak ediyorum.",("Why are you reading the manual?","Because ___ how it works.",["It's hard to believe that ...","I'm sorry to hear about ..."])),
  P("What made you decide to ...","... -meye ne karar verdirdi?","C1","","What made you decide to study abroad?","Yurtdışında okumaya ne karar verdirdi?",("I'm moving to Canada.","Wow! ___ go there?",["I can't believe ...","I can imagine how ..."])),
 ]},
 {'k':'rsurp','t':'Şaşkınlık bildirme','en':'Showing surprise','items':[
  P("I can't believe ...","... -e inanamıyorum","B2","samimi","I can't believe it is already December.","Aralık ayına geldiğimize inanamıyorum.",("Look at the calendar.","Oh, ___ it is already December.",["Tell me more about ...","That must have been ..."])),
  P("I had no idea that ...","... -diğinden haberim yoktu","B2","","I had no idea that you could play the piano.","Piyano çalabildiğinden haberim yoktu.",("I play the piano.","Really? ___ you could.",["I'd love to hear more about ...","I can imagine how ..."])),
  P("I'm amazed that ...","... -mesine şaşırdım","C1","","I'm amazed that nobody noticed the mistake.","Kimsenin hatayı fark etmemesine şaşırdım.",("Nobody saw the typo.","Yes, ___ nobody noticed it.",["How did you get into ...","I'm sorry to hear about ..."])),
  P("It's hard to believe that ...","... -ine inanmak zor","C1","","It's hard to believe that he is only twelve.","Onun sadece on iki yaşında olduğuna inanmak zor.",("He plays like a professional.","___ he is only twelve.",["I'm curious about ...","That must have been ..."])),
  P("I never would have guessed ...","... -ini asla tahmin edemezdim","C1","","I never would have guessed that she was a doctor.","Onun doktor olduğunu asla tahmin edemezdim.",("She is a famous surgeon.","Really? ___ that.",["What made you decide to ...","I can imagine how ..."])),
 ]},
 {'k':'rsym','t':'Anlayış ve üzüntü bildirme','en':'Showing sympathy','items':[
  P("I'm sorry to hear about ...","... duyduğuma üzüldüm","B2","","I'm sorry to hear about your accident.","Kazanı duyduğuma üzüldüm.",("I had a car accident last week.","Oh no! ___ it.",["Tell me more about ...","I'm amazed that ..."])),
  P("That must have been ...","Bu ... olmuş olmalı","B2","","That must have been a difficult time for you.","Bu senin için zor bir dönem olmuş olmalı.",("I lost my job last year.","___ really hard for you.",["I can't believe ...","How did you get into ..."])),
  P("I can imagine how ...","... -diğini tahmin edebiliyorum","C1","","I can imagine how tired you must feel.","Ne kadar yorgun olduğunu tahmin edebiliyorum.",("I worked three nights in a row.","___ tired you are.",["I'm curious about ...","I had no idea that ..."])),
  P("I know how you feel about ...","... hakkında ne hissettiğini biliyorum","C1","","I know how you feel about moving house.","Taşınma konusunda ne hissettiğini biliyorum.",("I hate packing boxes.","Yes, ___ moving.",["It's hard to believe that ...","What made you decide to ..."])),
  P("Hang in there ...","Dayan, pes etme ...","B2","samimi","Hang in there, the exams will be over soon.","Dayan, sınavlar yakında biter.",("I'm so stressed about exams.","___ they will end soon.",["I never would have guessed ...","I'd love to hear more about ..."])),
 ]},
]}
