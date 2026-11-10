"""Cycle 195 (IDEAS I-209): keyword-columnar permutation banks for the sandwich solver (cmp193, unchanged core).
Convention as all.bin: perm[j] = carved position holding plaintext letter j (int16, 97 per row). Column orders = case 50's
data/cycle52/orders.txt (1,837 distinct orders, widths 4-14; word, width, read sequence of column indices; tools/dcol.c col()).
col1.bin : every single keyed columnar, perm and its inverse (the decryption-direction transposition), duplicates merged.
col2.bin : double keyed columnar over the THEMED words only (dcol_gen.py THEMED list, lengths 4-14), ordered pairs incl. the same word
           twice (K3-style double transposition), perm and inverse, duplicates merged and rows already in col1 dropped.
Rows that also occur in all.bin (165,782 K3-law routes) are reported (overlap) and kept; index files list the label of each row.
usage: gen195.py orders52.txt all.bin outdir"""
import sys, numpy as np
THEMED = """KRYPTOS PALIMPSEST ABSCISSA BERLIN CLOCK BERLINCLOCK EASTNORTHEAST NORTHEAST SHADOW SHADOWFORCES LAYER
LAYERTWO UNDERGROUND IDBYROWS INVISIBLE MAGNETIC LODESTONE TUTANKHAMEN CARTER HOWARDCARTER CANDLE SLOWLY
DESPARATLY CHAMBER TOMB EGYPT LANGLEY SANBORN SCHEIDT WEBSTER ILLUSION IQLUSION NUANCE DIGETAL VIRTUALLY
TRANSPOSE TRANSPOSITION COLUMN COLUMNAR DOUBLE GRID MATRIX SQUARE TABLEAU VIGENERE QUAGMIRE KEYWORD CIPHER
COMPASS LATITUDE LONGITUDE MERIDIAN WELTZEITUHR URANIA ALEXANDERPLATZ WALL DELIVERING MESSAGE POSITION
SECRET HIDDEN BURIED LOCATION COORDINATES WHATSTHEPOINT POINT ANTIPODES MORSE OBELISK PETRIFIED QUARTZ
COPPER SCULPTURE AGENCY CENTRAL INTELLIGENCE TRUTH FREEDOM VERDIGRIS WHIRLPOOL SHELL STONE LIGHT DARKNESS
NORTH SOUTH EAST WEST BERLINWALL CHECKPOINT CHARLIE SPY DEADDROP REMINDER ENIGMA HIEROGLYPH ROSETTA""".split()
N = 97
def col(o):
    w = len(o); rows = (N + w - 1) // w; P = [0] * N; k = 0
    for c in o:
        for r in range(rows):
            i = r * w + c
            if i < N: P[i] = k; k += 1
    return P
def inv(P):
    Q = [0] * N
    for i, j in enumerate(P): Q[j] = i
    return Q
orders = []
for l in open(sys.argv[1]):
    w = l.split(); orders.append((w[0], [int(x) for x in w[2:]]))
A = np.fromfile(sys.argv[2], dtype=np.int16).reshape(-1, N); aset = {r.tobytes(): q for q, r in enumerate(A)}
out = sys.argv[3]
def write(name, rows):
    seen = {}; 
    for lab, P in rows:
        b = np.array(P, dtype=np.int16).tobytes()
        if b not in seen: seen[b] = lab
    arr = np.frombuffer(b"".join(seen), dtype=np.int16).reshape(-1, N); arr.tofile(f"{out}/{name}.bin")
    ov = [lab for b, lab in seen.items() if b in aset]
    with open(f"{out}/{name}_index.txt", "w") as f:
        for q, (b, lab) in enumerate(seen.items()): f.write(f"{q} {lab}{' ALL.BIN=' + str(aset[b]) if b in aset else ''}\n")
    print(f"{name}: {len(rows)} generated, {len(seen)} distinct, {len(ov)} also in all.bin")
    return set(seen)
rows1 = []
for w, o in orders:
    P = col(o); assert sorted(P) == list(range(N))
    rows1.append((f"{w}/enc", P)); rows1.append((f"{w}/inv", inv(P)))
s1 = write("col1", rows1)
th = [(w, o) for w, o in orders if w in THEMED]
rows2 = []
for w1, o1 in th:
    P1 = col(o1)
    for w2, o2 in th:
        P2 = col(o2); P = [P2[P1[i]] for i in range(N)]
        for lab, Q in ((f"{w1}+{w2}/enc", P), (f"{w1}+{w2}/inv", inv(P))):
            if np.array(Q, dtype=np.int16).tobytes() not in s1: rows2.append((lab, Q))
write("col2", rows2)
print("themed orders", len(th))
