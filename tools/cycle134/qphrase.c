/* Cycle 134: phrase-primer extension of cycle 133 (PT-autokey L 11-22
   and CT-autokey L 22-28) behind the 165k bank, model Q.

   Instead of hashing primer-independent crib signatures (underpowered
   for L >= 11: n = 24-2L <= 2), each permutation is fully known as an
   intermediate text I. Crib chains then *derive* the primer; a hit is
   looked up in the phrase set (vocabulary words of length 11-14, two
   joined vocabulary words, or three themed words). Most (perm, word,
   direction, L) settings fail the first extra chain check (about 25/26)
   and never reach the dictionary.

   Families
   (Q)  Quagmire III autokey, keyed alphabet from word W (K1/K2
        construction). PT-fed L 11-22 and CT-fed L 22-28; 3 directions.
   (KA) Repeating themed keyword W on A-Z or KRYPTOS, then autokey
        whose feedback is the first layer's output.
   (AK) Autokey of P, then repeating themed keyword W. 2 tableaux x 3 x 3
        directions.

   usage: qphrase CT words.txt themed.txt perms.bin label mode lo hi
          mode = Q  (Quagmire III, lo..hi rows of words.txt)
               = S  (KA/AK stacks, lo..hi rows of themed.txt)
*/
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

#define N 97
#define MAXW 20000
#define LMIN 11
#define LMAX 28
#define PT_MAX 22
#define CT_MIN 22

static const char *KASTR = "KRYPTOSABCDEFGHIJLMNQUVWXZ";
static const char *C1 = "EASTNORTHEAST";
static const char *C2 = "BERLINCLOCK";

static int AZ_A[26], AZ_I[26], KA_A[26], KA_I[26];
static char WQ[MAXW][32], WT[MAXW][32];
static int LQ[MAXW], LT[MAXW];
static int nQ, nT;
static int cp[24], cl[24], iscrib[N];
static int C[N];
static short *Perm;
static long np;

static char *wlen[16][MAXW];
static int nwlen[16];

static int MOD26[128];

static inline int enc(const int *A, const int *inv, int f, int p, int k){
  int r = f==0 ? inv[p]+inv[k] : f==1 ? inv[k]-inv[p] : inv[p]-inv[k];
  return A[MOD26[r+52]];
}
static inline int dec(const int *A, const int *inv, int f, int c, int k){
  int r = f==0 ? inv[c]-inv[k] : f==1 ? inv[k]-inv[c] : inv[c]+inv[k];
  return A[MOD26[r+52]];
}
/* k such that enc(p, k) = c */
static inline int invk(const int *A, const int *inv, int f, int p, int c){
  int r = f==0 ? inv[c]-inv[p] : f==1 ? inv[c]+inv[p] : inv[p]-inv[c];
  return A[MOD26[r+52]];
}

static int rd(const char *fn, char W[][32], int *L){
  FILE *f = fopen(fn, "r");
  if (!f) { perror(fn); exit(1); }
  int n = 0;
  while (n < MAXW && fscanf(f, "%31s", W[n]) == 1) { L[n] = (int)strlen(W[n]); n++; }
  fclose(f);
  return n;
}

static void keyed(const char *w, int *A, int *inv){
  int used[26] = {0}, n = 0;
  for (const char *p = w; *p; p++) {
    int c = *p - 'A';
    if (c >= 0 && c < 26 && !used[c]) { used[c] = 1; A[n++] = c; }
  }
  for (int c = 0; c < 26; c++) if (!used[c]) A[n++] = c;
  for (int i = 0; i < 26; i++) inv[A[i]] = i;
}

static void get_I(int v, int *I){
  if (v < np) {
    const short *s = Perm + (long)v * N;
    for (int i = 0; i < N; i++) I[i] = C[s[i]];
  } else {
    const short *s = Perm + (long)(v - np) * N;
    short u[N];
    for (int i = 0; i < N; i++) u[s[i]] = (short)i;
    for (int i = 0; i < N; i++) I[i] = C[u[i]];
  }
}

/* closest conflict pair (hi, lo, steps) per L; steps=0 if none */
static int pair_hi[32], pair_lo[32], pair_st[32];

static void init_pairs(void){
  for (int L = 0; L < 32; L++) pair_st[L] = 0;
  for (int L = LMIN; L <= LMAX; L++) {
    int best = 99, hi = -1, lo = -1;
    for (int a = 0; a < 24; a++) for (int b = 0; b < a; b++) {
      int c1 = cp[a], c2 = cp[b];
      if (c1 < c2) { int t = c1; c1 = c2; c2 = t; }
      if ((c1 - c2) % L == 0) {
        int st = (c1 - c2) / L;
        if (st > 0 && st < best) { best = st; hi = c1; lo = c2; }
      }
    }
    if (hi >= 0) { pair_hi[L] = hi; pair_lo[L] = lo; pair_st[L] = best; }
  }
}

/* PT: walk from a known plaintext at pos back to the primer region.
   Returns 0 on a crib-letter conflict. */
static int walk_pt(const int *I, const int *A, const int *inv, int f, int L,
                   int pos, int pval, int *pr_pos, int *pr_val){
  while (pos >= L) {
    pval = invk(A, inv, f, pval, I[pos]);
    pos -= L;
    if (iscrib[pos] >= 0 && pval != iscrib[pos]) return 0;
  }
  if (iscrib[pos] >= 0 && pval != iscrib[pos]) return 0;
  *pr_pos = pos;
  *pr_val = invk(A, inv, f, pval, I[pos]);
  return 1;
}

/* First (cheapest) PT consistency check: closest crib pair. */
static int pt_pair_ok(const int *I, const int *A, const int *inv, int f, int L){
  int st = pair_st[L];
  if (st <= 0) return 1;
  int pos = pair_hi[L], pval = iscrib[pos];
  for (int s = 0; s < st; s++) {
    pval = invk(A, inv, f, pval, I[pos]);
    pos -= L;
    if (iscrib[pos] >= 0 && pval != iscrib[pos]) return 0;
  }
  return pval == iscrib[pair_lo[L]];
}

/* Derive the PT primer. pr[] is -1 for unknown. Returns 0 on conflict. */
static int derive_pt(const int *I, const int *A, const int *inv, int f, int L, int *pr){
  if (!pt_pair_ok(I, A, inv, f, L)) return 0;
  for (int i = 0; i < L; i++) pr[i] = -1;
  for (int t = 0; t < 24; t++) {
    int pp, pv;
    if (!walk_pt(I, A, inv, f, L, cp[t], cl[t], &pp, &pv)) return 0;
    if (pr[pp] >= 0 && pr[pp] != pv) return 0;
    pr[pp] = pv;
  }
  return 1;
}

/* CT-autokey: cribs at c >= L constrain I only; cribs at c < L set primer[c]. */
static int derive_ct(const int *I, const int *A, const int *inv, int f, int L, int *pr){
  for (int t = 0; t < 24; t++) {
    int c = cp[t];
    if (c >= L && dec(A, inv, f, I[c], I[c - L]) != cl[t]) return 0;
  }
  for (int i = 0; i < L; i++) pr[i] = -1;
  for (int t = 0; t < 24; t++) {
    int c = cp[t];
    if (c < L) {
      int k = invk(A, inv, f, cl[t], I[c]);
      if (pr[c] >= 0 && pr[c] != k) return 0;
      pr[c] = k;
    }
  }
  return 1;
}

/* KA (keyword then autokey of I1): I1[c] = enc(P[c], W[c%Lw]) at cribs.
   PT-fed: K_ak[i] = primer[i] (i < L) else I1[i-L]. */
static int walk_ka_pt(const int *I2, const int *A, const int *inv, int f2, int L,
                      int pos, int i1val, int *pr_pos, int *pr_val){
  while (pos >= L) {
    /* I2[pos] = enc(I1[pos], I1[pos-L]) => I1[pos-L] = invk(I1[pos], I2[pos]) */
    i1val = invk(A, inv, f2, i1val, I2[pos]);
    pos -= L;
  }
  *pr_pos = pos;
  /* I2[pos] = enc(I1[pos], primer[pos]) */
  *pr_val = invk(A, inv, f2, i1val, I2[pos]);
  return 1;
}

static int derive_ka_pt(const int *I2, const int *A, const int *inv,
                        int f1, int f2, int L, const char *w, int Lw, int *pr){
  for (int i = 0; i < L; i++) pr[i] = -1;
  /* cheapest pair on the I1 layer */
  int st = pair_st[L];
  if (st > 0) {
    int pos = pair_hi[L];
    int i1 = enc(A, inv, f1, iscrib[pos], w[pos % Lw] - 'A');
    for (int s = 0; s < st; s++) {
      i1 = invk(A, inv, f2, i1, I2[pos]);
      pos -= L;
    }
    int expect = enc(A, inv, f1, iscrib[pair_lo[L]], w[pair_lo[L] % Lw] - 'A');
    if (i1 != expect) return 0;
  }
  for (int t = 0; t < 24; t++) {
    int pos = cp[t];
    int i1 = enc(A, inv, f1, cl[t], w[pos % Lw] - 'A');
    int pp, pv;
    if (!walk_ka_pt(I2, A, inv, f2, L, pos, i1, &pp, &pv)) return 0;
    if (pr[pp] >= 0 && pr[pp] != pv) return 0;
    pr[pp] = pv;
    /* if the walk passed through another crib, I1 must match */
    /* re-walk checking crib I1 values */
    int p = pos, v = i1;
    while (p >= L) {
      v = invk(A, inv, f2, v, I2[p]);
      p -= L;
      if (iscrib[p] >= 0) {
        int exp = enc(A, inv, f1, iscrib[p], w[p % Lw] - 'A');
        if (v != exp) return 0;
      }
    }
  }
  return 1;
}

static int derive_ka_ct(const int *I2, const int *A, const int *inv,
                        int f1, int f2, int L, const char *w, int Lw, int *pr){
  for (int i = 0; i < L; i++) pr[i] = -1;
  for (int t = 0; t < 24; t++) {
    int c = cp[t];
    int i1 = enc(A, inv, f1, cl[t], w[c % Lw] - 'A');
    if (c >= L) {
      if (dec(A, inv, f2, I2[c], I2[c - L]) != i1) return 0;
    } else {
      int k = invk(A, inv, f2, i1, I2[c]);
      if (pr[c] >= 0 && pr[c] != k) return 0;
      pr[c] = k;
    }
  }
  return 1;
}

/* AK: peel the repeating keyword to recover the autokey layer's output I1. */
static void peel_kw(const int *I2, const int *A, const int *inv, int f2,
                    const char *w, int Lw, int *I1){
  for (int i = 0; i < N; i++) I1[i] = dec(A, inv, f2, I2[i], w[i % Lw] - 'A');
}

static int match_word(const char *w, int n, const int *pr, int off){
  for (int i = 0; i < n; i++) {
    int v = pr[off + i];
    if (v >= 0 && w[i] - 'A' != v) return 0;
  }
  return 1;
}

static void emit(const char *lab, const char *fam, const char *w1,
                 const char *ph, int T, int f1, int f2, long v){
  printf("S %s %s %s %s T=%d f1=%d f2=%d perm=%ld dir=%d\n",
         lab, fam, w1, ph, T, f1, f2, v % np, (int)(v / np));
}
static int emit_unique(const char *lab, const char *fam, const char *w1,
                       const char *ph, int T, int f1, int f2, long v,
                       char seen[][64], int *shown){
  for (int i = 0; i < *shown; i++) if (strcmp(seen[i], ph) == 0) return 0;
  if (*shown < 8) {
    emit(lab, fam, w1, ph, T, f1, f2, v);
    strncpy(seen[*shown], ph, 63); seen[*shown][63] = 0;
    (*shown)++;
    return 1;
  }
  return 1; /* still count it */
}

/* Look up a (possibly partial) derived primer in the phrase set.
   Returns the number of matching phrases emitted. */
static int lookup_phrases(const char *lab, const char *fam, const char *w1,
                          int T, int f1, int f2, long v,
                          int L, const int *pr){
  int n = 0, shown = 0;
  char ph[64], seen[8][64];
  /* single vocabulary word */
  if (L >= 3 && L <= 14) {
    for (int i = 0; i < nwlen[L]; i++) {
      if (match_word(wlen[L][i], L, pr, 0)) {
        if (shown < 8) emit_unique(lab, fam, w1, wlen[L][i], T, f1, f2, v, seen, &shown);
        n++;
      }
    }
  }
  /* two joined vocabulary words */
  for (int k = 3; k <= 14 && k <= L - 3; k++) {
    int k2 = L - k;
    if (k2 < 3 || k2 > 14) continue;
    for (int i = 0; i < nwlen[k]; i++) {
      if (!match_word(wlen[k][i], k, pr, 0)) continue;
      for (int j = 0; j < nwlen[k2]; j++) {
        if (!match_word(wlen[k2][j], k2, pr, k)) continue;
        memcpy(ph, wlen[k][i], (size_t)k);
        memcpy(ph + k, wlen[k2][j], (size_t)k2);
        ph[L] = 0;
        if (shown < 8) emit_unique(lab, fam, w1, ph, T, f1, f2, v, seen, &shown);
        n++;
      }
    }
  }
  /* three themed words */
  for (int i = 0; i < nT; i++) {
    int li = LT[i];
    if (li < 3 || li > L - 6) continue;
    if (!match_word(WT[i], li, pr, 0)) continue;
    for (int j = 0; j < nT; j++) {
      int lj = LT[j];
      if (lj < 3 || li + lj > L - 3) continue;
      if (!match_word(WT[j], lj, pr, li)) continue;
      int klen = L - li - lj;
      if (klen < 3 || klen > 14) continue;
      for (int k = 0; k < nT; k++) {
        if (LT[k] != klen) continue;
        if (!match_word(WT[k], klen, pr, li + lj)) continue;
        memcpy(ph, WT[i], (size_t)li);
        memcpy(ph + li, WT[j], (size_t)lj);
        memcpy(ph + li + lj, WT[k], (size_t)klen);
        ph[L] = 0;
        if (shown < 8) emit_unique(lab, fam, w1, ph, T, f1, f2, v, seen, &shown);
        n++;
      }
    }
  }
  if (n > 8)
    printf("CLUSTER %s %s %s L=%d T=%d f1=%d f2=%d perm=%ld dir=%d n=%d\n",
           lab, fam, w1, L, T, f1, f2, v % np, (int)(v / np), n);
  return n;
}

static long g_cfg, g_surv, g_cons;

static void scan_Q(const int *I, long v, int x0, int x1, const char *lab){
  int pr[32];
  for (int x = x0; x < x1; x++) {
    int QA[26], QI[26];
    keyed(WQ[x], QA, QI);
    const char *w = WQ[x];
    for (int f = 0; f < 3; f++) {
      for (int L = LMIN; L <= PT_MAX; L++) {
        g_cfg++;
        if (derive_pt(I, QA, QI, f, L, pr)) {
          g_cons++;
          g_surv += lookup_phrases(lab, "QPT", w, 2, f, -1, v, L, pr);
        }
      }
      for (int L = CT_MIN; L <= LMAX; L++) {
        g_cfg++;
        if (derive_ct(I, QA, QI, f, L, pr)) {
          g_cons++;
          g_surv += lookup_phrases(lab, "QCT", w, 2, f, -1, v, L, pr);
        }
      }
    }
  }
}

static void scan_S(const int *I, long v, int x0, int x1, const char *lab){
  int pr[32], I1[N];
  for (int x = x0; x < x1; x++) {
    const char *w = WT[x];
    int Lw = LT[x];
    for (int T = 0; T < 2; T++) {
      const int *A = T ? KA_A : AZ_A;
      const int *inv = T ? KA_I : AZ_I;
      for (int f1 = 0; f1 < 3; f1++) for (int f2 = 0; f2 < 3; f2++) {
        /* KA PT / CT */
        for (int L = LMIN; L <= PT_MAX; L++) {
          g_cfg++;
          if (derive_ka_pt(I, A, inv, f1, f2, L, w, Lw, pr)) {
            g_cons++;
            g_surv += lookup_phrases(lab, "KAPT", w, T, f1, f2, v, L, pr);
          }
        }
        for (int L = CT_MIN; L <= LMAX; L++) {
          g_cfg++;
          if (derive_ka_ct(I, A, inv, f1, f2, L, w, Lw, pr)) {
            g_cons++;
            g_surv += lookup_phrases(lab, "KACT", w, T, f1, f2, v, L, pr);
          }
        }
        /* AK: peel keyword, then Q-style derive on I1 */
        peel_kw(I, A, inv, f2, w, Lw, I1);
        for (int L = LMIN; L <= PT_MAX; L++) {
          g_cfg++;
          if (derive_pt(I1, A, inv, f1, L, pr)) {
            g_cons++;
            g_surv += lookup_phrases(lab, "AKPT", w, T, f1, f2, v, L, pr);
          }
        }
        for (int L = CT_MIN; L <= LMAX; L++) {
          g_cfg++;
          if (derive_ct(I1, A, inv, f1, L, pr)) {
            g_cons++;
            g_surv += lookup_phrases(lab, "AKCT", w, T, f1, f2, v, L, pr);
          }
        }
      }
    }
  }
}

int main(int argc, char **argv){
  if (argc < 8) {
    fprintf(stderr, "usage: qphrase CT words.txt themed.txt perms.bin label mode lo hi\n");
    return 2;
  }
  const char *Cs = argv[1];
  if ((int)strlen(Cs) != N) { fprintf(stderr, "CT length %zu != 97\n", strlen(Cs)); return 2; }
  for (int i = 0; i < N; i++) C[i] = Cs[i] - 'A';
  nQ = rd(argv[2], WQ, LQ);
  nT = rd(argv[3], WT, LT);
  const char *lab = argv[5];
  const char *mode = argv[6];
  long lo = atol(argv[7]), hi = atol(argv[8]);
  int nsrc = (mode[0] == 'S' || mode[0] == 's') ? nT : nQ;
  if (hi > nsrc) hi = nsrc;
  if (lo < 0) lo = 0;

  for (int r = -52; r < 76; r++) {
    int x = r % 26; if (x < 0) x += 26;
    MOD26[r + 52] = x;
  }
  for (int i = 0; i < 26; i++) { AZ_A[i] = i; AZ_I[i] = i; }
  for (int i = 0; i < 26; i++) KA_A[i] = KASTR[i] - 'A';
  for (int i = 0; i < 26; i++) KA_I[KA_A[i]] = i;

  memset(iscrib, -1, sizeof iscrib);
  for (int i = 0; i < 13; i++) { cp[i] = 21 + i; cl[i] = C1[i] - 'A'; iscrib[21 + i] = cl[i]; }
  for (int i = 0; i < 11; i++) { cp[13 + i] = 63 + i; cl[13 + i] = C2[i] - 'A'; iscrib[63 + i] = cl[13 + i]; }
  init_pairs();

  memset(nwlen, 0, sizeof nwlen);
  for (int i = 0; i < nQ; i++) {
    int L = LQ[i];
    if (L >= 3 && L <= 14) wlen[L][nwlen[L]++] = WQ[i];
  }

  FILE *pf = fopen(argv[4], "rb");
  if (!pf) { perror(argv[4]); return 1; }
  fseek(pf, 0, SEEK_END);
  np = ftell(pf) / (2 * N);
  rewind(pf);
  Perm = malloc((size_t)np * N * sizeof(short));
  if (!Perm) { fprintf(stderr, "malloc perms\n"); return 1; }
  if (fread(Perm, 2, (size_t)np * N, pf) != (size_t)np * N) { fprintf(stderr, "read perms\n"); return 1; }
  fclose(pf);

  long nperm = np * 2;
  int I[N];
  for (long v = 0; v < nperm; v++) {
    get_I((int)v, I);
    if (mode[0] == 'S' || mode[0] == 's') scan_S(I, v, (int)lo, (int)hi, lab);
    else scan_Q(I, v, (int)lo, (int)hi, lab);
  }

  printf("C %s mode=%s lo=%ld hi=%ld configs %ld consistent %ld survivors %ld nperm %ld\n",
         lab, mode, lo, hi, g_cfg, g_cons, g_surv, nperm);
  return 0;
}
