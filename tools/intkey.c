/* Cycle 56: INTERRUPTED KEY (ACA "interrupted key"), exact test on the 24 crib letters.
   A keyword K (length L) is applied letter by letter on a tableau built from ONE mixed alphabet A (K1/K2 style:
   row for key letter k is A shifted so that row k starts at k). At arbitrary interruption points (e.g. every
   plaintext word, every X, wherever the encipherer chooses) the key restarts at K[0]; otherwise it advances by one
   and wraps after K[L-1]. Interruption points are unknown, so every segmentation is allowed: a bitmask DP over the
   key index state (continue: j -> j+1 mod L; restart: j -> 0). The key index at each crib start is free.
   Modes: 0 Vigenere a(k)=a(c)-a(p); 1 Beaufort a(k)=a(c)+a(p); 2 variant a(k)=a(p)-a(c)  (a = index in A).
   Required key letter at crib position i is A[r_i]; match mask = positions j with K[j] == that letter.
   usage: intkey CT alpha.bin words.txt [amax]   -> prints every (alphabet, mode, word) consistent with both cribs */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define N 97
static const char*CR[2]={"EASTNORTHEAST","BERLINCLOCK"}; static const int PO[2]={21,63},LE[2]={13,11};
#define MW 20000
static char W[MW][20]; static int WL[MW]; static unsigned M[MW][26];
int main(int argc,char**argv){
  const char*ct=argv[1]; if(strlen(ct)!=N){fprintf(stderr,"len\n");return 1;}
  FILE*f=fopen(argv[2],"rb"); fseek(f,0,2); int NA=ftell(f)/26; rewind(f);
  unsigned char(*AL)[26]=malloc((size_t)NA*26); if(fread(AL,26,NA,f)!=(size_t)NA)return 1; fclose(f);
  if(argc>4) NA = atoi(argv[4])<NA? atoi(argv[4]):NA;
  FILE*g=fopen(argv[3],"r"); int nw=0; char buf[64];
  while(nw<MW && fscanf(g,"%63s",buf)==1){ int l=strlen(buf); if(l<1||l>16)continue; strcpy(W[nw],buf); WL[nw]=l;
    memset(M[nw],0,sizeof M[nw]); for(int j=0;j<l;j++) M[nw][buf[j]-'A']|=1u<<j; nw++; }
  fclose(g);
  long hits=0, tests=0;
  for(int a=0;a<NA;a++){ int idx[26]; for(int i=0;i<26;i++) idx[AL[a][i]]=i;
    for(int mode=0;mode<3;mode++){
      int need[24]; int q=0;
      for(int cb=0;cb<2;cb++) for(int j=0;j<LE[cb];j++){ int pos=PO[cb]+j; int c=idx[ct[pos]-'A'], p=idx[CR[cb][j]-'A'];
        int r = mode==0? c-p : mode==1? c+p : p-c; r=((r%26)+26)%26; need[q++]=AL[a][r]; }
      for(int w=0;w<nw;w++){ int L=WL[w]; unsigned full=(L==32)?~0u:((1u<<L)-1); const unsigned*mm=M[w]; tests++;
        int ok=1, q2=0;
        for(int cb=0;cb<2&&ok;cb++){ unsigned S=full & mm[need[q2++]];
          for(int j=1;j<LE[cb]&&S;j++){ unsigned R=((S<<1)|(S>>(L-1)))&full; R|=1u; S=R&mm[need[q2++]]; }
          if(!S) ok=0; else q2=(cb==0?13:24); }
        if(ok){ hits++; printf("HIT a=%d mode=%d key=%s\n",a,mode,W[w]); }
      } } }
  fprintf(stderr,"alphabets=%d words=%d tests=%ld hits=%ld\n",NA,nw,tests,hits);
  printf("SUMMARY alphabets=%d words=%d tests=%ld hits=%ld\n",NA,nw,tests,hits);
  return 0; }
