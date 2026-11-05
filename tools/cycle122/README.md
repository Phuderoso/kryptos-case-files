# Cycle 122 — Kryha one-crib-error audit

Leave-one-out / soft_only audit of cycle 114's Kryha exclusions (B1 any V1 wheel,
B2 V2 any holes, A published wheels with free alphabets), in the spirit of
cycles 119–120.

## Build

```bash
gcc -O3 -o /workspace/k4c122/b1_loo122 tools/cycle122/b1_loo122.c
gcc -O3 -o /workspace/k4c122/v2_loo122 tools/cycle122/v2_loo122.c
```

## Run

```bash
mkdir -p /workspace/k4c122
python3 tools/cycle122/run122.py
# writes data/cycle122/{run122.log,histograms.txt,controls.txt}
# large raw pair dumps: /workspace/k4c122/{b1,b2}_raw.out and
#   /home/box/kryptos_support_backup/cycle122/ (not committed)
```

Needs `tools/cycle114/kryha114.py`, `testB114.py`, and `data/cycle114/a264.txt`.

## Metrics

For each alphabet pair × sense:

- **strict** — consistent with all 24 crib letters (cycle 114's test)
- **soft_only** — fails strict, but consistent after dropping exactly one crib

Soft adjacent-step logic for B1 ignores merged two-step constraints across a
dropped middle letter (lower-bound / cycle-119 spirit).

## Controls

- `ctl1_clean` / `ctl2_clean`: planted Kryha V1 / V2 → strict recovers
- `ctl1_flip` / `ctl2_flip`: one crib ciphertext letter flipped → strict 0,
  soft_only recovers
- `ctlA_clean` / `ctlA_flip`: published 17-sector wheel, free alphabets

Plus 5 shuffled-ciphertext nulls.
