"""Positive controls for cycle 3: synthetic K4s (random PT with the real cribs) encrypted with KNOWN keys must be detected.
Run from repo root: python3 tools/validate_cycle3.py"""
import random, io, contextlib, importlib, sys
sys.path.insert(0, "tools"); import kryptos_text
AZ = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"; KA = kryptos_text.KA; REAL = kryptos_text.K4
random.seed(42); pt = [random.choice(AZ) for _ in range(97)]
for p, w in {22: "EAST", 26: "NORTHEAST", 64: "BERLIN", 70: "CLOCK"}.items():
    for i, ch in enumerate(w): pt[p-1+i] = ch
def run(ct):
    kryptos_text.K4 = ct; buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        if "k4_cycle3" in sys.modules: importlib.reload(sys.modules["k4_cycle3"])
        else: import k4_cycle3
    return buf.getvalue()
def kal(w): return "".join(dict.fromkeys(w + AZ))
# C1: keyed columnar w=6 order (2,0,5,1,4,3), then KA Vigenere key 'CLOCK' indexed by CT position (model B2)
order = (2,0,5,1,4,3); rows = 17; tp = [pt[r*6+c] for c in order for r in range(rows) if r*6+c < 97]
ct = "".join(KA[(KA.index(x) + KA.index("CLOCK"[k % 5])) % 26] for k, x in enumerate(tp))
print("C1 columnar+Vig:", [l for l in run(ct).splitlines() if "order=(2, 0, 5, 1, 4, 3)" in l][:2])
# C2: Gromark primer (3,8,5,7), AZ Vigenere
k = [3,8,5,7]
while len(k) < 97: k.append((k[-4] + k[-3]) % 10)
ct = "".join(AZ[(AZ.index(x) + k[i]) % 26] for i, x in enumerate(pt))
print("C2 Gromark:", [l for l in run(ct).splitlines() if "gromark primer=(3, 8, 5, 7)" in l])
# C3: Quagmire IV PT alphabet EGYPT, CT alphabet URANIA, key 'BERLIN' (P=6)
A1, A2 = kal("EGYPT"), kal("URANIA"); key = [A2.index(c) for c in "BERLIN"]
ct = "".join(A2[(A1.index(x) + key[i % 6]) % 26] for i, x in enumerate(pt))
print("C3 Quagmire IV:", [l for l in run(ct).splitlines() if "EGYPT/URANIA" in l][:2])
kryptos_text.K4 = REAL
