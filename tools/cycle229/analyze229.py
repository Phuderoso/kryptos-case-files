"""Cycle 229 analysis (PREREG229). usage: analyze229.py WORKDIR PUBLISHED_R227_DIR > analyze229.log ; writes WORKDIR/summary229.json
Part A (I-335): floors F in {10, 11, 12} for the I-330 bar (known >= 49, NC >= -6.0, nq >= F); null passes per distinct decrypt
text and per null text (Wilson 95 %); Y tables (count / pass / max NC by nq) for nulls and K4; low-n plant ladder; published case 213
record; the pre-registered decision rule. Part B (I-337): full-scale V counts behind bank / all.bin, K4 vs 16 fresh nulls."""
import sys, os, re, json, glob, math, collections
W, PUB = sys.argv[1], sys.argv[2]; R = W + "/R"; FLOORS = (10, 11, 12)
def wilson(k, n, z=1.959964):
    if n == 0: return (float("nan"), float("nan"))
    ph = k/n; d = 1 + z*z/n; c = (ph + z*z/(2*n))/d; hw = z*math.sqrt(ph*(1-ph)/n + z*z/(4*n*n))/d
    return (round(max(0.0, c-hw), 3), round(min(1.0, c+hw), 3))
PRE = re.compile(r"^P (\S) (.*?) p=(\d+) known=(\d+) nqnc=(\d+) nc=(\S+) qg=\S+ pt=(\S+)")
YRE = re.compile(r"^Y model=(\S) p=(\d+) nq=(\d+) n=(\d+) pass=(\d+) max=(\S+)")
SRE = re.compile(r"^S V p=(\d+) hits=(\d+) exact=(\d+) prim=(\d+)")
def P_lines(fn):
    out = []
    for l in open(fn):
        m = PRE.match(l)
        if m: out.append(dict(model=m[1], cfg=m[2], p=int(m[3]), known=int(m[4]), nq=int(m[5]), nc=float(m[6]), pt=m[7]))
    return out
def Y_lines(fn):
    return [(m[1], int(m[2]), int(m[3]), int(m[4]), int(m[5]), float(m[6])) for m in map(YRE.match, open(fn)) if m]
def complete(fn): return any(l.startswith("T rows=") for l in open(fn))
seeds = [l.split()[0] for l in open(W + "/nulls229.tsv").read().splitlines()[1:]]
labels = ["k4"] + ["null" + s for s in seeds]
FILES = ["direct_a", "direct_b", "bank_Q_r10", "all_Q_r10", "bank_V_a", "bank_V_b", "all_V_a", "all_V_b"]
S = {"floors": FLOORS}
# completeness
inc = [f"{lb}_{f}" for lb in labels for f in FILES if not (os.path.exists(f"{R}/{lb}_{f}.txt") and complete(f"{R}/{lb}_{f}.txt"))]
print("incomplete files:", inc or "none"); S["incomplete"] = inc
# ---- Part A: passes per floor
def floor_table(lbls):
    res = {}
    for F in FLOORS:
        hits = 0; texts = set(); nulls_with = set(); best = None
        for lb in lbls:
            for f in FILES:
                fn = f"{R}/{lb}_{f}.txt"
                if not os.path.exists(fn): continue
                for h in P_lines(fn):
                    if h["nq"] >= F and h["known"] >= 49 and h["nc"] >= -6.0:
                        hits += 1; texts.add((lb, h["pt"])); nulls_with.add(lb)
                        if best is None or h["nc"] > best[0]: best = (h["nc"], lb, f, h["cfg"], h["p"], h["nq"], h["pt"])
        res[F] = dict(hits=hits, distinct_texts=len(texts), texts_with_pass=len(nulls_with), best=best,
                      wilson_texts=wilson(len(nulls_with), len(lbls)), which=sorted(nulls_with))
    return res
nulls = labels[1:]
S["null_floor"] = floor_table(nulls); S["k4_floor"] = floor_table(["k4"])
print("\n== Part A: I-330 bar passes by floor (fresh nulls 209559-209574, 16 texts) ==")
for F in FLOORS:
    a, k = S["null_floor"][F], S["k4_floor"][F]
    print(f"floor nq>={F}: nulls hits {a['hits']}, distinct texts {a['distinct_texts']}, null texts with a pass {a['texts_with_pass']}/16 "
          f"Wilson {a['wilson_texts']} best {a['best'][:6] if a['best'] else None} | K4 hits {k['hits']}")
    if a["best"]: print("   best null pt:", a["best"][6])
# ---- Y tables
def ytab(lbls, files):
    T = collections.defaultdict(lambda: [0, 0, -99.0])
    for lb in lbls:
        for f in files:
            fn = f"{R}/{lb}_{f}.txt"
            if not os.path.exists(fn): continue
            for (m, p, q, n, ps, mx) in Y_lines(fn):
                t = T[q]; t[0] += n; t[1] += ps; t[2] = max(t[2], mx)
    return T
YN, YK = ytab(nulls, FILES), ytab(["k4"], FILES)
S["null_by_nq"] = {q: YN[q] for q in sorted(YN)}; S["k4_by_nq"] = {q: YK[q] for q in sorted(YK)}
print("\n== Null / K4 decrypts by number of non-crib quadgrams (known >= 49; all cells pooled) ==")
print("nq | null decrypts | null NC>=-6 | null max NC | K4 decrypts | K4 max NC")
for q in range(1, 41):
    a = YN.get(q, [0, 0, None]); b = YK.get(q, [0, 0, None])
    if a[0] or b[0]: print(f"{q:2d} | {a[0]:8d} | {a[1]:4d} | {a[2] if a[0] else '—'} | {b[0]:7d} | {b[2] if b[0] else '—'}")
hi = [(q, v) for q, v in YN.items() if q > 40]
print(f"nq > 40: null decrypts {sum(v[0] for q, v in hi)}, passes {sum(v[1] for q, v in hi)}, max {max([v[2] for q, v in hi], default=None)}")
# ---- published record (case 213, data/cycle227/R)
pub = collections.defaultdict(set)
for fn in glob.glob(PUB + "/null*.txt"):
    for h in P_lines(fn):
        for F in FLOORS:
            if h["nq"] >= F and h["known"] >= 49 and h["nc"] >= -6.0: pub[F].add((os.path.basename(fn).split("_")[0], h["pt"]))
S["published_case213"] = {F: len(pub[F]) for F in FLOORS}
print("\n== Published record, case 213 null P lines: distinct null texts passing:", S["published_case213"])
# ---- plants
rows = [l.split("\t") for l in open(W + "/plants229.tsv").read().splitlines()]
hd = rows[0]; plants = [dict(zip(hd, r)) for r in rows[1:]]
print("\n== Low-n plant ladder (seed 209558) ==")
PL = []
for pl in plants:
    fn = f"{R}/plant_{pl['pid']}.txt"; L = open(fn).read().splitlines()
    key = f"perm={pl['row']} dir={pl['dir']} ix=1 X={pl['X']} Y={pl['Y']} form={pl['form']}"
    hit = any(l.startswith(f"H Q {key} p={pl['p']} ") for l in L)
    P = [h for h in P_lines(fn) if h["cfg"] == "Q " + key and h["p"] == int(pl["p"])] if False else \
        [h for h in P_lines(fn) if h["cfg"].endswith(key) and h["p"] == int(pl["p"])]
    m = P[0] if P else None
    agree = (m is not None and m["nq"] == int(pl["n_pred"]) and m["known"] == int(pl["known_pred"]) and abs(m["nc"] - float(pl["nc_pred"])) < 0.0015 and m["pt"] == pl["dec_pred"])
    r = dict(pid=int(pl["pid"]), scope=pl["scope"], p=int(pl["p"]), bad=int(pl["bad"]), n_pred=int(pl["n_pred"]), known_pred=int(pl["known_pred"]),
             nc_pred=float(pl["nc_pred"]), recovered=hit, P=bool(m), nq=m["nq"] if m else None, nc=m["nc"] if m else None, agree=agree)
    PL.append(r)
    print(f"plant {r['pid']:2d} {r['scope']:4s} p {r['p']} bad {r['bad']:3d} pred known {r['known_pred']} n {r['n_pred']} NC {r['nc_pred']:.3f} | "
          f"H hit {hit} P {bool(m)} nq {r['nq']} NC {r['nc']} agree {agree}")
S["plants"] = PL
n_rec = sum(r["recovered"] for r in PL); n_bar = sum(r["P"] for r in PL)
S["gateP0"] = dict(recovered=n_rec, passed_bar_floor10=n_bar, n=len(PL), wilson=wilson(n_bar, len(PL)), PASS=n_bar >= len(PL) - 1 and n_rec >= len(PL) - 1)
print(f"Gate P0 (recovery + bar at floor 10): recovered {n_rec}/24, bar {n_bar}/24 Wilson {wilson(n_bar, 24)} -> {'PASS' if S['gateP0']['PASS'] else 'FAIL'}")
S["plant_floor"] = {}
for F in FLOORS:
    el = [r for r in PL if r["n_pred"] >= F]; ok = [r for r in el if r["P"] and r["nq"] >= F]
    lost = [r["pid"] for r in PL if r["P"] and r["nq"] < F]
    gate = len(ok) >= len(el) - 1
    S["plant_floor"][F] = dict(eligible=len(el), pass_=len(ok), wilson=wilson(len(ok), len(el)), lost_by_floor=lost, gate=gate,
                               ladder_pass=len(ok), ladder_wilson=wilson(len(ok), len(PL)))
    print(f"floor {F}: plants n>=F pass {len(ok)}/{len(el)} Wilson {wilson(len(ok), len(el))} gate {'PASS' if gate else 'FAIL'}; "
          f"whole ladder {len(ok)}/24 Wilson {wilson(len(ok), 24)}; lost to the floor: {lost}")
# ---- decision
dec = None
for F in (11, 12):
    nf = S["null_floor"][F]["distinct_texts"] == 0 and S["published_case213"][F] == 0
    if nf and S["plant_floor"][F]["gate"] and S["gateP0"]["PASS"]: dec = F; break
S["decision"] = dec
print("\n== Decision (pre-registered rule) ==",
      f"ADOPT floor nq >= {dec}" if dec else "NO ADOPTION: floor stays at 10 with the case 213 caveat; quadgram-count-dependent bar queued")
# ---- Part B
print("\n== Part B (I-337): full-scale V behind bank / all.bin, K4 vs 16 fresh nulls ==")
PB = {}
for f in ["bank_V_a", "bank_V_b", "all_V_a", "all_V_b"]:
    cnt = {}
    for lb in labels:
        c = {}
        for l in open(f"{R}/{lb}_{f}.txt"):
            m = SRE.match(l)
            if m: c[int(m[1])] = int(m[2])
        cnt[lb] = c
    for p in range(17, 25):
        k = cnt["k4"].get(p, 0); nv = [cnt[lb].get(p, 0) for lb in nulls]; occ = sum(v > 0 for v in nv)
        pup = (1 + sum(v >= k for v in nv)) / (1 + len(nv))
        if k == 0: lab = "EXACT-EXCL (discriminating)" if occ <= 2 else "EXACT-EXCL (non-discriminating)"
        else: lab = "K4 above nulls (read decrypts)" if pup <= 0.05 else "INSUFFICIENT-DISCRIMINATION"
        PB[f"{f} p{p}"] = dict(k4=k, nulls=nv, occupancy=occ, wilson=wilson(occ, 16), p_up=round(pup, 3), label=lab)
        print(f"{f:9s} p {p:2d}: K4 {k:5d} | nulls {nv} occ {occ}/16 Wilson {wilson(occ, 16)} p_up {pup:.3f} -> {lab}")
S["partB"] = PB
json.dump(S, open(W + "/summary229.json", "w"), indent=1, default=str)
