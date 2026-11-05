"""Cycle 83 runner, resumable: results appended to results83.jsonl; a finished (text, p, tab, mode, align) is skipped.
Divisibility: periodic with p | p' is a special case of p', so UNSAT at {4,5,6} covers p 1-6 and {4,5,6,7} covers 1-7."""
import json, sys, os, time, multiprocessing as mp
from sat83 import solve
from kryptos_text import K4
TO = int(os.environ.get("TO", "240"))
def job(t):
    name, ct, p, tab, mode, a = t
    t0 = time.time()
    ok, w, npairs = solve(ct, p, tab, mode, a)
    return dict(text=name, p=p, tab=tab, mode=mode, a=a, sat=ok, witness=w, pairs=npairs, sec=round(time.time() - t0, 1))
def main():
    ctl = json.load(open("controls83.json"))
    texts = {"K4": K4, **{f"null{n}": open(f"null_{n}.txt").read().strip() for n in range(3)},
             **{f"ctl{c['ctl']}": c["ct"] for c in ctl}}
    plan = []
    for spec in sys.argv[1:]:          # spec  text:p1,p2:all|tab/mode/a
        name, ps, cf = spec.split(":")
        cfgs = [(t, m, a) for t in ("KA", "AZ") for m in (0, 1, 2) for a in (0, 1)] if cf == "all" else [(cf.split("/")[0], int(cf.split("/")[1]), int(cf.split("/")[2]))]
        for p in map(int, ps.split(",")):
            for (t, m, a) in cfgs: plan.append((name, texts[name], p, t, m, a))
    done = set()
    if os.path.exists("results83.jsonl"):
        for l in open("results83.jsonl"):
            r = json.loads(l)
            if r["sat"] is not None: done.add((r["text"], r["p"], r["tab"], r["mode"], r["a"]))
    plan = [x for x in plan if (x[0], x[2], x[3], x[4], x[5]) not in done]
    plan.sort(key=lambda x: (not x[0].startswith("ctl"), x[0] != "K4", -x[2]))
    print(len(plan), "jobs", flush=True)
    with mp.Pool(8) as pool, open("results83.jsonl", "a") as f:
        for r in pool.imap_unordered(job, plan):
            f.write(json.dumps(r) + "\n"); f.flush(); print(r["text"], r["p"], r["tab"], r["mode"], r["a"], "SAT" if r["sat"] else "UNSAT", r["sec"], flush=True)
if __name__ == "__main__": main()
