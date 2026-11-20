"""Chunk A of PREREG221: families IT, MC, MV, MB, EB, EN of keys221.bin -> keys221a.bin / keys221a.tsv (full_id kept).
Chunk B (IG, BC; 5,762 windows) is deferred to a later cycle because the whole list exceeds the 8-minute budget."""
rows = [l.rstrip('\n').split('\t') for l in open('keys221.tsv')][1:]
K = open('keys221.bin', 'rb').read(); A = {'IT', 'MC', 'MV', 'MB', 'EB', 'EN'}
with open('keys221a.bin', 'wb') as f, open('keys221a.tsv', 'w') as g:
    g.write('id\tfull_id\tfamily\tsource\toffset\n'); n = 0
    for r in rows:
        if r[1] in A:
            i = int(r[0]); f.write(K[i * 97:(i + 1) * 97]); g.write(f'{n}\t{r[0]}\t{r[1]}\t{r[2]}\t{r[3]}\n'); n += 1
print('chunk A', n)
