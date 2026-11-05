#!/bin/sh
# Cycle 97: single-rotor test (tools/cycle96/rotor.c) behind K3-law decimations and K3-grid routes.
# Perm files are int16 x97 per perm, perm[j] = carved position of plaintext letter j.
#   dec_perm.bin   159,712 decimations (cycle 59 generator, M=97..112, dec and enc directions)
#   route_perm.bin   6,070 spiral/diagonal/serpentine routes (cycle 61/62)
#   perms97.bin    165,065 transpositions (support backup; family from earlier cycles)
#   tw264.bin      264 themed alphabets (AZ, KA, word-keyed); azka.bin = first two (AZ, KA)
K=OBKRUOXOGHULBSOLIFBBWFLRVQQPRNGKSSOTWTQSJQSSEKZZWATJKLUDIAWINFBNYPVTTMZFPKWGDKZXTJCDIGKUHUAUEKCAR
python3 ctl97.py > controls.txt   # planted ciphertexts
./rotor $K tw264.bin 264 1 dec_perm.bin
./rotor $K tw264.bin 264 4 route_perm.bin
./rotor $K tw264.bin 264 4 route_perm.bin R
./rotor $K azka.bin 2 4 perms97.bin
./rotor "$(sed -n 1p nulls.txt)" tw264.bin 264 4 route_perm.bin   # shuffled-K4 null, seed 9400
