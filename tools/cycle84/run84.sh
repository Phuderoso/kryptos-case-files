#!/bin/bash
# Cycle 84: resumes cycle 83's checkpoint. Controls at p 7/8 first, then K4 p 7 and 8 (all 12 configs), then nulls.
cd "$(dirname "$0")"
TO=${TO:-240} timeout ${BUDGET:-480} python3 run83.py ctl4:7:AZ/1/0 ctl5:8:KA/0/1 K4:7,8:all null0:7:KA/0/0 null1:7:KA/0/0 null0:6:KA/0/0
