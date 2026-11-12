import json,subprocess,sys,os
ROOT=os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','..'))
js="global.window={};require(process.argv[1]+'/grammar.js');process.stdout.write(JSON.stringify(window.GRAMMAR))"
G=json.loads(subprocess.run(['node','-e',js,ROOT],capture_output=True,check=True).stdout)
for t in G:
    if t['id']!=sys.argv[1]:continue
    seen=set()
    for src in('quiz','dq'):
        for q in t.get(src,[]):
            if q['t'] in('Doğru cümle','Hatayı bul'):continue
            k=(q['q'],q['o'][q['a']])
            print(repr(q['q']),'|',' / '.join(('*' if i==q['a'] else '')+o for i,o in enumerate(q['o'])),'|',q['w'])
