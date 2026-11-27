"""Shuffled-K4 nulls (PREREG243): seeds 209771-209782, random.Random(seed).shuffle of the 97 carved letters."""
import random
K4 = open('k4.txt').read().strip()
with open('nulls243.tsv', 'w') as fo:
    for s in range(209771, 209783):
        L = list(K4); random.Random(s).shuffle(L); fo.write(f'{s}\t{"".join(L)}\n')
