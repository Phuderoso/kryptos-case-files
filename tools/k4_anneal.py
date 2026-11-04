"""Cycle 4: simulated annealing over rule-built transpositions (double columnar, Myszkowski) combined with periodic
substitution (Vigenere, AZ/KA alphabets). Score = English quadgram fitness of the decrypt - 40 * crib conflicts.
Key letters at crib-constrained residues are FORCED by the cribs (majority); free residues take the best monogram fit.
Usage: python3 tools/k4_anneal.py [--control] ; needs data/quadgrams.json (tools/build_quadgrams.py)."""
import zlib, json, math, random, sys, itertools
from multiprocessing import Pool
sys.path.insert(0, "tools")
import kryptos_text
AZ = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"; KA = kryptos_text.KA
CRIBS = {22: "EAST", 26: "NORTHEAST", 64: "BERLIN", 70: "CLOCK"}
KN = {p - 1 + i: ch for p, w in CRIBS.items() for i, ch in enumerate(w)}
Q = json.load(open("data/quadgrams.json")); QF = Q["floor"]; QQ = Q["q"]
MONO = dict(zip(AZ, [math.log10(x/100) for x in [8.17,1.49,2.78,4.25,12.70,2.23,2.02,6.09,6.97,0.15,0.77,4.03,2.41,6.75,7.51,1.93,0.10,5.99,6.33,9.06,2.76,0.98,2.36,0.15,1.97,0.07]]))
N = 97
def quad(t): return sum(QQ.get(t[i:i+4], QF) for i in range(len(t) - 3))

def columnar(src_len, order):  # returns list: output position k <- source index
    w = len(order); out = []
    for c in sorted(range(w), key=lambda i: order[i]):
        out += [r * w + c for r in range((src_len + w - 1) // w) if r * w + c < src_len]
    return out
def myszkowski(src_len, key):  # key: list of ranks with ties
    w = len(key); out = []
    for rank in sorted(set(key)):
        cols = [i for i in range(w) if key[i] == rank]
        for r in range((src_len + w - 1) // w):
            out += [r * w + c for c in cols if r * w + c < src_len]
    return out
def build(family, keys):
    if family == "double":
        p1 = columnar(N, keys[0]); p2 = columnar(N, keys[1])
        return [p1[s] for s in p2]  # CT pos k <- PT index
    return myszkowski(N, keys[0])

def evaluate(CT, perm, alpha, P, model):
    # perm[k] = PT index at CT position k ; model B2: key index = k ; B1: key index = PT index
    ct_of = [0] * N
    for k, s in enumerate(perm): ct_of[s] = k
    votes = [dict() for _ in range(P)]
    for i, pt in KN.items():
        k = ct_of[i]; idx = (k if model == "B2" else i) % P
        kv = (alpha.index(CT[k]) - alpha.index(pt)) % 26
        votes[idx][kv] = votes[idx].get(kv, 0) + 1
    key = [None] * P; conflicts = 0
    for r in range(P):
        if votes[r]:
            kv, n = max(votes[r].items(), key=lambda x: x[1]); key[r] = kv; conflicts += sum(votes[r].values()) - n
    for r in range(P):
        if key[r] is None:
            ks = [k for k in range(N) if ((k if model == "B2" else perm[k]) % P) == r]
            key[r] = max(range(26), key=lambda kv: sum(MONO[alpha[(alpha.index(CT[k]) - kv) % 26]] for k in ks))
    pt = [""] * N
    for k in range(N):
        idx = (k if model == "B2" else perm[k]) % P
        pt[perm[k]] = alpha[(alpha.index(CT[k]) - key[idx]) % 26]
    pt = "".join(pt)
    return quad(pt) - 40 * conflicts, conflicts, pt, key

def mutate(family, keys, rng):
    keys = [list(k) for k in keys]; k = rng.choice(keys)
    if family == "myszkowski" and rng.random() < 0.5: k[rng.randrange(len(k))] = rng.randrange(len(k))
    else:
        a, b = rng.sample(range(len(k)), 2); k[a], k[b] = k[b], k[a]
    return keys

def anneal(args):
    CT, family, widths, an, P, model, seed, iters = args
    alpha = AZ if an == "AZ" else KA; rng = random.Random(seed)
    keys = [rng.sample(range(w), w) for w in widths]
    cur = evaluate(CT, build(family, keys), alpha, P, model); best = (cur, keys)
    T0 = 5.0
    for it in range(iters):
        T = T0 * (1 - it / iters) + 0.05
        nk = mutate(family, keys, rng); r = evaluate(CT, build(family, nk), alpha, P, model)
        if r[0] > cur[0] or rng.random() < math.exp((r[0] - cur[0]) / T):
            keys, cur = nk, r
            if cur[0] > best[0][0]: best = (cur, [list(k) for k in keys])
    (sc, conf, pt, key), bk = best
    return dict(family=family, widths=widths, alpha=an, P=P, model=model, score=round(sc, 1), conflicts=conf,
                per_quad=round((sc + 40*conf) / (N - 3), 3), keys=bk, key="".join(alpha[k] for k in key), pt=pt)

def jobs(CT, iters, restarts):
    J = []
    for w1, w2 in itertools.product(range(5, 10), repeat=2):
        for an in ("AZ", "KA"):
            for P in range(1, 8):
                for model in ("B1", "B2"):
                    for s in range(restarts): J.append((CT, "double", (w1, w2), an, P, model, zlib.crc32(repr((w1,w2,an,P,model,s)).encode()), iters))
    for w in range(5, 13):
        for an in ("AZ", "KA"):
            for P in range(1, 8):
                for model in ("B1", "B2"):
                    for s in range(restarts): J.append((CT, "myszkowski", (w,), an, P, model, zlib.crc32(repr((w,an,P,model,s)).encode()), iters))
    return J

if __name__ == "__main__":
    control = "--control" in sys.argv
    if control:
        # Planted: English plaintext containing the cribs at the official positions, double columnar (6,8) + KA Vigenere 'CLOCK' (P=5, B2)
        eng = ("THEMESSAGEWASDELIVEREDATDAWNTOTHEEASTNORTHEASTCORNEROFTHESQUAREWHEREWEMETUNDERTHEBERLINCLOCKANDWAITEDFORTHESIGNALTOMOVEON")
        pt = list(eng[:97]); 
        for i, ch in KN.items(): pt[i] = ch
        pt = "".join(pt); o1, o2 = [3,0,5,1,4,2], [6,2,7,0,3,5,1,4]
        perm = build("double", [o1, o2]); key = "CLOCK"
        CT = "".join(KA[(KA.index(pt[perm[k]]) + KA.index(key[k % 5])) % 26] for k in range(N))
        J = [(CT, "double", (6, 8), "KA", 5, "B2", s, 20000) for s in range(16)]
        print("CONTROL plaintext:", pt); print("CONTROL ciphertext:", CT)
        print(f"English quad/char reference (control PT): {quad(pt)/(N-3):.3f}")
    else:
        CT = kryptos_text.K4; J = jobs(CT, int(sys.argv[1]) if len(sys.argv) > 1 else 20000, 4)
    with Pool() as pool: R = pool.map(anneal, J, chunksize=4)
    R.sort(key=lambda r: -r["score"])
    print(f"runs: {len(R)}")
    rnd = random.Random(0); base = []
    for _ in range(2000):
        s = "".join(rnd.choice(AZ) for _ in range(97)); base.append(quad(s)/(N-3))
    base.sort(); print(f"random-text quad/char: median {base[1000]:.3f}, max of 2000 {base[-1]:.3f}")
    for r in R[:25]: print(json.dumps(r))
    zc = [r for r in R if r["conflicts"] == 0]
    print(f"runs reaching 0 crib conflicts: {len(zc)}; best such per_quad: {max([r['per_quad'] for r in zc], default=None)}")
