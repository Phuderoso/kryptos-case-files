# word-keyed alphabets from words_alpha.txt: (a) keyword + rest A-Z, (b) keyword + rest continuing after last keyword letter (wrap)
import sys
ws=[w.strip().upper() for w in open('/workspace/k4c64/words_alpha.txt') if w.strip().isalpha()]
seen=set(); out=bytearray()
for w in ws:
    kw=''.join(dict.fromkeys(w))
    rest=[c for c in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ' if c not in kw]
    last=kw[-1]; r2=sorted(rest,key=lambda c:(ord(c)-ord(last))%26)
    for a in (kw+''.join(rest), kw+''.join(r2), (kw+''.join(rest))[::-1]):
        if a not in seen: seen.add(a); out+=bytes(ord(c)-65 for c in a)
open('words94.bin','wb').write(out); print(len(seen))
