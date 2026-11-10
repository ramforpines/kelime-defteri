import sys,os;sys.path.insert(0,os.path.dirname(os.path.dirname(os.path.abspath(__file__))));from gl import Q
DQ=[
 Q(2,'Soru yapma','___ does the next train leave?','When',['Who','Which'],'Zaman: When.'),
 Q(2,'Soru yapma','___ is your new flat like?','What',['How','Which'],'Bir şeyin nasıl olduğunu sorma: What ... like?'),
 Q(2,'Soru yapma','___ long does it take to get to the airport?','How',['What','Which'],'Süre: How long.'),
 Q(2,'Soru yapma','___ bag is this? Is it yours?','Whose',["Who's",'Who'],'Sahiplik: Whose + isim.'),
 Q(2,'Soru yapma','___ do you go to the gym? Twice a week?','How often',['How much','How long'],'Sıklık: How often.'),
 Q(2,'Soru yapma','___ T-shirt do you prefer, the red one or the blue one?','Which',['What','Who'],'Sınırlı seçenek: Which.'),
 Q(3,'Özne sorusu','Who ___ the window?','broke',['did break','did broke'],'Özne sorusunda did kullanılmaz.'),
 Q(3,'Edatlı soru','Who are you ___ to?','talking',['talk','talks'],'Edat soru sonunda kalır: Who are you talking to?'),
 Q(3,'Dolaylı soru','Could you tell me where the station ___?','is',['is it','does'],'Dolaylı soruda düz cümle sırası: where the station is.'),
 Q(3,'Etiket soru',"You're coming to the party, ___?","aren't you",["don't you","isn't it"],'Olumlu cümle + olumsuz etiket: aren\'t you?'),
]
