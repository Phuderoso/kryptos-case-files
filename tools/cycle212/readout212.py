"""Cycle 212 read-out of a wrj survivor: letters decryptable without guessing word boundaries (case 197 convention):
the o1 / o2 letters glued before the first crib word of each crib, and the continuation of the last crib word (key indices continue)."""
import struct, sys
K4 = open("k4.txt").read().strip()
def row(fn, q):
    with open(fn, "rb") as f: f.seek(q * 194); return list(struct.unpack("<97h", f.read(194)))
def readout(fam, q, d, X, Y, form, L, segE, segB, o1, o2, key):
    s = row(fam, q); S = s if d == 0 else [s.index(i) for i in range(97)]
    lay = [K4[S[i]] for i in range(97)]
    def dec(i, k):
        if key[k] == "?": return "?"
        kv = Y.index(key[k]); yc = Y.index(lay[i])
        return X[(yc - kv) % 26] if form == "vig" else X[(kv - yc) % 26]
    out = ["."] * 97
    lastE = len(segE.split("|")[-1]); lastB = len(segB.split("|")[-1])
    ws1 = 21 - o1; ws2 = 63 - o2
    for i in range(ws1, 21): out[i] = dec(i, (i - ws1) % L)
    b = 21; 
    for w in segE.split("|"):
        st = b if b > 21 or o1 == 0 else ws1
        for i in range(b, b + len(w)): out[i] = w[i - b] if True else ""
        b += len(w)
    stE = 34 - lastE if len(segE.split("|")) > 1 else ws1
    for i in range(34, 63 - o2 if 63 - o2 > 34 else 34): out[i] = dec(i, (i - stE) % L).lower()
    for i in range(ws2, 63): out[i] = dec(i, (i - ws2) % L)
    for i, ch in enumerate("BERLINCLOCK"): out[63 + i] = ch
    stB = 74 - lastB if len(segB.split("|")) > 1 else ws2
    for i in range(74, 97): out[i] = dec(i, (i - stB) % L).lower()
    return "".join(out)
if __name__ == "__main__":
    for l in open(sys.argv[1]):
        if not l.startswith("S "): continue
        kv = dict(t.split("=", 1) for t in l.split()[1:])
        if sys.argv[2:] and kv["L"] not in sys.argv[2:]: continue
        r = readout(sys.argv[3] if False else ("bank.bin" if "bank" in sys.argv[1] else "all.bin"), int(kv["perm"]), int(kv["dir"]), kv["X"], kv["Y"], kv["form"], int(kv["L"]),
                    kv["segE"], kv["segB"], int(kv["o1"]), int(kv["o2"]), kv["key"])
        print(kv["perm"], kv["dir"], kv["X"][:9], kv["Y"][:9], kv["form"], kv["L"], kv["segE"], kv["segB"], kv["o1"], kv["o2"], r)
