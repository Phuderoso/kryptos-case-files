/* Cycle 193 registered solver (IDEAS I-199 via pointer I-201): SANDWICH compound key on one or two tableaux behind the K3-law
   decimations/routes. Derived from cmp191.c (case 178) and the cycle-192 timing probe sw192probe.c (same core, mixed indices).
   Encryption (S1): pass 1 on tableau T1 with periodic key a (period m) at the PLAINTEXT index i, then K3's transposition (plaintext i is
   carved at S[i]), then pass 2 on tableau T2 with periodic key b (period n) at the CARVED index S[i]. Each pass is a Vig (x+k), Beau (k-x)
   or variant (x-k) step in that tableau's index space (variant is absorbed into the key sign), the letter handed over as a LETTER:
       z = s2*sigma(s1*x + a[i mod m]) + b[S[i] mod n],   x = T1idx(p), z = T2idx(c), sigma(y) = T2idx(T1[y]).
   S2 (the reverse index assignment): a at the carved index, b at the plaintext index (pass 1 keyed by the destination cell).
   For T1 = T2 the cipher is additive (one-tableau stacks with mixed indices, not covered by case 176); the solver is exact either way.
   Exact test: crib t is a BIJECTION between a[u] and b[v]; on every cyclic component of the residue graph all 26 root values are tried and
   propagated along a BFS spanning tree, every non-tree edge checked; tree components are always satisfiable.
   Chance meter (I-193): E_config = prod over cyclic components 26^(1-r_c) = exact expected number of solutions for uniform carved letters
   (z_t at distinct carved positions are independent). Printed per cell (H), per band e = round(-log26 E_config) (B) and, for the
   power/percentile question, per (model, m, n) band histogram of configs (G; the graph does not depend on tableau or form).
   Pairs: ordered (m, n), 2 <= m, n <= MM, INCLUDING m = n (with mixed indices m = n is not a single period): 625 at MM = 26.
   usage: cmp193 CT perms.bin tabpairs.txt label qlo qhi MM printE [sumtabs]
     sumtabs = 1: H lines summed over all tableau pairs of the file (tab name ALL) -> condensed output for C3
   out: M label q tabpair form model m n E_config nsol ; H label model tab form m n configs fits sols E ; B label band configs fits sols E ;
        G label model m n band configs ; END */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <omp.h>
static const char *PTC = "EASTNORTHEASTBERLINCLOCK";
static int CI[24];
#define NV 56   /* m + n <= 52 */
typedef struct { unsigned char typ, w, from, t; } Op;  /* typ 0: assign w from 'from' via edge t (G if w is a-side, F if b-side); typ 1: check F_t(val[w]) == val[from], w a-side, from b-side */
int main(int argc, char **argv) {
  if (argc < 9) { fprintf(stderr, "usage: cmp193 CT perms.bin tabpairs.txt label qlo qhi MM printE [sumtabs]\n"); return 1; }
  int SUMT = argc > 9 ? atoi(argv[9]) : 0;
  const char *ct = argv[1]; const char *lab = argv[4]; long qlo = atol(argv[5]), qhi = atol(argv[6]); int MM = atoi(argv[7]); double PE = atof(argv[8]);
  if (strlen(ct) != 97 || MM > 26) { fprintf(stderr, "bad args\n"); return 1; }
  for (int t = 0; t < 13; t++) CI[t] = 21 + t; for (int t = 0; t < 11; t++) CI[13 + t] = 63 + t;
  FILE *f = fopen(argv[2], "rb"); if (!f) return 2; fseek(f, 0, SEEK_END); long np = ftell(f) / (97 * 2); fseek(f, 0, SEEK_SET);
  short *P = malloc(np * 97 * 2); if (fread(P, 2, np * 97, f) != (size_t)(np * 97)) return 2; fclose(f);
  if (qhi > np) qhi = np; if (qlo < 0) qlo = 0;
  static char T1[64][27], T2[64][27], TN[64][64]; int nt = 0; char buf[256];
  f = fopen(argv[3], "r"); if (!f) return 2;
  while (fgets(buf, 256, f) && nt < 64) { char a[64], b[64], c[64]; if (sscanf(buf, "%63s %63s %63s", a, b, c) == 3 && strlen(a) == 26 && strlen(b) == 26) { memcpy(T1[nt], a, 27); memcpy(T2[nt], b, 27); strcpy(TN[nt], c); nt++; } } fclose(f);
  int pm[700], pn[700], npair = 0;
  for (int m = 2; m <= MM; m++) for (int n = 2; n <= MM; n++) { pm[npair] = m; pn[npair] = n; npair++; }
  int NC = 2 * nt * 4 * npair;   /* [model][tab][form][pair] */
  long long *cfg = calloc(NC, 8), *fit = calloc(NC, 8); double *sol = calloc(NC, 8), *esl = calloc(NC, 8);
  long long bc[30] = {0}, bf[30] = {0}; double bs[30] = {0}, be[30] = {0};
  long long *gh = calloc(2 * npair * 30, 8);
  static int X1[64][24], SIG[64][26], I2[64][26];
  for (int k = 0; k < nt; k++) { int i1[26]; for (int i = 0; i < 26; i++) { i1[T1[k][i] - 'A'] = i; I2[k][T2[k][i] - 'A'] = i; }
    for (int t = 0; t < 24; t++) X1[k][t] = i1[PTC[t] - 'A'];
    for (int y = 0; y < 26; y++) SIG[k][y] = I2[k][T1[k][y] - 'A']; }
  #pragma omp parallel
  {
    long long *lc = calloc(NC, 8), *lf = calloc(NC, 8); double *ls = calloc(NC, 8), *le = calloc(NC, 8);
    long long lbc[30] = {0}, lbf[30] = {0}; double lbs[30] = {0}, lbe[30] = {0};
    long long *lg = calloc(2 * npair * 30, 8);
    unsigned char (*F)[4][24][26] = malloc(64 * sizeof *F), (*G)[4][24][26] = malloc(64 * sizeof *G);
    #pragma omp for schedule(dynamic, 16)
    for (long q = qlo; q < qhi; q++) {
      const short *S = P + q * 97;
      for (int k = 0; k < nt; k++) for (int fm = 0; fm < 4; fm++) {
        int s1 = (fm & 2) ? -1 : 1, s2 = (fm & 1) ? -1 : 1;
        for (int t = 0; t < 24; t++) { int z = I2[k][ct[S[CI[t]]] - 'A'];
          for (int a = 0; a < 26; a++) { int y = ((s1 * X1[k][t] + a) % 26 + 26) % 26; int b = ((z - s2 * SIG[k][y]) % 26 + 26) % 26; F[k][fm][t][a] = b; G[k][fm][t][b] = a; } }
      }
      for (int md = 0; md < 2; md++) {
        int pos[24]; for (int t = 0; t < 24; t++) pos[t] = md == 0 ? CI[t] : S[CI[t]];
        for (int pi = 0; pi < npair; pi++) {
          int m = pm[pi], n = pn[pi], V = m + n;
          int eu[24], ev[24]; for (int t = 0; t < 24; t++) { int pp = CI[t], pc = S[CI[t]]; eu[t] = (md == 0 ? pp : pc) % m; ev[t] = m + (md == 0 ? pc : pp) % n; }
          int par[NV]; for (int x = 0; x < V; x++) par[x] = x;
          for (int t = 0; t < 24; t++) { int u = eu[t], v = ev[t]; while (par[u] != u) u = par[u]; while (par[v] != v) v = par[v]; if (u != v) par[u] = v; }
          int root[NV], ecount[NV], vcount[NV], touched[NV];
          for (int x = 0; x < V; x++) { int r = x; while (par[r] != r) r = par[r]; root[x] = r; ecount[x] = 0; vcount[x] = 0; touched[x] = 0; }
          for (int t = 0; t < 24; t++) { ecount[root[eu[t]]]++; touched[eu[t]] = 1; touched[ev[t]] = 1; }
          for (int x = 0; x < V; x++) if (touched[x]) vcount[root[x]]++;
          Op ops[16][32]; int nops[16], crt[16], ncy = 0; double cE = 1.0;
          for (int r = 0; r < V; r++) if (vcount[r] && ecount[r] > vcount[r] - 1) {
            int cyc = ecount[r] - vcount[r] + 1; cE *= pow(26.0, 1 - cyc);
            int deg[NV]; memset(deg, 0, sizeof deg); for (int t = 0; t < 24; t++) if (root[eu[t]] == r) { deg[eu[t]]++; deg[ev[t]]++; }
            int st = -1; for (int x = 0; x < V; x++) if (root[x] == r && touched[x] && (st < 0 || deg[x] > deg[st])) st = x;
            int asg[NV], used[24], qu[NV], qh = 0, qt = 0, no = 0; memset(asg, 0, sizeof asg); memset(used, 0, sizeof used);
            asg[st] = 1; qu[qt++] = st;
            while (qh < qt) { int x = qu[qh++];
              for (int t = 0; t < 24; t++) if (!used[t] && (eu[t] == x || ev[t] == x)) { int y = eu[t] == x ? ev[t] : eu[t];
                used[t] = 1;
                if (!asg[y]) { asg[y] = 1; qu[qt++] = y; ops[ncy][no++] = (Op){0, (unsigned char)y, (unsigned char)x, (unsigned char)t};
                  for (int t2 = 0; t2 < 24; t2++) if (!used[t2] && (eu[t2] == y || ev[t2] == y)) { int o = eu[t2] == y ? ev[t2] : eu[t2];
                    if (asg[o]) { used[t2] = 1; ops[ncy][no++] = (Op){1, (unsigned char)eu[t2], (unsigned char)ev[t2], (unsigned char)t2}; } } }
                else ops[ncy][no++] = (Op){1, (unsigned char)eu[t], (unsigned char)ev[t], (unsigned char)t}; } }
            nops[ncy] = no; crt[ncy] = st; ncy++;
          }
          int band = ncy ? (int)lround(-log(cE) / log(26.0)) : 25; if (band < 0) band = 0; if (ncy && band > 24) band = 24;
          lg[(md * npair + pi) * 30 + band]++;
          for (int k = 0; k < nt; k++) for (int fm = 0; fm < 4; fm++) {
            int c4 = ((md * nt + k) * 4 + fm) * npair + pi; lc[c4]++; le[c4] += cE; lbc[band]++; lbe[band] += cE;
            double ns = 1.0; int ok = 1;
            for (int c = 0; c < ncy && ok; c++) { int cnt = 0;
              for (int rho = 0; rho < 26; rho++) { unsigned char val[NV]; val[crt[c]] = rho; int good = 1;
                for (int o = 0; o < nops[c]; o++) { Op op = ops[c][o];
                  if (op.typ == 0) val[op.w] = op.w < m ? G[k][fm][op.t][val[op.from]] : F[k][fm][op.t][val[op.from]];
                  else if (F[k][fm][op.t][val[op.w]] != val[op.from]) { good = 0; break; } }
                cnt += good; }
              if (!cnt) ok = 0; ns *= cnt; }
            if (ok) { lf[c4]++; ls[c4] += ns; lbf[band]++; lbs[band] += ns;
              if (cE <= PE) {
                #pragma omp critical
                printf("M %s %ld %s %c%c %c %d %d %.4g %.0f\n", lab, q, TN[k], (fm & 2) ? 'B' : 'V', (fm & 1) ? 'B' : 'V', md ? '2' : '1', m, n, cE, ns);
              } }
          }
        }
      }
    }
    #pragma omp critical
    { for (int i = 0; i < NC; i++) { cfg[i] += lc[i]; fit[i] += lf[i]; sol[i] += ls[i]; esl[i] += le[i]; }
      for (int i = 0; i < 30; i++) { bc[i] += lbc[i]; bf[i] += lbf[i]; bs[i] += lbs[i]; be[i] += lbe[i]; }
      for (int i = 0; i < 2 * npair * 30; i++) gh[i] += lg[i]; }
  }
  if (!SUMT) for (int md = 0; md < 2; md++) for (int k = 0; k < nt; k++) for (int fm = 0; fm < 4; fm++) for (int pi = 0; pi < npair; pi++) {
    int c4 = ((md * nt + k) * 4 + fm) * npair + pi;
    printf("H %s %c %s %c%c %d %d %lld %lld %.6g %.6g\n", lab, md ? '2' : '1', TN[k], (fm & 2) ? 'B' : 'V', (fm & 1) ? 'B' : 'V', pm[pi], pn[pi], cfg[c4], fit[c4], sol[c4], esl[c4]);
  }
  else for (int md = 0; md < 2; md++) for (int fm = 0; fm < 4; fm++) for (int pi = 0; pi < npair; pi++) {
    long long c = 0, x = 0; double s = 0, e = 0;
    for (int k = 0; k < nt; k++) { int c4 = ((md * nt + k) * 4 + fm) * npair + pi; c += cfg[c4]; x += fit[c4]; s += sol[c4]; e += esl[c4]; }
    printf("H %s %c ALL %c%c %d %d %lld %lld %.6g %.6g\n", lab, md ? '2' : '1', (fm & 2) ? 'B' : 'V', (fm & 1) ? 'B' : 'V', pm[pi], pn[pi], c, x, s, e);
  }
  for (int md = 0; md < 2; md++) for (int pi = 0; pi < npair; pi++) for (int b = 0; b < 30; b++) if (gh[(md * npair + pi) * 30 + b])
    printf("G %s %c %d %d %d %lld\n", lab, md ? '2' : '1', pm[pi], pn[pi], b, gh[(md * npair + pi) * 30 + b]);
  for (int i = 0; i < 26; i++) if (bc[i]) printf("B %s %d %lld %lld %.6g %.6g\n", lab, i, bc[i], bf[i], bs[i], be[i]);
  printf("END %s perms %ld-%ld tabpairs %d pairs %d\n", lab, qlo, qhi, nt, npair);
  return 0;
}
