# Kalıplar: Duygu belirtme (özgün örnekler)
def P(en,tr,lv,reg,ex,extr,d):return {'en':en,'tr':tr,'lv':lv,'reg':reg,'ex':[ex,extr],'d':d}
GROUP={'id':'gfeel','t':'Duygu belirtme','en':'Expressing feelings',
'ins':'"I am happy" ya da "I am sad" demek yerine duyguyu daha canlı anlatan kalıplar kullan. Sevinç, öfke ve endişe için ayrı kalıplar vardır; konuşma sınavında bu çeşitlilik fark yaratır.',
'sub':[
 {'k':'fpos','t':'Sevinç ve heyecan','en':'Happiness and excitement','items':[
  P("I'm over the moon about ...","... yüzünden çok mutluyum, havalara uçuyorum","B2","samimi","I'm over the moon about my new job.","Yeni işim yüzünden çok mutluyum.",("How do you feel about the job?","Great! ___ it.",["I'm really annoyed that ...","I feel uneasy about ..."])),
  P("I'm thrilled to ...","... -mekten heyecanlıyım","B2","","I'm thrilled to be part of the team.","Ekibin bir parçası olmaktan heyecanlıyım.",("Welcome aboard!","Thank you! ___ be here.",["It drives me crazy when ...","I'm a bit worried about ..."])),
  P("I'm really looking forward to ...","... -i dört gözle bekliyorum","B1","","I'm really looking forward to the holiday.","Tatili dört gözle bekliyorum.",("Are you excited about the trip?","Yes! ___ the holiday.",["I'm so disappointed that ...","I'm nervous about ..."])),
  P("It makes me so happy to ...","... beni çok mutlu ediyor","B2","","It makes me so happy to see my family.","Ailemi görmek beni çok mutlu ediyor.",("Why are you smiling?","___ see my family.",["I'm absolutely furious about ...","I can't stop thinking about ..."])),
  P("I couldn't be happier about ...","... konusunda bundan daha mutlu olamazdım","C1","","I couldn't be happier about the results.","Sonuçlardan daha mutlu olamazdım.",("Are you pleased with the results?","Absolutely, ___ them.",["It really gets on my nerves when ...","I'm relieved that ..."])),
 ]},
 {'k':'fneg','t':'Öfke ve hayal kırıklığı','en':'Anger and disappointment','items':[
  P("I'm really annoyed that ...","... -mesine gerçekten sinirlendim","B2","","I'm really annoyed that nobody told me.","Kimsenin bana söylememesine gerçekten sinirlendim.",("You look irritated.","Yes, ___ nobody told me.",["I'm over the moon about ...","I'm relieved that ..."])),
  P("It drives me crazy when ...","... olunca çıldırıyorum","B2","samimi","It drives me crazy when people talk loudly in the library.","İnsanlar kütüphanede yüksek sesle konuşunca çıldırıyorum.",("Why are you upset?","___ people are so loud.",["I'm thrilled to ...","I'm nervous about ..."])),
  P("I'm absolutely furious about ...","... yüzünden çok öfkeliyim","C1","","I'm absolutely furious about the delay.","Gecikme yüzünden çok öfkeliyim.",("Did the flight arrive on time?","No, and ___ the delay.",["I'm really looking forward to ...","I feel uneasy about ..."])),
  P("I'm so disappointed that ...","... -mesine çok hayal kırıklığına uğradım","B2","","I'm so disappointed that the concert was cancelled.","Konserin iptal olmasına çok hayal kırıklığına uğradım.",("What's wrong?","___ the concert was cancelled.",["It makes me so happy to ...","I can't stop thinking about ..."])),
  P("It really gets on my nerves when ...","... olunca sinirlerim bozuluyor","C1","samimi","It really gets on my nerves when he interrupts me.","Sözümü kesince sinirlerim bozuluyor.",("Why do you avoid him?","___ he interrupts me.",["I couldn't be happier about ...","I'm a bit worried about ..."])),
 ]},
 {'k':'fanx','t':'Endişe ve rahatlama','en':'Worry and relief','items':[
  P("I'm a bit worried about ...","... konusunda biraz endişeliyim","B1","","I'm a bit worried about tomorrow's exam.","Yarınki sınav konusunda biraz endişeliyim.",("Are you ready for the exam?","Not really, ___ tomorrow's exam.",["I'm over the moon about ...","It drives me crazy when ..."])),
  P("I'm nervous about ...","... konusunda gergin hissediyorum","B2","","I'm nervous about giving the speech.","Konuşma yapma konusunda gergin hissediyorum.",("Are you ready to speak?","A little. ___ giving the speech.",["I'm thrilled to ...","I'm absolutely furious about ..."])),
  P("I can't stop thinking about ...","... -i aklımdan çıkaramıyorum","C1","","I can't stop thinking about what he said.","Onun söylediğini aklımdan çıkaramıyorum.",("Why can't you sleep?","___ what he said.",["It makes me so happy to ...","I'm so disappointed that ..."])),
  P("I'm relieved that ...","... -mesine rahatladım","B2","","I'm relieved that the test is over.","Sınavın bitmesine rahatladım.",("How do you feel now?","Much better. ___ the test is over.",["I'm really annoyed that ...","I couldn't be happier about ..."])),
  P("I feel uneasy about ...","... konusunda tedirginim","C1","","I feel uneasy about travelling alone at night.","Geceleyin yalnız seyahat etme konusunda tedirginim.",("Are you going home alone?","Yes, but ___ it.",["I'm really looking forward to ...","It really gets on my nerves when ..."])),
 ]},
]}
