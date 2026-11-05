"""Cycle 76: summarise nulltr76 runs (K4, 20 shuffled nulls, 6 planted controls) and the power map."""
import json, re
def hist(path):
    H = {}
    for l in open(path):
        m = re.match(r"(F\d) consistent-by-checks:(.*)", l)
        if m: H[m.group(1)] = {int(k): int(v) for k, v in (x.split(":") for x in m.group(2).split())}
    return H
def mx(h): return max(h)
res = {"model": "A: substitution in plaintext order -> b nulls between cribs (any before/after) -> transposition",
       "transpositions": 165065, "tableaux": ["KA", "AZ"], "modes": ["vig", "beau", "var"]}
k4 = hist("out_k4.txt"); res["k4_hist"] = k4
res["k4_hits_ge5"] = [l.strip() for l in open("out_k4.txt") if l.startswith("HIT")]
nulls = [hist(f"out_null_{i}.txt") for i in range(20)]
res["null_max_checks"] = {f: [mx(n[f]) for n in nulls] for f in ("F0", "F1", "F2")}
res["k4_max_checks"] = {f: mx(k4[f]) for f in ("F0", "F1", "F2")}
res["k4_ge4"] = {f: sum(v for k, v in k4[f].items() if k >= 4) for f in k4}
res["null_mean_ge4"] = {f: sum(sum(v for k, v in n[f].items() if k >= 4) for n in nulls) / 20 for f in k4}
ctl = json.load(open("controls76_planted.json")); cres = []
for c in ctl:
    raw = open(f"out_ctl_{c['ctl']}.raw").read().splitlines()
    m = [l for l in raw if l.startswith(c["signature"])]
    ck = int(m[0].split("checks=")[1]) if m else None
    # how many configurations in the whole run reach the planted check count (rank of the planted one)
    tot = sum(v for h in hist(f"out_ctl_{c['ctl']}.raw").values() for k, v in h.items() if ck is not None and k >= ck)
    cres.append({"ctl": c["ctl"], "planted": f"{c['tab']} {c['mode']} {c['kind']} key={c['key'] if len(c['key'])<12 else 'random'} L={c['L']} a={c['a']} b={c['b']} c={c['c']} perm={c['perm']}",
                 "recovered": bool(m), "checks": ck, "configs_with_at_least_as_many_checks": tot})
res["controls"] = cres
# power map: number of checks each effective configuration carries (independent of the text)
pw = {"periodic": {}, "autokey": {}}
for p in range(1, 27):
    for b in range(min(p, 30)):
        r = {(21 + j) % p for j in range(13)} | {(63 + j - b) % p for j in range(11)}
        pw["periodic"][f"p{p}b{b}"] = 24 - len(r)
def cross(d): return sum(1 for j1 in range(13) if 0 <= j1 + d <= 10)
for L in range(1, 13):
    intra = max(0, 13 - L) + max(0, 11 - L); pw["autokey"][f"L{L}"] = intra
    for d in range(-12, L - 12): pw["autokey"][f"L{L}d{d}"] = intra + cross(d)
for d in range(-12, 11): pw["autokey"][f"d{d}"] = cross(d)
res["power_threshold"] = 6
res["periodic_p_fully_testable(all b have >=6 checks)"] = [p for p in range(1, 27) if all(pw["periodic"][f"p{p}b{b}"] >= 6 for b in range(min(p, 30)))]
res["periodic_testable_fraction_by_p"] = {p: sum(pw["periodic"][f"p{p}b{b}"] >= 6 for b in range(p)) / p for p in range(1, 27)}
res["autokey_configs_testable"] = sum(v >= 6 for v in pw["autokey"].values()); res["autokey_configs_total"] = len(pw["autokey"])
res["autokey_blind"] = [k for k, v in pw["autokey"].items() if v < 6]
json.dump(res, open("cycle76_summary.json", "w"), indent=1)
print(json.dumps({k: res[k] for k in res if k not in ("k4_hist",)}, indent=0)[:4000])
