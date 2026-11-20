"""Cycle 224 (PREREG224): keyboard layouts -> kb224.bin (18 alphabets x 26, values 0-25) and geo224.txt
(per layout: row, colA, colB class of each letter A-Z, and colA index for the V torus)."""
import sys
L = {
 "QWERTY": [[(c, i) for i, c in enumerate("QWERTYUIOP")], [(c, i) for i, c in enumerate("ASDFGHJKL")], [(c, i) for i, c in enumerate("ZXCVBNM")]],
 "QWERTZ": [[(c, i) for i, c in enumerate("QWERTZUIOP")], [(c, i) for i, c in enumerate("ASDFGHJKL")], [(c, i) for i, c in enumerate("YXCVBNM")]],
 "AZERTY": [[(c, i) for i, c in enumerate("AZERTYUIOP")], [(c, i) for i, c in enumerate("QSDFGHJKLM")], [(c, i) for i, c in enumerate("WXCVBN")]],
 "DVORAK": [[(c, i + 3) for i, c in enumerate("PYFGCRL")], [(c, i) for i, c in enumerate("AOEUIDHTNS")], [(c, i + 1) for i, c in enumerate("QJKXBMWVZ")]],
}
NAMES = list(L)
def alphabets(lay):
    rows = L[lay]
    R1 = "".join(c for r in rows for c, _ in r)
    R2 = "".join(c for r in rows for c, _ in reversed(r))
    cols = {}
    for ri, r in enumerate(rows):
        for c, i in r: cols.setdefault(i, []).append((ri, c))
    C1 = "".join(c for i in sorted(cols) for _, c in sorted(cols[i]))
    C2 = "".join(c for i in sorted(cols) for _, c in sorted(cols[i], reverse=True))
    return {"R1": R1, "R2": R2, "C1": C1, "C2": C2}
ALPH = []
for lay in NAMES:
    for k, a in alphabets(lay).items():
        assert sorted(a) == [chr(65 + i) for i in range(26)], (lay, k, a)
        ALPH.append((lay + "-" + k, a))
ALPH.append(("AZ", "ABCDEFGHIJKLMNOPQRSTUVWXYZ")); ALPH.append(("KA", "KRYPTOSABCDEFGHIJLMNQUVWXZ"))
if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "."
    with open(out + "/kb224.bin", "wb") as f:
        for _, a in ALPH: f.write(bytes(ord(c) - 65 for c in a))
    with open(out + "/kb224_names.txt", "w") as f:
        for n, a in ALPH: f.write(f"{n} {a}\n")
    with open(out + "/geo224.txt", "w") as f:  # line per layout: 26 x (row colA colB)
        for lay in NAMES:
            d = {}
            for ri, r in enumerate(L[lay]):
                for c, i in r: d[c] = (ri, i, i + 1 if ri == 2 else i)
            f.write(lay + " " + " ".join(f"{d[chr(65+x)][0]},{d[chr(65+x)][1]},{d[chr(65+x)][2]}" for x in range(26)) + "\n")
    for n, a in ALPH: print(n, a)
