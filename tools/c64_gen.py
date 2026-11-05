"""Cycle 64 vocabulary: one English word sets BOTH the keyed-columnar order and the mixed tableau alphabet.
Words: cycle-56 themed+frequent list + dwyl words_alpha (370k), letters only, length 4-20.
Output: one line per distinct (column order, mixed alphabet): NAME W o0..o(W-1)."""
import re
ws=[l.strip().upper() for l in open('/workspace/kcl/tools/words56.txt') if l.strip()] if False else []
import os
p56='/workspace/k4_support_backup/c56/words56.txt'
ws=[l.strip().upper() for l in open(p56) if l.strip()]
ws+=[l.strip().upper() for l in open('words_alpha.txt') if l.strip()]
seen=set(); out=[]
for w in ws:
    if not re.fullmatch(r'[A-Z]{4,20}',w): continue
    o=tuple(sorted(range(len(w)),key=lambda i:(w[i],i)))
    a=''.join(dict.fromkeys(w+'ABCDEFGHIJKLMNOPQRSTUVWXYZ'))
    if (o,a) in seen: continue
    seen.add((o,a)); out.append(w+' %d '%len(w)+' '.join(map(str,o)))
open('words64.txt','w').write('\n'.join(out)+'\n'); print(len(out))
