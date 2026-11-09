/* Cycle 192 (IDEAS I-197): one-error audit of case 178. Compound key on two different tableaux (case 178's family):
       z = s2*sigma(s1*x + a[i mod m]) + b[i mod n]     (x = T1idx(p), z = T2idx(c), sigma(y) = T2idx(T1[y]), s1, s2 = +-1)
   behind the K3-law decimations/routes, key on the plaintext index (P) or the carved index (C).
   ONE-ERROR scope: a config fits if the 24 crib bijections are consistent after deleting at most one crib slot t (one wrong carved or
   crib letter anywhere in the cribs: an edge whose letter is unknown imposes no constraint, so a wrong letter = a deleted edge).
   Exact. Unlike the additive case (cycle 190), a BRIDGE between two cyclic parts constrains a bijection graph (each part keeps only some
   root values), so every slot is tried, not one per series class. Deleting t changes only t's connected component K, and pendant trees
   never constrain, so the deletions of K are reduced to the distinct 2-cores of K - t (deduplicated by edge mask).
   Fit: every cyclic component of G consistent (strict), or exactly one component K fails and some distinct core of K - t is consistent.
   Chance meter (I-193 for one error): with independent uniform carved letters, E[sols(H)] = prod over cyclic components 26^(1-r) for
   any subgraph H (cycle 191). Fit = union over (K, d) of {G\K consistent and core d consistent}, so
       P(fit) <= U = sum_K sum_d (E_G / E_K) * E_d   (capped at 1; U = 1 if G has no cycle)
   and the statistic S1 = sum_K sum_d sols(G\K) * sols(d) has EXACT expectation U (checked on random texts in meter mode).
   usage: cmp192 CT perms.bin tabpairs.txt label qlo qhi pairs.txt printU mode
     pairs.txt: lines "md m n" (md P or C) or the word ALL (all ordered m != n, 2..26, both models)
     mode 0: fits; 1: fits + meter statistic S1 (full counts); 2: structure only (U per model x pair, no text work)
   out: M label q tab form model m n U slot ; H label model tab form m n configs fits strictfits Usum [S1sum] ;
        S label model m n configs Usum (mode 2) ; B label band configs fits Usum [S1sum] ; END */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <omp.h>
static const char *PTC = "EASTNORTHEASTBERLINCLOCK";
static int CI[24];
#define NV 56
#define MAXD 24
typedef struct { unsigned char typ, w, from, t; } Op;
typedef struct { int nsub; unsigned char root[24], beg[25]; Op ops[24]; } Prog;
static unsigned coremask(unsigned mk, const int *eu, const int *ev, int V) {
  int deg[NV]; memset(deg, 0, V * sizeof(int));
  for (unsigned c = mk; c; c &= c - 1) { int t = __builtin_ctz(c); deg[eu[t]]++; deg[ev[t]]++; }
  for (int ch = 1; ch;) { ch = 0;
    for (unsigned c = mk; c; c &= c - 1) { int t = __builtin_ctz(c);
      if (deg[eu[t]] == 1 || deg[ev[t]] == 1) { mk &= ~(1u << t); deg[eu[t]]--; deg[ev[t]]--; ch = 1; } } }
  return mk;
}
/* E of a mask = prod over components with cycles 26^(1-r) */
static double emask(unsigned mk, const int *eu, const int *ev, int V) {
  int par[NV], ec[NV] = {0}, vc[NV] = {0}, tc[NV] = {0}; for (int x = 0; x < V; x++) par[x] = x;
  for (int t = 0; t < 24; t++) if (mk >> t & 1) { int u = eu[t], v = ev[t]; tc[u] = tc[v] = 1; while (par[u] != u) u = par[u]; while (par[v] != v) v = par[v]; if (u != v) par[u] = v; }
  for (int x = 0; x < V; x++) if (tc[x]) { int r = x; while (par[r] != r) r = par[r]; vc[r]++; }
  for (int t = 0; t < 24; t++) if (mk >> t & 1) { int r = eu[t]; while (par[r] != r) r = par[r]; ec[r]++; }
  double E = 1; for (int x = 0; x < V; x++) if (vc[x] && ec[x] > vc[x] - 1) E *= pow(26.0, 1 - (ec[x] - vc[x] + 1));
  return E;
}
static void build(unsigned mk, const int *eu, const int *ev, Prog *P, const unsigned *inc) {
  int asg[NV] = {0}; unsigned used = 0; int no = 0; P->nsub = 0;
  for (int t0 = 0; t0 < 24; t0++) if ((mk >> t0 & 1) && !asg[eu[t0]]) {
    int qu[NV], qh = 0, qt = 0; int st = eu[t0]; asg[st] = 1; qu[qt++] = st; P->root[P->nsub] = st; P->beg[P->nsub] = no;
    while (qh < qt) { int x = qu[qh++]; unsigned cand = inc[x] & mk & ~used;
      while (cand) { int t = __builtin_ctz(cand); cand &= cand - 1; if (used >> t & 1) continue; int y = eu[t] == x ? ev[t] : eu[t]; used |= 1u << t;
        if (!asg[y]) { asg[y] = 1; qu[qt++] = y; P->ops[no++] = (Op){0, (unsigned char)y, (unsigned char)x, (unsigned char)t}; }
        else P->ops[no++] = (Op){1, (unsigned char)eu[t], (unsigned char)ev[t], (unsigned char)t}; } }
    P->nsub++; }
  P->beg[P->nsub] = no;
}
/* returns product of per-sub consistent root counts (count=1) or 1/0 (count=0) */
static double evalp(const Prog *P, unsigned char (*F)[26], unsigned char (*G)[26], int m, int count) {
  double ns = 1;
  for (int s = 0; s < P->nsub; s++) { int cnt = 0;
    for (int rho = 0; rho < 26; rho++) { unsigned char val[NV]; val[P->root[s]] = rho; int good = 1;
      for (int o = P->beg[s]; o < P->beg[s + 1]; o++) { Op op = P->ops[o];
        if (op.typ == 0) val[op.w] = op.w < m ? G[op.t][val[op.from]] : F[op.t][val[op.from]];
        else if (F[op.t][val[op.w]] != val[op.from]) { good = 0; break; } }
      if (good) { cnt++; if (!count) break; } }
    if (!cnt) return 0; ns *= cnt; }
  return ns;
}
int main(int argc, char **argv) {
  if (argc < 10) { fprintf(stderr, "usage: cmp192 CT perms.bin tabpairs.txt label qlo qhi pairs.txt printU mode\n"); return 1; }
  const char *ct = argv[1]; const char *lab = argv[4]; long qlo = atol(argv[5]), qhi = atol(argv[6]); double PE = atof(argv[8]); int MODE = atoi(argv[9]);
  if (strlen(ct) != 97) { fprintf(stderr, "bad CT\n"); return 1; }
  for (int t = 0; t < 13; t++) CI[t] = 21 + t; for (int t = 0; t < 11; t++) CI[13 + t] = 63 + t;
  FILE *f = fopen(argv[2], "rb"); if (!f) return 2; fseek(f, 0, SEEK_END); long np = ftell(f) / (97 * 2); fseek(f, 0, SEEK_SET);
  short *P = malloc(np * 97 * 2); if (fread(P, 2, np * 97, f) != (size_t)(np * 97)) return 2; fclose(f);
  if (qhi > np) qhi = np; if (qlo < 0) qlo = 0;
  static char T1[64][27], T2[64][27], TN[64][64]; int nt = 0; char buf[256];
  f = fopen(argv[3], "r"); if (!f) return 2;
  while (fgets(buf, 256, f) && nt < 64) { char a[64], b[64], c[64]; if (sscanf(buf, "%63s %63s %63s", a, b, c) == 3 && strlen(a) == 26 && strlen(b) == 26) { memcpy(T1[nt], a, 27); memcpy(T2[nt], b, 27); strcpy(TN[nt], c); nt++; } } fclose(f);
  /* pair list per model */
  int pm[2][700], pn[2][700], npair[2] = {0, 0};
  f = fopen(argv[7], "r"); if (!f) return 2;
  if (fgets(buf, 256, f) && !strncmp(buf, "ALL", 3)) { for (int md = 0; md < 2; md++) for (int m = 2; m <= 26; m++) for (int n = 2; n <= 26; n++) if (m != n) { pm[md][npair[md]] = m; pn[md][npair[md]] = n; npair[md]++; } }
  else { do { char c; int m, n; if (sscanf(buf, " %c %d %d", &c, &m, &n) == 3) { int md = c == 'C'; pm[md][npair[md]] = m; pn[md][npair[md]] = n; npair[md]++; } } while (fgets(buf, 256, f)); }
  fclose(f);
  int NP = npair[0] > npair[1] ? npair[0] : npair[1]; if (!NP) NP = 1;
  int NC = 2 * nt * 4 * NP;
  long long *cfg = calloc(NC, 8), *fit = calloc(NC, 8), *sft = calloc(NC, 8); double *usum = calloc(NC, 8), *s1s = calloc(NC, 8);
  long long sc[2][700] = {{0}}; double su[2][700] = {{0}};
  long long bc[30] = {0}, bf[30] = {0}; double bu[30] = {0}, bs[30] = {0};
  static int X1[64][24], SIG[64][26], I2[64][26];
  for (int k = 0; k < nt; k++) { int i1[26]; for (int i = 0; i < 26; i++) { i1[T1[k][i] - 'A'] = i; I2[k][T2[k][i] - 'A'] = i; }
    for (int t = 0; t < 24; t++) X1[k][t] = i1[PTC[t] - 'A'];
    for (int y = 0; y < 26; y++) SIG[k][y] = I2[k][T1[k][y] - 'A']; }
  #pragma omp parallel
  {
    long long *lc = calloc(NC, 8), *lf = calloc(NC, 8), *lsf = calloc(NC, 8); double *lu = calloc(NC, 8), *ls1 = calloc(NC, 8);
    long long lsc[2][700] = {{0}}; double lsu[2][700] = {{0}};
    long long lbc[30] = {0}, lbf[30] = {0}; double lbu[30] = {0}, lbs[30] = {0};
    unsigned char (*F)[4][24][26] = malloc(64 * sizeof *F), (*G)[4][24][26] = malloc(64 * sizeof *G);
    Prog *PK = malloc(24 * sizeof(Prog)), *PD = malloc(24 * MAXD * sizeof(Prog));
    #pragma omp for schedule(dynamic, 16)
    for (long q = qlo; q < qhi; q++) {
      const short *S = P + q * 97;
      if (MODE != 2) for (int k = 0; k < nt; k++) for (int fm = 0; fm < 4; fm++) {
        int s1 = (fm & 2) ? -1 : 1, s2 = (fm & 1) ? -1 : 1;
        for (int t = 0; t < 24; t++) { int z = I2[k][ct[S[CI[t]]] - 'A'];
          for (int a = 0; a < 26; a++) { int y = ((s1 * X1[k][t] + a) % 26 + 26) % 26; int b = ((z - s2 * SIG[k][y]) % 26 + 26) % 26; F[k][fm][t][a] = b; G[k][fm][t][b] = a; } }
      }
      for (int md = 0; md < 2; md++) {
        int pos[24]; for (int t = 0; t < 24; t++) pos[t] = md == 0 ? CI[t] : S[CI[t]];
        for (int pi = 0; pi < npair[md]; pi++) {
          int m = pm[md][pi], n = pn[md][pi], V = m + n;
          int eu[24], ev[24]; for (int t = 0; t < 24; t++) { eu[t] = pos[t] % m; ev[t] = m + pos[t] % n; }
          unsigned inc[NV]; memset(inc, 0, V * sizeof(unsigned)); for (int t = 0; t < 24; t++) { inc[eu[t]] |= 1u << t; inc[ev[t]] |= 1u << t; }
          /* components of G */
          int par[NV]; for (int x = 0; x < V; x++) par[x] = x;
          for (int t = 0; t < 24; t++) { int u = eu[t], v = ev[t]; while (par[u] != u) u = par[u]; while (par[v] != v) v = par[v]; if (u != v) par[u] = v; }
          unsigned cm[NV]; memset(cm, 0, sizeof cm); for (int t = 0; t < 24; t++) { int r = eu[t]; while (par[r] != r) r = par[r]; cm[r] |= 1u << t; }
          int nk = 0; unsigned Kc[24]; double EK[24];
          for (int r = 0; r < V; r++) if (cm[r]) { unsigned c = coremask(cm[r], eu, ev, V); if (c) { Kc[nk] = c; EK[nk] = emask(c, eu, ev, V); nk++; } }
          double EG = 1; for (int i = 0; i < nk; i++) EG *= EK[i];
          /* distinct deletion cores per K */
          int nd[24]; unsigned Dm[24][MAXD]; int Dt[24][MAXD]; double De[24][MAXD]; int built[24][MAXD];
          double U = 0;
          for (int i = 0; i < nk; i++) { nd[i] = 0;
            for (int t = 0; t < 24; t++) if (Kc[i] >> t & 1) { unsigned d = coremask(Kc[i] & ~(1u << t), eu, ev, V); int dup = 0;
              for (int j = 0; j < nd[i]; j++) if (Dm[i][j] == d) { dup = 1; break; }
              if (!dup) { Dm[i][nd[i]] = d; Dt[i][nd[i]] = t; De[i][nd[i]] = d ? emask(d, eu, ev, V) : 1.0; built[i][nd[i]] = 0; U += EG / EK[i] * De[i][nd[i]]; nd[i]++; } } }
          if (!nk) U = 1;
          double Uc = U > 1 ? 1 : U;
          if (MODE == 2) { lsc[md][pi]++; lsu[md][pi] += Uc; continue; }
          for (int i = 0; i < nk; i++) build(Kc[i], eu, ev, &PK[i], inc);
          int band = Uc >= 1 ? 0 : (int)lround(-log(Uc) / log(26.0)); if (band < 0) band = 0; if (band > 24) band = 24; if (!nk) band = 25;
          for (int k = 0; k < nt; k++) for (int fm = 0; fm < 4; fm++) {
            int c4 = ((md * nt + k) * 4 + fm) * NP + pi; lc[c4]++; lu[c4] += Uc; lbc[band]++; lbu[band] += Uc;
            unsigned char (*FF)[26] = F[k][fm], (*GG)[26] = G[k][fm];
            double cntK[24]; int nfail = 0, fk = -1;
            for (int i = 0; i < nk; i++) { cntK[i] = evalp(&PK[i], FF, GG, m, MODE == 1); if (cntK[i] == 0) { nfail++; fk = i; } }
            int ok = 0, slot = -2; double S1 = 0;
            if (nfail == 0) { ok = 1; slot = -1; lsf[c4]++; }
            if (MODE == 1) { /* full meter statistic */
              for (int i = 0; i < nk; i++) { double oth = 1; for (int j = 0; j < nk; j++) if (j != i) oth *= cntK[j];
                if (oth == 0) continue;
                for (int j = 0; j < nd[i]; j++) { if (!built[i][j]) { build(Dm[i][j], eu, ev, &PD[i * MAXD + j], inc); built[i][j] = 1; }
                  double sd = Dm[i][j] ? evalp(&PD[i * MAXD + j], FF, GG, m, 1) : 1.0; S1 += oth * sd;
                  if (sd > 0 && !ok) { ok = 1; slot = Dt[i][j]; } } }
              ls1[c4] += S1; lbs[band] += S1;
            } else if (nfail == 1) {
              int i = fk;
              for (int j = 0; j < nd[i] && !ok; j++) { if (!built[i][j]) { build(Dm[i][j], eu, ev, &PD[i * MAXD + j], inc); built[i][j] = 1; }
                if (!Dm[i][j] || evalp(&PD[i * MAXD + j], FF, GG, m, 0) > 0) { ok = 1; slot = Dt[i][j]; } }
            }
            if (ok) { lf[c4]++; lbf[band]++;
              if (Uc <= PE) {
                #pragma omp critical
                printf("M %s %ld %s %c%c %c %d %d %.4g %d\n", lab, q, TN[k], (fm & 2) ? 'B' : 'V', (fm & 1) ? 'B' : 'V', md ? 'C' : 'P', m, n, Uc, slot);
              } }
          }
        }
      }
    }
    #pragma omp critical
    { for (int i = 0; i < NC; i++) { cfg[i] += lc[i]; fit[i] += lf[i]; sft[i] += lsf[i]; usum[i] += lu[i]; s1s[i] += ls1[i]; }
      for (int md = 0; md < 2; md++) for (int i = 0; i < 700; i++) { sc[md][i] += lsc[md][i]; su[md][i] += lsu[md][i]; }
      for (int i = 0; i < 30; i++) { bc[i] += lbc[i]; bf[i] += lbf[i]; bu[i] += lbu[i]; bs[i] += lbs[i]; } }
  }
  if (MODE == 2) { for (int md = 0; md < 2; md++) for (int pi = 0; pi < npair[md]; pi++) printf("S %s %c %d %d %lld %.6g\n", lab, md ? 'C' : 'P', pm[md][pi], pn[md][pi], sc[md][pi], su[md][pi]); }
  else {
    for (int md = 0; md < 2; md++) for (int k = 0; k < nt; k++) for (int fm = 0; fm < 4; fm++) for (int pi = 0; pi < npair[md]; pi++) {
      int c4 = ((md * nt + k) * 4 + fm) * NP + pi;
      printf("H %s %c %s %c%c %d %d %lld %lld %lld %.6g", lab, md ? 'C' : 'P', TN[k], (fm & 2) ? 'B' : 'V', (fm & 1) ? 'B' : 'V', pm[md][pi], pn[md][pi], cfg[c4], fit[c4], sft[c4], usum[c4]);
      if (MODE == 1) printf(" %.6g", s1s[c4]); printf("\n"); }
    for (int i = 0; i < 26; i++) if (bc[i]) { printf("B %s %d %lld %lld %.6g", lab, i, bc[i], bf[i], bu[i]); if (MODE == 1) printf(" %.6g", bs[i]); printf("\n"); }
  }
  printf("END %s perms %ld-%ld tabpairs %d pairs %d %d mode %d\n", lab, qlo, qhi, nt, npair[0], npair[1], MODE);
  return 0;
}
