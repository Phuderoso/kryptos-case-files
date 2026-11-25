"""Fresh shuffled nulls (PREREG239): seeds 209711-209716, random.Random(seed).shuffle(list(K4)). Writes nulls239.tsv: seed text sha256"""
import random, hashlib
K4 = open('k4.txt').read().strip()
with open('nulls239.tsv', 'w') as fh:
    for s in range(209711, 209717):
        L = list(K4); random.Random(s).shuffle(L); t = ''.join(L)
        fh.write(f"{s}\t{t}\t{hashlib.sha256(t.encode()).hexdigest()}\n")
