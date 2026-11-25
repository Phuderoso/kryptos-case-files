"""Fresh shuffled nulls (PREREG238 Part B): seeds 209707, 209708, random.Random(seed).shuffle(list(K4)). Writes nulls238.tsv: seed text sha256"""
import random, hashlib
K4 = open('k4.txt').read().strip()
with open('nulls238.tsv', 'w') as fh:
    for s in (209707, 209708):
        L = list(K4); random.Random(s).shuffle(L); t = ''.join(L)
        fh.write(f"{s}\t{t}\t{hashlib.sha256(t.encode()).hexdigest()}\n")
