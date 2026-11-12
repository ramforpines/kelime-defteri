import sys,os;sys.path.insert(0,os.path.dirname(os.path.dirname(os.path.abspath(__file__))));from gl import Q
DQ=[
 Q(2,'a / an','She is ___ engineer.','an',['a','the'],'Meslek, ünlüyle başlıyor: an.'),
 Q(2,'the','Can you pass me ___ salt, please?','the',['a','many'],'Bilinen, belirli nesne: the.'),
 Q(2,'Tanımlıksız','I go to ___ school by bike.','(boş)',['the','a'],'go to school (amacıyla): tanımlık yok.'),
 Q(2,'the','___ sun rises in the east.','The',['A','(boş)'],'Tek olan şeyler: the sun.'),
 Q(2,'a / the','I saw ___ film last night. ___ film was really funny.','a / The',['the / A','a / A'],'İlk söz: a; tekrar: the.'),
 Q(3,'Tanımlıksız','___ dogs are usually friendly animals.','(boş)',['The','A'],'Genelleme, çoğul: tanımlık yok.'),
 Q(3,'Yer adları','We went sailing on ___ Mediterranean.','the',['a','(boş)'],'Deniz/okyanus adları: the.'),
 Q(3,'Yer adları','She lives in ___ Turkey.','(boş)',['the','a'],'Ülke adları genellikle tanımlıksız (the UK, the USA hariç).'),
 Q(3,'Müzik aleti','He plays ___ guitar in a band.','the',['a','(boş)'],'play the + çalgı.'),
 Q(3,'Spor','They play ___ football every Friday.','(boş)',['the','a'],'play + spor: tanımlık yok.'),
]
