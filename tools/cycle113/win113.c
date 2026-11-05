/* Cycle 113: C port of tools/cycle110/window110.py (exact count of column orders consistent with the
   cribs for "periodic substitution (period p) first, complete columnar width w last", columns-in = dir1).
   Same recursion and memo state as the Python: (start, longs used, shorts used [implied], set of
   specific columns, partial key restricted to phases that still occur in later crib positions).
   Usage: win113 W P KIND CIPHERTEXT     KIND in vigAZ beauAZ varAZ vigKA beauKA varKA
   Cribs (0-indexed, repo convention 1-indexed 22-34 / 64-74): EASTNORTHEAST@21, BERLINCLOCK@63. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
typedef unsigned __int128 u128;
static int N,W,P,NLONG,LS,SS,NL,NS; static char CT[128]; static int CRIB[128]; /* -1 or letter index in alphabet */
static int KV[32][128]; /* KV[c][start] encoded cons: computed lazily */
static const char *AZ="ABCDEFGHIJKLMNOPQRSTUVWXYZ", *KA="KRYPTOSABCDEFGHIJLMNQUVWXZ";
static int kindt; static const char *al;
static int idx(char ch){ return (int)(strchr(al,ch)-al); }
static int kf(char c,char p){int a=idx(c),b=idx(p); if(kindt==0) return ((a-b)%26+26)%26; if(kindt==1) return (a+b)%26; return ((b-a)%26+26)%26;}
static char PTCRIB[128];
static int touches(int s,int l){ for(int r=0;r<l;r++) if(s+r<N && PTCRIB[s+r]) return 1; return 0; }
static int laterph[128][32]; /* laterph[pos][ph]=1 if some crib i>=pos with i%P==ph */
/* 40-byte entry; counts are bounded by NL!*NS! (13!*8! ~ 2.5e14 at w21), so 64 bits suffice for stored values */
typedef struct { uint8_t start,nl,used,pad; uint32_t mask; int8_t key[24]; uint64_t val; } Ent;
static Ent *T; static size_t TS=1<<22, TN=0;
static uint64_t hsh(int s,int nl,uint32_t m,const int8_t*k){ uint64_t h=1469598103934665603ULL; h=(h^s)*1099511628211ULL; h=(h^nl)*1099511628211ULL; h=(h^m)*1099511628211ULL; for(int i=0;i<P;i++) h=(h^(uint8_t)k[i])*1099511628211ULL; return h^(h>>29); }
static void grow(void);
static Ent* find(int s,int nl,uint32_t m,const int8_t*k,int *found){
  uint64_t h=hsh(s,nl,m,k); size_t i=h&(TS-1);
  while(T[i].used){ Ent*e=&T[i]; if(e->start==s&&e->nl==nl&&e->mask==m&&!memcmp(e->key,k,P)){*found=1;return e;} i=(i+1)&(TS-1);}
  *found=0; return &T[i];
}
static void put(int s,int nl,uint32_t m,const int8_t*k,u128 v){
  if(TN*10>TS*7) grow(); int f; Ent*e=find(s,nl,m,k,&f); if(!f){TN++; e->used=1; e->start=s; e->nl=nl; e->mask=m; memcpy(e->key,k,P);} e->val=(uint64_t)v;
}
static void grow(void){ Ent*o=T; size_t os=TS; TS<<=1; T=calloc(TS,sizeof(Ent)); if(!T){fprintf(stderr,"oom\n");exit(2);} TN=0;
  for(size_t i=0;i<os;i++) if(o[i].used) put(o[i].start,o[i].nl,o[i].mask,o[i].key,o[i].val); free(o); }
static u128 fact(int n){ u128 r=1; for(int i=2;i<=n;i++) r*=i; return r; }
static int cons(int c,int start,int l,int8_t*out){ /* out: per phase -1 or value; returns 0 if self-inconsistent */
  for(int i=0;i<P;i++) out[i]=-1;
  for(int r=0;r<l;r++){ int i=start+r; if(i<N && PTCRIB[i]){ int v=kf(CT[r*W+c],PTCRIB[i]); int ph=i%P; if(out[ph]!=-1&&out[ph]!=v) return 0; out[ph]=v; } }
  return 1;
}
static long long nodes=0;
static u128 rec(int start,int nl,int ns,uint32_t spec,int8_t*key){
  if(start==N){ int sl=0,ss=0; for(int c=0;c<W;c++) if(spec>>c&1){ if(c<NLONG) sl++; else ss++; } return fact(NL-sl)*fact(NS-ss); }
  /* memoise only where the next slot (long or short) touches a crib; pure-filler stretches are re-walked
     (at most ~2^7 paths across the gap) instead of stored, which keeps the table small */
  int memo=touches(start,LS)||touches(start,SS);
  int f; if(memo){ Ent*e=find(start,nl,spec,key,&f); if(f) return e->val; }
  nodes++;
  u128 tot=0; int8_t cs[32],k2[32];
  for(int isl=1;isl>=0;isl--){
    if(isl && nl>=NL) continue; if(!isl && ns>=NS) continue;
    int l=isl?LS:SS; int nl2=nl+isl, ns2=ns+!isl;
    if(!touches(start,l)){ tot+=rec(start+l,nl2,ns2,spec,key); continue; }
    int c0=isl?0:NLONG, c1=isl?NLONG:W;
    for(int c=c0;c<c1;c++){
      if(spec>>c&1) continue;
      if(!cons(c,start,l,cs)) continue;
      int ok=1; for(int ph=0;ph<P;ph++) if(cs[ph]!=-1 && key[ph]!=-1 && key[ph]!=cs[ph]){ok=0;break;}
      if(!ok) continue;
      int np=start+l; for(int ph=0;ph<P;ph++){ int v=key[ph]!=-1?key[ph]:cs[ph]; k2[ph]=(np<N && laterph[np][ph])?v:-1; }
      tot+=rec(np,nl2,ns2,spec|1u<<c,k2);
    }
  }
  if(memo) put(start,nl,spec,key,tot); return tot;
}
static void pr128(u128 v){ char b[64]; int i=63; b[i]=0; if(!v) b[--i]='0'; while(v){ b[--i]='0'+(int)(v%10); v/=10; } printf("%s",b+i); }
int main(int argc,char**argv){
  if(argc<5||0){fprintf(stderr,"usage\n");return 1;}
  W=atoi(argv[1]); P=atoi(argv[2]); if(P>24||W>32){fprintf(stderr,"P<=24, W<=32\n");return 1;} const char*k=argv[3]; strcpy(CT,argv[4]); N=strlen(CT);
  al=strstr(k,"KA")?KA:AZ; kindt=!strncmp(k,"vig",3)?0:!strncmp(k,"beau",4)?1:2;
  memset(PTCRIB,0,sizeof PTCRIB);
  const char*c1="EASTNORTHEAST",*c2="BERLINCLOCK"; for(int j=0;c1[j];j++) PTCRIB[21+j]=c1[j]; for(int j=0;c2[j];j++) PTCRIB[63+j]=c2[j];
  for(int pos=0;pos<=N;pos++) for(int ph=0;ph<P;ph++){ laterph[pos][ph]=0; for(int i=pos;i<N;i++) if(PTCRIB[i]&&i%P==ph) laterph[pos][ph]=1; }
  NLONG=N%W; LS=N/W+1; SS=N/W; NL=NLONG; NS=W-NLONG;
  T=calloc(TS,sizeof(Ent)); int8_t key[32]; for(int i=0;i<32;i++) key[i]=-1;
  u128 r=rec(0,0,0,0,key); pr128(r); printf(" nodes=%lld states=%zu\n",nodes,TN); return 0;
}
