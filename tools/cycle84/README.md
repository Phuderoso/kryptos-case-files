# Cycle 84 tools
Resumes cycle 83's arbitrary-square Playfair SAT run. Copy `tools/cycle83/*` next to these files, then:
- `python3 mkctl84.py` builds two planted controls (p 7 AZ/Beaufort/even, p 8 KA/Vigenère/odd; seed 8401). Append them to `controls83.json` as ctl4 and ctl5 (cycle 84 did this in its scratch copy).
- `./run84.sh` runs controls, then K4 p 7 and 8 (all 12 configs), then nulls, under an 8-minute `timeout`. Finished jobs in `results83.jsonl` are skipped, so it resumes.
Note: `timeout` kills only the parent; run `pkill -f "python3 run83.py"` afterwards to stop orphaned pool workers.
