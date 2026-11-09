#!/usr/bin/env python3
"""chunks/*.js dosyalarındaki yeni okuma şıklarını ../../reading-fix.js olarak birleştirir.
Her soru: [[şıklar (doğru olan İLK)], [Türkçe şıklar]]. reading-fix.js, yüklenince şıkları ve çevirileri değiştirir."""
import glob,os
H=os.path.dirname(os.path.abspath(__file__));ROOT=os.path.abspath(os.path.join(H,'..','..'))
body=''.join(open(f,encoding='utf8').read().rstrip().rstrip(',')+',\n' for f in sorted(glob.glob(H+'/chunks/*.js')))
adj=''.join(open(f,encoding='utf8').read().rstrip().rstrip(',')+',\n' for f in sorted(glob.glob(H+'/adj/*.js')))
out='''/* Okuma şıkları: reading*.js içindeki şıkları ve reading-tr.js'deki şık çevirilerini değiştirir (tools/reading/build.py üretir).
   Her soru için ilk şık doğru cevaptır; ekranda şıklar zaten karıştırılır. */
window.READFIX={
'''+body+'''};
window.READADJ={
'''+adj+'''};
(function(){var R=window.READINGS||[],T=window.READINGS_TR||{};
var tr=function(s){return s.replace(/(^|[\\s(])I(?!sı|şık|rak|rmak|lık)(?=[a-zçğöşü])/g,function(m,a){return a+'\\u0130'})};
R.forEach(function(p){var f=window.READFIX[p.id];if(!f)return;
 f.forEach(function(x,i){var q=p.q[i];if(!q||x[0].length!==q.o.length)return;q.o=x[0].slice();q.a=0;
  var t=T[p.id]&&T[p.id].q&&T[p.id].q[i];if(t)t.o=x[1].map(tr);var a=window.READADJ[p.id+'#'+i];if(a)for(var k in a){q.o[k]=a[k][0];if(t)t.o[k]=tr(a[k][1])}})})})();
'''
open(os.path.join(ROOT,'reading-fix.js'),'w',encoding='utf8').write(out)
print('reading-fix.js',len(out))
