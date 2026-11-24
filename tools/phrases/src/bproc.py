# Kalıplar: Süreç, değişim ve duyuru (Berlitz 6 temalarından esinlenilmiş, özgün) – B1/B2
import sys,os;sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'..'))
from ext_meta import fix
def P(en,tr,lv,reg,ex,extr,d):return {'en':en,'tr':tr,'lv':lv,'reg':reg,'ex':[ex,extr],'d':d}
GROUP={'id':'bproc','t':'Süreç, değişim ve duyuru','en':'Processes, changes and announcements',
'ins':'Bir işin adımlarını anlatmak, zaman içindeki değişimi göstermek ve kısa duyuru yapmak için kalıplar.',
'sub':[
 {'k':'pr1','t':'Adımları anlatmak','en':'Explaining a process','items':[
  P("The first step is to ...","İlk adım ... -mektir","B1","","The first step is to open a new account.","İlk adım yeni bir hesap açmaktır.",("How do I register?","___ open a new account."  ,["Prices have risen sharply.","May I have your attention, please?"])),
  P("Once you have done that, ...","Bunu yaptıktan sonra, ...","B1","","Once you have done that, click Save.","Bunu yaptıktan sonra Kaydet'e tıkla.",("I've typed my name.","___ click Save."  ,["Prices have risen sharply.","May I have your attention, please?"])),
  P("After that, you need to ...","Ondan sonra ... -men gerekiyor","B1","","After that, you need to wait for an email.","Ondan sonra bir e-posta beklemen gerekiyor.",("What comes next?","___ wait for an email."  ,["Prices have risen sharply.","May I have your attention, please?"])),
  P("Finally, make sure that ...","Son olarak, ... olduğundan emin ol","B2","","Finally, make sure that you log out.","Son olarak, oturumu kapattığından emin ol.",("Is that everything?","Almost. ___ you log out."  ,["Prices have risen sharply.","May I have your attention, please?"])),
 ]},
 {'k':'pr2','t':'Değişimi anlatmak','en':'Describing change','items':[
  P("It only takes a few minutes.","Yalnızca birkaç dakika sürer.","B1","","It only takes a few minutes. Then you are ready.","Yalnızca birkaç dakika sürer. Sonra hazırsın.",("Is it a long process?","No. ___ Then you are ready."  ,["Prices have risen sharply.","May I have your attention, please?"])),
  P("Prices have risen sharply.","Fiyatlar keskin biçimde yükseldi.","B2","","Prices have risen sharply this year.","Fiyatlar bu yıl keskin biçimde yükseldi.",("How is the market?","Not good. ___ this year."  ,["The first step is to ...","May I have your attention, please?"])),
  P("Everything is more expensive now.","Artık her şey daha pahalı.","B1","","Everything is more expensive now than last year.","Artık her şey geçen yıldan daha pahalı.",("Is life cheaper these days?","No. ___ than last year."  ,["The first step is to ...","May I have your attention, please?"])),
  P("It's getting harder and harder to ...","... gittikçe zorlaşıyor","B1","","It's getting harder and harder to find a flat.","Daire bulmak gittikçe zorlaşıyor.",("How is the housing market?","___ find a flat."  ,["The first step is to ...","May I have your attention, please?"])),
  P("There has been a steady increase in ...","... sürekli bir artış oldu","B2","","There has been a steady increase in online shopping.","Çevrimiçi alışverişte sürekli bir artış oldu.",("What does the chart show?","___ online shopping."  ,["The first step is to ...","May I have your attention, please?"])),
  P("Things have changed a lot since ...","... beri işler çok değişti","B1","","Things have changed a lot since I was a child.","Ben çocukken beri işler çok değişti.",("Do you like the old town?","It's different. ___ I was a child."  ,["The first step is to ...","May I have your attention, please?"])),
 ]},
 {'k':'pr3','t':'Duyuru yapmak','en':'Making an announcement','items':[
  P("May I have your attention, please?","Dikkatinizi çekebilir miyim?","B1","resmî","May I have your attention, please? The show is about to start.","Dikkatinizi çekebilir miyim? Gösteri başlamak üzere.",("(microphone)","___ The show is about to start."  ,["The first step is to ...","Prices have risen sharply."])),
  P("I'm pleased to announce that ...","... duyurmaktan memnuniyet duyuyorum","B2","resmî","I'm pleased to announce that we have won the contract.","Sözleşmeyi kazandığımızı duyurmaktan memnuniyet duyuyorum.",("Why is everyone clapping?","___ we have won the contract."  ,["The first step is to ...","Prices have risen sharply."])),
  P("Please note that ...","Lütfen şunu unutmayın: ...","B1","resmî","Please note that the office closes at five.","Lütfen ofisin beşte kapandığını unutmayın.",("Any other news?","Yes. ___ the office closes at five."  ,["The first step is to ...","Prices have risen sharply."])),
  P("That's all for now.","Şimdilik bu kadar.","B1","","That's all for now. Thank you for listening.","Şimdilik bu kadar. Dinlediğiniz için teşekkürler.",("Is there anything else?","No. ___ Thank you for listening."  ,["The first step is to ...","Prices have risen sharply."])),
 ]},
]}
fix(GROUP)
