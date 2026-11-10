/* Cycle 198 (IDEAS I-222 / I-221): one-error audit of case 184. Same model as cmp197 (two periodic keys, one tableau = solver A or two
   tableaux = solver B; one DROPPED (del, C' 98) or EXTRA (ins, C' 96) carved letter at d; direct records or K3-law decimations), PLUS at most
   ONE WRONG crib letter: a config fits if the usable crib constraints are consistent after deleting at most one crib slot t.
   Exact search: consistency of a constraint set depends only on its 2-core (pendant edges never constrain, both solvers), so for each
   (record, model, pair) the distinct 2-cores of G - t (t over the usable slots) are listed once (dedup by edge mask) and each is checked.
   Chance bound (union bound over distinct events, uniform independent carved letters):
       U = sum over distinct cores d of E(d),  E(d) = 26^-(excess d) (A) or prod_cyclic 26^(1-r) (B, expected solutions >= P(consistent)),
   capped at 1; U = 1 if G has no cycle. U >= P(fit). The strict event is inside every G - t event, so it adds nothing.
   usage: cmp198 MODE CT src N kind label qlo qhi alphas.txt tabpairs.txt pairsA.txt pairsB.txt PE
   out: M A label q d model alpha form m n U slot ; M B label q d model tab form m n U slot ;
        H A|B label model alpha|tab form m n configs fits strictfits Usum searched fits_searched Usum_searched ; END
   SEARCH RULE (registered, budget): the one-error deletion search runs only for configs with U <= PE (= the full-power line 0.05);
   other configs are tested strictly only. A cell is full power iff its U sum <= 0.05, so every config of a full-power cell is searched.
   slot = -1 strict fit, else the deleted crib slot (0-23, EASTNORTHEASTBERLINCLOCK order) of the first consistent core. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <omp.h>
static const char *PTC = "EASTNORTHEASTBERLINCLOCK";
static int CI[24];
#define NV 56
typedef struct { short kp[24], kc[24], cv[24]; int q, d; } Rec;
typedef struct { unsigned char typ, w, from, t; } Op;
typedef struct { int nsub; unsigned char root[24], beg[25]; Op ops[24]; } Prog;
static int npA[2], pAm[2][400], pAn[2][400], npB[2], pBm[2][700], pBn[2][700];
static double P26[64];
static unsigned coremask(unsigned mk, const int *eu, const int *ev, int V) {
  /* leaf peeling with a stack: O(E + V) */
  int deg[NV]; unsigned im[NV]; memset(deg, 0, V * sizeof(int)); memset(im, 0, V * sizeof(unsigned));
  for (unsigned c = mk; c; c &= c - 1) { int t = __builtin_ctz(c); deg[eu[t]]++; deg[ev[t]]++; im[eu[t]] |= 1u << t; im[ev[t]] |= 1u << t; }
  int st[NV], sp = 0; for (int x = 0; x < V; x++) if (deg[x] == 1) st[sp++] = x;
  while (sp) { int x = st[--sp]; if (deg[x] != 1) continue; unsigned e = im[x] & mk; if (!e) continue; int t = __builtin_ctz(e);
    mk &= ~(1u << t); int y = eu[t] == x ? ev[t] : eu[t]; deg[x]--; deg[y]--; if (deg[y] == 1) st[sp++] = y; }
  return mk;
}
/* returns cyclomatic data: total excess (A) and product E (B) */
static void emask(unsigned mk, const int *eu, const int *ev, int V, int *exA, double *EB) {
  int par[NV], ec[NV] = {0}, vc[NV] = {0}, tc[NV] = {0}; for (int x = 0; x < V; x++) par[x] = x;
  for (int t = 0; t < 24; t++) if (mk >> t & 1) { int u = eu[t], v = ev[t]; tc[u] = tc[v] = 1; while (par[u] != u) u = par[u]; while (par[v] != v) v = par[v]; if (u != v) par[u] = v; }
  for (int x = 0; x < V; x++) if (tc[x]) { int r = x; while (par[r] != r) r = par[r]; vc[r]++; }
  for (int t = 0; t < 24; t++) if (mk >> t & 1) { int r = eu[t]; while (par[r] != r) r = par[r]; ec[r]++; }
  int ex = 0; double E = 1;
  for (int x = 0; x < V; x++) if (vc[x] && ec[x] > vc[x] - 1) { int r = ec[x] - vc[x] + 1; ex += r; E *= P26[r - 1]; }
  *exA = ex; *EB = E;
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
static int evalp(const Prog *P, unsigned char (*F)[26], unsigned char (*G)[26], int m) {
  for (int s = 0; s < P->nsub; s++) { int any = 0;
    for (int rho = 0; rho < 26 && !any; rho++) { unsigned char val[NV]; val[P->root[s]] = rho; int good = 1;
      for (int o = P->beg[s]; o < P->beg[s + 1]; o++) { Op op = P->ops[o];
        if (op.typ == 0) val[op.w] = op.w < m ? G[op.t][val[op.from]] : F[op.t][val[op.from]];
        else if (F[op.t][val[op.w]] != val[op.from]) { good = 0; break; } }
      any = good; }
    if (!any) return 0; }
  return 1;
}
/* solver A: weighted union-find on mask */
static int consA(unsigned mk, const int *eu, const int *ev, const int *K, int V) {
  int par[NV], off[NV]; for (int x = 0; x < V; x++) { par[x] = x; off[x] = 0; }
  for (unsigned c = mk; c; c &= c - 1) { int t = __builtin_ctz(c); int u = eu[t], v = ev[t], ou = 0, ov = 0;
    while (par[u] != u) { ou += off[u]; u = par[u]; } while (par[v] != v) { ov += off[v]; v = par[v]; }
    ou %= 26; ov %= 26;
    if (u == v) { if (((ou - ov - K[t]) % 26 + 52) % 26) return 0; }
    else { par[u] = v; off[u] = ((K[t] + ov - ou) % 26 + 52) % 26; } }
  return 1;
}
int main(int argc, char **argv) {
  if (argc < 14) { fprintf(stderr, "usage\n"); return 1; }
  const char *mode = argv[1], *ct = argv[2], *src = argv[3]; int N = atoi(argv[4]); const char *kind = argv[5], *lab = argv[6];
  long qlo = atol(argv[7]), qhi = atol(argv[8]); double PE = atof(argv[13]);
  int isrec = !strcmp(mode, "rec"), isdel = !strcmp(kind, "del");
  if (strlen(ct) != 97) { fprintf(stderr, "ct len\n"); return 1; }
  P26[0] = 1; for (int e = 1; e < 64; e++) P26[e] = P26[e - 1] / 26.0;
  for (int t = 0; t < 13; t++) CI[t] = 21 + t; for (int t = 0; t < 11; t++) CI[13 + t] = 63 + t;
  npA[0] = npA[1] = npB[0] = npB[1] = 0;
  for (int s = 0; s < 2; s++) { const char *fn = argv[11 + s];
    if (strcmp(fn, "-")) { FILE *f = fopen(fn, "r"); if (!f) { fprintf(stderr, "no %s\n", fn); return 2; } char md; int m, n;
      while (fscanf(f, " %c %d %d", &md, &m, &n) == 3) { int k = md == 'C';
        if (s == 0) { pAm[k][npA[k]] = m; pAn[k][npA[k]] = n; npA[k]++; } else { pBm[k][npB[k]] = m; pBn[k][npB[k]] = n; npB[k]++; } }
      fclose(f); } }
  int NM = isrec ? 1 : 2;
  Rec *R = NULL; long nr = 0; short *PB = NULL; long np = 0;
  if (isrec) { FILE *f = fopen(src, "r"); if (!f) return 2; long cap = 1 << 16; R = malloc(cap * sizeof(Rec)); int q;
    while (fscanf(f, "%d", &q) == 1) { Rec r; r.q = q; int d; if (fscanf(f, "%d", &d) != 1) return 3; r.d = d;
      for (int t = 0; t < 24; t++) { int v; if (fscanf(f, "%d", &v) != 1) return 3; r.kp[t] = v; r.kc[t] = v; }
      for (int t = 0; t < 24; t++) { int v; if (fscanf(f, "%d", &v) != 1) return 3; r.cv[t] = v; }
      if (nr == cap) { cap *= 2; R = realloc(R, cap * sizeof(Rec)); } R[nr++] = r; }
    fclose(f); if (qhi > nr) qhi = nr; }
  else { FILE *f = fopen(src, "rb"); if (!f) return 2; fseek(f, 0, SEEK_END); np = ftell(f) / (N * 2); fseek(f, 0, SEEK_SET);
    PB = malloc(np * N * 2); if (fread(PB, 2, np * N, f) != (size_t)(np * N)) return 2; fclose(f); if (qhi > np) qhi = np; }
  if (qlo < 0) qlo = 0;
  static char AL[64][27], AN[64][64]; int na = 0; char buf[256];
  if (strcmp(argv[9], "-")) { FILE *f = fopen(argv[9], "r"); while (fgets(buf, 256, f) && na < 64) { char a[64], b[64]; if (sscanf(buf, "%63s %63s", a, b) == 2 && strlen(a) == 26) { memcpy(AL[na], a, 27); strcpy(AN[na], b); na++; } } fclose(f); }
  static int AIDX[64][26]; for (int a = 0; a < na; a++) for (int i = 0; i < 26; i++) AIDX[a][AL[a][i] - 'A'] = i;
  static char T1[8][27], T2[8][27], TN[8][64]; int nt = 0;
  if (strcmp(argv[10], "-")) { FILE *f = fopen(argv[10], "r"); while (fgets(buf, 256, f) && nt < 8) { char a[64], b[64], c[64]; if (sscanf(buf, "%63s %63s %63s", a, b, c) == 3) { memcpy(T1[nt], a, 27); memcpy(T2[nt], b, 27); strcpy(TN[nt], c); nt++; } } fclose(f); }
  static unsigned char FF[8][4][24][26][26], GG[8][4][24][26][26];
  for (int k = 0; k < nt; k++) { int i1[26], i2[26]; for (int i = 0; i < 26; i++) { i1[T1[k][i] - 'A'] = i; i2[T2[k][i] - 'A'] = i; }
    int sig[26]; for (int y = 0; y < 26; y++) sig[y] = i2[T1[k][y] - 'A'];
    for (int fm = 0; fm < 4; fm++) { int s1 = (fm & 2) ? -1 : 1, s2 = (fm & 1) ? -1 : 1;
      for (int t = 0; t < 24; t++) { int x = i1[PTC[t] - 'A'];
        for (int L = 0; L < 26; L++) { int z = i2[L];
          for (int a = 0; a < 26; a++) { int y = ((s1 * x + a) % 26 + 26) % 26; int b = ((z - s2 * sig[y]) % 26 + 26) % 26; FF[k][fm][t][L][a] = b; GG[k][fm][t][L][b] = a; } } } } }
  int CA = NM * (na > 0 ? na : 1) * 2 * 400, CB = NM * (nt > 0 ? nt : 1) * 4 * 700;
  long long *cA = calloc(CA, 8), *fA = calloc(CA, 8), *sA = calloc(CA, 8), *qA = calloc(CA, 8), *gA = calloc(CA, 8); double *uA = calloc(CA, 8), *wA = calloc(CA, 8);
  long long *cB = calloc(CB, 8), *fB = calloc(CB, 8), *sB = calloc(CB, 8), *qB = calloc(CB, 8), *gB = calloc(CB, 8); double *uB = calloc(CB, 8), *wB = calloc(CB, 8);
  long long nrec = 0;
  #pragma omp parallel reduction(+:nrec)
  {
    long long *lcA = calloc(CA, 8), *lfA = calloc(CA, 8), *lsA = calloc(CA, 8), *lqA = calloc(CA, 8), *lgA = calloc(CA, 8); double *luA = calloc(CA, 8), *lwA = calloc(CA, 8);
    long long *lcB = calloc(CB, 8), *lfB = calloc(CB, 8), *lsB = calloc(CB, 8), *lqB = calloc(CB, 8), *lgB = calloc(CB, 8); double *luB = calloc(CB, 8), *lwB = calloc(CB, 8);
    Rec *loc = malloc(128 * sizeof(Rec));
    unsigned char (*Fl)[4][24][26] = malloc(8 * sizeof *Fl), (*Gl)[4][24][26] = malloc(8 * sizeof *Gl);
    Prog *PK = malloc(24 * sizeof(Prog)), *PD = malloc(24 * 24 * sizeof(Prog));
    #pragma omp for schedule(dynamic, 8)
    for (long q = qlo; q < qhi; q++) {
      int nl = 0;
      if (isrec) loc[nl++] = R[q];
      else { const short *S = PB + q * N; int c[24]; char isc[100] = {0}; for (int t = 0; t < 24; t++) { c[t] = S[CI[t]]; isc[c[t]] = 1; }
        int dmax = isdel ? N - 1 : N;
        for (int d = 0; d <= dmax; d++) { if (!(d == 0 || isc[d - 1] || (isdel && d < N && isc[d]))) continue;
          Rec r; r.q = q; r.d = d;
          for (int t = 0; t < 24; t++) { r.kp[t] = CI[t]; r.kc[t] = c[t];
            if (isdel) r.cv[t] = c[t] < d ? c[t] : (c[t] == d ? -1 : c[t] - 1); else r.cv[t] = c[t] < d ? c[t] : c[t] + 1; }
          loc[nl++] = r; } }
      for (int ir = 0; ir < nl; ir++) { const Rec *r = &loc[ir]; nrec++;
        unsigned Gm = 0; int Lt[24]; for (int t = 0; t < 24; t++) if (r->cv[t] >= 0) { Gm |= 1u << t; Lt[t] = ct[r->cv[t]] - 'A'; }
        for (int k = 0; k < nt; k++) for (int fm = 0; fm < 4; fm++) for (int t = 0; t < 24; t++) if (Gm >> t & 1) {
          memcpy(Fl[k][fm][t], FF[k][fm][t][Lt[t]], 26); memcpy(Gl[k][fm][t], GG[k][fm][t][Lt[t]], 26); }
        int KA_[64][2][24];
        for (int a = 0; a < na; a++) for (int t = 0; t < 24; t++) if (Gm >> t & 1) { int xp = AIDX[a][PTC[t] - 'A'], xc = AIDX[a][Lt[t]];
          KA_[a][0][t] = (xc - xp + 26) % 26; KA_[a][1][t] = (xc + xp) % 26; }
        for (int md = 0; md < NM; md++) {
          const short *pos = md ? r->kc : r->kp;
          for (int sv = 0; sv < 2; sv++) { int npp = sv ? (nt ? npB[md] : 0) : (na ? npA[md] : 0);
          for (int pi = 0; pi < npp; pi++) { int m = sv ? pBm[md][pi] : pAm[md][pi], n = sv ? pBn[md][pi] : pAn[md][pi], V = m + n;
            int eu[24], ev[24]; unsigned inc[NV]; memset(inc, 0, V * sizeof(unsigned));
            for (int t = 0; t < 24; t++) { eu[t] = pos[t] % m; ev[t] = m + pos[t] % n; if (Gm >> t & 1) { inc[eu[t]] |= 1u << t; inc[ev[t]] |= 1u << t; } }
            unsigned c0 = coremask(Gm, eu, ev, V);
            /* cyclic components of the core; per component the distinct cores of K - t */
            unsigned Kc[24]; int nk = 0;
            { int par[NV]; for (int x = 0; x < V; x++) par[x] = x;
              for (unsigned cc = c0; cc; cc &= cc - 1) { int t = __builtin_ctz(cc); int u = eu[t], v = ev[t]; while (par[u] != u) u = par[u]; while (par[v] != v) v = par[v]; if (u != v) par[u] = v; }
              unsigned cm[NV]; memset(cm, 0, sizeof cm);
              for (unsigned cc = c0; cc; cc &= cc - 1) { int t = __builtin_ctz(cc); int r0 = eu[t]; while (par[r0] != r0) r0 = par[r0]; cm[r0] |= 1u << t; }
              for (int x = 0; x < V; x++) if (cm[x]) Kc[nk++] = cm[x]; }
            double EK[24], EG = 1; int nd[24]; unsigned Dm[24][24]; int Dt[24][24]; double U = 0;
            for (int i = 0; i < nk; i++) { int ex; double EB; emask(Kc[i], eu, ev, V, &ex, &EB); EK[i] = sv ? EB : P26[ex]; EG *= EK[i]; }
            for (int i = 0; i < nk; i++) { nd[i] = 0;
              for (unsigned cc = Kc[i]; cc; cc &= cc - 1) { int t = __builtin_ctz(cc); unsigned d = coremask(Kc[i] & ~(1u << t), eu, ev, V); int dup = 0;
                for (int j = 0; j < nd[i]; j++) if (Dm[i][j] == d) { dup = 1; break; }
                if (!dup) { Dm[i][nd[i]] = d; Dt[i][nd[i]] = t; int ex; double EB; emask(d, eu, ev, V, &ex, &EB); U += EG / EK[i] * (d ? (sv ? EB : P26[ex]) : 1.0); nd[i]++; } } }
            if (Gm != c0) U += EG;
            if (!nk) U = 1;
            if (U > 1) U = 1;
            if (sv == 0) {
              for (int a = 0; a < na; a++) for (int fm = 0; fm < 2; fm++) {
                int k3 = ((md * na + a) * 2 + fm) * 400 + pi; lcA[k3]++; luA[k3] += U; if (U <= PE) { lqA[k3]++; lwA[k3] += U; }
                int ok = 0, slot = -2, nf = 0, fk = -1;
                for (int i = 0; i < nk && nf < 2; i++) if (!consA(Kc[i], eu, ev, KA_[a][fm], V)) { nf++; fk = i; }
                if (nf == 0) { ok = 1; slot = -1; lsA[k3]++; }
                else if (nf == 1 && U <= PE) for (int j = 0; j < nd[fk] && !ok; j++) if (!Dm[fk][j] || consA(Dm[fk][j], eu, ev, KA_[a][fm], V)) { ok = 1; slot = Dt[fk][j]; }
                if (ok) { lfA[k3]++; if (U <= PE) { lgA[k3]++;
                  #pragma omp critical
                  printf("M A %s %d %d %c %s %s %d %d %.4g %d\n", lab, r->q, r->d, isrec ? 'D' : (md ? 'C' : 'P'), AN[a], fm ? "beau" : "vig", m, n, U, slot); } }
              }
            } else {
              for (int i = 0; i < nk; i++) build(Kc[i], eu, ev, &PK[i], inc);
              int built[24][24]; for (int i = 0; i < nk; i++) for (int j = 0; j < nd[i]; j++) built[i][j] = 0;
              for (int k = 0; k < nt; k++) for (int fm = 0; fm < 4; fm++) {
                int c4 = ((md * nt + k) * 4 + fm) * 700 + pi; lcB[c4]++; luB[c4] += U; if (U <= PE) { lqB[c4]++; lwB[c4] += U; }
                int ok = 0, slot = -2, nf = 0, fk = -1;
                for (int i = 0; i < nk && nf < 2; i++) if (!evalp(&PK[i], Fl[k][fm], Gl[k][fm], m)) { nf++; fk = i; }
                if (nf == 0) { ok = 1; slot = -1; lsB[c4]++; }
                else if (nf == 1 && U <= PE) for (int j = 0; j < nd[fk] && !ok; j++) {
                  if (!Dm[fk][j]) { ok = 1; slot = Dt[fk][j]; break; }
                  if (!built[fk][j]) { build(Dm[fk][j], eu, ev, &PD[fk * 24 + j], inc); built[fk][j] = 1; }
                  if (evalp(&PD[fk * 24 + j], Fl[k][fm], Gl[k][fm], m)) { ok = 1; slot = Dt[fk][j]; } }
                if (ok) { lfB[c4]++; if (U <= PE) { lgB[c4]++;
                  #pragma omp critical
                  printf("M B %s %d %d %c %s %c%c %d %d %.4g %d\n", lab, r->q, r->d, isrec ? 'D' : (md ? 'C' : 'P'), TN[k], (fm & 2) ? 'B' : 'V', (fm & 1) ? 'B' : 'V', m, n, U, slot); } }
              }
            }
          } } } } }
    #pragma omp critical
    { for (int i = 0; i < CA; i++) { cA[i] += lcA[i]; fA[i] += lfA[i]; sA[i] += lsA[i]; uA[i] += luA[i]; qA[i] += lqA[i]; gA[i] += lgA[i]; wA[i] += lwA[i]; }
      for (int i = 0; i < CB; i++) { cB[i] += lcB[i]; fB[i] += lfB[i]; sB[i] += lsB[i]; uB[i] += luB[i]; qB[i] += lqB[i]; gB[i] += lgB[i]; wB[i] += lwB[i]; } }
  }
  for (int md = 0; md < NM; md++) {
    for (int a = 0; a < na; a++) for (int fm = 0; fm < 2; fm++) for (int pi = 0; pi < npA[md]; pi++) { int k3 = ((md * na + a) * 2 + fm) * 400 + pi;
      printf("H A %s %c %s %s %d %d %lld %lld %lld %.6g %lld %lld %.6g\n", lab, isrec ? 'D' : (md ? 'C' : 'P'), AN[a], fm ? "beau" : "vig", pAm[md][pi], pAn[md][pi], cA[k3], fA[k3], sA[k3], uA[k3], qA[k3], gA[k3], wA[k3]); }
    for (int k = 0; k < nt; k++) for (int fm = 0; fm < 4; fm++) for (int pi = 0; pi < npB[md]; pi++) { int c4 = ((md * nt + k) * 4 + fm) * 700 + pi;
      printf("H B %s %c %s %c%c %d %d %lld %lld %lld %.6g %lld %lld %.6g\n", lab, isrec ? 'D' : (md ? 'C' : 'P'), TN[k], (fm & 2) ? 'B' : 'V', (fm & 1) ? 'B' : 'V', pBm[md][pi], pBn[md][pi], cB[c4], fB[c4], sB[c4], uB[c4], qB[c4], gB[c4], wB[c4]); }
  }
  printf("END %s %s %s q %ld-%ld records %lld alphas %d tabpairs %d\n", lab, mode, kind, qlo, qhi, nrec, na, nt);
  return 0;
}
