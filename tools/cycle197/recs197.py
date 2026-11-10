"""Cycle 197: direct-application records for cmp197 rec mode (I-196). Independent of cmp197's perm-mode generator.
Reading R1: cribs at the official PLAINTEXT positions (0-based 21-33, 63-73) of an N-letter plaintext (N 98 del, 96 ins); direct, so the
key index = plaintext index = C' index. Reading R2: cribs at the official CARVED positions. del: C' (98) lost letter d; ins: C' (96) with
an extra carved letter at carved index d. Record line: id d kp[24] cv[24] (cv -1 = crib letter not on the copper / crib on the extra letter).
Writes recs197_direct.txt (deduplicated) and recs197_direct_map.txt (id -> every (reading, kind, d) giving that record)."""
CI = list(range(21, 34)) + list(range(63, 74))
recs = {}
def add(key, tag):
    recs.setdefault(key, []).append(tag)
for d in range(98):  # del, C' 98 letters, C'[d] dropped
    # R1: crib at C' index i -> carved i (i<d), lost (i==d), i-1 (i>d)
    kp = tuple(CI); cv = tuple(i if i < d else (-1 if i == d else i - 1) for i in CI)
    add((kp, cv), f"R1 del {d}")
    # R2: carved j -> C' j (j<d) or j+1 (j>=d)
    kp = tuple(j if j < d else j + 1 for j in CI); cv = tuple(CI)
    add((kp, cv), f"R2 del {d}")
for d in range(97):  # ins, C' 96 letters, extra carved at d
    kp = tuple(CI); cv = tuple(i if i < d else i + 1 for i in CI)
    add((kp, cv), f"R1 ins {d}")
    kp = tuple(j if j < d else (0 if j == d else j - 1) for j in CI); cv = tuple(j if j != d else -1 for j in CI)
    add((kp, cv), f"R2 ins {d}")
with open("recs197_direct.txt", "w") as f, open("recs197_direct_map.txt", "w") as g:
    for i, (k, tags) in enumerate(recs.items()):
        d = int(tags[0].split()[-1])
        f.write(" ".join(map(str, [i, d] + list(k[0]) + list(k[1]))) + "\n")
        g.write(f"{i} " + ";".join(tags) + "\n")
print("distinct direct records", len(recs))
