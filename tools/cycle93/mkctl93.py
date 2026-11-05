"""Cycle 93: planted two-square Bifid control (p 28, orient 0) and three shuffled W-free nulls for the annealer."""
import random, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bifid5w import SYM, KW, CRIB, bifid_enc
rng = random.Random(931)
filler = list("THEVALLEYLAYSILENTUNDERTHEOLDSTONESANDTHEBURIEDROOMHELDACANDLEFLAMEFLICKERINGINTHEDARKAIR" * 2)
pt = "".join(CRIB[i] if i in CRIB else filler.pop(0) for i in range(92))
a = list(SYM); rng.shuffle(a); b = rng.sample(SYM, 25)
print(bifid_enc(pt, a, b, 28)); print(pt)
for r in range(3):
    l = list(KW); rng.shuffle(l); print("".join(l))
