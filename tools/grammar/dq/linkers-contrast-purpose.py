import sys,os;sys.path.insert(0,os.path.dirname(os.path.dirname(os.path.abspath(__file__))));from gl import Q
DQ=[
 Q(2,'Amaç','I went to the chemist ___ buy some medicine.','to',['for','so'],'Amaç: to + fiil.'),
 Q(2,'Amaç','She saved money ___ she could buy a new laptop.','so that',['because','so as'],'so that + özne + can/could.'),
 Q(2,'Sebep','We stayed inside ___ the bad weather.','because of',['because','so'],'because of + isim.'),
 Q(2,'Sonuç','The shop was closed, ___ we went home.','so',['because','although'],'Sonuç: so.'),
 Q(2,'Zıtlık','___ he was tired, he finished the race.','Although',['Despite','However'],'although + cümle.'),
 Q(2,'Zıtlık','The flat is small. ___, it is in a great location.','However',['Although','Despite'],'However cümle başında, virgülle.'),
 Q(3,'Sebep','The match was cancelled ___ heavy rain.','due to',['because','so that'],'due to + isim.'),
 Q(3,'Sonuç','He missed the bus. ___, he was late for the exam.','As a result',['Because of','So that'],'As a result = sonuç olarak.'),
 Q(3,'Ekleme','The hotel was cheap and, ___, the staff were very friendly.','what is more',['even though','as long as'],'what is more = üstelik.'),
 Q(3,'Zıtlık','___ having a map, we got lost.','Despite',['Although','However'],'despite + -ing / isim.'),
 Q(3,'so / such','It was ___ a hot day that we went to the beach.','such',['so','too'],'such + (a) + sıfat + isim + that.'),
 Q(3,'so / such','The film was ___ boring that I fell asleep.','so',['such','too'],'so + sıfat + that.'),
]
