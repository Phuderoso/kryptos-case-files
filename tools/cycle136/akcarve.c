/* Cycle 136: transposition-first autokey with vocabulary Quagmire III alphabets.
   After a bank transposition the autokey is read at the carved position
   (key index = carved_index).  Any primer of length L is tested: the 24 official
   cribs either set a primer letter or constrain the autokey recurrence, so the
   primer itself need not be a dictionary word.

   ix=0: key at the plaintext position, then transpose (model Q).
         Cycles 133–134 closed this only for vocabulary / phrase primers;
         this scan allows any primer.
   ix=1: transpose first, key at the carved position (the open sibling of
         cycles 19/22, which did this only on the A–Z/KRYPTOS tableaux).

   Family: Quagmire III, both sides keyed by W (K1/K2 construction).
   Feeds: PT-autokey (K[j] = primer[j] if j < L else P_layer[j-L])
          CT-autokey (K[j] = primer[j] if j < L else C_layer[j-L])
   Modes: Vigenere (f=0), Beaufort (f=1), variant Beaufort (f=2).
          Unlike periodic keys, vig and variant are not duals here: the
          feedback letter is constrained, so all three directions are distinct.

   usage: akcarve CT words.txt perms.bin label lo hi [LMAX]
   A configuration is a survivor if it is crib-consistent with at least MINCHK
   extra constraints.  Survivors are fully checked against all 24 crib letters
   and, when every autokey chain is determined, decrypted in full.
*/
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

#define N 97
#define MAXW 12000
#define MINCHK 6
#define LDEFAULT 16

static const int CI[24] = {
  21,22,23,24,25,26,27,28,29,30,31,32,33,
  63,64,65,66,67,68,69,70,71,72,73
};
static const char *PT = "EASTNORTHEASTBERLINCLOCK";

static char W[MAXW][32];
static unsigned char A[MAXW][26], INV[MAXW][26];
static int PV[MAXW][24];
static int Plet[24];
static int C[N];
static const char *lab;

static inline int key_from(const unsigned char *Al, const unsigned char *In,
                           int f, int c, int p){
  int ci = In[c], pi = In[p];
  int ki = f == 0 ? ci - pi : f == 1 ? ci + pi : pi - ci;
  return Al[((ki % 26) + 26) % 26];
}

static inline int dec_let(const unsigned char *Al, const unsigned char *In,
                          int f, int c, int k){
  int ci = In[c], ki = In[k];
  int r = f == 0 ? ci - ki : f == 1 ? ki - ci : ci + ki;
  return Al[((r % 26) + 26) % 26];
}

typedef struct { unsigned char t1, t2, nstep; } Pair;

static void keyed(const char *w, unsigned char *alph, unsigned char *inv){
  int used[26] = {0}, n = 0;
  for (const char *p = w; *p; p++) {
    int c = *p - 'A';
    if (c < 0 || c > 25 || used[c]) continue;
    used[c] = 1; alph[n++] = (unsigned char)c;
  }
  for (int c = 0; c < 26; c++) if (!used[c]) alph[n++] = (unsigned char)c;
  for (int i = 0; i < 26; i++) inv[alph[i]] = (unsigned char)i;
}

static void build_pairs(const int *kp, int L, Pair *out, int *n_out, int *nchk_pt, int *nchk_ct){
  int ord[24];
  for (int t = 0; t < 24; t++) ord[t] = t;
  for (int a = 1; a < 24; a++) {
    int t = ord[a], p = kp[t], b = a;
    while (b > 0 && kp[ord[b - 1]] > p) { ord[b] = ord[b - 1]; b--; }
    ord[b] = t;
  }
  int last[32];
  for (int r = 0; r < L; r++) last[r] = -1;
  int n = 0, occ = 0, nct = 0;
  for (int i = 0; i < 24; i++) {
    int t = ord[i], j = kp[t], r = j % L;
    if (last[r] >= 0) {
      int t1 = last[r];
      out[n].t1 = (unsigned char)t1;
      out[n].t2 = (unsigned char)t;
      out[n].nstep = (unsigned char)((j - kp[t1]) / L);
      n++;
    } else {
      occ++;
    }
    last[r] = t;
    if (j >= L) nct++;
  }
  *n_out = n;
  *nchk_pt = 24 - occ;
  *nchk_ct = nct;
}

static const char *MN[3] = {"vig", "beau", "var"};
static const char *XN[2] = {"pt", "carved"};

/* layer_ct[j] is the ciphertext letter of the autokey layer at key-index j:
   carved: C[j]; model Q: C[S[j]]. */
__attribute__((noinline))
static int report(int feed_ct, const char *word, int f, int ix, int L,
                  long q, int dir, int checks,
                  const unsigned char *Al, const unsigned char *In,
                  const short *S, const int *kp, const int *layer_ct){
  int T[N];
  for (int i = 0; i < N; i++) T[i] = -1;
  if (feed_ct) {
    for (int j = L; j < N; j++)
      T[j] = dec_let(Al, In, f, layer_ct[j], layer_ct[j - L]);
    for (int t = 0; t < 24; t++) if (kp[t] < L) T[kp[t]] = Plet[t];
  } else {
    int seen[32];
    memset(seen, 0, sizeof seen);
    for (int t = 0; t < 24; t++) {
      int j = kp[t], r = j % L;
      if (seen[r]) continue;
      seen[r] = 1;
      int val = Plet[t];
      T[j] = val;
      int pos = j, v = val;
      while (pos + L < N) {
        v = dec_let(Al, In, f, layer_ct[pos + L], v);
        pos += L;
        T[pos] = v;
      }
      pos = j; v = val;
      while (pos >= L) {
        v = key_from(Al, In, f, layer_ct[pos], v);
        pos -= L;
        T[pos] = v;
      }
    }
  }
  char ps[N + 1]; ps[N] = 0; int fully = 1;
  for (int i = 0; i < N; i++) {
    int src = ix ? S[i] : i;
    if (T[src] < 0) { ps[i] = '?'; fully = 0; }
    else ps[i] = (char)('A' + T[src]);
  }
  for (int t = 0; t < 24; t++) if (ps[CI[t]] != PT[t]) return 0;
  char primer[40];
  for (int r = 0; r < L; r++) {
    if (T[r] < 0) primer[r] = '?';
    else primer[r] = (char)('A' + key_from(Al, In, f, layer_ct[r], T[r]));
  }
  primer[L] = 0;
  printf("S %s feed=%s word=%s %s ix=%s L=%d perm=%ld dir=%d checks=%d primer=%s",
         lab, feed_ct ? "CT" : "PT", word, MN[f], XN[ix], L, q, dir, checks, primer);
  if (fully) printf(" plain=%s", ps);
  else printf(" partial=%s", ps);
  printf("\n");
  return 1;
}

int main(int argc, char **argv){
  if (argc < 7) {
    fprintf(stderr, "usage: akcarve CT words.txt perms.bin label lo hi [LMAX]\n");
    return 1;
  }
  const char *Cs = argv[1];
  if ((int)strlen(Cs) != N) { fprintf(stderr, "CT length %zu != 97\n", strlen(Cs)); return 1; }
  for (int i = 0; i < N; i++) C[i] = Cs[i] - 'A';
  lab = argv[4];
  long lo = atol(argv[5]), hi = atol(argv[6]);
  int LMAX = argc > 7 ? atoi(argv[7]) : LDEFAULT;
  if (LMAX < 1) LMAX = 1;
  if (LMAX > 32) LMAX = 32;

  FILE *wf = fopen(argv[2], "r");
  if (!wf) { perror(argv[2]); return 1; }
  int nw = 0;
  while (nw < MAXW && fscanf(wf, "%31s", W[nw]) == 1) {
    keyed(W[nw], A[nw], INV[nw]);
    nw++;
  }
  fclose(wf);
  if (lo < 0) lo = 0;
  if (hi > nw) hi = nw;
  if (lo >= hi) {
    printf("C %s x x x x 0 consistent 0 survivors 0 alphabets 0-%d\n", lab, nw);
    return 0;
  }

  for (int t = 0; t < 24; t++) {
    Plet[t] = PT[t] - 'A';
    for (int a = 0; a < nw; a++) PV[a][t] = INV[a][Plet[t]];
  }

  FILE *pf = fopen(argv[3], "rb");
  if (!pf) { perror(argv[3]); return 1; }
  fseek(pf, 0, SEEK_END);
  long np = ftell(pf) / (2 * N);
  rewind(pf);
  short *Perm = malloc((size_t)np * N * sizeof(short));
  if (!Perm || fread(Perm, sizeof(short), (size_t)np * N, pf) != (size_t)np * N) {
    fprintf(stderr, "failed to read perms\n"); return 1;
  }
  fclose(pf);

  int kp_pt[24];
  for (int t = 0; t < 24; t++) kp_pt[t] = CI[t];
  Pair pairs_pt[33][24];
  int npair_pt[33], nchk_pt_pt[33], nchk_pt_ct[33];
  for (int L = 1; L <= LMAX; L++)
    build_pairs(kp_pt, L, pairs_pt[L], &npair_pt[L], &nchk_pt_pt[L], &nchk_pt_ct[L]);

  long long tests = 0, cons = 0, surv = 0;
  long long hist[2][3][2][33];
  memset(hist, 0, sizeof hist);
  const char *FN[2] = {"PT", "CT"};

  for (long q = 0; q < np; q++) {
    const short *s = Perm + q * N;
    short u[N];
    for (int i = 0; i < N; i++) u[s[i]] = (short)i;
    for (int dir = 0; dir < 2; dir++) {
      const short *S = dir ? u : s;
      int kp_cv[24], layer_cv[N], layer_pt[N];
      for (int i = 0; i < N; i++) {
        layer_cv[i] = C[i];
        layer_pt[i] = C[S[i]];
      }
      for (int t = 0; t < 24; t++) kp_cv[t] = S[CI[t]];
      Pair pairs_cv[33][24];
      int npair_cv[33], nchk_cv_pt[33], nchk_cv_ct[33];
      for (int L = 1; L <= LMAX; L++)
        build_pairs(kp_cv, L, pairs_cv[L], &npair_cv[L], &nchk_cv_pt[L], &nchk_cv_ct[L]);

      int CT_AZ[24];
      for (int t = 0; t < 24; t++) CT_AZ[t] = C[kp_cv[t]];

      for (long a = lo; a < hi; a++) {
        const unsigned char *Al = A[a], *In = INV[a];
        int ci[24];
        for (int t = 0; t < 24; t++) ci[t] = In[CT_AZ[t]];

        for (int f = 0; f < 3; f++) {
          int kv[24];
          for (int t = 0; t < 24; t++) {
            int pi = PV[a][t];
            int ki = f == 0 ? ci[t] - pi : f == 1 ? ci[t] + pi : pi - ci[t];
            kv[t] = Al[((ki % 26) + 26) % 26];
          }

          /* Carved index (transposition first). */
          for (int L = 1; L <= LMAX; L++) {
            tests += 2;
            int ok_ct = 1;
            for (int t = 0; t < 24; t++) {
              int j = kp_cv[t];
              if (j >= L && kv[t] != layer_cv[j - L]) { ok_ct = 0; break; }
            }
            if (ok_ct) {
              cons++;
              hist[1][f][1][L]++;
              if (nchk_cv_ct[L] >= MINCHK &&
                  report(1, W[a], f, 1, L, q, dir, nchk_cv_ct[L], Al, In, S, kp_cv, layer_cv))
                surv++;
            }
            int ok_pt = 1;
            const Pair *pr = pairs_cv[L];
            int npt = npair_cv[L];
            for (int k = 0; k < npt; k++) {
              int val = Plet[pr[k].t1], pos = kp_cv[pr[k].t1];
              int nstep = pr[k].nstep;
              for (int s = 0; s < nstep; s++) {
                pos += L;
                val = dec_let(Al, In, f, layer_cv[pos], val);
              }
              if (val != Plet[pr[k].t2]) { ok_pt = 0; break; }
            }
            if (ok_pt) {
              cons++;
              hist[0][f][1][L]++;
              if (nchk_cv_pt[L] >= MINCHK &&
                  report(0, W[a], f, 1, L, q, dir, nchk_cv_pt[L], Al, In, S, kp_cv, layer_cv))
                surv++;
            }
          }

          /* Plaintext index (model Q). */
          for (int L = 1; L <= LMAX; L++) {
            tests += 2;
            int ok_ct = 1;
            for (int t = 0; t < 24; t++) {
              int j = kp_pt[t];
              if (j >= L && kv[t] != layer_pt[j - L]) { ok_ct = 0; break; }
            }
            if (ok_ct) {
              cons++;
              hist[1][f][0][L]++;
              if (nchk_pt_ct[L] >= MINCHK &&
                  report(1, W[a], f, 0, L, q, dir, nchk_pt_ct[L], Al, In, S, kp_pt, layer_pt))
                surv++;
            }
            int ok_pt = 1;
            const Pair *pr = pairs_pt[L];
            int npt = npair_pt[L];
            for (int k = 0; k < npt; k++) {
              int val = Plet[pr[k].t1], pos = kp_pt[pr[k].t1];
              int nstep = pr[k].nstep;
              for (int s = 0; s < nstep; s++) {
                pos += L;
                val = dec_let(Al, In, f, layer_pt[pos], val);
              }
              if (val != Plet[pr[k].t2]) { ok_pt = 0; break; }
            }
            if (ok_pt) {
              cons++;
              hist[0][f][0][L]++;
              if (nchk_pt_pt[L] >= MINCHK &&
                  report(0, W[a], f, 0, L, q, dir, nchk_pt_pt[L], Al, In, S, kp_pt, layer_pt))
                surv++;
            }
          }
        }
      }
    }
  }

  printf("C %s x x x x %lld consistent %lld survivors %lld alph=%ld..%ld nperm=%ld lmax=%d minchk=%d\n",
         lab, tests, cons, surv, lo, hi, np, LMAX, MINCHK);
  for (int feed = 0; feed < 2; feed++)
    for (int f = 0; f < 3; f++)
      for (int ix = 0; ix < 2; ix++) {
        printf("H %s feed=%s %s ix=%s", lab, FN[feed], MN[f], XN[ix]);
        for (int L = 1; L <= LMAX; L++) printf(" %d:%lld", L, hist[feed][f][ix][L]);
        printf("\n");
      }
  free(Perm);
  return 0;
}
