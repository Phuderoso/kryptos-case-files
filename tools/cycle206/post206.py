#!/usr/bin/env python3
"""Cycle 206 Part A summary: K4 vs 20 full-bank shuffled nulls per L; read-out of K4 survivors at L 18-19
(letters decryptable without guessing word boundaries: the crib words' hidden starts, and continuations if the word goes on)."""
import sys, struct, json, glob, re
AZ = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"; KA = "KRYPTOSABCDEFGHIJLMNQUVWXZ"
OUT = sys.argv[1]; BANK = sys.argv[2]
K4 = open(__file__.rsplit('/', 3)[0] + "/data/k4.txt").read().split()[0].strip()
def hist(fn):
    h = {}
    for l in open(fn):
        if l.startswith("H "):
            _, tm, L, n = l.split(); tm, L, n = int(tm), int(L), int(n)
            h[L] = h.get(L, 0) + n * (2 if tm in (0, 2) else 1)    # variant counted like Vigenere (case 190 convention)
    return h
k4 = hist(f"{OUT}/k4_bank_L1-22.txt"); k4.update(hist(f"{OUT}/k4_bank_L23-26.txt"))
nulls = [hist(f) for f in sorted(glob.glob(f"{OUT}/null_*.txt"), key=lambda s: int(re.findall(r"\d+", s.rsplit('/',1)[1])[0]))]
res = {"n_nulls": len(nulls), "per_L": {}}
print("L  K4cells  null_mean  null_min  null_max  nulls_with_any")
for L in range(1, 27):
    row = {"K4": k4.get(L, 0)}
    if L <= 22:
        v = [h.get(L, 0) for h in nulls]
        row.update(null_mean=sum(v) / len(v), null_min=min(v), null_max=max(v), nulls_with_any=sum(1 for x in v if x))
        print(f"{L:2d} {row['K4']:9d} {row['null_mean']:10.1f} {row['null_min']:9d} {row['null_max']:9d} {row['nulls_with_any']:4d}/{len(v)}")
    else:
        print(f"{L:2d} {row['K4']:9d}   (nulls not run, saturated)")
    res["per_L"][L] = row
def perm(q):
    with open(BANK, "rb") as f:
        f.seek(q * 194); return list(struct.unpack("<97h", f.read(194)))
SEGS = {"EASTNORTHEAST": [], "EAST|NORTHEAST": [4], "EASTNORTH|EAST": [9], "EAST|NORTH|EAST": [4, 9], "BERLINCLOCK": [], "BERLIN|CLOCK": [6]}
reads = []
for l in open(f"{OUT}/k4_bank_L18-19.txt"):
    if not l.startswith("S "): continue
    d = dict(x.split("=") for x in l.split()[1:])
    q, dr, tm, L, o1, o2, key = int(d["perm"]), int(d["dir"]), int(d["tm"]), int(d["L"]), int(d["o1"]), int(d["o2"]), d["key"]
    s = perm(q); S = s[:] if dr == 0 else [0] * 97
    if dr == 1:
        for i in range(97): S[s[i]] = i
    lay = "".join(K4[S[i]] for i in range(97))
    al = KA if tm >= 2 else AZ
    def dec(i, k):
        if key[k] == "?": return "?"
        c, kk = al.index(lay[i]), al.index(key[k])
        return al[(c - kk) % 26] if tm % 2 == 0 else al[(kk - c) % 26]
    pre1 = "".join(dec(21 - o1 + t, t) for t in range(o1))
    pre2 = "".join(dec(63 - o2 + t, t) for t in range(o2))
    lastE = 13 - (SEGS[d["segE"]][-1] if SEGS[d["segE"]] else -o1)       # in-word index of the letter after the crib
    lastB = 11 - (SEGS[d["segB"]][-1] if SEGS[d["segB"]] else -o2)
    post1 = "".join(dec(34 + t, (lastE + t) % L) for t in range(min(8, 63 - 34)))
    post2 = "".join(dec(74 + t, (lastB + t) % L) for t in range(8))
    reads.append(dict(perm=q, dir=dr, tm=tm, L=L, segE=d["segE"], segB=d["segB"], o1=o1, o2=o2, key=key,
                      before_crib1=pre1, after_crib1_if_word_continues=post1, before_crib2=pre2, after_crib2_if_word_continues=post2))
res["K4_survivors_L18_19"] = reads
print(f"\nK4 survivors at L 18-19: {len(reads)} cells")
for r in reads[:80]:
    print(r["L"], r["perm"], r["dir"], r["tm"], r["segE"], r["segB"], "o", r["o1"], r["o2"], "|", r["before_crib1"] + "[EASTNORTHEAST]" + r["after_crib1_if_word_continues"],
          "|", r["before_crib2"] + "[BERLINCLOCK]" + r["after_crib2_if_word_continues"])
json.dump(res, open("results206_bank.json", "w"), indent=1)
