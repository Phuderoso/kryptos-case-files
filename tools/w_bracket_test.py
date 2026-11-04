"""Cycle 9: how unusual is it that W sits at both 21 (just before EAST..., starts at 22) and 75 (just after ...CLOCK, ends 74)?
Monte Carlo: shuffle K4's letters, count crib-boundary neighbours (21,35,63,75; 1-indexed) holding the same letter type."""
import random, sys
sys.path.insert(0, "tools"); from kryptos_text import K4
B = [20, 34, 62, 74]  # 0-indexed neighbours just outside the two crib blocks
obs = sum(K4[b] == "W" for b in B)
rng = random.Random(97); T = 200000
p_w = sum(sum(s[b] == "W" for b in B) >= obs for s in (rng.sample(K4, 97) for _ in range(T))) / T
def anyletter(s):  # look-elsewhere: ANY single letter occupying >= obs of the 4 boundary slots
    from collections import Counter; return max(Counter(s[b] for b in B).values())
p_any = sum(anyletter(rng.sample(K4, 97)) >= obs for _ in range(T)) / T
print(f"observed W at boundaries: {obs} of 4 ({[b+1 for b in B if K4[b]=='W']})")
print(f"P(>= {obs} W in boundary slots | random order) = {p_w:.4f}")
print(f"P(some letter fills >= {obs} boundary slots | random order) = {p_any:.4f}  (look-elsewhere corrected)")
