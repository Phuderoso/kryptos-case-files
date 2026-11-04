"""Cycle 8 (2): diff the Kryptos-side text of Antipodes (text transcription at https://scirealm.org/Antipodes.html,
saved to data/antipodes_kryptos_side_scirealm.txt) against the Kryptos K3+K4+K1+K2 sequence. Text only, no photos."""
import sys, difflib
sys.path.insert(0, "tools")
from kryptos_text import K1, K2, K3, K4
a = open("data/antipodes_kryptos_side_scirealm.txt").read().replace(" ", "").replace("\n", "").replace(".", "")
segs = [("K3", K3), ("K4", K4), ("K1", K1), ("K2", K2)] * 2
ref = "".join(s for _, s in segs)[:len(a) + 40]
def where(i):
    for n, s in segs:
        if i < len(s): return f"{n}+{i + 1}"
        i -= len(s)
print("Antipodes letters (incl. ?):", len(a))
for op, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, ref, autojunk=False).get_opcodes():
    if op != "equal": print(op, "Antipodes", repr(a[i1:i2]), "Kryptos", repr(ref[j1:j2]), "at", where(j1))
for k, start in enumerate([i for i in range(len(a)) if a.startswith(K4, i)]): print(f"K4 copy {k + 1} found verbatim at offset {start}")
