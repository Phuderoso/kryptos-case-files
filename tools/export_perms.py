"""Cycle 22: export the cycle-19 transposition family (97 letters) plus identity as raw int16 for the C checker."""
import numpy as np
from k4_autokey_trans import family
fam = family(97)
ident = (np.arange(97, dtype=np.int16), "identity")
fam = [ident] + fam
np.stack([f[0] for f in fam]).astype(np.int16).tofile("perms97.bin")
open("perms97_tags.txt", "w").write("\n".join(f[1] for f in fam))
print(len(fam))
