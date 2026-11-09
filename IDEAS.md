# IDEAS — the persistent idea queue (canonical)

> *Every hunch gets a card. Every card gets a test, a control and a verdict, or it stays in the drawer marked "queued". No card is closed on a plan alone.*

Created in **cycle 151 (2026-11-08)**. Before this file, open ideas lived only in the "Ideas for later" lines of the
[journals](journal/), the *Limits* sections of the case files and the "Still open" column of the
[README coverage table](README.md#coverage-table-started-cycle-39-update-every-cycle). A check in cycle 151 found no maintained
queue elsewhere in the repo, so this file is now the single place where ideas are queued, prioritised and closed. Each cycle
reads it first, picks from it, and updates it at the end.

**Fields.** ID (stable, never reused) · date / source · hypothesis and rationale · priority (P1 high … P3 low) · discriminating test ·
controls / null model · rough cost · dependencies · status (`queued`, `in progress`, `blocked`, `tested`, `superseded`) · result / links.
**Evidence tags:** `[sourced]` = rests on a cited public source; `[repo]` = derived from this repo's own results; `[speculation]` = a hunch with no source.
**Result labels (from I-004):** `EXACT-EXCL` = excluded exactly under the stated assumptions; `NO-SIGNAL` = heuristic search (scoring, annealing) found nothing;
`LOW-POWER` = the test cannot tell K4 from shuffled text at this scale (insufficient discrimination). A small null sample never supports a tail claim.

## Summary (top of queue first)
| ID | Short name | Prio | Status |
|---|---|---|---|
| I-001 | Superseded notices for stale strips/transposition and S2/S6 text (case 10, README) | P1 | tested (done, cycle 151) |
| I-002 | Provenance of the circled tableau letters and archival carving differences | P1 | blocked (unpublished sources) |
| I-003 | One-error robustness audit of high-impact exact exclusions | P1 | in progress (Hill done in 151; I-007, I-008, I-040, I-041 left) |
| I-004 | Separate exact / heuristic / low-power results; full-scale nulls for tail claims | P1 | queued |
| I-005 | Hill n = 2–4 under one carving error (block-drop + exact one-letter repair) | P1 | tested — EXACT-EXCL ([case 139](case-file/139-hill-one-carving-error.md)) |
| I-006 | Robustness by design: which count-scored families already tolerate one error | P1 | tested ([case 139](case-file/139-hill-one-carving-error.md) audit table) |
| I-007 | Keyword / arbitrary columnar w 9–11 × periodic key under one crib error | P2 | queued |
| I-008 | Gromark / Periodic Gromark under one crib error | P2 | queued |
| I-009 | Two-letter differences anchored to the archive charts | P2 | blocked (needs archive data, see I-002) |
| I-010 | Quagmire IV with two different vocabulary alphabets | P2 | queued |
| I-011 | Word-keyed zig-zag autokey; zig-zag + progressive shift | P1 | tested — EXACT-EXCL (CT feed, n ≥ 12) / LOW-POWER (PT feed, long lags) ([case 140](case-file/140-free-form-zigzag-autokey.md)) |
| I-012 | Hill with a key on the ciphertext side (`p = D·(c − f)`, non-linear) | P2 | queued (new structure) |
| I-013 | Key change at a boundary keeping the width-7 phase | P2 | queued |
| I-014 | CT-autokey with both alphabets free | P2 | queued |
| I-015 | Quagmire I/II/IV autokey, themed × vocabulary alphabets, behind the bank | P2 | queued |
| I-016 | Periodic, both alphabets arbitrary (SAT), open periods 8, 13, 16, 19, 20, 23, 24, 26 | P2 | queued (mostly LOW-POWER expected) |
| I-017 | Full-bank nulls for thin-baseline claims (cycles 140, 145, 147) | P2 | queued |
| I-018 | Gromark L ≥ 7 with arbitrary alphabets; Gromark behind transpositions | P3 | queued |
| I-019 | Constant-digit keys: triples, A=1..26 with carries, backward or decimated reading | P3 | queued |
| I-020 | Phrase-keyed (two-word) alphabets for the ptfree / CT-autokey free-alphabet tests | P3 | queued |
| I-021 | Mixed direction on a keyed alphabet; P ≥ 27 behind the bank with bit-counted checks | P3 | queued |
| I-022 | Periods / lags 17–26 with dictionary or phrase completion of the partial key | P3 | queued |
| I-023 | Columnar w 12–13 arbitrary orders × periodic key | P3 | queued (expensive) |
| I-024 | Bifid 6×6 behind transpositions; Trifid periods 21–97 behind transpositions | P3 | queued |
| I-025 | Playfair p ≥ 8 arbitrary squares by annealing; Doppelkasten's 14 underdetermined configs | P3 | queued |
| I-026 | Hill n = 6 behind transpositions; n = 5 arbitrary numbering; n ≥ 7 | P3 | queued |
| I-027 | Linear-recurrence key L 5 (perms 20,000+) and L 6 behind the bank | P3 | queued |
| I-028 | Multi-rotor / Hagelin exact feasibility (CP-SAT) | P3 | queued |
| I-029 | Better score for weakly constrained solutions (letter likelihood, not partial quadgrams) | P3 | queued (method) |
| I-030 | Physical measurement of the sculpture (letter spacing, re-cut letters) | P3 | blocked (no access) |
| I-039 | Hill under a dropped or extra carved letter (alignment-shifting slip) | P2 | queued |
| I-040 | One-error audit of Hill + key (cycles 143–144) and Hill n = 5 | P2 | queued |
| I-041 | One-error audit of strict vocabulary families behind the bank (cycles 135–137, 146) | P2 | queued |
| I-042 | Zig-zag over keyed (Quagmire) or affine alphabets | P3 | queued |
| I-043 | Zig-zag autokey + periodic key (form free, shift periodic) | P3 | queued (power check first) |
| I-044 | Free-choice superset for other per-letter choices (AZ vs KRYPTOS tableau per letter; free Vig/Beau per letter on periodic keys behind other transposition families) | P2 | queued (method from cycle 152) |
| I-045 | Language-scored PT-feed / long-lag zig-zag (the LOW-POWER part of I-011) | P3 | queued (needs I-029) |
| I-031 | Strip transposition (case 10 S6) | — | tested (case 12) |
| I-032 | Single-letter anomaly × periodic KA/AZ key (direct and behind 165k transpositions) | — | tested (case 23) |
| I-033 | Two-letter anomalies × direct KA/AZ periodic key | — | tested (case 24) |
| I-034 | One-crib-error leave-one-out: stepping disk, Quagmire I–III, Kryha | — | tested (cases 107, 108, 110) |
| I-035 | ptfree (PT-autokey, free plain alphabet) behind the bank, all 10,057 vocabulary alphabets | — | tested (cases 127, 128, 133, 135, 137) |
| I-036 | Zig-zag autokey (fixed 2–3 form cycles) | — | tested (case 138) |
| I-037 | Constant-digit running keys (8 constants, 40 streams) | — | tested (case 136) |
| I-038 | Mixed-direction periodic key, P 1–28 | — | tested (case 134) |

---

## Open and in-progress items

### I-001 — Superseded notices for stale strips / transposition / S2 / S6 text
- **Date / source:** 2026-11-08, Firefly documentary review (F1). `[repo]`
- **Hypothesis / rationale:** [case file 10](case-file/10-style-profile.md) §5 and §7 (S2, S6) and the README cycle-2 status line still read the "scrambled plain text" / "cut into strips" reports as evidence of a cipher transposition. [Case file 12](case-file/12-strips-and-periodic-keys.md) §1 corrected that (the strips were a 1990 disclosure device for the plaintext; S2 was subsumed by the generic periodic test; S6 tested and downgraded). A reader landing on case 10 alone gets the stale reading.
- **Test / action:** add explicit "superseded — see case 12" notices next to the stale passages, keeping the historical text intact.
- **Controls:** n/a (documentation). **Cost:** minutes. **Dependencies:** none.
- **Status:** tested (action done in cycle 151). **Result:** superseded notices added at the top of case 10, after its S6 line, in its §7 S2/S6 rows, and on the README cycle-2 status line; historical text kept.

### I-002 — Provenance of the circled tableau letters and archival carving differences
- **Date / source:** 2026-11-08, Firefly review (F2); kryptosbot findings page (Sep 2026, secondary) reports "newly documented circled letters on a tableau in the sculptor's working papers (not yet analyzed)" and planned sculpture measurements `[sourced, secondary]`; noted in [case 67](case-file/67-tableau-walk-running-keys.md).
- **Hypothesis:** circled letters, or differences between Sanborn's coding charts and the copper, could encode a key or reveal a carving error. `[speculation]`
- **Test:** source work first, no variant tests: find a primary description (who saw it, which document, which letters), with archive call numbers. Only then preregister a test (fix letters/positions before looking at K4 output).
- **Controls:** preregistration; for any variant test, the same pipeline on shuffled ciphertext. **Cost:** research hours; compute small. **Dependencies:** public release of the papers (the K4 files are sealed to 2075; Paradigm holds the archive).
- **Status:** blocked (no primary public source as of 2026-11-08). **Result:** —

### I-003 — One-error robustness audit of high-impact exact exclusions
- **Date / source:** 2026-11-08, Firefly review (F3); community talk of a carving error (journal cycle 150); kryptosbot notes its one-letter CT-perturbation runs were limited to the families it tested `[sourced, secondary]`.
- **Hypothesis:** if one carved letter or one crib letter is wrong, a strict "all 24 cribs must agree" test rejects the true configuration. Every high-impact `EXACT-EXCL` claim should state whether it survives one error. `[repo]`
- **Test:** per family, rerun with (a) leave-one-crib-out and (b) one carved-letter substitution, counting survivors; planted controls with one corrupted letter must be recovered; shuffled nulls at the same tolerance.
- **Controls / nulls:** planted control with one corrupted letter (must be recovered) and without (must still be recovered); ≥ 2 shuffled-K4 nulls at full scale. **Cost:** family-dependent, usually ≤ 25× the strict run. **Dependencies:** I-004 labels.
- **Status:** in progress. Done before: periodic KA/AZ ([case 23](case-file/23-one-letter-anomaly.md)), two letters direct ([case 24](case-file/24-two-letter-anomalies.md)), stepping disk ([107](case-file/107-stepping-disk-one-crib-error.md)), Quagmire I–III ([108](case-file/108-quagmire-one-crib-error.md)), Kryha ([110](case-file/110-kryha-one-crib-error.md)). Cycle 151: Hill (I-005) and the design audit (I-006). Remaining: I-007, I-008.

### I-004 — Separate exact, heuristic and low-power results
- **Date / source:** 2026-11-08, Firefly review (F4). `[repo]`
- **Hypothesis / rationale:** the coverage table mixes exact exclusions under assumptions, heuristic no-signal results (annealing, quadgram ranking) and tests that cannot discriminate K4 from shuffled text. Small null samples (1/10 of the bank, 2–5 shuffles) were sometimes used to call K4 "at chance".
- **Test / action:** add an evidence-type label (`EXACT-EXCL` / `NO-SIGNAL` / `LOW-POWER`) to each coverage row; for tail claims, rerun nulls at full scale (I-017).
- **Controls:** n/a (classification), plus I-017 nulls. **Cost:** an hour of reading per ~20 rows. **Dependencies:** none.
- **Status:** queued (cycle 151 applies the labels to its own result and to the I-006 audit table).

### I-005 — Hill n = 2–4 under one carving error
- **Date / source:** 2026-11-08, cycle 151. [Case 26](case-file/26-hill-behind-transposition.md) lists "Hill combined with a carved-anomaly layer" as untested; Bauer, Link & Molle's HILL conjecture (Cryptologia) makes Hill a high-impact family `[sourced]`.
- **Hypothesis:** K4 is a Hill cipher (n 2–4, A–Z or KRYPTOS numbering) directly or around a 165k-bank transposition, with one carved letter wrong. `[speculation]`
- **Test:** exact: drop all crib equations of one Hill block (a wrong carved letter breaks exactly one block; a wrong crib letter one equation in it), solve each row mod 2 and mod 13, then require an exact one-letter repair of the dropped block.
- **Controls / nulls:** planted Hill encryptions with one corrupted carved letter under a crib (direct, model Q, carved order) and uncorrupted; two shuffled-K4 nulls at full scale. **Cost:** ~2–4 min on 8 cores. **Dependencies:** bank `perms97.bin`.
- **Status:** tested (cycle 151). **Result:** `EXACT-EXCL` — K4 0 survivors for n = 2, 3, 4 under one substituted carved letter (exact repair) and under one wrong crib letter; nulls 0/0 (n 2–3), 0/2 gibberish (n 4); 6/6 corrupted-letter controls recovered with the exact error position. At n = 4 the block-drop screen alone is LOW-POWER (K4 164 vs nulls 132/136); the repair carries the exclusion. [Case 139](case-file/139-hill-one-carving-error.md), [data](data/cycle151/), [tools](tools/cycle151/).

### I-006 — Which count-scored families already tolerate one error
- **Date / source:** 2026-11-08, cycle 151. `[repo]`
- **Rationale:** families scored by "best k of 24 crib letters" (cycles 148, 150, …) report the maximum agreement, so a configuration hit by one wrong letter would still show ≥ 22–23/24. Their exclusions are one-error-robust by construction; strict-consistency families are not.
- **Test:** read the code and scoring of each family; tabulate robust / not robust / partial. **Controls:** n/a. **Cost:** reading. **Status:** tested (cycle 151). **Result:** cycles 148 (constant digits) and 150 (zig-zag, incl. ordinary CT/PT autokey on A–Z/KRYPTOS behind the bank) are one-error-robust by design (K4 best 10/24 where ≥ 22 would be needed); strict families listed in [case 139](case-file/139-hill-one-carving-error.md) remain unaudited.

### I-007 — Columnar w 9–11 (all orders) × periodic key under one crib error
- **Source:** 2026-11-08, cycle 151 from I-003; strict result in cycles 124/126 ([case 112](case-file/112-all-orders-w9-w10.md), [114](case-file/114-quagmire-w9-10-and-all-w11.md)). `[repo]`
- **Hypothesis:** K3-style keyword columnar + K1-style Vigenère with one bad letter. **Test:** leave-one-crib-out in the exact DFS (24 runs, or a tolerant DFS). **Controls:** planted control with one corrupted letter; nulls. **Cost:** high (11! orders × 24); start with w 9–10. **Status:** queued.

### I-008 — Gromark / Periodic Gromark under one crib error
- **Source:** cycle 151 from I-003; strict in cycles 129–130 ([117](case-file/117-periodic-gromark.md), [118](case-file/118-periodic-gromark-unknown-keyword.md)). `[repo]`
- **Test:** leave-one-crib-out in the weighted union-find. **Controls:** planted ACA example with one corrupted letter. **Cost:** moderate. **Status:** queued.

### I-009 — Two-letter differences anchored to the archive charts
- **Source:** kryptosbot findings (Sep 2026): "two-character differences anchored to the archive were never run" `[sourced, secondary]`. Generic two-letter anomalies were tested direct only ([case 24](case-file/24-two-letter-anomalies.md)).
- **Test:** needs the archive's chart text to anchor the positions; without it the space (≈ 4,900 patterns × families) has low power. **Status:** blocked on I-002.

### I-010 — Quagmire IV with two different vocabulary alphabets
- **Source:** README coverage "still open" (Quagmire row); kryptosbot lists two-alphabet repeating keys as "not fully ruled out" `[sourced, secondary]`.
- **Test:** hash the 24-letter crib signature per bank permutation (cycle 132 method) and look up vocabulary alphabet pairs; p ≤ 16. **Controls:** planted QIV controls; 2 nulls. **Cost:** 10,056² pairs × periods: high; start themed × vocabulary. **Status:** queued.

### I-011 — Word-keyed zig-zag autokey; zig-zag + progressive shift
- **Source:** journal cycle 150 ideas; [case 138](case-file/138-zigzag-autokey.md) limits. `[speculation]`
- **Test:** the form sequence (Vig/Beau/variant) read from a word's letters (e.g. letter mod 3), CT feed exact count, direct and behind the bank. **Controls:** planted; nulls at full scale. **Cost:** ~10,000 words × cycle-150 cost/36: moderate. **Status:** tested (cycle 152).
- **Result (cycle 152):** tested as a strict **superset** — the form left free at every position (covers any word, any letter→form map mod 2 or 3, any phase, any cycle length), progressive step d = 0–25, CT and PT feed, L 1–96, A–Z/KRYPTOS, direct and behind the 165k bank both orders (4.58 × 10⁹ configs per text, ~4 min for three texts). CT feed with n ≥ 12 eligible cribs: K4 **0** configurations at m = n, n − 1 or (n ≥ 14) n − 2, nulls 0/0 → `EXACT-EXCL`, also under one wrong crib letter or one wrong carved letter. Best m 15 for K4 and both nulls. PT feed and CT lags with n ≤ 11: K4 inside null range → `LOW-POWER`. Controls 7/7 (incl. a corrupted-letter plant at 22/24), independently re-decrypted in Python with the word recovered from the vocabulary. [Case 140](case-file/140-free-form-zigzag-autokey.md), [data](data/cycle152/), [tools](tools/cycle152/) (commits e5aac61, 526dcdd, 4413bae). Follow-ups: I-042–I-045.

### I-012 — Hill with a key on the ciphertext side (`p = D·(c − f)`)
- **Source:** [case 132](case-file/132-hill-plus-periodic-key.md) limits. `[speculation]`
- **Test:** for short periods of f, enumerate f (26^k, k ≤ 3) and solve D linearly; exact. **Controls:** planted; nulls. **Cost:** 26^k × cycle-144 cost; k ≤ 2 cheap. **Status:** queued — candidate new structure.

### I-013 — Key change at a boundary keeping the width-7 phase
- **Source:** coverage row 93 (cycle 104), journal cycle 145. `[repo]` **Test:** two periodic keys of period 7 (or dividing 7k) switching at any boundary, exact per segment. **Cost:** small. **Status:** queued.

### I-014 — CT-autokey with both alphabets free
- **Source:** journal cycle 145. `[repo]` **Test:** SAT / union-find with both alphabets unknown, lags 1–21. **Controls:** planted random-alphabet controls; nulls (expect LOW-POWER at long lags). **Status:** queued.

### I-015 — Quagmire I/II/IV autokey, themed × vocabulary alphabets, behind the bank
- **Source:** journals 133–136. `[repo]` **Test:** cycle-136 tool with two different alphabets. **Cost:** moderate–high. **Status:** queued.

### I-016 — Periodic, both alphabets arbitrary, open periods
- **Source:** coverage row (cycle 11b). `[repo]` **Test:** SAT; expect underdetermination at P ≥ 8 (case 23 shows many wrong patterns SAT at P ≥ 6). Label LOW-POWER unless nulls are UNSAT. **Status:** queued.

### I-017 — Full-bank nulls for thin-baseline claims
- **Source:** cycles 140, 145, 147 used 1/10-bank null samples; cycle 149 ran the first full-bank null (F4). `[repo]`
- **Test:** rerun two shuffled nulls over the full bank for one slice of each. **Cost:** ~3–6 min each. **Status:** queued.

### I-018 — Gromark L ≥ 7 with arbitrary alphabets; Gromark behind transpositions
- **Source:** coverage table. **Status:** queued (likely LOW-POWER; needs language scoring).

### I-019 — Constant-digit keys, other readings
- **Source:** journals 148–149. `[speculation]` **Test:** triples mod 26, A=1..26 codings with carries, reversed and decimated streams, cycle-148 exact tool. **Cost:** small. **Status:** queued.

### I-020 — Phrase-keyed alphabets for the free-alphabet autokey tests
- **Source:** journal 149. `[speculation]` **Status:** queued (low expected value after the full vocabulary sweep came back at chance).

### I-021 — Mixed direction on a keyed alphabet; P ≥ 27 with bit-counted checks
- **Source:** journals 146–147. **Status:** queued.

### I-022 — Periods / lags 17–26 with dictionary or phrase completion
- **Source:** journals 135–136. **Status:** queued.

### I-023 — Columnar w 12–13 arbitrary orders × periodic key
- **Source:** coverage table. **Cost:** very high (12! = 4.8 × 10⁸ orders). **Status:** queued.

### I-024 — Bifid 6×6 / Trifid behind transpositions
- **Source:** coverage table; journal 145. **Status:** queued (crib-underdetermined: needs scoring).

### I-025 — Playfair p ≥ 8 arbitrary squares; Doppelkasten underdetermined configs
- **Source:** coverage table (cycles 68, 86). **Status:** queued (annealing, NO-SIGNAL at best).

### I-026 — Hill n = 6 behind transpositions; n = 5 arbitrary numbering; n ≥ 7
- **Source:** coverage table. **Status:** queued.

### I-027 — Linear-recurrence key L 5 (perms 20,000+), L 6 behind the bank
- **Source:** coverage table (cycles 80–81). **Status:** queued.

### I-028 — Multi-rotor / Hagelin exact feasibility
- **Source:** coverage table (cycles 96–97, 111). **Status:** queued.

### I-029 — Score for weakly constrained solutions
- **Source:** journal 138. **Status:** queued (method).

### I-030 — Physical measurement of the sculpture
- **Source:** kryptosbot mentions planned measurements `[sourced, secondary]`. **Status:** blocked (no access).

### I-039 — Hill under a dropped or extra carved letter
- **Date / source:** 2026-11-08, cycle 151 blind spot ([case 139](case-file/139-hill-one-carving-error.md)); K2's dropped S is the precedent `[sourced]`.
- **Hypothesis:** one carved letter missing or extra shifts the Hill block alignment after the slip. `[speculation]`
- **Test:** for each slip position d (≈ 98 + 97), rebuild the 96/98-letter stream (unknown letter = free variable in its block), solve rows exactly with a block-drop at the slip; direct first, bank for 96/98-letter permutations (`tools/export_perms_96_98.py`, cycle 24). **Controls:** planted Hill with one dropped / one extra letter. **Nulls:** two shuffles. **Cost:** direct seconds; bank ~200× cycle 151 (~2 h) → direct + model-Q first. **Status:** queued.

### I-040 — One-error audit of Hill + key and Hill n = 5
- **Source:** cycle 151 audit table. **Test:** add the block-drop + repair step to `hillvk.c` (cycle 144) and `hill5.c` (cycle 141). **Controls:** corrupted-letter plants. **Cost:** ~25× the strict runs (minutes). **Status:** queued.

### I-041 — One-error audit of strict vocabulary families behind the bank
- **Source:** cycle 151 audit table (cycles 135–137 Quagmire / autokey on 10,056 vocabulary alphabets, 146 mixed direction). **Test:** leave-one-crib-out in the crib-signature hash (24 hashes per permutation) or a ≥ 23/24 count. **Controls:** corrupted-letter plants; full-scale nulls (the tolerant test will admit more chance hits). **Cost:** 24× strict (tens of minutes). **Status:** queued.

### I-042 — Zig-zag over keyed (Quagmire) or affine alphabets
- **Source:** cycle 152 blind spot ([case 140](case-file/140-free-form-zigzag-autokey.md)). `[speculation]` **Test:** free form per position with KRYPTOS-keyed plain/cipher alphabets (Quagmire I–III indexing) or affine multipliers; same superset counter. **Controls:** planted; 2 full-scale nulls. **Cost:** small–moderate (×3 alphabet schemes). **Status:** queued.

### I-043 — Zig-zag autokey plus a periodic key
- **Source:** cycle 152 blind spot. `[speculation]` **Test:** free form, shift periodic with period p; each phase has ≈ 24/p cribs, so check power on nulls first (likely LOW-POWER above p ≈ 3). **Status:** queued.

### I-044 — Free-choice superset method for other per-letter choices
- **Source:** cycle 152 method (`[repo]`). Leaving a per-letter binary/ternary choice free costs only ×3 in chance matches per crib and stays exact. **Test:** per-letter choice of tableau (A–Z vs KRYPTOS), or of Vig/Beau on periodic keys behind the non-bank transposition families (rails, routes, AMSCO). **Controls:** planted; nulls. **Cost:** small. **Status:** queued.

### I-045 — Language-scored PT-feed / long-lag zig-zag
- **Source:** cycle 152 LOW-POWER part. **Test:** for crib-consistent PT-feed configurations, search the primer and forms by quadgram score (needs I-029's better score). **Status:** queued.

## Tested (historical, with links)
- **I-031** strip transposition (S6): [case 12](case-file/12-strips-and-periodic-keys.md) — negative; the strips lead itself downgraded.
- **I-032** one dropped / extra / changed / swapped letter × periodic KA/AZ key, direct and behind 165k transpositions; arbitrary alphabets P ≤ 5: [case 23](case-file/23-one-letter-anomaly.md) — EXACT-EXCL for p ≤ 18 behind the family; P ≥ 6 arbitrary LOW-POWER.
- **I-033** two-letter anomalies × direct KA/AZ periodic key: [case 24](case-file/24-two-letter-anomalies.md).
- **I-034** one-crib-error leave-one-out: [107](case-file/107-stepping-disk-one-crib-error.md), [108](case-file/108-quagmire-one-crib-error.md), [110](case-file/110-kryha-one-crib-error.md).
- **I-035** ptfree full vocabulary sweep: [127](case-file/127-pt-autokey-free-plain-alphabet-crib-links.md), [128](case-file/128-pt-autokey-free-plain-bank-words-601-3600.md), [133](case-file/133-ptfree-bank-3601-6800.md), [135](case-file/135-ptfree-bank-6801-9000.md), [137](case-file/137-ptfree-bank-9001-end-full-null.md) — K4 at chance (full-bank null only for the last slice).
- **I-036** zig-zag autokey: [138](case-file/138-zigzag-autokey.md); extended to free/word-keyed form sequences + progressive shift in [140](case-file/140-free-form-zigzag-autokey.md) (I-011). **I-037** constant digits: [136](case-file/136-constant-digit-running-keys.md). **I-038** mixed-direction periodic: [134](case-file/134-mixed-direction-periodic-key.md).

## Log
- 2026-11-08, cycle 151: file created (38 items: 30 open/blocked/in progress, 8 historical tested).
- 2026-11-08, cycle 151 end: I-001, I-005, I-006 tested; I-003 still in progress; added I-039–I-041 (41 items). Recommended next: cycle 152 new family I-011 (word-keyed zig-zag autokey) or I-012 (Hill with a key before the matrix); then the one-error audits I-007 / I-040.
- 2026-11-08, cycle 152: I-011 in progress at start, then tested (EXACT-EXCL for CT feed n ≥ 12, one-error tolerant; LOW-POWER for PT feed / long lags). Added I-042–I-045 (45 items). Recommended next: cycle 153 variant/audit — I-040 (one-error Hill + key / Hill 5) or I-007 (columnar w 9–10 × periodic key, one crib error); then new family I-012 or I-044.
