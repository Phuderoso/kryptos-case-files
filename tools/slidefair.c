/* Cycle 57: SLIDEFAIR (ACA; Vigenere, Beaufort and variant forms), exact crib test.
   Plaintext split into digraphs starting at offset off (0: the 97th letter is left over; 1: the first is).
   Digraph j uses key letter K[j mod L]. Top row = mixed alphabet A; bottom row: vig A[x+k], beau A[k-x], var A[x-k].
   p1 on top, p2 on bottom; c1 = bottom under p1's column, c2 = top above p2's column; if the two columns coincide,
   both move one column right. For every digraph touching a crib, the set of key values k (0..25, index into A) that
   decrypt it to the known letters is a 26-bit mask; for each period L the masks are ANDed per residue class.
   usage: slidefair CT alpha.bin nalpha LMAX   -> prints every (alphabet, mode, off, L) with all residue sets non-empty */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define N 97
static const char *PT="EASTNORTHEASTBERLINCLOCK";
int main(int argc,char**argv){
  const char*CT=argv[1]; FILE*f=fopen(argv[2],"rb"); static unsigned char AL[100000][26]; int NA=fread(AL,26,100000,f); fclose(f);
  int na=atoi(argv[3]); if(na>NA) na=NA; int LMAX=atoi(argv[4]);
  int known[N]; for(int i=0;i<N;i++) known[i]=-1;
  for(int i=0;i<13;i++) known[21+i]=PT[i]-65; for(int i=0;i<11;i++) known[63+i]=PT[13+i]-65;
  long hits=0,tests=0; long hist[64]={0};
  for(int a=0;a<na;a++){ int idx[26]; for(int i=0;i<26;i++) idx[AL[a][i]]=i;
    for(int mode=0;mode<3;mode++) for(int off=0;off<2;off++){
      int pj[64], np=0; unsigned msk[64];
      for(int j=0, i=off; i+1<N; j++, i+=2){ if(known[i]<0 && known[i+1]<0) continue;
        int c1=idx[CT[i]-65], c2=idx[CT[i+1]-65]; unsigned m=0;
        for(int k=0;k<26;k++){
          int x = mode==0? (c1-k+26)%26 : mode==1? (k-c1+26)%26 : (c1+k)%26;   /* column of c1 in bottom row */
          int y = c2, cx;                                                      /* column of c2 in top row */
          int p1,p2;
          if(x!=y){ cx=x; p1=AL[a][x]; int col=y; p2 = mode==0? AL[a][(col+k)%26] : mode==1? AL[a][(k-col+26)%26] : AL[a][(col-k+26)%26]; }
          else { cx=(x+25)%26; p1=AL[a][cx]; p2 = mode==0? AL[a][(cx+k)%26] : mode==1? AL[a][(k-cx+26)%26] : AL[a][(cx-k+26)%26]; }
          if((known[i]<0||known[i]==p1)&&(known[i+1]<0||known[i+1]==p2)) m|=1u<<k; }
        pj[np]=j; msk[np]=m; np++; }
      for(int L=1;L<=LMAX;L++){ unsigned R[64]; for(int r=0;r<L;r++) R[r]=(1u<<26)-1; int ok=1; tests++;
        for(int q=0;q<np&&ok;q++){ R[pj[q]%L]&=msk[q]; if(!R[pj[q]%L]) ok=0; }
        if(ok){ hits++; hist[L]++; if(L>=3){ printf("HIT a=%d mode=%d off=%d L=%d key=",a,mode,off,L);
          for(int r=0;r<L;r++){ unsigned m=R[r]; if(m==(1u<<26)-1){putchar('?');continue;} if(__builtin_popcount(m)>1){putchar('[');for(int k=0;k<26;k++) if(m>>k&1) putchar('A'+AL[a][k]); putchar(']');} else putchar('A'+AL[a][__builtin_ctz(m)]); }
          putchar('\n'); } } } } }
  printf("SUMMARY alphabets=%d tests=%ld hits=%ld HIST",na,tests,hits); for(int L=1;L<=LMAX;L++) printf(" %d:%ld",L,hist[L]); printf("\n"); return 0; }
