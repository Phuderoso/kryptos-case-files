# Cycle 83 shuffled-K4 nulls (same letters, random order), seeds 8310-8312.
import random
import os as _os, sys as _sys; _sys.path.insert(0, _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), ".."))
from kryptos_text import K4
for n in range(3):
    l = list(K4); random.Random(8310 + n).shuffle(l); open(f"null_{n}.txt", "w").write("".join(l))
