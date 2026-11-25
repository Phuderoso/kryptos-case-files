# PREREG239 — Cycle 239 (new family): I-379 audioactive digit streams

Filed 2026-11-25 03:40 MST (UTC−7), **before** any plant, null or K4 run with `keys239.bin`. Base: origin/main **6cd742e** (c238 published). Case file 225.
Slots (I-385): **239 new family**, 240 free (I-368, I-371, I-380), 241 audit. Seeds: plants **209710**, nulls **209711–209716**; next free after this cycle **209717**.

## Why this family (choice among I-379 / I-375 / I-313 / I-336)
- **I-379 chosen**: the only candidate whose source data is exact and already validated in the repo (case 223 derived Conway's 92 atoms in code, OEIS A005341 0 mismatches to n 3000), so the window list can be built without transcription risk; cost < 5 min; continues the case 223 blind spot (the *string*, not the length).
- I-375 (wider compass) needs foreign-language rose tables (transcription risk) and is a widening of a family already at 0 hits; I-313 needs PK8 / PK9 ciphertexts verified first (secondary sources); I-336 Selectric needs a primary typeball layout. All stay queued.
- K1–K3 fit is weak and stated as such (`[speculation]`): look-and-say is a "count what you see" rule (the kind of layered, simple, explainable-by-hand rule Sanborn's K1–K3 use), digits 1–3 read as shifts B–D (or A–C) on the KRYPTOS-keyed / themed alphabets, and digit pairs (I-304 style) give full-range keys. No source says Sanborn used it.

## Disclosed before filing
- `gn217.c` unchanged (sha 97bae55f…d793; binary copied from the case 224 work dir). No search was run before filing; no timing smoke.
- `las_exact.py` = case 223 file (sha 1dc74c3e…4292). `conway_table.py` parses Conway's element table from the Wikipedia article "Look-and-say sequence" (raw wikitext fetched 2026-11-25, `data/cycle239/las_wiki.txt`, sha 7e99db3e…f047, CC BY-SA, cited as `[secondary]`). Checks in `keys239.py` (all pass): the 92 atoms **derived in code** equal the 92 table strings as a set; every derived decay list equals the table's "decays into" column; the element sequences of terms 8–21 concatenate back to the term strings exactly; term 8 = Hf.Sn (Conway).
- Frozen list: `keys239.bin` sha256 **4bcec305…00ae**, **6,810 windows** (`keys239.tsv` sha b92b45dc…870d); 94 candidates dropped as duplicates (of earlier lists keys217 / 218 / 221 / 221a / 222b / 233 / 234 / 236 / 237 or earlier in this list).
- `plants239.tsv` (sha ef1fb7d4…245e, seed 209710) and `nulls239.tsv` (sha 97bb8c84…05b9) generated before filing, not run. Plant windows by family: ELEMD1 5, LSTERM18 3, ELEMZ 2, LSCAT 2, LSTERM20 2, LSTERM21 2, PAIRCAT 1, S18PAIR 1, LSTERM17 1, LSTERM19 1.

## Window families (all fwd, 97 values, mod 26; term 1 = `1`)
| family | stream | windows |
|---|---|---|
| LSCAT | digits of T1 T2 T3 … concatenated; k_i = d_{o+i} + c, o 0–499, c ∈ {0, 1} | 1,000 |
| LSTERM16–21 | digits of term n (lengths 102, 134, 176, 226, 302, 408) read cyclically from every offset o, k = d + c | 2,602 |
| PAIRCAT | LSCAT in two-digit groups from offset o: k_i = (10 d_{o+2i} + d_{o+2i+1}) mod 26, o 0–399 | 400 |
| PAIRT21 | term 21 cyclic in two-digit groups, o 0–407 | 408 |
| ELEMZ | element stream (element sequences of terms 8, 9, 10, … concatenated), k_i = Z_{o+i} + c (Z = Conway atomic number 1–92: H = 1 … U = 92), o 0–499, c ∈ {0, 1} | 1,000 |
| ELEMD1 | same element stream, first digit of each element string + c | 1,000 |
| S18PAIR | decimal digits of S18(1) S18(2) … (exact, case 223) in two-digit groups, o 0–399 | 400 |

## Degeneracy audit (I-382, `audit238.py` unchanged, sha 07dc85bc…1970) — pasted output (S / L / D lines; F lines in `data/cycle239/audit239.txt`)
```
S k239 ELEMD1 windows 1000 ANY 1000 BLOCKCONST=2 CONST60=732 DISTINCT3=1000 HEADRUN=4 TAILRUN=4
S k239 ELEMZ windows 1000 ANY 0
S k239 LSCAT windows 1000 ANY 1000 DISTINCT3=1000
S k239 LSTERM16 windows 188 ANY 188 DISTINCT3=188
S k239 LSTERM17 windows 190 ANY 190 DISTINCT3=190
S k239 LSTERM18 windows 352 ANY 352 DISTINCT3=352
S k239 LSTERM19 windows 452 ANY 452 DISTINCT3=452
S k239 LSTERM20 windows 604 ANY 604 DISTINCT3=604
S k239 LSTERM21 windows 816 ANY 816 DISTINCT3=816
S k239 PAIRCAT windows 400 ANY 0
S k239 PAIRT21 windows 408 ANY 0
S k239 S18PAIR windows 400 ANY 0
L k239 windows 6810 distinct 6810 sha256 4bcec305f6e48d5e
S keys237 keys237 windows 960 ANY 0
L keys237 windows 960 distinct 960 sha256 b43e35dbd1d2bf3e
D within-list duplicate windows 0 cross-list duplicates (first occurrence elsewhere) 0
```
Reading (frozen now): DISTINCT3 on every single-digit window is **DESIGN** (look-and-say strings use only 1, 2, 3). ELEMD1 CONST60 (732 / 1000) is **DESIGN** (most Conway elements start with `1`), not a size cap: the stream is built from exact strings with no cap (asserts on length). No TAILRUN / ZEROTAIL in any long-stream family; no BUG flag. No SEATCONST.

## Model and commands (as cases 219–223)
`gn217` model Q, forms Vig / variant / Beaufort, hit = ≥ 23 / 24 crib seats (EASTNORTHEAST 0-based 21–33, BERLINCLOCK 63–73); scopes direct (86,731² `alpha.bin`), bank (165,065 rows), all.bin (165,782 rows), 144² `themed144.bin`.
`runA.sh`: K4 full scale in all three scopes; 6 nulls direct full, bank / all.bin at **row stride 10** (declared now; full-scale nulls would exceed the 8-minute budget). `runP.sh`: gate P (ids 0–7 direct, 8–13 bank, 14–19 all.bin; odd ids carry one corrupted crib letter → 10 one-error plants; Y stride 1000 / row stride 2000 slices), `check237.py` unchanged (sha 42e8ad28…b142) for gate T. Whole run in its own process group under `setsid timeout 600`.

## Gates and labels (frozen)
- **P:** 20 plants, pass ≥ 19 / 20 recovered with planted (w, form, X, Y, perm), Wilson reported. **T:** `check237.py` re-derives agreement for every H line and decrypts all 97 letters; mismatches 0.
- **I-342 NC bar** for any decrypted K4 / null H line: bar(nq, N) = −6.8417 + 0.0786 ln N + 0.00027 (ln N)² − 0.0192 nq + 0.879, N = max(10, H lines in scope); candidate only if NC ≥ bar **and** the 97 letters read as English (both cribs at the official positions).
- **Labels:** K4 0 hits with P passing → `EXACT-EXCL` within the frozen list and model (one wrong crib letter tolerated); hits failing the bar and null-like → `NO-SIGNAL`; P failing → `INSUFFICIENT-DISCRIMINATION`. The six nulls calibrate false hits (machinery), not power.

## Honesty clause
Any plain-English decrypt with both cribs at the official positions and NC ≥ bar is reported prominently and reproduced independently before being called a solution. Nothing is submitted anywhere.
