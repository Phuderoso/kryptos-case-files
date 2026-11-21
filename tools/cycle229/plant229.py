"""Cycle 229 (PREREG229, I-335 audit) low-n plant ladder + fresh shuffled-K4 nulls.
Plants: 24 Q-model plaintexts (kb227 conventions: c = Y[X(p)+k] form 0, Y[X(p)-k] form 1, Y[k-X(p)] form 2; X, Y rows of kb227.bin,
pairs with both in {AZ, KA} skipped), carved index (ix = 1), behind bank.bin (even pid) or all.bin (odd pid... see SCOPE), p 19-24,
dir 0/1. Target n (non-crib quadgrams of the kb227 decrypt of the TRUE configuration, tie = '?') = 10 + pid // 4 (n 10-15, four
plants per n); pid % 2 == 1 -> one carved crib letter replaced by a different random letter (one-error plant). Rows / keys are
redrawn (rejection sampling, same RNG stream) until known >= 49 and n == target. Plaintext: K1-K3 English (pid % 4 in {0, 1}) or
Jane Eyre body (pid % 4 in {2, 3}), cribs written in. The predicted (known, n, NC) come from an independent Python reimplementation
of kb227's decrypt; kb229's own P / Y lines are the measured values.
usage: plant229.py WORKDIR SEED > plants229.tsv ;  plant229.py --nulls k4.txt FIRST COUNT > nulls229.tsv"""
import sys, random, numpy as np
N = 97; POS = list(range(21, 34)) + list(range(63, 74)); CRIB = "EASTNORTHEAST" + "BERLINCLOCK"; CRSET = set(POS)
def decrypt_q(C, S, p, x, y, f, kb, AI):
    """kb227 score_hit for model Q, ix = 1, tie = '?'. C = carved letters (ints), S = layer->carved map."""
    t = [S[i] for i in POS]; v = []
    for j, i in enumerate(POS):
        yv = int(AI[y, C[S[i]]]); xv = int(AI[x, ord(CRIB[j]) - 65])
        v.append((yv - xv) % 26 if f == 0 else (xv - yv) % 26 if f == 1 else (xv + yv) % 26)
    kv = [-1] * p; kc = [0] * p; tie = [0] * p
    for j in range(24):
        r = t[j] % p; m = sum(1 for b in range(24) if t[b] % p == r and v[b] == v[j])
        if m > kc[r]: kc[r], kv[r], tie[r] = m, v[j], 0
        elif m == kc[r] and v[j] != kv[r]: tie[r] = 1
    for r in range(p):
        if tie[r]: kv[r] = -1
    out = []
    for i in range(N):
        r = S[i] % p
        if kv[r] < 0: out.append("?"); continue
        yv = int(AI[y, C[S[i]]]); k = kv[r]; xv = (yv - k) % 26 if f == 0 else (yv + k) % 26 if f == 1 else (k - yv) % 26
        out.append(chr(65 + int(kb[x, xv])))
    return "".join(out)
def nc(P, qg):
    q = [float(qg[((ord(P[i])-65)*26 + ord(P[i+1])-65)*676 + (ord(P[i+2])-65)*26 + ord(P[i+3])-65]) for i in range(N - 3)
         if "?" not in P[i:i+4] and not (CRSET & {i, i+1, i+2, i+3})]
    return (sum(q) / len(q) if q else float("nan")), len(q)
def main():
    if sys.argv[1] == "--nulls":
        K4 = open(sys.argv[2]).read().strip(); a, n = int(sys.argv[3]), int(sys.argv[4]); print("seed\tct")
        for s in range(a, a + n):
            l = list(K4); random.Random(s).shuffle(l); print(f"{s}\t{''.join(l)}")
        return
    W, SEED = sys.argv[1], int(sys.argv[2])
    txt = "".join(c for c in open(W + "/k123_eng.txt").read().upper() if c.isalpha())
    je = open(W + "/rk_plain.txt", errors="ignore").read(); je = je[je.index("CHAPTER I"):je.index("END OF THE PROJECT GUTENBERG")]
    je = "".join(c for c in je.upper() if "A" <= c <= "Z")
    kb = np.fromfile(W + "/kb227.bin", dtype=np.uint8).reshape(-1, 26); nA = len(kb); AZ, KA = nA - 2, nA - 1
    AI = np.zeros_like(kb)
    for a in range(nA):
        for i in range(26): AI[a, kb[a, i]] = i
    qg = np.fromfile(W + "/qg.bin", dtype=np.float32)
    banks = {"bank": np.fromfile(W + "/bank.bin", dtype=np.int16).reshape(-1, N), "all": np.fromfile(W + "/all.bin", dtype=np.int16).reshape(-1, N)}
    R = random.Random(SEED)
    print("pid\tscope\trow\tdir\tp\tX\tY\tform\tbad\ttries\tknown_pred\tn_pred\tnc_pred\tct\tpt\tdec_pred")
    for pid in range(24):
        target = 10 + pid // 4; scope = "bank" if (pid // 2) % 2 == 0 else "all"; src = txt if pid % 4 < 2 else je
        tries = 0
        while True:
            tries += 1
            s0 = R.randrange(len(src) - N); pt = list(src[s0:s0 + N])
            for j, i in enumerate(POS): pt[i] = CRIB[j]
            P = [ord(c) - 65 for c in pt]
            row = R.randrange(len(banks[scope])); d = R.randrange(2); perm = [int(v) for v in banks[scope][row]]
            inv = [0] * N
            for i, v in enumerate(perm): inv[v] = i
            S = perm if d == 0 else inv
            while True:
                x, y = R.randrange(nA), R.randrange(nA)
                if not ((x in (AZ, KA)) and (y in (AZ, KA))): break
            f, p = R.randrange(3), R.randrange(19, 25); key = [R.randrange(26) for _ in range(p)]
            layer = [0] * N
            for i in range(N):
                xv, k = int(AI[x, P[i]]), key[S[i] % p]
                layer[i] = int(kb[y, (xv + k) % 26 if f == 0 else (xv - k) % 26 if f == 1 else (k - xv) % 26])
            C = [0] * N
            for i in range(N): C[S[i]] = layer[i]
            bad = -1
            if pid % 2 == 1:
                bad = R.randrange(24); c = S[POS[bad]]; C[c] = R.choice([v for v in range(26) if v != C[c]])
            dec = decrypt_q(C, S, p, x, y, f, kb, AI); known = N - dec.count("?"); sc, nq = nc(dec, qg)
            if known >= 49 and nq == target: break
        ct = "".join(chr(65 + v) for v in C)
        print(f"{pid}\t{scope}\t{row}\t{d}\t{p}\t{x}\t{y}\t{f}\t{bad}\t{tries}\t{known}\t{nq}\t{sc:.3f}\t{ct}\t{''.join(pt)}\t{dec}")
if __name__ == "__main__": main()
