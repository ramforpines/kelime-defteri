#!/usr/bin/env python3
"""Seviye tespiti soru bankası: tools/pl/*.txt → pl-bank.js (window.PLB).
Kontroller: şık sayısı, tek doğru, tekrar eden soru, şık uzunluk dengesi (doğru şık en uzun/en kısa olma oranı),
uydurma kelimelerin gerçek kelime olmaması (wordfreq + words.js), C-test boşluklarının dökümü (gözle kontrol için).
Kimlikler sorunun metninden türetilir (md5): soru değişirse yeni soru sayılır, kalibrasyon verisi karışmaz."""
import re, json, hashlib, sys, os, glob
D = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.join(D, '..', '..')
LV = ['A1', 'A2', 'B1', 'B2', 'C1', 'C2']
hid = lambda p, s: p + hashlib.md5(s.encode()).hexdigest()[:7]

def blocks(fn):
    lv = None; out = []
    txt = '\n\n'.join(open(f, encoding='utf-8').read() for f in sorted(glob.glob(os.path.join(D, fn))))
    for b in re.split(r'\n\s*\n', txt):
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

CT_ALT = {'this': ['that'], 'these': ['those'], 'paralysing': ['paralyzing'], 'favourite': ['favorite'], 'realise': ['realize'], 'organisations': ['organizations'], 'metres': ['meters']}   # bağlamda da doğru olan başka tamamlamalar
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
    from english_words import get_english_words_set as gw
    E = gw(['web2', 'gcide'], lower=True)
    words = set(re.findall(r'\["([a-z\-]+)"', open(os.path.join(ROOT, 'words.js'), encoding='utf-8').read()))
    nw = [l.strip() for l in open(os.path.join(D, fn)) if l.strip() and not l.startswith('#')]
    assert len(nw) == len(set(nw)), 'tekrar eden uydurma kelime'
    bad = [w for w in nw if z(w, 'en') > 0 or w in words or w in E]
    assert not bad, ('gerçek kelime olabilir', bad)
    print(f'{fn}: {len(nw)} uydurma kelime (hiçbiri sözlükte/frekans listesinde yok)')
    return nw

ALT = {}
if os.path.exists(os.path.join(D, 'alt.json')): ALT = json.load(open(os.path.join(D, 'alt.json')))
def wtasks(fn):
    out = []
    for lv, L in blocks(fn):
        lvl, g = [x.strip() for x in lv.split('|')]
        d = {}
        for l in L:
            k, v = l.split(':', 1); d[k.strip()] = v.strip()
        assert lvl in LV and set(d) == {'TR', 'EN', 'P'}, (lv, d.keys())
        pts = [p.strip() for p in d['P'].split(';')]; assert len(pts) == 3, d['P']
        out.append({'id': hid('w', d['EN']), 'lv': lvl, 'g': g, 'tr': d['TR'], 't': d['EN'].replace(' // ', '\n'), 'p': pts})
    print(f'{fn}: {len(out)} yazma konusu · ' + ' '.join(f'{l}:{sum(1 for i in out if i["lv"]==l)}' for l in LV))
    return out


def texts(fn, listen=False):
    out = []
    txt = '\n'.join(open(f, encoding='utf-8').read() for f in sorted(glob.glob(os.path.join(D, fn))))
    for blk in txt.split('\n=== ')[1:]:
        L = [l.rstrip() for l in blk.strip().split('\n') if l.strip() and not l.startswith('#')]
        lvl, title = [x.strip() for x in L[0].split('|', 1)]; assert lvl in LV, L[0]
        body, qs, cur = [], [], None
        for l in L[1:]:
            if l.startswith('Q: '): cur = {'q': l[3:], 'o': [], 'm': []}; qs.append(cur)
            elif l[:2] in ('* ', '- ') and cur: cur['o'].append(l[2:].strip()); cur['m'].append(l[0])
            else:
                m = re.match(r'(P|M|F|M2|F2):\s*(.*)', l); assert m and not cur, ('beklenmeyen satır', title, l)
                body.append([m.group(1), m.group(2)])
        assert 2 <= len(qs) <= 6, (title, len(qs))
        Q = []
        for q in qs:
            assert q['m'].count('*') == 1 and len(q['o']) >= 3, (title, q['q'])
            a = q['m'].index('*'); Q.append({'q': q['q'], 'o': [q['o'][a]] + [x for i, x in enumerate(q['o']) if i != a]})
        it = {'id': hid('l' if listen else 'r', title + body[0][1][:60]), 'lv': lvl, 't': title, 'q': Q}
        if listen: assert all(b[0] != 'P' for b in body); it['sc'] = body; it['au'] = 'audio/pl/' + it['id'] + '.mp3'
        else: assert all(b[0] == 'P' for b in body); it['p'] = [b[1] for b in body]
        out.append(it)
    n = len(out); qn = sum(len(x['q']) for x in out)
    lg = sum(1 for x in out for q in x['q'] if len(q['o'][0]) == max(len(o) for o in q['o']) and [len(o) for o in q['o']].count(len(q['o'][0])) == 1)
    print(f'{fn}: {n} metin, {qn} soru · ' + ' '.join(f'{l}:{sum(1 for i in out if i["lv"]==l)}' for l in LV) + f' · doğru şık en uzun %{round(100*lg/max(1,qn))}')
    return out

def audio(items):
    import hashlib as H, subprocess, tempfile
    AD = os.path.join(ROOT, 'audio', 'pl'); os.makedirs(AD, exist_ok=True)
    VOICE = {'M': 'bm_george', 'F': 'bf_emma', 'M2': 'bm_lewis', 'F2': 'bf_isabella'}
    TTS = os.environ.get('KD_TTS', '/tmp/claude-0/tts'); k = None; keep = set()
    for it in items:
        name = it['id']; mp3 = os.path.join(AD, name + '.mp3'); sg = mp3 + '.sig'; keep |= {name + '.mp3', name + '.mp3.sig'}
        sig = H.sha1(json.dumps([it['lv'], it['sc']], ensure_ascii=False).encode()).hexdigest()[:16]
        if os.path.exists(mp3) and os.path.exists(sg) and open(sg).read() == sig: continue
        if '--no-audio' in sys.argv: print('SES EKSİK:', name); continue
        if k is None:
            from kokoro_onnx import Kokoro
            import numpy as np, soundfile as sf
            k = Kokoro(os.path.join(TTS, 'kokoro-v1.0.int8.onnx'), os.path.join(TTS, 'voices-v1.0.bin'))
        parts = []; sr = 24000; sp_ = 0.85 if it['lv'] in ('A2', 'B1') else 0.95
        for sp, line in it['sc']:
            s, sr = k.create(line, voice=VOICE[sp], speed=sp_, lang='en-gb'); parts.append(s); parts.append(np.zeros(int(sr * 0.5), dtype=s.dtype))
        wav = tempfile.mktemp(suffix='.wav'); sf.write(wav, np.concatenate(parts), sr)
        subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', wav, '-ac', '1', '-ar', '22050', '-b:a', '40k', mp3], check=True); os.remove(wav)
        open(sg, 'w').write(sig); print('ses:', name, it['t'], flush=True)
    for f in os.listdir(AD):
        if f not in keep: os.remove(os.path.join(AD, f)); print('silindi:', f)

RD = texts('rd*.txt'); LS = texts('ls*.txt', listen=True); audio(LS)
B = {'v': 1, 'gr': mc('gr*.txt', 'g'), 'mn': mc('mn*.txt', 'm'), 'kv': mc('kv*.txt', 'k', typed=True), 'ct': ctest('ct*.txt'), 'nw': nonwords('nw.txt'), 'wt': wtasks('wt.txt'), 'rd': RD, 'ls': [{k: v for k, v in x.items() if k != 'sc'} | {'n': len(x['sc'])} for x in LS], 'alt': ALT}
open(os.path.join(ROOT, 'pl-bank.js'), 'w', encoding='utf-8').write(
    '/* Seviye tespiti soru bankası — tools/pl/build.py üretir, elle düzenleme */\nwindow.PLB=' + json.dumps(B, ensure_ascii=False, separators=(',', ':')) + ';\n')
print('pl-bank.js yazıldı', os.path.getsize(os.path.join(ROOT, 'pl-bank.js')), 'bayt')
