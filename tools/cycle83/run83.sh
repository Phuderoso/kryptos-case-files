#!/bin/bash
# Cycle 83 runner (resumable: finished entries in results83.jsonl are skipped). Needs python-sat (CaDiCaL 1.5.3).
cd "$(dirname "$0")"
python3 mknull83.py && python3 mkctl83.py
# done this cycle: controls at their true configuration; K4 at p 4,5,6 x 12 configs (covers p 1-6); 4 null runs at p 6
python3 run83.py ctl0:4:KA/0/0 ctl1:5:AZ/1/1 ctl2:6:KA/2/1 ctl3:6:AZ/0/0 K4:4,5,6:all null0:6:KA/0/0 null1:6:KA/0/0 null0:6:AZ/1/1 null1:6:AZ/1/1
# checkpoint for cycle 84: p 7 and 8 (p 8 covers 1,2,4,8; with 5,6,7 this closes p <= 8)
# python3 run83.py K4:7,8:all null0:7:KA/0/0 null1:7:KA/0/0
python3 summarize83.py
