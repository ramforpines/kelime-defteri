#!/usr/bin/env python3
"""Seviye tespiti soru bankası: tools/pl/*.txt → pl-bank.js (window.PLB).
Kontroller: şık sayısı, tek doğru, tekrar eden soru, şık uzunluk dengesi (doğru şık en uzun/en kısa olma oranı),
uydurma kelimelerin gerçek kelime olmaması (wordfreq + words.js), C-test boşluklarının dökümü (gözle kontrol için).
Kimlikler sorunun metninden türetilir (md5): soru değişirse yeni soru sayılır, kalibrasyon verisi karışmaz."""
import re, json, hashlib, sys, os
D = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.join(D, '..', '..')
LV = ['A1', 'A2', 'B1', 'B2', 'C1', 'C2']
hid = lambda p, s: p + hashlib.md5(s.encode()).hexdigest()[:7]

def blocks(fn):
    lv = None; out = []
    for b in re.split(r'\n\s*\n', open(os.path.join(D, fn), encoding='utf-8').read()):
        lines = [l for l in b.strip().split('\n') if l.strip() and not l.startswith('#')]
        while lines and lines[0].startswith('@'):
            lv = lines[0][1:].strip(); lines = lines[1:]
        if lines: out.append((lv, lines))
    return out

def mc(fn, pre, typed=False):
    items = []; warn = []
    for lv, L in blocks(fn):
        assert lv in LV, (fn, lv)
        q = L[0]; ty = None
        if typed:
            m = re.match(r'(syn|def|use|col):\s*(.*)', q); assert m, q; ty, q = m.group(1), m.group(2)
        opts = [l[2:].strip() for l in L[1:]]; marks = [l[0] for l in L[1:]]
        assert all(m in '*-' for m in marks), L
        assert marks.count('*') == 1, ('tek doğru şık olmalı', q)
        assert len(set(o.lower() for o in opts)) == len(opts), ('aynı şık', q)
        a = marks.index('*'); o = [opts[a]] + [x for i, x in enumerate(opts) if i != a]   # doğru şık başta; uygulama karıştırır
        it = {'id': hid(pre, q), 'lv': lv, 'q': q, 'o': o}
        if ty: it['t'] = ty
        items.append(it)
    ids = [i['id'] for i in items]; assert len(ids) == len(set(ids)), 'tekrar eden soru'
    # uzunluk dengesi
    longest = shortest = 0; ratios = []
    for it in items:
        ln = [len(x) for x in it['o']]
        if ln[0] == max(ln) and ln.count(max(ln)) == 1: longest += 1
        if ln[0] == min(ln) and ln.count(min(ln)) == 1: shortest += 1
        ratios.append(max(ln) / max(1, min(ln)))
    n = len(items)
    print(f'{fn}: {n} soru · seviyeler ' + ' '.join(f'{l}:{sum(1 for i in items if i["lv"]==l)}' for l in LV) +
          f' · doğru şık tek başına en uzun %{round(100*longest/n)} · en kısa %{round(100*shortest/n)} (rastgele beklenti ~%25)')
    return items

CT_ALT = {'this': ['that'], 'these': ['those'], 'paralysing': ['paralyzing'], 'favourite': ['favorite']}   # bağlamda da doğru olan başka tamamlamalar
def ctest(fn):
    texts = []
    for lv, L in blocks(fn):
        lvl, title = lv.split('|')[0].strip(), lv.split('|')[1].strip()
        text = ' '.join(L).strip()
        sents = re.split(r'(?<=[.!?])\s+', text)
        first, rest = sents[0], ' '.join(sents[1:])
        toks = re.findall(r"[A-Za-z][A-Za-z'\-]*|[^A-Za-z]+", rest)
        out = []; gaps = 0; k = 0; tail = False
        for t in toks:
            if tail or not re.match(r'[A-Za-z]', t): out.append(t); continue
            k += 1
            w = t
            if k % 2 == 0 and gaps < 20 and len(re.sub(r"[^A-Za-z]", '', w)) >= 2 and "'" not in w and '-' not in w and not (w[0].isupper()):
                keep = len(w) // 2
                out.append({'p': w[:keep], 'a': w[keep:].lower()}); gaps += 1
            else:
                out.append(t)
            if gaps >= 20 and k % 2 == 0: tail = True
        assert gaps == 20, (title, gaps)
        for x in out:
            if isinstance(x, dict) and (x['p'] + x['a']).lower() in CT_ALT: x['x'] = [w[len(x['p']):] for w in CT_ALT[(x['p'] + x['a']).lower()]]
        texts.append({'id': hid('ct', text[:80]), 'lv': lvl, 't': title, 'f': first, 's': out})
        print(f'  C-test {lvl} "{title}": ' + ''.join(x if isinstance(x, str) else f"{x['p']}[{x['a']}]" for x in out)[:900])
    return texts

def nonwords(fn):
    from wordfreq import zipf_frequency as z
    words = set(re.findall(r'\["([a-z\-]+)"', open(os.path.join(ROOT, 'words.js'), encoding='utf-8').read()))
    nw = [l.strip() for l in open(os.path.join(D, fn)) if l.strip() and not l.startswith('#')]
    bad = [w for w in nw if z(w, 'en') > 0 or w in words]
    assert not bad, ('gerçek kelime olabilir', bad)
    print(f'{fn}: {len(nw)} uydurma kelime (hiçbiri sözlükte/frekans listesinde yok)')
    return nw

ALT = {}
if os.path.exists(os.path.join(D, 'alt.json')): ALT = json.load(open(os.path.join(D, 'alt.json')))
B = {'v': 1, 'gr': mc('gr.txt', 'g'), 'mn': mc('mn.txt', 'm'), 'kv': mc('kv.txt', 'k', typed=True), 'ct': ctest('ct.txt'), 'nw': nonwords('nw.txt'), 'alt': ALT}
open(os.path.join(ROOT, 'pl-bank.js'), 'w', encoding='utf-8').write(
    '/* Seviye tespiti soru bankası — tools/pl/build.py üretir, elle düzenleme */\nwindow.PLB=' + json.dumps(B, ensure_ascii=False, separators=(',', ':')) + ';\n')
print('pl-bank.js yazıldı', os.path.getsize(os.path.join(ROOT, 'pl-bank.js')), 'bayt')
