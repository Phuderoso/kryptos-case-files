"""Cycle 169 one-error planted controls, built on cycle 168's 12 string-level planted controls (ctl168/).
  e0..e11  : exactly one error at a crib position. Even i: wrong CARVED letter (random other letter at the carved
             position that holds a crib letter). Odd i: wrong CRIB (plaintext letter at a crib position changed,
             then re-encrypted with the planted key) -> expect FIT23 with miss = that crib index, no FULL.
  n0..n1   : one wrong carved letter at a NON-crib position -> expect FULL (strict fit unaffected).
  d0..d3   : two errors at two crib positions -> the planted config must NOT appear (tolerance is exactly one).
usage: ctl169.py all.bin texts.txt ctl168_dir SEED   (writes ctl169/*.txt, *_slice.bin links, ctl169/planted.txt)"""
import sys, os, re, random, numpy as np
KA = "KRYPTOSABCDEFGHIJLMNQUVWXZ"; AZ = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
P = np.fromfile(sys.argv[1], dtype=np.int16).reshape(-1, 97)
T = dict(l.split() for l in open(sys.argv[2])); D = sys.argv[3]; rnd = random.Random(int(sys.argv[4]))
CP = list(range(21, 34)) + list(range(63, 74))
def enc(p, k, md):
    ty, ap, ac, ak = md % 3, (md // 3) & 1, (md // 6) & 1, (md // 12) & 1
    kv = KA.index(k) if ak else ord(k) - 65; pp = KA.index(p) if ap else ord(p) - 65
    c = (pp + kv) % 26 if ty == 0 else (kv - pp) % 26 if ty == 1 else (pp - kv) % 26
    return KA[c] if ac else AZ[c]
os.makedirs("ctl169", exist_ok=True); out = []
for line in open(f"{D}/controls_planted.txt"):
    m = re.match(r"ctl(\d+): perm (\d+) \(slice index (\d+)\) model (\w) mode (\d+) text (\S+) offset (\d+) pt (\w+)", line)
    i, j, si, model, md, name, o, pt = int(m[1]), int(m[2]), int(m[3]), m[4], int(m[5]), m[6], int(m[7]), m[8]
    perm = P[j]; inv = np.argsort(perm); t = T[name]; car = open(f"{D}/ctl{i}.txt").read().strip()
    cpos = lambda c: int(perm[c]) if model == "A" else int(inv[c])          # carved position holding plaintext c
    kidx = lambda c: o + (c if model == "A" else int(inv[c]))                # key index used for plaintext c
    def put(name_, c_):
        open(f"ctl169/{name_}.txt", "w").write(c_ + "\n")
        if not os.path.exists(f"ctl169/{name_}_slice.bin"): os.symlink(os.path.abspath(f"{D}/ctl{i}_slice.bin"), f"ctl169/{name_}_slice.bin")
    # e_i: one error at a crib position
    jj = rnd.randrange(24); c = CP[jj]; L = list(car)
    if i % 2 == 0:
        L[cpos(c)] = rnd.choice([x for x in AZ if x != car[cpos(c)]]); kind = "carved"
    else:
        newp = rnd.choice([x for x in AZ if x != pt[c]]); L[cpos(c)] = enc(newp, t[kidx(c)], md); kind = f"crib({pt[c]}->{newp})"
    put(f"e{i}", "".join(L)); out.append(f"e{i}: perm {j} slice {si} model {model} mode {md} text {name} offset {o} error {kind} crib_index {jj} carved_pos {cpos(c)} expect FIT23 miss={jj}")
    if i < 2:   # n_i: error at a non-crib position
        x = rnd.choice([x for x in range(97) if x not in {cpos(c) for c in CP}]); L = list(car); L[x] = rnd.choice([y for y in AZ if y != car[x]])
        put(f"n{i}", "".join(L)); out.append(f"n{i}: perm {j} slice {si} model {model} mode {md} text {name} offset {o} error carved non-crib pos {x} expect FULL")
    if i < 4:   # d_i: two crib-position errors
        a, b = rnd.sample(range(24), 2); L = list(car)
        for jj2 in (a, b): q = cpos(CP[jj2]); L[q] = rnd.choice([y for y in AZ if y != car[q]])
        put(f"d{i}", "".join(L)); out.append(f"d{i}: perm {j} slice {si} model {model} mode {md} text {name} offset {o} errors crib_index {a},{b} expect planted config ABSENT")
open("ctl169/planted.txt", "w").write("\n".join(out) + "\n"); print("\n".join(out))
