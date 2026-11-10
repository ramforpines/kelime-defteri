import json,re,sys,importlib.util
spec=importlib.util.spec_from_file_location('m',sys.argv[1]);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
p='words.js';s=open(p,encoding='utf-8').read()
pre='window.WORDS=';assert s.startswith(pre)
body=s[len(pre):].rstrip().rstrip(';')
D=json.loads(body)
have={r[0].lower() for r in D}
add=[r for r in m.ROWS if r[0].lower() not in have and len(r)==11]
skip=[r[0] for r in m.ROWS if r[0].lower() in have]
D+=add
open(p,'w',encoding='utf-8').write(pre+json.dumps(D,ensure_ascii=False,separators=(',',':'))+';')
print('added',len(add),'skip',skip)
