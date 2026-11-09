/* Cycle 169 (I-087 + I-090): bookrk (cycle 35) with one-error tolerance and a masked depth diagnostic.
   Same substitutions (24 additive tableaux + 5 five-bit XOR codes), same Models A/B, same perms/texts format.
   For each (perm, model, mode, text) two bitsets over valid offsets 0..nofs-1 are kept while the 24 crib
   constraints are processed in a fixed order:  A = offsets satisfying all constraints so far,
   O = offsets missing at most one so far.  Update: O <- (O & v) | A ;  A <- A & v.  Every word is masked to
   real offsets (o < nofs), which fixes the I-090 tail-bit issue (bookrk counted <= 63 bits past the last offset).
   One wrong crib letter or one wrong carved letter at a crib position = exactly one failed constraint, so
   O != 0 after all 24 <=> some offset fits >= 23 of 24.
   depth  = strict depth (number of leading constraints some real offset satisfies together)  [masked]
   depth1 = number of leading constraints some real offset satisfies with at most one miss    [masked]
   Prints FULL (24/24) and FIT23 (exactly 23/24, with the missed crib index) lines, CAND1 for depth1 >= THR,
   and a SUMMARY with both histograms. usage: bookrk1e CARVED perms.bin texts.txt THR */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#define N 97
static const char*KA="KRYPTOSABCDEFGHIJLMNQUVWXZ";
static int ita2[26]={0x03,0x19,0x0E,0x09,0x01,0x0D,0x1A,0x14,0x06,0x0B,0x0F,0x12,0x1C,0x0C,0x18,0x16,0x17,0x0A,0x05,0x10,0x07,0x1E,0x13,0x1D,0x15,0x11};
int STRICTCFG=0;int code[5][26],dec[5][32],kai[26];
int main(int argc,char**argv){
  if(argc<5){fprintf(stderr,"usage: bookrk1e CARVED perms.bin texts.txt THR\n");return 2;}
  const char*car=argv[1];FILE*f=fopen(argv[2],"rb");fseek(f,0,SEEK_END);long sz=ftell(f);fseek(f,0,SEEK_SET);
  int np=sz/(2*N);short*perms=malloc(sz);if(fread(perms,2,(size_t)np*N,f)!=(size_t)np*N)return 1;fclose(f);
  int THR=atoi(argv[4]); if(argc>5&&!strcmp(argv[5],"strictcfg"))STRICTCFG=1;
  for(int l=0;l<26;l++)kai[l]=strchr(KA,'A'+l)-KA;
  for(int e=0;e<5;e++){for(int v=0;v<32;v++)dec[e][v]=-1;
    for(int l=0;l<26;l++){int c;if(e==0)c=ita2[l];else if(e==1)c=l;else if(e==2)c=l+1;else c=(e==3)?kai[l]:kai[l]+1;code[e][l]=c;dec[e][c]=l;}}
  const char*cr1="EASTNORTHEAST",*cr2="BERLINCLOCK";int cp[24],cl[24],nc=0;
  for(int i=0;i<13;i++){cp[nc]=21+i;cl[nc++]=cr1[i]-'A';}for(int i=0;i<11;i++){cp[nc]=63+i;cl[nc++]=cr2[i]-'A';}
  FILE*t=fopen(argv[3],"r");static char name[64];char*buf=malloc(1<<22);
  long hist[25]={0},hist1[25]={0},histS[25]={0};int gbestS=0;int gbest=0,gbest1=0;long full=0,fit23=0,cfg=0;
  while(fscanf(t,"%63s %4000000s",name,buf)==2){
    int T=strlen(buf);int W=(T+63)/64+4;int nofs=T-N+1;int WO=(nofs+63)/64;
    uint64_t last=(nofs%64)?((1ULL<<(nofs%64))-1):~0ULL;
    uint64_t*B=calloc((size_t)26*W,8);for(int i=0;i<T;i++)B[(size_t)(buf[i]-'A')*W+i/64]|=1ULL<<(i%64);
    uint64_t*A=malloc(8*(size_t)W),*O=malloc(8*(size_t)W);
    for(int p=0;p<np;p++){short*P=perms+(long)p*N;int inv[N];for(int k=0;k<N;k++)inv[P[k]]=k;
     for(int m=0;m<2;m++)for(int md=0;md<29;md++){
      int q[24],req[24],ok=1;
      for(int j=0;j<24;j++){int ci; if(m==0){q[j]=cp[j];ci=car[P[cp[j]]]-'A';}else{q[j]=inv[cp[j]];ci=car[inv[cp[j]]]-'A';}
        int pl=cl[j],k;
        if(md<24){int ty=md%3,ap=(md/3)&1,ac=(md/6)&1,ak=(md/12)&1;
          int c=ac?kai[ci]:ci, pp=ap?kai[pl]:pl;
          int kv= ty==0?(c-pp+26)%26: ty==1?(c+pp)%26:(pp-c+26)%26; k= ak? KA[kv]-'A':kv;}
        else{int e=md-24;int kc=code[e][ci]^code[e][pl];k=dec[e][kc];if(k<0){k=-1;}}
        req[j]=k;}
      /* XOR codes: an undecodable key symbol (k<0) is a constraint no offset satisfies (strict bookrk skipped the
         whole config; here it may be the one miss). */
      int nbad=0;for(int j=0;j<24;j++)if(req[j]<0)nbad++; if(nbad>1||(STRICTCFG&&nbad>0))ok=0;
      if(!ok)continue; cfg++;
      int depth=0,depth1=0,aalive=1,j0=24;
      for(int j=0;j<24;j++){int s=q[j]/64,b=q[j]%64;uint64_t anyA=0,anyO=0;long cnt=0;const uint64_t*Bl=req[j]>=0?B+(size_t)req[j]*W:NULL;
        for(int w=0;w<WO;w++){uint64_t v=0; if(Bl) v= b? (Bl[w+s]>>b)|(Bl[w+s+1]<<(64-b)) : Bl[w+s];
          uint64_t mk=(w==WO-1)?last:~0ULL; v&=mk;
          if(j==0){A[w]=v;O[w]=mk;} else {O[w]=(O[w]&v)|A[w]; A[w]&=v;}
          anyA|=A[w];anyO|=O[w]; if(j>0)cnt+=__builtin_popcountll(O[w]);}
        if(aalive){ if(anyA) depth=j+1; else aalive=0; }
        if(!anyO)break;
        depth1=j+1;
        if(j>0 && j<23 && cnt*8<WO){j0=j+1;break;}   /* sparse: finish offset by offset */
      }
      if(j0<24){ /* list phase: every surviving offset scanned letter by letter over constraints j0..23 */
        for(int w=0;w<WO;w++){uint64_t v=O[w];while(v){int o=w*64+__builtin_ctzll(v);v&=v-1;
          int mis=((A[w]>>(o%64))&1)?0:1, d0=mis?0:j0, d1=j0;
          for(int j=j0;j<24;j++){int hit=req[j]>=0&&buf[o+q[j]]-'A'==req[j];
            if(!hit){mis++; if(mis>1)break;} if(mis==0)d0=j+1; d1=j+1;}
          if(d0>depth)depth=d0; if(d1>depth1)depth1=d1;}}
      }
      if(depth1==24){
        for(int w=0;w<WO;w++){uint64_t v=O[w];while(v){int o=w*64+__builtin_ctzll(v);v&=v-1;
          int miss=-1,nm=0;for(int j=0;j<24;j++){int pos=o+q[j];if(req[j]<0||buf[pos]-'A'!=req[j]){miss=j;nm++;}}
          if(nm==0){full++;printf("FULL perm=%d model=%c mode=%d text=%s offset=%d\n",p,m?'B':'A',md,name,o);}
          else if(nm==1){fit23++;printf("FIT23 perm=%d model=%c mode=%d text=%s offset=%d miss=%d\n",p,m?'B':'A',md,name,o,miss);}
          }}}
      hist[depth]++;hist1[depth1]++; if(!nbad){histS[depth]++; if(depth>gbestS)gbestS=depth;} if(depth>gbest)gbest=depth; if(depth1>gbest1)gbest1=depth1;
      if(depth1>=THR&&depth1<24)printf("CAND1 depth1=%d depth=%d perm=%d model=%c mode=%d text=%s\n",depth1,depth,p,m?'B':'A',md,name);
     }}
    free(B);free(A);free(O);}
  printf("SUMMARY perms=%d configs=%ld best=%d best1=%d full=%ld fit23=%ld hist:",np,cfg,gbest,gbest1,full,fit23);
  for(int c=0;c<=24;c++)if(hist[c])printf(" %d:%ld",c,hist[c]);printf(" hist1:");
  for(int c=0;c<=24;c++)if(hist1[c])printf(" %d:%ld",c,hist1[c]);printf(" bestS=%d histS:",gbestS);
  for(int c=0;c<=24;c++)if(histS[c])printf(" %d:%ld",c,histS[c]);printf("\n");return 0;}
