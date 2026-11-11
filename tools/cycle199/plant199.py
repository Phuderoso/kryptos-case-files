"""Cycle 199 controls (I-220 chunk 1): case 184's P7/P8 re-planted on NON-M = N perms inside the registered chunk, plus two
negatives (two crib-position letters corrupted in each plant: must NOT fit at the planted record). Encryption = plant197 make() (lib197)."""

import random, sys
from lib197 import *
FILL = ("THEQUIETROOMHELDASINGLELAMPANDTHEMAPWASFOLDEDTWICEWHENTHEMESSAGECAMEWESTOODBYTHEWINDOWANDWAITEDFORTHESIGNAL"
        "UNDERTHEOLDBRIDGETHECOURIERLEFTAPACKAGEANDWALKEDAWAYSLOWLYTOWARDTHESTATIONBEFOREDAWN")
sup = sys.argv[1] if len(sys.argv) > 1 else "../../../sup"
def kv(word, alph): return [alph.index(ch) for ch in word]
def make(name, N, kind, d, out, model, solver, ab, form, wa, wb, rng, kpos=None, extra=None):
    P = list(FILL[:N]); kpos = kpos or CI
    for t, k in enumerate(kpos):
        if not (kpos is not CI and kind == "ins" and CI[t] == d): P[k] = PTC[t]
    m, n = len(wa), len(wb)
    if solver == "A":
        alph = AZ if ab == "AZ" else KA; a, b = kv(wa, alph), kv(wb, alph)
    else:
        T1, T2 = TABS[ab]; a, b = kv(wa, T1), kv(wb, T2)
    C = [None] * N
    for k in range(N):
        i = k if model in "PD" else out[k]
        if solver == "A":
            K = (a[i % m] + b[i % n]) % 26
            if extra: K = (K + extra[i % len(extra)]) % 26
            C[out[k]] = enc_add(form, alph, P[k], K)
        else: C[out[k]] = enc_two(ab, form, P[k], a[i % m], b[i % n])
    if kind == "del": carved = C[:d] + C[d + 1:]
    elif kind == "ins": carved = C[:d] + [rng.choice(AZ)] + C[d:]
    else: carved = C
    assert len(carved) == 97
    return "".join(carved), "".join(P)

rng = random.Random(199)
rows = [("P7n", 98, "del", 60, "dec98", 10000, "C", "B", "AZ>KA", "VB", "TIME", "KRYPTOS"),
        ("P8n", 96, "ins", 10, "dec96", 20000, "P", "B", "KA>AZ", "VV", "SHADOW", "LIGHT"),
        ("P9n", 98, "del", 33, "dec98", 27000, "P", "B", "KA>AZ", "BB", "ABSCISSA", "CLOCK")]
with open("ctl199.txt", "w") as f:
    for (nm, N, kind, d, src, q, model, solver, ab, form, wa, wb) in rows:
        out = load_perm(f"{sup}/{src}.bin", N, q)
        ctx, P = make(nm, N, kind, d, out, model, solver, ab, form, wa, wb, rng)
        f.write(" ".join(map(str, [nm, ctx, src, N, kind, d, q, model, solver, ab, form, len(wa), len(wb), wa + "+" + wb, P])) + "\n")
        # negative: corrupt carved letters at two crib positions' carved slots (pick crib plaintext idx 25 and 66 -> their carved slot)
        c = list(ctx)
        for t in (4, 17):
            k = CI[t]; cidx = out[k]
            j = carved_of(cidx, kind, d)
            if j >= 0: c[j] = AZ[(AZ.index(c[j]) + 7) % 26]
        f.write(" ".join(map(str, ["N" + nm[1:], "".join(c), src, N, kind, d, q, model, solver, ab, form, len(wa), len(wb), wa + "+" + wb, "NEG"])) + "\n")
print(open("ctl199.txt").read())
