"""Fresh shuffled nulls (PREREG236): seeds 209673-209678, random.Random(seed).shuffle(list(K4)). Writes nulls236.tsv: seed text sha256"""
import random, hashlib
K4 = open('k4.txt').read().strip()
with open('nulls236.tsv', 'w') as fh:
    for s in range(209673, 209679):
        L = list(K4); random.Random(s).shuffle(L); t = ''.join(L)
        fh.write(f"{s}\t{t}\t{hashlib.sha256(t.encode()).hexdigest()}\n")
