"""Independent pure-Python recount of the registered 64-statistic panel (no numpy, no lib200 code paths).
Usage: python3 recount200.py  -> compares with lib200.panel on K4, K1, and 20 random strings."""
import random, sys, os
AZ = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"; KA = "KRYPTOSABCDEFGHIJLMNQUVWXZ"


def stats(s):
    n = len(s)
    A = {d: sum(1 for i in range(n - d) if s[i] == s[i + d]) for d in range(1, 49)}
    def B(d, al):
        cnt = {}
        for i in range(n - d):
            v = (al.index(s[i + d]) - al.index(s[i])) % 26
            cnt[v] = cnt.get(v, 0) + 1
        return sum(m * (m - 1) // 2 for m in cnt.values())
    out = []
    out += [sum(A[k * p] for k in range(1, 49) if k * p <= 48) for p in range(4, 27)]
    out += [B(p, AZ) for p in range(4, 17)]
    out += [B(p, KA) for p in range(4, 17)]
    out += [sum(A[d] for d in range(1, L + 1)) for L in range(2, 17)]
    return out


if __name__ == "__main__":
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
    from lib200 import panel, enc, K4
    from kryptos_text import K1
    rnd = random.Random(20099)
    tests = [K4, K1] + ["".join(rnd.choice(AZ) for _ in range(97)) for _ in range(20)]
    bad = 0
    for t in tests:
        a = stats(t); b = [int(v) for v in panel(enc(t)[None, :])[0]]
        bad += (a != b)
    print(f"recount: {len(tests)} strings, {bad} mismatches, {len(stats(K4))} statistics each")
