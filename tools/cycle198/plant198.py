"""Cycle 198 planted controls (pre-registered in PREREG198.md): case 184-style plants (two keys + one dropped/extra letter) with ONE
WRONG crib letter: the carved letter of a 2-core crib slot is replaced by a different random letter (independent of cmp198).
Writes ctl198.txt: name ct src N kind d q model solver ab form m n keys wrongslots plaintext"""
import random, sys
from lib198 import *
FILL = ("THEQUIETROOMHELDASINGLELAMPANDTHEMAPWASFOLDEDTWICEWHENTHEMESSAGECAMEWESTOODBYTHEWINDOWANDWAITEDFORTHESIGNAL"
        "UNDERTHEOLDBRIDGETHECOURIERLEFTAPACKAGEANDWALKEDAWAYSLOWLYTOWARDTHESTATIONBEFOREDAWN")
sup = sys.argv[1]
def kv(word, alph): return [alph.index(ch) for ch in word]
def R2kp(kind, d):
    if kind == "del": return [j if j < d else j + 1 for j in CI]
    return [j if j < d else (0 if j == d else j - 1) for j in CI]
def make(N, kind, d, out, model, solver, ab, form, wa, wb, rng, kpos, extra=None):
    P = list(FILL[:N])
    for t, k in enumerate(kpos):
        if not (kpos is not CI and kind == "ins" and CI[t] == d): P[k] = PTC[t]
    m, n = len(wa), len(wb)
    if solver == "A": alph = AZ if ab == "AZ" else KA; a, b = kv(wa, alph), kv(wb, alph)
    else: T1, T2 = TABS[ab]; a, b = kv(wa, T1), kv(wb, T2)
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
    return carved, "".join(P)
rng = random.Random(198)
rows = [  # name N kind d src q model solver ab form wa wb nwrong extra
 ("P1e", 98, "del", 50, "direct", 0, "D", "A", "KA", "vig", "ABSCISSA", "PALIMPSEST", 1, None),
 ("P1b", 98, "del", 50, "direct", 0, "D", "A", "KA", "vig", "ABSCISSA", "PALIMPSEST", -1, None),
 ("P2e", 96, "ins", 30, "directR2", 0, "D", "A", "AZ", "beau", "BERLIN", "KRYPTOS", 1, None),
 ("P3e", 96, "ins", 5, "direct", 0, "D", "B", "AZ>KA", "VV", "CLOCK", "NORTHEAST", 1, None),
 ("P4e", 98, "del", 70, "directR2", 0, "D", "B", "KA>AZ", "BV", "ABSCISSA", "PALIMPSEST", 1, None),
 ("P7e", 98, "del", 60, "decM98_s8", 300, "C", "B", "AZ>KA", "VB", "TIME", "KRYPTOS", 1, None),
 ("P8e", 96, "ins", 10, "decM96_s8", 200, "P", "B", "KA>AZ", "VV", "SHADOW", "LIGHT", 1, None),
 ("P10e", 98, "del", 30, "decM98_s8", 100, "P", "A", "KA", "vig", "ABSCISSA", "PALIMPSEST", 1, None),
 ("P11e", 96, "ins", 20, "decM96_s8", 50, "C", "A", "AZ", "beau", "CLOCK", "BERLIN", 1, None),
 ("P1s", 98, "del", 50, "direct", 0, "D", "A", "KA", "vig", "ABSCISSA", "PALIMPSEST", 0, None),
 ("N3", 98, "del", 50, "direct", 0, "D", "A", "KA", "vig", "ABSCISSA", "PALIMPSEST", 2, None),
 ("N4", 98, "del", 60, "decM98_s8", 300, "C", "B", "AZ>KA", "VB", "TIME", "KRYPTOS", 2, None),
 ("N1", 98, "del", 50, "direct", 0, "D", "A", "KA", "vig", "CLOCK", "KRYPTOS", 0, "BERLINCLOCK"),
]
with open("ctl198.txt", "w") as f:
    for (nm, N, kind, d, src, q, model, solver, ab, form, wa, wb, nw, ex) in rows:
        if src.startswith("direct"):
            out = list(range(N)); kpos = R2kp(kind, d) if src == "directR2" else CI
            cv = [(-1 if (kind == "ins" and j == d) else j) for j in CI] if src == "directR2" else [carved_of(i, kind, d) for i in CI]
            rec = [list(kpos), list(kpos), cv]
        else:
            out = load_perm(f"{sup}/{src}.bin", N, q); kpos = CI; rec = perm_record(out, kind, d)
        carved, P = make(N, kind, d, out, model, solver, ab, form, wa, wb, rng, kpos, kv(ex, KA) if ex else None)
        E = edges_of(rec, model, len(wa), len(wb)); c = sorted(core(E))
        wrong = []
        def exc(Em):
            vs = {x for e in Em.values() for x in e}; par = {x: x for x in vs}
            def f(x):
                while par[x] != x: x = par[x]
                return x
            k = 0
            for (u, v) in Em.values():
                a, b = f(u), f(v)
                if a != b: par[a] = b; k += 1
            return len(Em) - k
        # one-tableau (additive) case: a bridge never constrains, so a wrong letter there is invisible; P*e plants use a cycle slot,
        # P1b deliberately uses a bridge (documented as undetectable: found as a strict fit, wrong at one carved position)
        cyc = [t for t in c if exc({u: E[u] for u in c if u != t}) < exc({u: E[u] for u in c})]
        brg = [t for t in c if t not in cyc]
        if nw == -1: wrong = [rng.choice(brg)]
        elif nw:
            if nw == 1: wrong = [rng.choice(cyc if solver == "A" else c)]
            else:  # two wrong letters in the core, chosen so that neither single deletion leaves a consistent core: different slots
                wrong = rng.sample(c, 2)
        for t in wrong:
            j = rec[2][t]; old = carved[j]; carved[j] = rng.choice([x for x in AZ if x != old])
        f.write(" ".join(map(str, [nm, "".join(carved), src, N, kind, d, q, model, solver, ab, form, len(wa), len(wb),
                 wa + "+" + wb + ("+" + ex if ex else ""), ",".join(map(str, wrong)) or "-", P])) + "\n")
print(open("ctl198.txt").read())
