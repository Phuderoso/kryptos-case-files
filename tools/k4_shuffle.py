"""Cycle 8 (3): 'scrambled plaintext' = block/word shuffle + one simple cipher.
Reasoning: if Sanborn's crib positions refer to the *scrambled* text, the shuffle is invisible to the crib test and the
model collapses to CT = Sub(X), already excluded for periodic keys (cycle 1) and the plain-sight keyword list (cycle 7,
identity T). So the only new case is: cribs at ORIGINAL plaintext positions, with
   S1 CT = Sub(Shuffle(PT))   key indexed by CT position
   S2 CT = Shuffle(Sub(PT))   key indexed by PT position
Shuffles: K4 cut into blocks of length b (last block shorter, 97 is prime).
   b = 2..13: simple shuffles (reverse block order, swap halves, odd/even blocks, reverse inside blocks, block rotations)
   b = 14..49 (<= 7 blocks): ALL block permutations.
Sub: periodic Vigenere/Beaufort, period 1-26, KA and AZ; survivor = consistent with all cribs and >= 6 redundant constraints.
Run: python3 tools/k4_shuffle.py [control]"""
import sys, itertools
sys.path.insert(0, "tools")
from k4_anneal import AZ, KA, KN, N
import kryptos_text
K4 = kryptos_text.K4
def blocks(b): return [list(range(s, min(s + b, N))) for s in range(0, N, b)]
def shuffles():
    for b in range(2, 50):
        B = blocks(b); n = len(B); cand = {}
        if n <= 7:
            for p in itertools.permutations(range(n)):
                cand[f"b{b} perm{p}"] = [i for k in p for i in B[k]]
        else:
            cand[f"b{b} revorder"] = [i for blk in B[::-1] for i in blk]
            cand[f"b{b} revinside"] = [i for blk in B for i in blk[::-1]]
            cand[f"b{b} odd/even"] = [i for blk in B[0::2] + B[1::2] for i in blk]
            cand[f"b{b} even/odd"] = [i for blk in B[1::2] + B[0::2] for i in blk]
            h = n // 2
            cand[f"b{b} swaphalves"] = [i for blk in B[h:] + B[:h] for i in blk]
            for r in range(1, n):
                cand[f"b{b} rot{r}"] = [i for blk in B[r:] + B[:r] for i in blk]
        for k, v in cand.items():
            if v != list(range(N)): yield k, v
ITEMS = list(KN.items())
def run(CT=K4):
    tests = 0; surv = []
    pre = {(an, mode): [((alpha.index(CT[j]) - alpha.index(p)) % 26 if mode == "vig" else (alpha.index(CT[j]) + alpha.index(p)) % 26)
                        for j in range(N) for p in [None]] for an, alpha in (("KA", KA), ("AZ", AZ)) for mode in ("vig", "beau")} if False else None
    for name, perm in shuffles():
        inv = [0] * N
        for j, i in enumerate(perm): inv[i] = j
        for an, alpha in (("KA", KA), ("AZ", AZ)):
            for mode in ("vig", "beau"):
                es = []
                for i, p in ITEMS:
                    j = inv[i]; c = alpha.index(CT[j]); q = alpha.index(p)
                    es.append((i, j, (c - q) % 26 if mode == "vig" else (c + q) % 26))
                for model in ("S1", "S2"):
                    for P in range(1, 27):
                        tests += 1; key = {}; n = 0; ok = True
                        for i, j, e in es:
                            kk = (j if model == "S1" else i) % P
                            if kk in key:
                                n += 1
                                if key[kk] != e: ok = False; break
                            else: key[kk] = e
                        if ok and n >= 6: surv.append((name, model, an, mode, P, n))
    return tests, surv
if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "control":
        eng = "WEMETATTHECORNERWHERETHEROADTURNSEASTNORTHEASTANDTHEOLDSTATIONSTOODWAITINGFORTHEBERLINCLOCKTOSTRIKE"
        pt = list(eng[:N])
        for i, ch in KN.items(): pt[i] = ch
        perm = [i for k in (3, 0, 5, 1, 2, 6, 4) for i in blocks(14)[k]]
        key = "SHADOW"
        ct = "".join(KA[(KA.index(pt[perm[j]]) + KA.index(key[j % 6])) % 26] for j in range(N))
        t, s = run(ct); print(f"CONTROL planted b14 perm(3,0,5,1,2,6,4) S1 KA vig SHADOW: tests {t}, survivors {s}")
    else:
        t, s = run(); print(f"K4: tests {t}, survivors {len(s)}"); [print(" ", x) for x in s[:50]]
