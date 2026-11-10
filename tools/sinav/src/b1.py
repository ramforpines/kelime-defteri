# B1 Preliminary (PET): sınav ve çalışma bölümü
import os,sys
sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'..'))
from common import load,pet,PETDIR
P1=load(os.path.join(PETDIR,'src','pet1.py'));P2=load(os.path.join(PETDIR,'src','pet2.py'));P3=load(os.path.join(PETDIR,'src','pet3.py'))
WS=load(os.path.join(PETDIR,'ws.py'),'W');SS=load(os.path.join(PETDIR,'ws.py'),'S')+load(os.path.join(PETDIR,'src','ws3.py'),'S')
PP1={p['k']:p for p in P1['parts']};PP2={p['k']:p for p in P2['parts']};PP3={p['k']:p for p in P3['parts']}

W_EXAM=[
 {'id':'b1x-w1','part':1,'t':'Part 1 · E-posta: İngilizce kulübü',
  'in':'Read this email from your English teacher, Mr Clark, and the notes you have made. Write your email to Mr Clark using all the notes. Write about 100 words.',
  'mail':'From: Mr Clark\nSubject: English club\n\nDear students,\nWe are starting an English club after school this term. [Great idea!]\nWe can meet on Tuesdays or Fridays. Which day is better for you? [Say which and why]\nWhat activities would you like to do in the club? [Suggest ...]\nCould you also help us to tell other students about the club? [Yes, I can ...]\nBest wishes,\nMr Clark',
  'pts':[('Fikri beğendiğini söyle',['great','good idea','love','excited','fantastic','brilliant','sounds']),('Gün seç ve nedenini söyle',['tuesday','friday']),('Etkinlik öner',['film','game','play','song','quiz','drama','speak','talk','music','book','debate']),('Diğer öğrencilere nasıl haber vereceğini söyle',['poster','tell','social media','message','website','class','friends','announce'])],
  'min':80,'max':130,
  'model':'Dear Mr Clark,\nThank you for your email. I think an English club is a great idea, and I would love to join it.\nFriday would be better for me, because I have basketball training on Tuesdays after school. Also, on Fridays we don\'t have much homework, so everyone will be more relaxed.\nIn the club, we could watch short English films and talk about them. It would also be fun to play quiz games and sing songs together.\nOf course I can help. I could make some posters for the school corridors and send a message to my classmates.\nBest wishes,\nDeniz'},
 {'choice':[
  {'id':'b1x-w2','part':2,'kind':'article','t':'Part 2 · Makale: Unutulmaz bir gün',
   'in':'You see this announcement in an English-language magazine. Write your article in about 100 words.',
   'mail':'ARTICLES WANTED!\nA day I will never forget\nTell us about a special day in your life. What happened? Who were you with? Why will you always remember it?\nThe best articles will be published next month.',
   'pts':[('Ne olduğunu anlat',['was','were','went','had','happened','saw']),('Kiminle olduğunu söyle',['with','friend','family','mother','father','sister','brother','cousin','grandmother','grandfather']),('Neden unutamayacağını açıkla',['because','never forget','remember','special','reason','so']),('Bir başlık kullan',['@title'])],
   'min':80,'max':140,
   'model':'My first concert\nThe day I will never forget is the day I saw my favourite band live. It was my fifteenth birthday, and my older sister had bought tickets as a surprise.\nWe travelled to Istanbul by train and arrived at the stadium two hours early. When the band finally came on stage, everyone started singing and dancing. I knew every word of every song!\nI will always remember that day because it was the first time I had been to a concert, and because my sister had planned everything for me. It made me feel really special.'},
  {'id':'b1x-w3','part':2,'kind':'story','t':'Part 2 · Hikâye: Yanlış otobüs',
   'in':'Your English teacher has asked you to write a story. Your story must begin with this sentence. Write your story in about 100 words.',
   'mail':'Your story must begin with this sentence:\nAfter ten minutes on the bus, Maya realised she was going the wrong way.',
   'pts':[('Verilen cümleyle başla',['after ten minutes on the bus']),('Geçmiş zamanla olayları anlat',['was','were','got','looked','asked','decided','saw']),('Bir sorun ve çözüm olsun',['but','so','then','luckily','suddenly']),('Hikâyeyi bitir (sonuç)',['in the end','finally','at last','happy','relieved','laughed','never'])],
   'min':80,'max':140,
   'model':'After ten minutes on the bus, Maya realised she was going the wrong way. She was supposed to be at her friend\'s birthday party at six, and it was already half past five.\nShe got off at the next stop and looked around. She didn\'t know the area at all, and her phone battery was almost empty. Luckily, she saw an old man waiting at the bus stop and asked him for help.\n"Take the number 12," he said. "It goes straight to the city centre."\nIn the end, Maya arrived at the party only fifteen minutes late, and she had a funny story to tell everyone.'}]}]

S_EXAM=[
 {'id':'b1x-s1','p':1,'t':'Part 1 · Tanışma','ins':'Sınav görevlisi seni tanımak için sorular soruyor. Her soruya 2–3 cümleyle cevap ver.','q':[
  ["What's your name? Where do you live?",20,['my name is','I live in','I come from'],"My name is Deniz and I live in Izmir, in the west of Turkey. I've lived there all my life."],
  ['Do you work or are you a student?',20,['I\'m a student','I study','I work as'],"I'm a student. I'm in my last year at high school, and my favourite subject is biology."],
  ['What do you usually do at the weekend?',30,['usually','often','at the weekend','I like'],"I usually meet my friends on Saturday and we go to a café or play football in the park. On Sundays I often stay at home and relax with my family."],
  ['Tell us about something you did last week.',30,['last week','I went','it was'],"Last week I went to the cinema with my cousin. We watched a science fiction film. It was a bit long, but the special effects were amazing."],
  ['What would you like to do in the future?',30,['I\'d like to','I hope','I want to','because'],"I'd like to study medicine at university, because I want to help people. I also hope to travel to Canada one day."]]},
 {'id':'b1x-s2','p':2,'t':'Part 2 · Fotoğrafı anlat','ins':'Bu bölümde bir fotoğrafı yaklaşık 1 dakika anlatırsın: kimler var, ne yapıyorlar, nerede, neler görüyorsun, nasıl hissediyor olabilirler.',
  'img':[['👨‍🍳👩‍🍳🧑‍🍳🍕🥗🔥','Bir mutfakta üç genç birlikte yemek yapıyor: biri pizza hamuru açıyor, biri salata hazırlıyor, arkada fırın yanıyor. Herkes gülümsüyor.','b1-cooking']],
  'q':[['Now, here is your photograph. It shows people cooking together. Please tell us what you can see in the photograph.',60,['in this photo I can see','on the left','on the right','in the background','they are','it looks like','they seem'],"In this photo I can see three young people who are cooking together in a kitchen. On the left, a boy is making a pizza. He's wearing a white apron. In the middle, a girl is preparing a salad, and on the right another girl is watching the oven. In the background there's an oven, and it looks quite hot. They all seem very happy – I think they're friends and they're preparing dinner for a party. It looks like a modern kitchen, and there are lots of vegetables on the table."]]},
 {'id':'b1x-s3','p':3,'t':'Part 3 · Birlikte karar verme','ins':'Gerçek sınavda bu bölüm bir partnerle yapılır. Burada iki tarafı da sen düşün: önce seçenekleri tek tek değerlendir, sonra en iyisine karar ver.',
  'opts':['🎨 sanat atölyesi','⚽ spor turnuvası','🎬 film gecesi','🌳 park temizliği','🎤 müzik yarışması'],
  'q':[["A school wants to organise an activity to help students make new friends. Here are some ideas they're thinking about. Talk about the different activities and say how they would help students make friends.",90,['what about','I think','because','it would be','on the other hand','that\'s a good idea','I\'m not sure'],"Let's start with the art workshop. I think it would be good for quiet students, but people mostly work alone, so they might not talk very much. A sports tournament is fun, and students have to work in teams, so they would get to know each other. However, some people don't like sport. A film night is relaxing, but you can't talk during the film. Cleaning the park is a good idea because students work together and do something useful at the same time. A music competition could be exciting, but some students might feel nervous on stage."],
   ['Now decide which activity would be best for making new friends.',30,['I think the best','because','I\'d choose','in my opinion'],"In my opinion, the best activity would be the park clean-up, because everyone can join, students work together in small groups, and they have plenty of time to talk to each other."]]},
 {'id':'b1x-s4','p':4,'t':'Part 4 · Tartışma','ins':'Sınav görevlisi 3. bölümün konusuyla ilgili görüşünü soruyor. Her soruya fikrini ve nedenini söyle.','q':[
  ['Is it easy or difficult to make new friends at a new school? Why?',40,['I think','because','for example','it depends'],"I think it can be quite difficult at first, because everyone already has their own group of friends. But if you join a club or a team, it becomes much easier, because you meet people who like the same things as you."],
  ['Do you prefer doing activities in a big group or in a small group?',40,['I prefer','because','on the other hand','in a small group'],"I prefer small groups, because everyone can speak and you get to know people better. In a big group it's more exciting, but quiet people often don't say anything."],
  ['Do you think young people spend too much time online instead of meeting friends?',40,['I agree','I don\'t think','however','for example','these days'],"I partly agree. These days many young people chat online for hours, and that isn't the same as meeting face to face. However, online chats can also help you stay in touch with friends who live far away."]]}]

EXAMS=[{'id':'b1-1','t':'Sınav 1','sec':{
 'R':{'min':45,'parts':[pet(PP1[k]) for k in('R1','R2','R3','R4','R5','R6')]},
 'L':{'min':30,'parts':[pet(PP1[k]) for k in('L1','L2','L3','L4')]},
 'W':{'min':45,'tasks':W_EXAM},
 'S':{'parts':S_EXAM}}}]

def tt(p,t,pid):p=pet(p,pid);p['t']=t;return p
L_EXTRA={'k':'L3','id':'b1l5','t':'Not tamamlama: Yemek kursu','nm':'Dinleme 3 · Not tamamlama','ti':'Listening Part 3','ty':'open','title':'Notlar',
 'ins':'Bir yemek kursu tanıtımını dinle. Her boşluğa bir kelime, sayı ya da tarih yaz.',
 'sc':[('M','Hello, and thanks for calling the Green Kitchen Cookery School. Here is some information about our summer course for young people. The course is for students aged fourteen to eighteen, and it runs for two weeks, starting on the third of July. Classes take place every weekday morning from ten until one. In the first week, students learn how to make different kinds of bread, and in the second week we focus on Italian dishes, especially pasta. The course costs one hundred and twenty pounds, and that includes all the food. Students only need to bring an apron. At the end of the course, there is a special lunch, and every student can invite two members of their family. To book a place, please visit our website or send us an email. We look forward to cooking with you!')],
 'p':'Green Kitchen summer course\nAge: 14 to 18\nStarts on: (1) ______ July\nClasses every weekday: 10 a.m. to (2) ______ p.m.\nWeek 1: different kinds of (3) ______\nWeek 2: Italian food, especially (4) ______\nPrice: £(5) ______, including all the food\nStudents must bring: an (6) ______',
 'a':[['3','3rd','third'],['1','one','1.00'],['bread'],['pasta'],['120','one hundred and twenty'],['apron']],
 'tg':[['spelling'],['spelling'],['detail'],['detail'],['spelling'],['detail']],
 'e':['"starting on the third of July"','"from ten until one"','"how to make different kinds of bread"','"Italian dishes, especially pasta"','"one hundred and twenty pounds"','"Students only need to bring an apron"']}
RT={'R1':'Kısa metinler: duyurular ve mesajlar','R2':'Eşleştirme: kitap seçimi','R3':'Uzun metin: davul öğrenmek','R4':'Cümle yerleştirme: ödevsiz okul','R5':'Çoktan seçmeli boşluk: köy festivali','R6':'Açık boşluk: Mr Lee\'ye mektup'}
LT={'L1':'Kısa kayıtlar (7 soru)','L2':'Kısa konuşmalar: görüşler','L3':'Not tamamlama: yaz kampı','L4':'Röportaj: gönüllü çalışma'}
def wid(w):w=dict(w);w['id']='b1'+w['id'];return w
def sid(s):s=dict(s);s['id']='b1'+s['id'];return s
RT3={'R1':'Kısa metinler: duyurular ve notlar 2','R2':'Eşleştirme: spor ve sağlık','R3':'Uzun metin: köy okulunda bir yıl','R4':'Cümle yerleştirme: arabasız kasaba','R5':'Çoktan seçmeli boşluk: fırtına','R6':'Açık boşluk: fotoğraf kulübü'}
LT3={'L1':'Kısa kayıtlar 2 (7 soru)','L2':'Kısa konuşmalar: okul, iş, tatil','L3':'Not tamamlama: liman müzesi','L4':'Röportaj: genç şef'}
PRAC={'R':[tt(PP2[k],RT[k],'b1r'+k[1]) for k in RT]+[tt(PP3[k],RT3[k],'b1r'+k[1]+'b') for k in RT3],
 'L':[tt(PP2[k],LT[k],'b1l'+k[1]) for k in LT]+[L_EXTRA]+[tt(PP3[k],LT3[k],'b1l'+k[1]+'b') for k in LT3],
 'W':[wid(w) for w in WS],'S':[sid(s) for s in SS]}
