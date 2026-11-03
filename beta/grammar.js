/* Gramer konu anlatımları (taslak, yalnızca beta). *...* = vurgulanan gramer parçası. Örnek cümleler ve kelimeler uygulamanın seviyelerine uygun seçilir. */
window.GRAMMAR=[
{id:'present-perfect',lv:'A2',title:'Present Perfect',form_name:'have / has + V3',
 sub:'Geçmişte olmuş ama şimdiyle bağı olan durumları anlatır: yaşanmış deneyim, sonucu şimdi görülen olay ve hâlâ süren durum.',
 form:[
  {k:'Olumlu',p:'I / you / we / they + *have* + V3',e:['I *have finished* my homework.','Ödevimi bitirdim.']},
  {k:'Olumlu',p:'he / she / it + *has* + V3',e:['She *has finished* her homework.','O ödevini bitirdi.']},
  {k:'Olumsuz',p:'have / has + *not* + V3',e:['We *haven\'t seen* that film.','O filmi görmedik.']},
  {k:'Soru',p:'*Have / Has* + özne + V3?',e:['*Have* you *tried* sushi?','Hiç suşi denedin mi?']}],
 uses:[
  {h:'1. Hayat deneyimi',why:'Hayatın içinde bir zaman bir şey yapıp yapmadığını söylersin; ne zaman olduğu önemli değildir. "Hiç ...?" sorusu ve "hiç ... yapmadım" cümleleri bunu anlatır.',
   ex:[['I *have visited* Paris twice.','Paris\'i iki kez ziyaret ettim.'],['*Have* you ever *tried* sushi?','Hiç suşi denedin mi?'],['She *has never flown* in a plane.','O hiç uçağa binmedi.']]},
  {h:'2. Sonucu şimdi görülen olay',why:'Olay geçmişte olmuştur ama etkisi şu an devam eder. "Az önce", "zaten", "henüz" gibi kelimelerle sık kullanılır.',
   ex:[['I *have lost* my keys.','Anahtarlarımı kaybettim. (Şu an yok.)'],['They *have just arrived*.','Az önce geldiler.'],['He *has already finished* his work.','İşini çoktan bitirdi.']]},
  {h:'3. Hâlâ süren durum',why:'Geçmişte başlayan ve şu an devam eden durumlar için <b>for</b> (ne kadar süredir) ve <b>since</b> (ne zamandan beri) kullanılır.',
   ex:[['We *have lived* here *for* ten years.','On yıldır burada yaşıyoruz.'],['I *have known* her *since* 2015.','Onu 2015\'ten beri tanıyorum.']]},
  {h:'4. Yeni gelişmeler ve "yet"',why:'Olumsuz ve soru cümlelerinde cümle sonunda <b>yet</b> (henüz) kullanılır.',
   ex:[['*Have* you *done* your homework *yet*?','Ödevini henüz yaptın mı?'],['I *haven\'t seen* the film *yet*.','Filmi henüz görmedim.']]}],
 signals:[['ever','hiç (soru)'],['never','hiç (olumsuz)'],['already','çoktan'],['yet','henüz'],['just','az önce'],['recently','yakın zamanda'],['since','…den beri'],['for','…dir (süre)'],['so far','şimdiye kadar'],['this week','bu hafta']],
 vs:{a:['I *saw* that film last year.','O filmi geçen yıl izledim.','Bitmiş zaman belirtilir (last year) → Past Simple'],b:['I *have seen* that film.','O filmi izledim (biliyorum).','Zaman belirtilmez, deneyim önemlidir → Present Perfect']},
 mistakes:[
  {bad:'I have seen him yesterday.',good:'I saw him yesterday.',why:'yesterday, last week, ago gibi bitmiş zaman ifadeleriyle Present Perfect kullanılmaz.'},
  {bad:'She has went home.',good:'She has gone home.',why:'have / has ile fiilin 3. hâli (V3) kullanılır: go → went → gone.'},
  {bad:'I am here since Monday.',good:'I have been here since Monday.',why:'since / for ile süren durumlarda Present Perfect kullanılır.'}],
 tip:'Türkçede "-dı" ve "-mıştır" ikisi de geçmişi anlatır. İngilizcede zaman (dün, geçen yıl) söylüyorsan Past Simple, söylemiyorsan ve şimdiyle bağ varsa Present Perfect kullan.',
 vocab:['experience','achieve','manage','improve','recently','already','yet','ever','never','since'],
 quiz:[
  {q:'She ___ never ___ to Italy.',o:['has / been','have / been','is / been'],a:0,w:'she → has; never ile Present Perfect: has never been.'},
  {q:'I ___ him yesterday.',o:['have seen','saw','has seen'],a:1,w:'yesterday bitmiş zaman belirtir → Past Simple.'},
  {q:'We have lived here ___ 2018.',o:['for','since','from'],a:1,w:'2018 bir başlangıç noktasıdır → since. (for + süre: for five years)'},
  {q:'___ you finished the report yet?',o:['Did','Have','Are'],a:1,w:'yet ile Present Perfect: Have you finished…?'}]},
{id:'second-conditional',lv:'B1',title:'Second Conditional',form_name:'If + Past Simple, would + V1',
 sub:'Şu an gerçek olmayan ya da gerçekleşmesi çok zor durumları hayal ederken ve tavsiye verirken kullanılır.',
 form:[
  {k:'Kalıp',p:'*If* + özne + Past Simple, özne + *would* + V1',e:['*If* I *had* more time, I *would learn* French.','Daha çok vaktim olsaydı Fransızca öğrenirdim.']},
  {k:'Ters sıra',p:'özne + *would* + V1 + *if* + Past Simple',e:['I *would travel* more *if* I *had* more money.','Daha çok param olsaydı daha çok seyahat ederdim.']},
  {k:'Olumsuz',p:'If + Past Simple, *wouldn\'t* + V1',e:['If she *were* here, she *wouldn\'t say* that.','O burada olsaydı bunu söylemezdi.']},
  {k:'Soru',p:'*What would* you do *if* + Past Simple?',e:['*What would* you do *if* you *won* the lottery?','Piyangoyu kazansan ne yapardın?']}],
 uses:[
  {h:'1. Hayali durumlar',why:'Şu an doğru olmayan bir durumu "olsaydı ne olurdu" diye düşünürsün. Fiil Past Simple olsa da anlam geçmiş değil, şimdiki hayaldir.',
   ex:[['If I *were* rich, I *would buy* a big house.','Zengin olsaydım büyük bir ev alırdım.'],['If he *studied* harder, he *would pass* the exam.','Daha çok çalışsa sınavı geçerdi.']]},
  {h:'2. Tavsiye: If I were you',why:'Birine tavsiye verirken kullanılan çok yaygın bir kalıptır. <b>were</b> tüm öznelerle kullanılır.',
   ex:[['If I *were* you, I *would apologise*.','Senin yerinde olsam özür dilerdim.'],['I *wouldn\'t do* that if I *were* you.','Senin yerinde olsam bunu yapmazdım.']]},
  {h:'3. Olası ama pek mümkün olmayan durumlar',why:'Gerçekleşmesi çok düşük bir ihtimali konuşurken Second Conditional kullanılır. Gerçekleşmesi mümkünse First Conditional (If + Present, will) kullanılır.',
   ex:[['If I *won* the lottery, I *would travel* the world.','Piyangoyu kazansam dünyayı gezerdim.'],['If it *rains*, we *will stay* home. (mümkün → First)','Yağmur yağarsa evde kalırız.']]}],
 signals:[['if','eğer'],['would','…ırdı'],['were','olsaydım (tüm özneler)'],['imagine','hayal et'],['suppose','varsay'],['what if','ya … olsaydı']],
 vs:{a:['If I *have* time, I *will call* you.','Vaktim olursa seni ararım.','Gerçekçi ihtimal → First Conditional'],b:['If I *had* time, I *would call* you.','Vaktim olsa seni ararım.','Şu an vakit yok / ihtimal düşük → Second Conditional']},
 mistakes:[
  {bad:'If I would have money, I would buy it.',good:'If I had money, I would buy it.',why:'if bölümünde would kullanılmaz; Past Simple kullanılır.'},
  {bad:'If I will see him, I would tell him.',good:'If I saw him, I would tell him.',why:'if bölümünde will / would olmaz.'},
  {bad:'If I was you, I would go.',good:'If I were you, I would go.',why:'Resmî ve doğru kullanım were\'dir (günlük konuşmada was da duyulur).'}],
 tip:'Past Simple görünce "geçmiş" diye düşünme: burada zaman geçmiş değil, gerçeklikten uzaklık anlatılıyor. Fiil geçmiş olduğu için "ihtimal uzak" mesajı verir.',
 vocab:['imagine','suppose','wish','apologise','suggest','regret','unless','provided'],
 quiz:[
  {q:'If I ___ you, I would study more.',o:['am','was','were'],a:2,w:'Tavsiye kalıbında If I were you kullanılır.'},
  {q:'If she ___ more money, she would buy a car.',o:['has','had','would have'],a:1,w:'if bölümü Past Simple olur: had.'},
  {q:'What ___ you do if you lost your job?',o:['will','would','did'],a:1,w:'Hayali durum: What would you do if…?'},
  {q:'I would help you if I ___ the answer.',o:['know','knew','would know'],a:1,w:'if bölümü Past Simple: knew.'}]}
];
window.GRAMMAR_PLAN={A1:['to be (am/is/are)','Present Simple','There is / There are','a / an / the','Çoğul isimler','İyelik (my, your, \'s)','can / can\'t'],A2:['Past Simple','Present Continuous','Karşılaştırma ve üstünlük','will / going to','Sayılabilir / sayılamaz','must / have to'],B1:['Present Perfect Continuous','Passive (basit)','First Conditional','Relative clauses','used to','Reported speech (temel)'],B2:['Third Conditional','Passive (tüm zamanlar)','Reported speech','wish / if only','Modals of deduction','Gerund ve infinitive'],C1:['Inversion','Mixed conditionals','Cleft sentences','Advanced linkers'],C2:['İnce anlam farkları ve üslup']};
