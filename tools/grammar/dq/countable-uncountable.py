import sys,os;sys.path.insert(0,os.path.dirname(os.path.dirname(os.path.abspath(__file__))));from gl import Q
DQ=[
 Q(2,'some / any','Is there ___ milk in the fridge?','any',['a','many'],'Soruda sayılamayan isimle any.'),
 Q(2,'much / many','How ___ eggs do we need for the cake?','many',['much','lot'],'Sayılabilen çoğul: many.'),
 Q(2,'much / many',"We haven't got ___ time, so hurry up.",'much',['many','few'],'Sayılamayan: much.'),
 Q(2,'a few / a little','Add ___ salt and stir well.','a little',['a few','many'],'Sayılamayan küçük miktar: a little.'),
 Q(2,'a few / a little','I have ___ friends who live in Bursa.','a few',['a little','much'],'Sayılabilen küçük miktar: a few.'),
 Q(2,'Ölçü','Can I have a ___ of bread, please?','loaf',['cup','bar'],'a loaf of bread: bir somun ekmek.'),
 Q(2,'Ölçü','I bought a ___ of olive oil.','bottle',['slice','loaf'],'a bottle of oil: bir şişe yağ.'),
 Q(3,'Tanımlık','I usually have ___ apple for breakfast.','an',['a','some'],'Ünlüyle başlayan sayılabilen tekil: an.'),
 Q(3,'Sayılamayan','Can you give me some ___ about the hotel?','information',['informations','an information'],'information sayılamaz, çoğul olmaz.'),
 Q(3,'few / little','There were very ___ people at the concert, so we got good seats.','few',['little','much'],'few (az, olumsuz anlam) sayılabilen isimle.'),
 Q(3,'Tanımlık','___ fruit is good for you.','(boş)',['The','A'],'Genel anlamda sayılamayan isim tanımlıksız kullanılır.'),
]
