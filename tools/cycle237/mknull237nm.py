"""I-376 nulls (PREREG237): seeds 209686-209705, random.Random(seed).shuffle(list(K4)). Writes nulls237nm.tsv: seed text sha256"""
import random, hashlib
K4 = open('k4.txt').read().strip()
with open('nulls237nm.tsv', 'w') as fh:
    for s in range(209686, 209706):
        L = list(K4); random.Random(s).shuffle(L); t = ''.join(L)
        fh.write(f"{s}\t{t}\t{hashlib.sha256(t.encode()).hexdigest()}\n")
