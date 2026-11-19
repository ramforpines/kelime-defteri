# add.py gibi, ama a/an/the/be/to/your/one's farklarını yok sayarak yinelenenleri atlar.
import json,re,sys,importlib.util
def norm(s):
    s=s.lower().replace('’',"'")
    s=re.sub(r"\b(sb|sth|somebody|something|someone|one's|your|his|her|their|my|a|an|the|to|be|you)\b",'',s)
    s=re.sub(r"[^a-z' -]",' ',s)
    return re.sub(r'\s+',' ',s).strip()
spec=importlib.util.spec_from_file_location('m',sys.argv[1]);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
p='words.js';s=open(p,encoding='utf-8').read();pre='window.WORDS='
D=json.loads(s[len(pre):].rstrip().rstrip(';'))
have={norm(r[0]) for r in D}|{r[0].lower() for r in D}
add=[];skip=[]
for r in m.ROWS:
    n=norm(r[0])
    if len(r)!=11 or r[0].lower() in have or n in have: skip.append(r[0])
    else: add.append(r);have.add(n)
D+=add
open(p,'w',encoding='utf-8').write(pre+json.dumps(D,ensure_ascii=False,separators=(',',':'))+';')
print('added',len(add),'skip',len(skip),skip)
