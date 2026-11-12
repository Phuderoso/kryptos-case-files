# PREREG203 — word-restart key (I-256), new family (cycle 203, 2026-11-12, written before any K4 run)

**Family.** K1/K2-style single tableau (AZ = straight, KA = KRYPTOS-keyed), Vigenère / Beaufort / variant, key word of
length L, with one hand-cipher tweak:
- **R1 (word restart):** the key index of a letter is its position inside its plaintext word, mod L (the key starts over at every word).
- **R2 (word-wise key):** every letter of a word uses the same key letter; the key advances by one per word (index = word number mod L).
- **QIII-R1:** R1 with an unknown keyed alphabet on both sides (Quagmire III, any of 26! alphabets), by SAT (pysat, Glucose).

Cribs at the carved positions (EASTNORTHEAST 22–34, BERLINCLOCK 64–74, 1-indexed). No transposition layer.

**Segmentations (primary, English):** crib 1 ∈ {EASTNORTHEAST, EAST|NORTHEAST, EASTNORTH|EAST, EAST|NORTH|EAST};
crib 2 ∈ {BERLINCLOCK, BERLIN|CLOCK}. The word holding the first crib letter may start earlier: free offset o ∈ 0..L−1
for each crib (R1), free word-number offset for crib 2 relative to crib 1 (R2). L = 1..26 (L ≥ 14 never wraps inside a crib word, so it stands for "key longer than every word").

**Secondary (descriptive):** every boundary set inside the cribs whose fully internal words have ≥ 2 letters.

**Decision rules.** R1 / R2 direct: a configuration survives iff equal key indices give equal key letters on all 24 crib letters.
Zero survivors at L ≤ 13 over the primary segmentations = **EXCLUDED (exact, under these assumptions)**. Where shuffled-K4 nulls
(1,000 shuffles, seed 203203, cribs kept, ciphertext letters permuted) survive in ≥ 5 % of draws at some L, survivors there are
**NO-DISCRIMINATION**, not evidence. Survivors on K4 at a discriminating L go to a dictionary key-word check (dwyl words_alpha if
present, else the repo word list). QIII-R1: SAT/UNSAT per (segmentation, L, o1, o2); UNSAT everywhere at an L = exact exclusion; SAT at
the null rate = underdetermined.

**Controls (must pass before reading K4):** C1 planted R1 (invented example text, KA Vigenère, key ABSCISSA) — true config must survive
and the crib-implied key letters must match ABSCISSA; C2 planted R2 (AZ Beaufort, key PALIMPSEST); C3 planted QIII-R1 with a random
alphabet must be SAT at the true config; C4 shuffled-null rates reported.
