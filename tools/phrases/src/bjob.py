# Kalıplar: İş başvurusu ve mülakat (B1-B2). P(İngilizce, Türkçe, seviye, üslup, örnek İngilizce, örnek Türkçe, diyalog)
import sys,os;sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'..'))
from ext_meta import fix
def P(en,tr,lv,reg,ex,extr,d):return {'en':en,'tr':tr,'lv':lv,'reg':reg,'ex':[ex,extr],'d':d}
GROUP={'id':'bjob','t':'İş başvurusu ve mülakat','en':'Applying for a job',
'ins':'Başvuru mektubu yazmak, mülakatta kendini tanıtmak ve görüşmenin sonunda soru sormak için kalıplar.',
'sub':[
 {'k':'jcv','t':'Başvuru mektubu','en':'Writing an application','items':[
  P("I am writing to apply for the position of ...","... pozisyonuna başvurmak için yazıyorum","B2","resmî","I am writing to apply for the position of sales assistant.","Satış asistanı pozisyonuna başvurmak için yazıyorum.",("What does the first line of your letter say?","___ sales assistant, which I saw on your website.",["Could you tell me about the salary?","I am a hard-working person."])),
  P("I have experience in ...","... konusunda deneyimim var","B1","","I have experience in working with children.","Çocuklarla çalışma konusunda deneyimim var.",("Why do you think you are suitable?","___ customer service."  ,["Could you tell me about the salary?","I would be grateful for the chance to ..."])),
  P("I would be grateful for the opportunity to ...","... fırsatı için minnettar olurum","B2","resmî","I would be grateful for the opportunity to attend an interview.","Mülakata katılma fırsatı için minnettar olurum.",("How do you end your letter?","___ discuss my application in person.",["I have experience in ...","What are the working hours?"])),
  P("I enclose my CV.","Özgeçmişimi ekte sunuyorum.","B1","resmî","I enclose my CV and two references.","Özgeçmişimi ve iki referansı ekte sunuyorum.",("Did you send any documents with your letter?","Yes. ___",["I'm good at working in a team.","What are the working hours?"])),
  P("I look forward to hearing from you.","Yanıtınızı bekliyorum.","B1","resmî","Thank you for your time. I look forward to hearing from you.","Zamanınız için teşekkürler. Yanıtınızı bekliyorum.",("How should I finish a formal letter?","Write: Thank you for your time. ___",["I enclose my CV.","I'm good at working in a team."])),
 ]},
 {'k':'jint','t':'Mülakatta cevap vermek','en':'Answering interview questions','items':[
  P("I'm good at working in a team.","Takım çalışmasında iyiyim.","B1","","I'm good at working in a team, and I enjoy helping my colleagues.","Takım çalışmasında iyiyim ve iş arkadaşlarıma yardım etmeyi severim.",("What are your strengths?","___ and I learn quickly."  ,["I enclose my CV.","What are the working hours?"])),
  P("My greatest weakness is ...","En büyük zayıf noktam ...","B2","","My greatest weakness is that I sometimes take on too much work.","En büyük zayıf noktam, bazen çok fazla iş üstlenmem.",("And what about your weaknesses?","Well, ___ I'm working on it.",["I look forward to hearing from you.","I enclose my CV."])),
  P("I'm used to working under pressure.","Baskı altında çalışmaya alışkınım.","B2","","I'm used to working under pressure because I worked in a busy café.","Baskı altında çalışmaya alışkınım, çünkü yoğun bir kafede çalıştım.",("This job can be very stressful.","That's no problem. ___",["Could you tell me about the salary?","I enclose my CV."])),
  P("Where do you see yourself in five years?","Beş yıl sonra kendini nerede görüyorsun?","B2","","Interviewers often ask, \"Where do you see yourself in five years?\"","Mülakatçılar sık sık \"Beş yıl sonra kendini nerede görüyorsun?\" diye sorar.",("What is a typical interview question about the future?","It's: \"___\"",["I'm good at working in a team.","What are the working hours?"])),
  P("My main strength is ...","En büyük gücüm ...","B1","","My main strength is that I always finish my work on time.","En büyük gücüm, işimi her zaman zamanında bitirmem.",("What would you say is your best quality?","___ I always finish on time.",["I enclose my CV.","What are the working hours?"])),
  P("I have always been interested in ...","Her zaman ... ile ilgilendim","B1","","I have always been interested in design.","Her zaman tasarımla ilgilendim.",("Why did you apply for this job?","___ working with computers.",["When will I hear from you?","What are the working hours?"])),
  P("That's a good question.","Bu güzel bir soru.","B1","","That's a good question. Let me think for a second.","Bu güzel bir soru. Bir saniye düşüneyim.",("Why did you leave your last job?","Hmm, ___ I wanted new challenges.",["I enclose my CV.","I look forward to hearing from you."])),
 ]},
 {'k':'jask','t':'Mülakat sonunda soru sormak','en':'Asking your own questions','items':[
  P("What are the working hours?","Çalışma saatleri nedir?","A2","","What are the working hours, and is there any weekend work?","Çalışma saatleri nedir, hafta sonu çalışma var mı?",("Do you have any questions for us?","Yes. ___",["I enclose my CV.","I'm used to working under pressure."])),
  P("Could you tell me about the salary?","Maaş hakkında bilgi verebilir misiniz?","B2","resmî","Could you tell me about the salary and benefits?","Maaş ve yan haklar hakkında bilgi verebilir misiniz?",("Is there anything else you'd like to know?","Yes. ___",["I'm good at working in a team.","I enclose my CV."])),
  P("When will I hear from you?","Ne zaman haber alacağım?","B1","","When will I hear from you about the decision?","Karar hakkında ne zaman haber alacağım?",("Thank you for coming today.","Thank you. ___",["I'm used to working under pressure.","I enclose my CV."])),
  P("I'd like to know more about ...","... hakkında daha fazla bilgi almak isterim","B1","","I'd like to know more about the team I would work with.","Birlikte çalışacağım ekip hakkında daha fazla bilgi almak isterim.",("Do you have any questions about the company?","Yes. ___ the team."  ,["I enclose my CV.","I'm used to working under pressure."])),
  P("Is there any training?","Eğitim veriliyor mu?","B1","","Is there any training for new staff?","Yeni çalışanlara eğitim veriliyor mu?",("We'd like to tell you about the job.","Great. ___ in the first month?",["That's a good question.","I enclose my CV."])),
 ]},
]}
fix(GROUP)
