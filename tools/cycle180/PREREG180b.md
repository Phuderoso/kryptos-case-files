# Cycle 180 add-on pre-registration — replication of the D2 diagnostic flag (written after the main run, before any replication run)

**Why.** The registered main run (PREREG180.md) gave **0 fits for K4 and all 19 nulls in every fit cell** (R1–R3 all-zero, not
scored). The registered grid was then carried by the two *diagnostic* cells: D2 (M1 mod-2 passes, L 1–3 on all_s8 + L 4 themed)
**K4 7,309 vs nulls 6,199–7,117, above all 19 → rank p⁺ 0.05 = the floor**; D1 (M0 mod-2 passes L 6–7) K4 near the low end
(grid p⁻ 0.10). The leave-one-out Poisson tails are not meaningful at these counts (overdispersed, correlated alphabets); the rank is.
Exactly as for case 165's C2 flag (I-133), a floor rank among 19 shuffles is not evidence by itself; it is replicated with fresh
shuffles, pre-registered here, **before** running them.

**Cell (one, one-sided):** D2′ = M1 (key on the carved index) mod-2 pass count, L 1–3, all 18,776 vocabulary alphabets × q1/q2/q3,
on `all_s8.bin`, summed over L and types, Vigenère lines only (= Beaufort). **K4 value already observed: 6,273** (19 registered nulls
3,857 … 6,089 in this sum). The L 4 themed part is dropped (it does not separate: K4 1,036 vs null mean 1,018).
**Fresh nulls:** 40 shuffles `random.Random(s).shuffle(list(K4))`, s = **18041…18080** (never used before).
**Statistic:** p_F = (1 + #{fresh null ≥ 6,273}) / 41. **Decision:** replicated iff p_F ≤ 0.05 (at most one fresh null ≥ K4);
otherwise **not replicated**, and the flag is closed as a chance upper-tail draw. Reported also: mean, SD, z of K4, and the per-type
split (q1/q2/q3) as description only (the q1 part depends on K4 only through the A–Z parity of the carved letters at the crib slots'
carved positions, a fixed 97-bit pattern per text).
**Meaning either way:** this is a statement about the parity structure of K4's letter *positions* under the decimation perms, not a
fit. Even a replicated D2′ would not be a decryption signal (no K4 fit exists in this family); it would be a covariate to explain.
**Run:** `run_d2rep180.sh` (lrk180 mode 1 L 1–3 on all_s8, 6 threads, one at a time; ≈ 2.5 s per text).
