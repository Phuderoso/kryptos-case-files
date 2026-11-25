# Case 224 — Audit of every frozen key list: degeneracy detector, independent digit streams, full-scale nulls (cycle 238)

**Slot:** audit (237 free, 239 new family, 240 free; I-381). Idea **I-382** (degeneracy part tested here; value part split off as **I-383**), closes the case 223 stride-10 deviation; new **I-383–I-385**.
Pre-registered as [PREREG238](../tools/cycle238/PREREG238.md) (local commit 92985bc, 2026-11-24 19:45 MST, before `audit238.py` touched any published list and before any null). Base: origin/main **20f9948** (c237 already published there, tree 8fb12327). Code: [`tools/cycle238/`](../tools/cycle238/) (`audit238.py`, `plant238.py`, `calN.py`, `indep238.py`, `srcscan238.sh`, `mknull238.py`, `runB.sh`, `HASHES238.txt`); `gn217` **unchanged** (source sha 97bae55f…d792); results (stamped, rule 5): [`data/cycle238/`](../data/cycle238/).
**Verdict: no solution, no new bug.** The nine frozen lists (85,818 windows) hold **no silent-truncation family other than the S18 already repaired in case 223**. Every other flagged family is arithmetic or designed. Two fresh nulls at full scale: 0 hits. K4 was not re-run (the published K4 results on these lists stand; the tool and lists are unchanged).

## Why this audit
Cases 219 / 220 carried a silent bug for 15 cycles: the look-and-say generator stopped at 10⁵ characters and returned 0, so 94 of 136 key positions were zero. It surfaced by chance. Every `EXACT-EXCL` label rests on the window list behind it, so one frozen detector over every published list checks the premise of ~20 exclusions at once.

## Method (`audit238.py`, thresholds frozen in PREREG238)
Per 97-value window: **CONST60** (most common value ≥ 60), **DISTINCT3** (≤ 3 distinct values), **TAILRUN / HEADRUN** (≥ 10 identical at the end / start; **ZEROTAIL** if zeros), **RUN20**, **SEATCONST** (the 24 crib seats equal), **BLOCKCONST** (one crib block equal), **PERIOD12** (exactly periodic, period ≤ 12), and duplicates within and across lists. Lists: keys217, keys218, keys221a + keys222b (= keys221.bin), keys233, keys234, keys236, keys237. Tags come from the `.tsv` files.

| gate | result |
|---|---|
| **P** plants (seed **209706**): 20 clean random windows + 40 defective (zero tail, clamp / size cap, constant, 3-valued, head run, seat-constant, block-constant, periodic; 5 each) | every defective window carries its **expected** flag **40 / 40**; clean flagged **0 / 20** |
| **N** 100,000 random windows over Z₂₆ (seed **209709**) | **0** flagged (the null: any real flag is structural) |
| **known positive** old S18 rows of keys233 (the case 219 bug) | **160 / 160** flagged (BLOCKCONST 160, CONST60 148, run / tail flags by direction; PREREG238 said "ZEROTAIL" but only the c = 0 forward rows end in zeros, the c = 1 rows end in 1s and the reversed rows start with the run, all caught by BLOCKCONST / HEADRUN / TAILRUN) |

Duplicates: **0** within any list and **0** across lists (85,818 distinct windows; keys221 = keys221a + keys222b).

## Findings (flagged families, read by hand against the generators)
| family (list) | flagged | class | cause |
|---|---|---|---|
| S18 look-and-say (keys233 / keys234) | 160 / 160, 800 / 800 | **BUG, already repaired** | 10⁵-character cap (`keys233.py` line 72), zeros after term 42; case 223 redid it exactly (keys237, 960 windows, 0 flags) |
| S12 Catalan (keys233 / 234) | 160, 800 | ARITHMETIC | C_n ≡ 0 mod 26 for 79 of n ≤ 136 (Kummer), long zero runs; known since case 223 |
| S14 Möbius, S9 Thue–Morse, S17 Kolakoski (keys233 / 234) | all windows | ARITHMETIC | values only in {0, ±1}, {0, 1}, {1, 2} |
| S3 π(n) (20 windows keys233, 100 keys234) | tail / head runs | ARITHMETIC | prime-counting steps: runs of 10 equal values at gaps ≥ 10 (n ≈ 114–127) |
| short cyclic keys (keys217 K2 / dates / years; keys221a EN / MC / MB / IT / EB; keys222b BC; keys236 L16) | PERIOD12, DISTINCT3, some CONST60 | DESIGN | the named strings are short (4–14 symbols) and read cyclically; a periodic key of period ≤ 12 is also inside the Gromark / periodic exclusions (cases 143, 202, 214, 216); cross-check → I-384 |
| `D3 U:CIA` (keys218), `BC g8:y1986` (keys222b) | 1, 2 windows fully constant | DESIGN | 3-digit grouping of a 3-letter string gives one value; period-1 keys (long excluded) |
| MC (keys221a) | 27 windows DISTINCT3 / CONST60 without exact period ≤ 12 | DESIGN | Morse element counts (1–5) of words ≥ 13 letters, low-entropy by construction |

**Source scan** (`srcscan238.sh`, [`data/cycle238/srcscan238.txt`](../data/cycle238/srcscan238.txt)): the only size cap that changes values is `keys233.py` line 72 (S18, repaired). The digit caps in keys217 (`[:700]`, offsets 0–399 + 194 < 700) and keys218 (`[:900]`) never wrap; `return 0` in keys233 line 43 is the Möbius value for non-squarefree n.
**Independent value check (extra, disclosed; PREREG238 §A promised only the detector):** `indep238.py` regenerates the seven keys217 long digit streams with plain integers (π by Machin, e by series, √2 √3 √5 φ by integer sqrt, ln 2 by series; no mpmath) and compares **5,600 of 5,600** long-stream windows with the published `keys217.bin`: **0 mismatches**. The 270 short-stream (cyclic) windows and the other lists were *not* value-checked → I-383.

## Part B — full-scale nulls (closes the case 223 deviation)
`runB.sh`: two fresh shuffled K4 texts (**209707, 209708**), `gn217` on `keys237.bin`, all rows (stride 1), hit = ≥ 23 / 24 seats:

| scope | rows | pair-forms | hits (24 / 23), null 209707 | null 209708 |
|---|---|---|---|---|
| direct | 1 | 2.17 × 10¹³ | 0 / 0 | 0 / 0 |
| bank | 165,065 | 4.11 × 10¹⁰ (tool printout) | 0 / 0 | 0 / 0 |
| all.bin | 165,782 | 4.13 × 10¹⁰ (tool printout) | 0 / 0 | 0 / 0 |

(`pairforms` is the tool's own printout; its unit differs between the direct and the row scopes, as in case 223's table, which multiplies by the 960 windows. Hits are the content.) Wall 330 s total for the two nulls (166 s + 164 s), own process group (`setsid timeout 700`). Machinery check only (two nulls, no tail claim): the case 223 row-stride-10 deviation is **closed**; full-scale nulls on keys237 give 0, as the 24-seat filter predicts (≪ 1 chance hit per text).

## Reading and labels
- Degeneracy audit: `CLEAN` for keys236, keys237 and the sequence rows of keys233 / 234 other than S3, S9, S12, S14, S17, S18; every other flag is ARITHMETIC or DESIGN. Old S18 rows remain what case 223 said (look-and-say, then zeros). **No old label changes**; a clean list does not enlarge the scope of its `EXACT-EXCL` (list, model Q, stated assumptions).
- Unflagged ≠ correct: the detector sees degeneracy, not wrong-but-varied values. Only the keys217 long digit streams have an independent value check so far.
- No K4 re-run, no hit lines, so the I-342 NC bar was not exercised.

## Compute
Detector on 85,818 windows 4 s; gates < 2 s; independent digit check < 1 s; Part B 330 s (own process group). No other processes touched.

## News check (2026-11-24)
No new solution. Public state unchanged: plaintext from Sanborn's papers sealed (Smithsonian, until 2075) and the archive sold for $962,500 (RR Auction, 20 Nov 2025) `[secondary, relatablehistory.com 2026-11-04]`; Paradigm holds the secret behind a $1 verifier (blog 2026-06-12, Robinson / Huang) `[primary]`. Community items: glthr.com "W-rectangle and its half-turn" (published 2026-11-11, updated 2026-11-15: five W's on a rectangle in rows of 19, cribs on its edges; the author states it does not decipher K4 and that AR / ZZ are unexplained) `[community, unverified]`; a Waggle post framing K4 as an agent task (no result) `[community]`. Nothing here changes a label; the rows-of-19 / W-corner structure could be a future structural check (not queued as a test yet; follow-up noted in I-385 context).

## Blind spots
Value correctness of keys218 / 233 / 236 sequences (I-383); window offsets and multipliers outside each list; flagged-by-design windows vs the periodic exclusions (I-384); the detector's thresholds are descriptive (10 / 20 / 60 / 3 / 12), a window can be degenerate in other ways (e.g. two-valued alternation of period 13+); case 219 / 220 S18 rows are still the zero-tail rows (superseded by case 223).
