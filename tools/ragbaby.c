/* Cycle 55: Ragbaby (word-progressive keyed-alphabet cipher), exact test on the 24 crib letters.
   Ragbaby: letter j (0-based) of word w is shifted s = n0 + w + j places along ONE mixed alphabet
   (dir +1: c = A[idx p + s]; dir -1: c = A[idx p - s]). With t_i = s_i - i, t is constant inside a word, and at a
   word start b whose previous word started at a, t jumps by 1 - (b - a)  (mod 26).
   Word divisions are unknown: every segmentation of each crib is tried (2^12 x 2^10). The first word of a crib may
   have started before the crib, so the first jump inside a crib is free if word length <= LMAX(=20) allows it; the
   offset n0 and everything outside the cribs is free, so the test uses only the cribs (exact, offset-free).
   Alphabets: the 86,731 themed/keyword alphabets of alpha.bin (A-Z, KRYPTOS, keyword and keyphrase alphabets).
   usage: ragbaby CT alpha.bin [stepmax]  ; step d generalises "+1 per letter" to "+d per letter/word" (d=1 classic) */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define N 97
#define LMAX 20
static const char *C[2]={"EASTNORTHEAST","BERLINCLOCK"}; static const int P[2]={21,63},L[2]={13,11};
/* returns number of segmentations of crib cb consistent with t[] (values at crib positions), step d */
static int G_cnt,G_first,G_L,G_P,G_d; static const int*G_t;
static void dfs(int j,int start,int cur,int m){
  if(j==G_L){ if(!G_cnt)G_first=m; G_cnt++; return; }
  int pos=G_P+j;
  if(G_t[j]==cur) dfs(j+1,start,cur,m);                       /* same word */
  /* word starts at pos */
  if(start>=0){ if(G_t[j]==((cur+G_d*(1-(pos-start)))%26+26)%26) dfs(j+1,pos,G_t[j],m|1<<(j-1)); }
  else { for(int len=pos-G_P;len<=LMAX;len++) if(G_t[j]==((cur+G_d*(1-len))%26+26)%26){ dfs(j+1,pos,G_t[j],m|1<<(j-1)); break; } }
}
static int cribfit(int cb,const int*t,int d,int*firstmask){
  G_cnt=0;G_first=0;G_L=L[cb];G_P=P[cb];G_d=d;G_t=t; dfs(1,-1,t[0],0); if(firstmask)*firstmask=G_first; return G_cnt;
}
int main(int argc,char**argv){
  const char*ct=argv[1]; if(strlen(ct)!=N){fprintf(stderr,"len\n");return 1;}
  FILE*f=fopen(argv[2],"rb"); fseek(f,0,2); int NA=ftell(f)/26; rewind(f); unsigned char(*AL)[26]=malloc(NA*26);
  if(fread(AL,26,NA,f)!=(size_t)NA)return 1; fclose(f);
  int dmax= argc>3? atoi(argv[3]):1;
  long n1=0,n2=0,nboth=0,shown=0;
  for(int a=0;a<NA;a++){ int idx[26]; for(int i=0;i<26;i++) idx[AL[a][i]]=i;
    for(int dir=-1;dir<=1;dir+=2) for(int d=1;d<=dmax;d++){ if(d%2==0||d%13==0) continue; /* d must be a unit mod 26 */
      int t[2][13], ok[2], fm[2]={0,0};
      for(int cb=0;cb<2;cb++){ for(int j=0;j<L[cb];j++){ int pos=P[cb]+j; int s=dir*(idx[ct[pos]-'A']-idx[C[cb][j]-'A']);
          /* s = n0 + d*(w + j_in_word)  -> t = s - d*pos */
          t[cb][j]=((s - d*pos)%26+26)%26; }
        ok[cb]=cribfit(cb,t[cb],d,&fm[cb]); }
      if(ok[0])n1++; if(ok[1])n2++;
      if(ok[0]&&ok[1]){ nboth++; if(shown<20){ shown++; printf("BOTH a=%d dir=%d d=%d segs=%d/%d mask1=%x mask2=%x\n",a,dir,d,ok[0],ok[1],fm[0],fm[1]); } }
    } }
  printf("alphabets=%d crib1_fit=%ld crib2_fit=%ld both=%ld\n",NA,n1,n2,nboth);
  return 0;
}
