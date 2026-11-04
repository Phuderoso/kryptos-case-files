"""Cycle 8 (1): physical-position readings of K4 on the panel, using Elonka Dunin's row-by-row transcript
(https://elonka.com/kryptos/transcript.html, fetched 2026-11-04; she notes her font does not perfectly reproduce the
column alignment). Rows saved to data/elonka_panel_rows.txt. Layout as transcribed: cipher top half (14 rows) beside
tableau header+A..M; cipher bottom half (14 rows) beside tableau N..Z+footer. K4 = last 4 cipher rows.
Short hypothesis list, each gated by the 24 crib letters:
 P1 column-wise readings of K4's 4 physical rows (8 variants) x periodic Vig/Beau P1-26 (KA/AZ) consistency (>=6 constraints)
 P2 per-row Caesar with the key = tableau row label beside that row (row offset -2..+2), KA/AZ, Vig/Beau/VarBeau
 P3 running key = tableau letter at the same physical (row, col) (row offset -2..+2, col offset -2..+2)
 P4 progressive key = column header letter (header row ABCD... above/below), col offset -3..+3
Run: python3 tools/k4_physical.py [control]"""
import sys
sys.path.insert(0, "tools")
from k4_anneal import AZ, KA, KN, N
import kryptos_text
from collections import Counter
K4 = kryptos_text.K4
rows = [r.rstrip("\n") for r in open("data/elonka_panel_rows.txt")]
# indices in file order: 0-13 cipher top, 14 header, 15-27 tableau A..M, 28-41 cipher bottom, 42-54 tableau N..Z, 55 footer
cipher = rows[0:14] + rows[28:42]; tableau = rows[14:28] + rows[42:56]
assert "".join(cipher).replace("?", "").endswith(K4), "transcript does not end with K4"
# physical coords of each K4 letter: (panel_row, col)
coords = []
for r in range(27, 23, -1):
    pass
flat = []
for r, line in enumerate(cipher):
    for c, ch in enumerate(line):
        if ch != "?": flat.append((r, c, ch))
k4c = [(r, c) for r, c, ch in flat[-N:]]
assert "".join(ch for _, _, ch in flat[-N:]) == K4
def gate_key(keyfun, alpha, mode, CT):
    m = 0
    for i, p in KN.items():
        s = keyfun(i)
        if s is None: continue
        c = alpha.index(CT[i]); q = alpha.index(p)
        e = (c - q) % 26 if mode == "vig" else (c + q) % 26 if mode == "beau" else (q - c) % 26
        m += (s == e)
    return m
def periodic_ok(order, alpha, P, mode, CT):
    """order[k] = K4 index read k-th (the read-out is the 'transposed' text); key index k."""
    pos = {i: k for k, i in enumerate(order)}; key = {}; n = 0
    for i, p in KN.items():
        k = pos[i]; c = alpha.index(CT[i]); q = alpha.index(p)
        e = (c - q) % 26 if mode == "vig" else (c + q) % 26
        if k % P in key:
            n += 1
            if key[k % P] != e: return False, n
        key[k % P] = e
    return True, n
def run(CT=K4):
    out = []; total = 0
    # P1
    R = sorted(set(r for r, c in k4c)); cols = sorted(set(c for r, c in k4c))
    idx = {rc: i for i, rc in enumerate(k4c)}
    reads = {}
    for cdir in (1, -1):
        for rdir in (1, -1):
            o = [idx[(r, c)] for c in cols[::cdir] for r in R[::rdir] if (r, c) in idx]; reads[f"cols c{cdir} r{rdir}"] = o
            o = [idx[(r, c)] for r in R[::rdir] for c in cols[::cdir] if (r, c) in idx]; reads[f"rows c{cdir} r{rdir}"] = o
    p1 = []
    for name, o in reads.items():
        for an, alpha in (("KA", KA), ("AZ", AZ)):
            for mode in ("vig", "beau"):
                for P in range(1, 27):
                    total += 1; ok, n = periodic_ok(o, alpha, P, mode, CT)
                    if ok and n >= 6: p1.append((name, an, mode, P, n))
    out.append(("P1 column/row readings x periodic P1-26", total, p1)); t0 = total
    # P2/P3/P4
    best = Counter(); surv = []
    for an, alpha in (("KA", KA), ("AZ", AZ)):
        for mode in ("vig", "beau", "varbeau"):
            for dr in range(-2, 3):
                def p2(i):
                    r = k4c[i][0] + dr
                    if not 0 <= r < 28 or not tableau[r].strip(): return None
                    lab = tableau[r][0]
                    return None if lab == ' ' else alpha.index(lab)
                m = gate_key(p2, alpha, mode, CT); total += 1; best["P2"] = max(best["P2"], m)
                if m == 24: surv.append(("P2", an, mode, dr))
                for dc in range(-2, 3):
                    def p3(i):
                        r, c = k4c[i]; r += dr; c += dc
                        if not 0 <= r < 28 or not 0 <= c < len(tableau[r]) or tableau[r][c] == " ": return None
                        return alpha.index(tableau[r][c])
                    m = gate_key(p3, alpha, mode, CT); total += 1; best["P3"] = max(best["P3"], m)
                    if m == 24: surv.append(("P3", an, mode, dr, dc))
            for dc in range(-3, 4):
                hdr = tableau[0]
                def p4(i):
                    c = k4c[i][1] + dc
                    if not 0 <= c < len(hdr) or hdr[c] == " ": return None
                    return alpha.index(hdr[c])
                m = gate_key(p4, alpha, mode, CT); total += 1; best["P4"] = max(best["P4"], m)
                if m == 24: surv.append(("P4", an, mode, dc))
    out.append(("P2-P4 tableau-position keys", total - t0, surv))
    return out, best, reads
if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "control":
        # planted: P3-type key (tableau letter one row up, dr=-1, dc=0), KA Vigenere, applied to English+cribs
        eng = "WEMETATTHECORNERWHERETHEROADTURNSEASTNORTHEASTANDTHEOLDSTATIONSTOODWAITINGFORTHEBERLINCLOCKTOSTRIKE"
        pt = list(eng[:N])
        for i, ch in KN.items(): pt[i] = ch
        CT = "".join(KA[(KA.index(pt[i]) + KA.index(tableau[k4c[i][0]-1][k4c[i][1]])) % 26] for i in range(N))
        out, best, _ = run(CT); print("CONTROL (planted P3 dr=-1 dc=0 KA vig):")
        for name, t, s in out: print(f"  {name}: tests {t}, survivors {s}")
        # planted P1: column read + KA vig 'CLOCK'
        _, _, reads = run(K4); o = reads["cols c1 r1"]; key = "CLOCK"; ct = [""] * N
        for k, i in enumerate(o): ct[i] = KA[(KA.index(pt[i]) + KA.index(key[k % 5])) % 26]
        out, best, _ = run("".join(ct)); print("CONTROL (planted P1 cols c1 r1 + KA vig CLOCK):")
        for name, t, s in out: print(f"  {name}: tests {t}, survivors {s}")
    else:
        print("K4 physical coords (row, col) first/last:", k4c[0], k4c[-1], "rows:", sorted(set(r for r, c in k4c)))
        print("tableau labels beside K4 rows:", [tableau[r][0] if tableau[r][0] != " " else "(plain-alphabet footer)" for r in sorted(set(r for r, c in k4c))])
        out, best, _ = run()
        for name, t, s in out: print(f"{name}: tests {t}; survivors {s}")
        print("best crib matches:", dict(best))
