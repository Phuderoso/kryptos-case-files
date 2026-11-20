"""Chunk B of PREREG221 / PREREG222: families IG, BC of keys221.bin (frozen in cycle 221) -> keys222b.bin / keys222b.tsv (full_id kept).
Chunk A (IT, MC, MV, MB, EB, EN; 7,012 windows) was run in cycle 221 (case 207)."""
rows = [l.rstrip('\n').split('\t') for l in open('keys221.tsv')][1:]
K = open('keys221.bin', 'rb').read(); B = {'IG', 'BC'}
with open('keys222b.bin', 'wb') as f, open('keys222b.tsv', 'w') as g:
    g.write('id\tfull_id\tfamily\tsource\toffset\n'); n = 0
    for r in rows:
        if r[1] in B:
            i = int(r[0]); f.write(K[i * 97:(i + 1) * 97]); g.write(f'{n}\t{r[0]}\t{r[1]}\t{r[2]}\t{r[3]}\n'); n += 1
print('chunk B', n)
