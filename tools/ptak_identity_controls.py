"""Cycle 23b: plaintext autokey applied directly (identity transposition), blind lags 24-96, English-scored.
Small search space (2 tableaux x 3 modes x 73 lags), so short fragments are not swamped by look-elsewhere."""
import random, subprocess
from kryptos_text import K4, KA
AZ = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
PTS = ["SLOWLYTHEREMAINSOFTHE" + "EASTNORTHEAST" + "PASSAGEWEREREMOVEDANDIHEARDTH" + "BERLINCLOCK" + "STRIKEATDUSKWHILEWEWAIT",
       "WEFOLLOWEDTHEOLDROADT" + "EASTNORTHEAST" + "UNTILTHESHADOWFELLACROSSTHEDO" + "BERLINCLOCK" + "ANDTHEVAULTOPENEDSLOWLY",
       "ITWASDARKINTHEROOMAND" + "EASTNORTHEAST" + "OFTHEDOORWAYSTOODANOLDBRASSDI" + "BERLINCLOCK" + "MARKINGTHEHOURFORTHEMEN"]
def ak(src, A, mode, L, rnd):
    prim = [rnd.randrange(26) for _ in range(L)]; out = []
    for i, ch in enumerate(src):
        p = A.index(ch); k = prim[i] if i < L else A.index(src[i - L])
        out.append(A[{0: p + k, 1: k - p, 2: p - k}[mode] % 26])
    return "".join(out)
def run(t, strict):
    return subprocess.run(["./ptak_score", t, "perm_identity.bin", "qg.bin", "4" if strict else "6", "24", "96", "5", str(strict)],
                          capture_output=True, text=True).stdout.splitlines()
out = []
for seed in range(1, 13):
    rnd = random.Random(500 + seed); L = rnd.randrange(24, 97); A = rnd.choice([KA, AZ]); mode = rnd.randrange(3)
    c = ak(PTS[seed % 3], A, mode, L, rnd)
    for strict in (1, 0):
        r = run(c, strict); body = r[1:]
        rank = next((i for i, l in enumerate(body, 1) if f" L={L} " in l and f"mode={mode} " in l and l.split()[2] == f"tab={'KA' if A == KA else 'AZ'}"), None)
        out.append(f"[control] L={L} tab={'KA' if A==KA else 'AZ'} mode={mode} [{'strict' if strict else 'loose'}] {r[0]}; rank={rank or '>5'}; best: {body[0] if body else 'none'}")
for s in range(1, 21):
    l = list(K4); random.Random(s).shuffle(l)
    for strict in (1, 0):
        r = run("".join(l), strict); out.append(f"[null s={s}] [{'strict' if strict else 'loose'}] {r[0]}; best: {r[1] if len(r)>1 else 'none'}")
for strict in (1, 0):
    r = run(K4, strict); out.append(f"[K4] [{'strict' if strict else 'loose'}] {r[0]}"); out += ["    " + x for x in r[1:]]
open("ptak_identity_report.txt", "w").write("\n".join(out) + "\n"); print("\n".join(out))
