"""K4 diagnostics: frequencies, IoC, and falsification tests of periodic substitution against Sanborn's
official cribs. Run: python3 tools/k4_analysis.py > analysis/k4_report.txt"""
from collections import Counter
from kryptos_text import K4, KA
AZ = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
# Official cribs, 1-indexed positions (sources in case-file/03-k4-evidence.md)
CRIBS = {22: "EAST", 26: "NORTHEAST", 64: "BERLIN", 70: "CLOCK"}
known = {p + i: ch for p, w in CRIBS.items() for i, ch in enumerate(w)}

def ioc(t):
    c = Counter(t); n = len(t)
    return sum(v*(v-1) for v in c.values()) / (n*(n-1))

print("== K4 ciphertext (97 chars) ==\n" + K4)
print("\n== Crib alignment check ==")
for p, w in CRIBS.items():
    print(f"pos {p:>2}-{p+len(w)-1:<2} CT={K4[p-1:p-1+len(w)]}  PT={w}")
c = Counter(K4)
print("\n== Frequencies ==")
print(" ".join(f"{k}:{c.get(k,0)}" for k in AZ))
print(f"\nIoC(K4) = {ioc(K4):.4f}  (random 26-letter ~0.0385; English ~0.0667)")
print(f"Self-encryptions in cribs: {[p for p,ch in known.items() if K4[p-1]==ch]}")

def keys(alpha, mode):
    out = {}
    for p, pt in known.items():
        ct = K4[p-1]; a, b = alpha.index(ct), alpha.index(pt)
        k = (a-b) % 26 if mode == "vig" else (a+b) % 26 if mode == "beau" else (b-a) % 26
        out[p] = alpha[k]
    return out

print("\n== Periodic-key consistency (Vigenere / Beaufort / Variant-Beaufort; AZ and KRYPTOS alphabets) ==")
print("A period P is CONSISTENT if every crib position sharing (pos mod P) implies the same key letter.")
for aname, alpha in (("AZ", AZ), ("KA", KA)):
    for mode in ("vig", "beau", "varbeau"):
        ks = keys(alpha, mode)
        ok = [P for P in range(1, 50) if all(len({ks[q] for q in ks if q % P == r}) <= 1 for r in range(P))]
        seq = "".join(ks[p] for p in sorted(ks))
        col = {P: sum(1 for a in ks for b in ks if a < b and (b-a) % P == 0) for P in ok}
        print(f"{aname}-{mode:8s} implied key at cribs: {seq}  consistent periods<50: {ok}  constraining pairs: {col}")
print("\nInterpretation: if no small period is consistent, simple periodic polyalphabetic substitution"
      " directly on K4 (the K1/K2 method) is falsified for those alphabets; a transposition and/or"
      " non-periodic key layer is required.")
