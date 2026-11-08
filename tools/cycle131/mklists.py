"""Cycle 131 word lists: themed.txt (tools/dcol_gen.py THEMED, 97 words) and all.txt (themed + cycle-56 vocabulary, 10,056)."""
import re
src=open('/tmp/kcf/tools/dcol_gen.py').read(); th=re.search(r'THEMED="""(.*?)"""',src,re.S).group(1).split()
voc=[l.split()[0].upper() for l in open('/tmp/kcf/data/cycle56/words56.txt') if l.strip()]
w=list(dict.fromkeys([x for x in th+voc if x.isalpha() and 2<=len(x)<=31]))
open('themed.txt','w').write('\n'.join(th)+'\n'); open('all.txt','w').write('\n'.join(w)+'\n')
