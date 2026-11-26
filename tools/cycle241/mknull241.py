"""Fresh nulls (PREREG241): set C 209731-209742, set D 209743-209754; random.Random(seed).shuffle(list(K4)), as mknull235.py."""
import random, hashlib
K4 = open('k4.txt').read().strip()
with open('nulls241.tsv', 'w') as fh:
    for s in range(209731, 209755):
        t = list(K4); random.Random(s).shuffle(t); t = ''.join(t)
        fh.write(f"{s}\t{'C' if s < 209743 else 'D'}\t{t}\t{hashlib.sha256(t.encode()).hexdigest()[:16]}\n")
