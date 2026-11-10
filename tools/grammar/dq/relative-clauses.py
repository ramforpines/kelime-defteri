import sys,os;sys.path.insert(0,os.path.dirname(os.path.dirname(os.path.abspath(__file__))));from gl import Q
DQ=[
 Q(2,'who / which','The woman ___ lives next door is a nurse.','who',['which','what'],'İnsanlar için who.'),
 Q(2,'who / which','This is the bike ___ I bought last week.','which',['who','where'],'Eşyalar için which (veya that).'),
 Q(2,'where','That is the hotel ___ we stayed on our honeymoon.','where',['which','who'],'Yer bildiren ilgi cümlesi: where.'),
 Q(2,'whose','I have a friend ___ father is a famous chef.','whose',['who','who\'s'],'Sahiplik: whose + isim.'),
 Q(2,'when','I remember the day ___ we first met.','when',['which','where'],'Zaman bildiren ilgi cümlesi: when.'),
 Q(2,'that','Is this the book ___ you were talking about?','that',['what','where'],'that, who/which yerine kullanılabilir.'),
 Q(3,'what','I didn\'t understand ___ the teacher said.','what',['that','which'],'what = the thing that; öncesinde isim yoktur.'),
 Q(3,'Virgüllü','My sister, ___ works in Ankara, is coming for the weekend.','who',['that','which'],'Virgüllü (ek bilgi) cümlede that kullanılmaz.'),
 Q(3,'Zamir atma','The people ___ we met on holiday were very friendly.','(boş)',['who they','which'],'Nesne olan ilgi zamiri atılabilir; zamir tekrar edilmez.'),
 Q(3,'which (tüm cümle)','He passed all his exams, ___ surprised everyone.','which',['what','that'],'Önceki cümlenin tamamına which ile atıf yapılır.'),
]
