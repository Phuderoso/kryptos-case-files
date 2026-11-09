"""Cycle 168 summary: part A (bookrk outputs), part B (fragment scores), controls, provenance, analytic bound.
usage: summarize168.py RUNDIR  (writes to stdout)"""
import sys, os, glob, json, re
R = sys.argv[1]; out = []
def summ(f):
    for l in open(f):
        if l.startswith("SUMMARY"):
            h = {int(a): int(b) for a, b in (x.split(":") for x in l.split("hist:")[1].split())}
            return int(re.search(r"best=(\d+)", l).group(1)), int(re.search(r"full=(\d+)", l).group(1)), h
    return None
# provenance (I-078)
outs = sorted(glob.glob(f"{R}/out/*.out")); tmps = glob.glob(f"{R}/out/*.tmp")
fin = [f for f in outs if summ(f)]
out.append(f"PROVENANCE outputs={len(outs)} finished={len(fin)} tmp={len(tmps)}")
# part A K4
H = {}; full = 0; best = 0
k4 = sorted(glob.glob(f"{R}/out/k4_chunk_*.out"))
for f in k4:
    b, fu, h = summ(f); full += fu; best = max(best, b)
    for k, v in h.items(): H[k] = H.get(k, 0) + v
out.append(f"PART-A K4 chunks={len(k4)}/16 configs={sum(H.values())} full={full} best_depth={best} hist=" + " ".join(f"{k}:{H[k]}" for k in sorted(H)))
for f in k4:
    for l in open(f):
        if l.startswith(("FULL", "CAND")): out.append("  " + os.path.basename(f) + " " + l.strip())
# part A K4 vs nulls on chunk_15
b15, f15, h15 = summ(f"{R}/out/k4_chunk_15.out")
nb = []
for f in sorted(glob.glob(f"{R}/out/null*_chunk_15.out"), key=lambda s: int(re.search(r"null(\d+)", s).group(1))):
    s = summ(f)
    if s: nb.append((os.path.basename(f), s[0], s[1], sum(v for k, v in s[2].items() if k >= 8)))
k8 = sum(v for k, v in h15.items() if k >= 8)
out.append(f"PART-A chunk_15 (10,352 decimations incl. all 6,070 routes): K4 best={b15} full={f15} depth>=8 configs={k8}")
out.append(f"  nulls={len(nb)} full_total={sum(x[2] for x in nb)} best depths: " + " ".join(str(x[1]) for x in nb))
out.append(f"  nulls with best >= K4's {b15}: {sum(x[1] >= b15 for x in nb)}/{len(nb)}; depth>=8 counts: " + " ".join(str(x[3]) for x in nb))
# controls part A
plant = {}
for l in open(f"{R}/ctl/controls_planted.txt"):
    m = re.match(r"(ctl\d+): perm (\d+) \(slice index (\d+)\) model (\w) mode (\d+) text (\S+) offset (\d+)", l)
    plant[m.group(1)] = m.groups()[1:]
ok = 0
for c, (perm, si, model, md, text, o) in sorted(plant.items(), key=lambda x: int(x[0][3:])):
    lines = [l.strip() for l in open(f"{R}/out/{c}.out") if l.startswith("FULL")] if os.path.exists(f"{R}/out/{c}.out") else []
    hit = any(f"perm={si} model={model} mode={md} text={text} offset={o}" in l for l in lines)
    ok += hit; out.append(f"  CONTROL-A {c}: planted perm {perm} model {model} mode {md} {text}@{o}: {'RECOVERED' if hit else 'MISSED'}; FULL lines {len(lines)}")
out.append(f"PART-A controls recovered {ok}/{len(plant)}")
# part B
k = json.load(open(f"{R}/partb_k4.json")); nl = [json.loads(l) for l in open(f"{R}/partb_nulls.jsonl")]
bs = sorted(x["best"] for x in nl)
out.append(f"PART-B K4 best={k['best']:.3f} {k['top'][0][1:]}; nulls n={len(bs)} min={bs[0]:.3f} median={bs[len(bs)//2]:.3f} max={bs[-1]:.3f}; nulls >= K4: {sum(x >= k['best'] for x in bs)}/{len(bs)}")
cl = [json.loads(l) for f in ("partb_controls.jsonl", "partb_controls2.jsonl") for l in open(f"{R}/{f}")]
out.append(f"PART-B controls rank1 {sum(c['rank'] == 1 for c in cl)}/{len(cl)}; true-fragment top scores > null max: {sum(c['rank'] == 1 and c['best'] > bs[-1] for c in cl)}/{len(cl)}")
for c in cl: out.append(f"  CONTROL-B {c['item']} {c['truth']['alphabet']} {c['truth']['mode']} {c['truth']['frag1']}/{c['truth']['frag2']} rank {c['rank']} best {c['best']:.3f}")
# analytic bound (part A): placements tested x 26^-24
T = [l.split() for l in open(f"{R}/texts.txt")]
offs = sum(len(t) - 96 for _, t in T)
cfg = 165782 * 58
out.append(f"BOUND placements ~ {cfg} configs/text-set x {offs} offsets = {cfg*offs:.3e}; expected chance 24/24 fits ~ {cfg*offs/26**24:.1e} (26^-24 per placement)")
print("\n".join(out))
