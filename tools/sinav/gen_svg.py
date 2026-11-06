#!/usr/bin/env python3
"""Konuşma bölümündeki fotoğraf görevleri için sade çizimler üretir: ../../img/sx/*.svg
Kullanım: python3 gen_svg.py"""
import os
HERE=os.path.dirname(os.path.abspath(__file__));OUT=os.path.join(HERE,'..','..','img','sx');os.makedirs(OUT,exist_ok=True)
SK={'a':'#f0c9a0','b':'#e0ac7e','c':'#c98b5e','d':'#8d5a3b'}
def head(hair,hc,skin,smile=True):
    h={'short':f'<path d="M-17 18 q17 -26 34 0 q-4 -14 -17 -14 q-13 0 -17 14z" fill="{hc}"/>',
       'long':f'<path d="M-19 26 q-2 -30 19 -30 q21 0 19 30 q-6 -18 -19 -18 q-13 0 -19 18z" fill="{hc}"/><path d="M-19 24 q-4 22 2 32 M19 24 q4 22 -2 32" stroke="{hc}" stroke-width="7" fill="none"/>',
       'bun':f'<circle cx="0" cy="-2" r="8" fill="{hc}"/><path d="M-17 20 q17 -28 34 0 q-4 -14 -17 -14 q-13 0 -17 14z" fill="{hc}"/>',
       'bald':f'<path d="M-17 22 q-2 -6 0 -10 M17 22 q2 -6 0 -10" stroke="{hc}" stroke-width="5" fill="none"/>',
       'curly':''.join(f'<circle cx="{x}" cy="{y}" r="7" fill="{hc}"/>' for x,y in [(-13,10),(-5,4),(5,4),(13,10),(-16,18),(16,18)]),
       'helmet':f'<path d="M-20 18 q0 -24 20 -24 q20 0 20 24z" fill="{hc}"/><rect x="-23" y="15" width="46" height="5" rx="2" fill="{hc}"/>',
       'hood':f'<path d="M-21 34 q-4 -38 21 -38 q25 0 21 38 q-4 -26 -21 -26 q-17 0 -21 26z" fill="{hc}"/>',
       'cap':f'<path d="M-17 16 q17 -24 34 0z" fill="{hc}"/><rect x="0" y="12" width="24" height="5" rx="2" fill="{hc}"/>'}[hair]
    face=f'<circle cx="0" cy="22" r="17" fill="{skin}"/>'
    eyes='<circle cx="-6" cy="21" r="2" fill="#222"/><circle cx="6" cy="21" r="2" fill="#222"/>'
    mouth='<path d="M-6 29 q6 5 12 0" stroke="#7a3e2b" stroke-width="2" fill="none"/>' if smile else '<path d="M-5 30 h10" stroke="#7a3e2b" stroke-width="2"/>'
    return face+h+eyes+mouth
def person(x,y,s=1,skin='b',hair='short',hc='#3a2a1d',top='#4a7bd1',legs=None,arms='down',apron=False,smile=True,extra=''):
    sk=SK.get(skin,skin)
    body=f'<path d="M-24 92 q0 -46 24 -46 q24 0 24 46z" fill="{top}"/>'
    if apron:body+='<path d="M-12 52 h24 v42 h-24z" fill="#fff"/>'
    A={'down':'M-21 60 l-8 30|M21 60 l8 30','forward':'M-21 60 l-6 30|M21 60 l6 30','up':'M-21 58 l-14 -26|M21 58 l14 -26',
       'right':'M-21 60 l-6 30|M21 58 l26 14','left':'M-21 58 l-26 14|M21 60 l6 30','hold':'M-21 60 l10 24|M21 60 l-10 24'}[arms].split('|')
    arm=''.join(f'<path d="{a}" stroke="{sk}" stroke-width="8" stroke-linecap="round"/>' for a in A)
    lg=f'<rect x="-18" y="90" width="14" height="44" rx="5" fill="{legs}"/><rect x="4" y="90" width="14" height="44" rx="5" fill="{legs}"/><rect x="-21" y="128" width="18" height="8" rx="3" fill="#333"/><rect x="3" y="128" width="18" height="8" rx="3" fill="#333"/>' if legs else ''
    return f'<g transform="translate({x},{y}) scale({s})">{lg}{body}{arm}{head(hair,hc,sk,smile)}{extra}</g>'
def svg(name,inner,bg='#f6efe4'):
    open(os.path.join(OUT,name+'.svg'),'w').write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 260"><rect width="400" height="260" fill="{bg}"/>{inner}</svg>\n')
def table(x,y,w,c='#8d6e4c'):return f'<rect x="{x}" y="{y}" width="{w}" height="14" rx="3" fill="{c}"/><rect x="{x+10}" y="{y+14}" width="10" height="{250-y}" fill="#6f5338"/><rect x="{x+w-20}" y="{y+14}" width="10" height="{250-y}" fill="#6f5338"/>'
def win(x,y,w,h,sky='#bfe3f5'):return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="4" fill="{sky}" stroke="#fff" stroke-width="5"/><line x1="{x+w/2}" y1="{y}" x2="{x+w/2}" y2="{y+h}" stroke="#fff" stroke-width="4"/>'
def laptop(x,y):return f'<rect x="{x}" y="{y}" width="46" height="30" rx="3" fill="#3b3f45"/><rect x="{x+3}" y="{y+3}" width="40" height="24" fill="#9fd3f0"/><rect x="{x-6}" y="{y+30}" width="58" height="5" rx="2" fill="#555"/>'

# 1 B1: mutfakta birlikte yemek
svg('b1-cooking',f'<rect x="0" y="170" width="400" height="90" fill="#c9a77c"/>{win(150,20,100,70)}'
 '<rect x="318" y="96" width="74" height="110" rx="6" fill="#9aa3ad"/><rect x="328" y="126" width="54" height="40" rx="4" fill="#3b3f45"/><rect x="333" y="131" width="44" height="30" rx="3" fill="#f2994a"/><circle cx="335" cy="108" r="4" fill="#3b3f45"/><circle cx="355" cy="108" r="4" fill="#3b3f45"/><circle cx="375" cy="108" r="4" fill="#3b3f45"/>'
 +person(85,60,hair='short',top='#4a7bd1',apron=True,arms='forward')+person(200,50,skin='c',hair='long',hc='#1f1610',top='#e5649a',apron=True,arms='forward')+person(290,64,skin='a',hair='long',hc='#c8862f',top='#5fb38a',apron=True,arms='right')
 +table(20,150,290)+'<ellipse cx="85" cy="146" rx="34" ry="8" fill="#f3d9a4"/><ellipse cx="85" cy="144" rx="28" ry="6" fill="#d9452b"/><path d="M175 132 h52 a26 16 0 0 1 -52 0z" fill="#f1f1f1" stroke="#ccc"/><circle cx="190" cy="132" r="7" fill="#5dbb63"/><circle cx="203" cy="129" r="7" fill="#7ccf5a"/><circle cx="214" cy="132" r="6" fill="#e23b3b"/><circle cx="255" cy="143" r="7" fill="#e23b3b"/><circle cx="268" cy="145" r="6" fill="#e23b3b"/><rect x="236" y="140" width="14" height="6" rx="3" fill="#4caf50"/>')

# 2 B2: kalabalık ofis
svg('b2-office','<rect x="0" y="180" width="400" height="80" fill="#cfd6de"/>'+win(20,20,90,60,'#d6ecf8')+win(290,20,90,60,'#d6ecf8')
 +person(150,62,s=.75,skin='a',hair='short',top='#7a8899',arms='forward')+person(260,62,s=.75,skin='d',hair='bald',hc='#222',top='#a3b18a',arms='forward')
 +table(110,136,90,'#b9c2cc')+table(220,136,90,'#b9c2cc')+laptop(133,104)+laptop(243,104)
 +'<rect x="330" y="110" width="40" height="80" rx="4" fill="#6b4f3a"/><rect x="338" y="122" width="24" height="18" fill="#2d2d2d"/><rect x="344" y="150" width="12" height="14" fill="#fff"/>'
 +person(170,105,skin='c',hair='long',hc='#3a2a1d',top='#3c6e71',arms='forward')+table(90,170,200,'#e0e4e8')+laptop(150,140)
 +'<rect x="235" y="155" width="12" height="15" rx="2" fill="#fff" stroke="#bbb"/>')

# 3 B2: tarlada çiftçi
svg('b2-farm','<rect x="0" y="0" width="400" height="140" fill="#bfe3f5"/><circle cx="340" cy="45" r="24" fill="#ffd34d"/><rect x="0" y="130" width="400" height="130" fill="#9ccf6b"/>'
 +''.join(f'<path d="M0 {150+i*20} Q200 {140+i*20} 400 {150+i*20}" stroke="#86b85a" stroke-width="4" fill="none"/>' for i in range(5))
 +'<path d="M0 132 q60 -30 120 -4 q60 -26 120 2 q70 -30 160 0 v6 h-400z" fill="#7fb15a"/>'
 +'<g transform="translate(200,110)"><rect x="0" y="20" width="110" height="40" rx="6" fill="#d9442b"/><rect x="58" y="-12" width="42" height="36" rx="4" fill="#d9442b"/><rect x="64" y="-6" width="30" height="22" fill="#bfe3f5"/><rect x="-14" y="34" width="20" height="10" fill="#555"/><circle cx="85" cy="68" r="26" fill="#333"/><circle cx="85" cy="68" r="10" fill="#999"/><circle cx="20" cy="70" r="16" fill="#333"/><circle cx="20" cy="70" r="6" fill="#999"/></g>'
 +person(120,88,skin='b',hair='cap',hc='#2f6690',top='#6a8d73',legs='#3d5a80',arms='right'))

# 4 C1: yangına müdahale
svg('c1-fire','<rect width="400" height="260" fill="#3a2f45"/><rect x="0" y="200" width="400" height="60" fill="#555"/>'
 +'<rect x="40" y="60" width="150" height="140" fill="#7a6a5c"/>'+''.join(f'<rect x="{55+(i%3)*45}" y="{75+(i//3)*45}" width="30" height="30" fill="#f2994a"/>' for i in range(6))
 +'<path d="M60 70 q10 -40 30 -20 q5 -30 25 -10 q10 -35 30 0 q15 -25 25 10 q-55 20 -110 20z" fill="#f2c94c"/><path d="M75 68 q10 -25 22 -10 q8 -22 22 -2 q10 -20 20 6z" fill="#eb5757"/>'
 +'<path d="M200 170 q-60 -40 -60 -60" stroke="#ccc" stroke-width="4" fill="none" stroke-dasharray="6 6"/>'
 +person(240,98,skin='b',hair='helmet',hc='#e8c547',top='#2f2f2f',legs='#2f2f2f',arms='left',smile=False,extra='<rect x="-24" y="66" width="48" height="5" fill="#f2c94c"/>')
 +person(320,104,s=.9,skin='c',hair='helmet',hc='#e8c547',top='#2f2f2f',legs='#2f2f2f',arms='left',smile=False,extra='<rect x="-24" y="66" width="48" height="5" fill="#f2c94c"/>')
 +'<path d="M214 168 q40 10 110 4" stroke="#b33a3a" stroke-width="8" fill="none" stroke-linecap="round"/>')

# 5 C1: dağda kurtarma
svg('c1-rescue','<rect width="400" height="260" fill="#c9dbe8"/><path d="M0 170 L90 60 L160 140 L240 40 L330 150 L400 100 V260 H0z" fill="#e9eef3"/><path d="M90 60 l-20 25 l12 -4 l8 10 l10 -12z M240 40 l-25 30 l14 -5 l10 12 l12 -14z" fill="#fff"/>'
 +''.join(f'<circle cx="{x}" cy="{y}" r="2.5" fill="#fff"/>' for x,y in [(30,30),(80,20),(130,50),(180,25),(260,70),(300,30),(350,60),(370,20),(210,90),(50,90)])
 +'<rect x="0" y="200" width="400" height="60" fill="#f5f8fb"/>'
 +person(130,92,skin='a',hair='helmet',hc='#f2f2f2',top='#e8743b',legs='#2f3e46',arms='right',smile=False,extra='<rect x="-24" y="70" width="48" height="5" fill="#f2f2f2"/>')
 +person(270,92,skin='c',hair='helmet',hc='#f2f2f2',top='#e8743b',legs='#2f3e46',arms='left',smile=False,extra='<rect x="-24" y="70" width="48" height="5" fill="#f2f2f2"/>')
 +'<rect x="150" y="160" width="100" height="14" rx="4" fill="#d9442b"/><rect x="160" y="146" width="60" height="16" rx="7" fill="#4a7bd1"/><circle cx="232" cy="150" r="11" fill="#f0c9a0"/><path d="M222 146 q10 -12 20 0" fill="#6b4a2b"/>')

# 6 C1: gece acil serviste doktor
svg('c1-doctor','<rect width="400" height="260" fill="#dde8ea"/><rect x="0" y="200" width="400" height="60" fill="#b8c7cb"/>'+win(280,20,90,70,'#1d2b4a')+'<circle cx="345" cy="45" r="12" fill="#f2f2c4"/>'
 +'<rect x="30" y="40" width="70" height="40" rx="4" fill="#20343a"/><path d="M36 62 l12 0 l6 -12 l8 22 l6 -10 l26 0" stroke="#5be37d" stroke-width="3" fill="none"/>'
 +'<rect x="30" y="150" width="190" height="20" rx="6" fill="#fff" stroke="#9fb3b8"/><rect x="40" y="170" width="8" height="40" fill="#9fb3b8"/><rect x="200" y="170" width="8" height="40" fill="#9fb3b8"/><rect x="40" y="138" width="40" height="14" rx="6" fill="#e9f1f2"/><rect x="80" y="140" width="130" height="12" rx="5" fill="#9cc3d5"/><circle cx="62" cy="138" r="13" fill="#e0ac7e"/><path d="M50 134 q12 -14 24 0" fill="#3a2a1d"/>'
 +person(270,92,skin='c',hair='bun',hc='#1f1610',top='#ffffff',legs='#5a7f8a',arms='left',smile=False,extra='<path d="M-14 50 q14 26 28 0" stroke="#333" stroke-width="3" fill="none"/><path d="M-12 50 v44 M12 50 v44" stroke="#5a7f8a" stroke-width="10"/>'))

# 7 B2: sınıf
svg('b2-classroom','<rect width="400" height="260" fill="#f3efe6"/><rect x="0" y="210" width="400" height="50" fill="#c9a77c"/><rect x="40" y="20" width="200" height="90" rx="4" fill="#2e5e4e" stroke="#8d6e4c" stroke-width="6"/>'
 +'<path d="M60 45 h80 M60 65 h120 M60 85 h60" stroke="#e8f1ec" stroke-width="3"/>'
 +person(290,40,skin='a',hair='bun',hc='#6b4a2b',top='#8e5ea2',legs='#3b3b55',arms='left')
 +person(60,140,s=.8,skin='b',hair='short',top='#e8743b',arms='forward')+person(170,140,s=.8,skin='d',hair='curly',hc='#1f1610',top='#4a7bd1',arms='forward')+person(280,148,s=.8,skin='a',hair='long',hc='#c8862f',top='#5fb38a',arms='forward')
 +table(20,200,90,'#b5895c')+table(130,200,90,'#b5895c')+table(240,200,90,'#b5895c')
 +'<rect x="45" y="192" width="30" height="8" fill="#fff"/><rect x="155" y="192" width="30" height="8" fill="#fff"/><rect x="265" y="192" width="30" height="8" fill="#fff"/>')

# 8 B2: evde çevrim içi ders
svg('b2-online','<rect width="400" height="260" fill="#e9e4f1"/><rect x="0" y="200" width="400" height="60" fill="#b9a58c"/>'+win(270,20,100,80)
 +'<rect x="30" y="40" width="70" height="90" fill="#8d6e4c"/><rect x="36" y="48" width="58" height="8" fill="#e5649a"/><rect x="36" y="62" width="58" height="8" fill="#4a7bd1"/><rect x="36" y="76" width="58" height="8" fill="#5fb38a"/>'
 +person(200,70,skin='b',hair='short',hc='#2a1d14',top='#f2b134',arms='forward',extra='<path d="M-20 18 q20 -34 40 0" stroke="#333" stroke-width="5" fill="none"/><rect x="-24" y="16" width="8" height="14" rx="3" fill="#333"/><rect x="16" y="16" width="8" height="14" rx="3" fill="#333"/>')
 +table(110,160,200,'#a07d58')+laptop(178,128)+'<path d="M250 152 h22 v8 h-22z" fill="#fff"/><rect x="132" y="146" width="14" height="14" rx="3" fill="#fff" stroke="#bbb"/>')

# 9 B2: evde doğum günü
svg('b2-birthday','<rect width="400" height="260" fill="#fbeee6"/><rect x="0" y="200" width="400" height="60" fill="#c9a77c"/>'
 +''.join(f'<ellipse cx="{x}" cy="{y}" rx="14" ry="18" fill="{c}"/><path d="M{x} {y+18} q-6 14 2 30" stroke="#999" fill="none"/>' for x,y,c in [(40,40,'#e5649a'),(75,30,'#4a7bd1'),(330,35,'#f2b134'),(365,45,'#5fb38a')])
 +person(70,90,s=.85,skin='a',hair='bald',hc='#bbb',top='#7a8899',arms='forward')+person(150,75,s=.85,skin='b',hair='long',hc='#3a2a1d',top='#e5649a',arms='up')+person(240,75,s=.85,skin='b',hair='short',top='#4a7bd1',arms='up')+person(320,95,s=.7,skin='b',hair='curly',hc='#3a2a1d',top='#f2b134',arms='forward')
 +table(30,170,340,'#8d6e4c')+'<rect x="170" y="140" width="60" height="30" rx="4" fill="#f7d6e0"/><rect x="170" y="150" width="60" height="6" fill="#e5649a"/>'+''.join(f'<rect x="{x}" y="128" width="4" height="12" fill="#4a7bd1"/><ellipse cx="{x+2}" cy="124" rx="3" ry="5" fill="#f2b134"/>' for x in (180,198,216)))

# 10 B2: şehirde havai fişek
svg('b2-fireworks','<rect width="400" height="260" fill="#1d2b4a"/>'
 +''.join(f'<g transform="translate({x},{y})">'+''.join(f'<line x1="0" y1="0" x2="{dx}" y2="{dy}" stroke="{c}" stroke-width="3" stroke-linecap="round"/>' for dx,dy in [(0,-28),(20,-20),(28,0),(20,20),(0,28),(-20,20),(-28,0),(-20,-20)])+'</g>' for x,y,c in [(90,60,'#f2c94c'),(210,45,'#eb5757'),(320,70,'#56ccf2'),(150,95,'#bb6bd9')])
 +'<path d="M0 170 h40 v-40 h30 v40 h20 v-60 h40 v60 h30 v-30 h40 v30 h20 v-70 h30 v70 h40 v-45 h40 v45 h70 v90 h-400z" fill="#141c30"/>'
 +''.join(f'<circle cx="{x}" cy="{y}" r="11" fill="#0b0f1c"/><path d="M{x-18} {y+40} q0 -28 18 -28 q18 0 18 28z" fill="#0b0f1c"/>' for x,y in [(20,214),(55,208),(95,216),(135,206),(175,214),(215,208),(255,216),(295,206),(335,214),(375,210)]))

# 11 C1: torun büyükanneye telefon öğretiyor
svg('c1-phone','<rect width="400" height="260" fill="#f2ebe1"/><rect x="0" y="200" width="400" height="60" fill="#b99a74"/>'+win(160,20,90,60)
 +'<rect x="40" y="120" width="320" height="80" rx="20" fill="#8e5ea2"/><rect x="30" y="110" width="40" height="90" rx="14" fill="#7d4f90"/><rect x="330" y="110" width="40" height="90" rx="14" fill="#7d4f90"/>'
 +person(140,70,skin='a',hair='bun',hc='#d9d9d9',top='#5fb38a',arms='hold',extra='<rect x="-6" y="40" width="20" height="4" fill="#ccc"/>')
 +person(250,72,skin='a',hair='short',hc='#8a5a2b',top='#4a7bd1',arms='left')
 +'<rect x="160" y="128" width="18" height="30" rx="3" fill="#222"/><rect x="162" y="131" width="14" height="22" fill="#9fd3f0"/>')

# 12 C1: usta ve çırak araba tamiri
svg('c1-mechanic','<rect width="400" height="260" fill="#d6d9dc"/><rect x="0" y="210" width="400" height="50" fill="#8a8f96"/>'
 +'<rect x="250" y="40" width="130" height="60" fill="#b0b6bd"/>'+''.join(f'<rect x="{258+i*30}" y="50" width="6" height="40" fill="#555"/>' for i in range(4))
 +'<g transform="translate(40,120)"><path d="M10 60 q10 -40 60 -44 h80 q40 4 60 44z" fill="#2f80ed"/><rect x="0" y="56" width="230" height="30" rx="10" fill="#2f80ed"/><path d="M80 22 h60 l20 34 h-90z" fill="#bfe3f5"/><circle cx="50" cy="88" r="20" fill="#333"/><circle cx="50" cy="88" r="8" fill="#999"/><circle cx="185" cy="88" r="20" fill="#333"/><circle cx="185" cy="88" r="8" fill="#999"/><path d="M180 30 l50 -24" stroke="#2f80ed" stroke-width="6"/></g>'
 +person(260,90,skin='c',hair='bald',hc='#555',top='#2f4858',legs='#2f4858',arms='left')
 +person(340,96,s=.9,skin='b',hair='cap',hc='#e8743b',top='#2f4858',legs='#2f4858',arms='hold'))

# 13 C1: öğretmen küre gösteriyor
svg('c1-globe','<rect width="400" height="260" fill="#f3efe6"/><rect x="0" y="210" width="400" height="50" fill="#c9a77c"/><rect x="20" y="20" width="170" height="80" rx="4" fill="#2e5e4e" stroke="#8d6e4c" stroke-width="6"/>'
 +person(250,50,skin='c',hair='long',hc='#1f1610',top='#e8743b',legs='#3b3b55',arms='left')
 +'<rect x="186" y="160" width="40" height="8" fill="#6f5338"/><rect x="202" y="128" width="8" height="34" fill="#6f5338"/><circle cx="206" cy="118" r="26" fill="#56a3d9"/><path d="M190 105 q10 -6 14 6 q-6 10 -14 4z M210 116 q12 -4 14 10 q-8 6 -16 -2z" fill="#6fbf73"/>'
 +person(80,150,s=.7,skin='b',hair='curly',hc='#3a2a1d',top='#4a7bd1',arms='up')+person(140,155,s=.7,skin='a',hair='long',hc='#c8862f',top='#e5649a',arms='forward')+person(330,150,s=.7,skin='d',hair='short',hc='#1f1610',top='#5fb38a',arms='forward'))
print('tamam')
