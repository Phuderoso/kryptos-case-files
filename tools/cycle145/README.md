# Cycle 145 tools

Variant run of cycles 139–140. No new solver: `tools/cycle139/ptfree.c` is reused unchanged
(same thresholds: at least 5 crib-to-crib checks; 23.5 bits when the key is read through the
free plain alphabet, z = x). `run_cycle145.sh` feeds it all.txt words 3601–6800 as keyed
alphabets behind all 330,130 bank permutations, carved order and model Q.

Controls are cycle 139's (`data/cycle139/controls_check.txt`, 5/5 above threshold); the
binary and thresholds are identical, so they were not re-run.
