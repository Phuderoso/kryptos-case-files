# 22 — Plaintext-autokey chains scored by English (cycle 23)
> *The algebra went quiet at the long lags. So I made the chains talk instead and listened for English. Mostly I heard the noise floor, and I'm writing down how loud it was.*

## 1. Why
Cycle 22 ([case file 21](21-plaintext-autokey-chains.md)) showed that with a fixed tableau each crib letter fixes its whole residue chain mod L, but at lags 24–34 and 48–96 two cribs rarely share a chain, so the exact test is blind. The chains still produce **derived plaintext letters** (often the crib blocks shifted by L). If K4 were plaintext autokey at such a lag, those derived fragments would read as English.

## 2. Test (`tools/ptak_score.c`)
For every fully crib-consistent configuration (lags 24–96, KRYPTOS-keyed and straight tableau, Vigenère/Beaufort/variant, Model A = autokey then transpose, Model B = transpose then autokey), collect the derived letters and score them with quadgrams (mean log-probability over 4-letter windows). Two scorings: **strict** (windows made only of derived letters) and **loose** (windows containing at least one derived letter, crib letters allowed). Two search sizes:
- **Family run:** cycle 19's 165,064 transpositions plus the identity, 144.6M configurations, about 21–22M scorable. Controls, nulls and K4: `tools/ptak_score_controls.py` → `analysis/ptak_score_report.txt`.
- **Direct run:** identity only (autokey applied straight to the carved text), 876 configurations, about 250 scorable. `tools/ptak_identity_controls.py` → `analysis/ptak_identity_report.txt`.

## 3. Results
| Run | Planted controls | Shuffled-K4 nulls (best) | K4 (best) |
|---|---|---|---|
| Family, strict | **0 of 6** in top 20 | −3.55 to −4.11 (6 nulls) | −4.22 (below every null) |
| Family, loose | 2 of 6 in top 20 (ranks 2, 15) | −4.16 to −4.47 | −4.28 (inside nulls) |
| Direct, strict / loose | 2 / 4 of 12 ranked first; the misses are lags ≥ 77 (almost no derived letters) and one at L=43 | −5.60 to −7.41 (20 nulls) | −7.10 (at the bottom of the null range) |

K4's best direct fragments (`ILMNSK…SHRINHBO`, `KORNA…WUMRPMA`) are not English.

## 4. Verdict
| Hypothesis | Status |
|---|---|
| Plaintext autokey applied **directly** to the carved text, lags 24–~70, fixed KA/AZ tableau | **negative** (K4 scores below shuffled nulls; controls recovered where fragments are long enough) |
| Same behind columnar w ≤ 8 / K3-style rotations | **inconclusive**: with ~22M scorable configurations and fragments of 6–13 letters, chance fragments outscore true ones; controls fail, so this test has no power here |
| Lags ≳ 75 | **untestable** with 24 cribs: the chains leave almost no derived letters |

Honest limits: K4's family result is *not* evidence against the model, only evidence that this scoring cannot see it. A stronger test would need more known plaintext (or a smaller, motivated transposition set).
