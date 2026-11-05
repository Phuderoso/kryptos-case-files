"""Cycle 83 summary: per text and period, SAT/UNSAT counts over the 12 (tableau, mode, alignment) configurations;
control witnesses decrypted with verify83.decrypt and compared with the planted key and plaintext."""
import json
from collections import defaultdict
from verify83 import decrypt
R = [json.loads(l) for l in open("results83.jsonl")]
C = {f"ctl{c['ctl']}": c for c in json.load(open("controls83.json"))}
crib = {**{21 + i: c for i, c in enumerate("EASTNORTHEAST")}, **{63 + i: c for i, c in enumerate("BERLINCLOCK")}}
tab = defaultdict(lambda: {"sat": 0, "unsat": 0, "unfinished": 0})
for r in R:
    k = f"{r['text']} p={r['p']}"
    tab[k]["sat" if r["sat"] else "unsat" if r["sat"] is False else "unfinished"] += 1
ctl = []
for r in R:
    if r["text"] in C and r["sat"]:
        c = C[r["text"]]; sq, key = r["witness"]
        d = decrypt(c["ct"], sq, key, r["tab"], r["mode"], r["a"])
        ctl.append(dict(control=r["text"], p=c["p"], tab=c["tab"], mode=c["mode"], a=c["a"], planted_key=c["key"], witness_key=key,
                        key_recovered=key == c["key"], cribs_ok=sum(d[i] == v for i, v in crib.items()),
                        letters_matching_planted=sum(x == y for x, y in zip(d, c["pt"])), witness_square=sq, witness_decryption=d))
out = dict(by_text_period=dict(sorted(tab.items())), controls=ctl, total_solver_seconds=round(sum(r["sec"] or 0 for r in R), 1))
json.dump(out, open("cycle83_summary.json", "w"), indent=1)
for k, v in sorted(tab.items()): print(k, v)
for c in ctl: print(c["control"], c["key_recovered"], c["cribs_ok"], c["letters_matching_planted"])
