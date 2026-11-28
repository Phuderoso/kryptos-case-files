"""Shuffled-K4 nulls (PREREG244, I-408): seeds 209783-209806, random.Random(seed).shuffle of the 97 carved letters (as mknull243.py)."""
import random
K4 = open('k4.txt').read().strip()
with open('nulls244.tsv', 'w') as fo:
    for s in range(209783, 209807):
        L = list(K4); random.Random(s).shuffle(L); fo.write(f'{s}\t{"".join(L)}\n')
