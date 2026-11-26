"""Shuffled-K4 nulls (PREREG242): seeds 209758-209769, random.Random(seed).shuffle of the 97 carved letters."""
import random
K4 = open('k4.txt').read().strip()
with open('nulls242.tsv', 'w') as fo:
    for s in range(209758, 209770):
        L = list(K4); random.Random(s).shuffle(L); fo.write(f'{s}\t{"".join(L)}\n')
