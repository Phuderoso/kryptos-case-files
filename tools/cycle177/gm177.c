/* Cycle 177 (IDEAS I-128 + I-129): ordinary Gromark behind the 165,782 K3-law decimations / routes (all.bin), STRICT or ONE-ERROR,
   any digit base b (5..10). Extends cycle 176's gm176.c (same model G, same perm convention, same output for err 0, base 10).
   Model G: d[i] = d[i-L] + d[i-L+1] mod b from a primer of L digits (0..b-1); PA = A-Z or KRYPTOS; cipher alphabet ARBITRARY;
   w = PA(p) + d (vig) or d - PA(p) (beau; variant = beau after reflecting the alphabet), mod 26.
   Strict fit  <=> over the 24 crib slots  ct_a == ct_b  <=>  w_a == w_b.
   One-error   <=> there is a slot t such that the condition holds on the other 23 slots (one wrong carved letter OR one wrong
                   crib letter at t: with an arbitrary alphabet both just free slot t; a consistent true letter always exists
                   because 23 slots use at most 23 of the 26 letters). The set of such t ("drop mask") = the slots lying in EVERY
                   violated pair; mask == all 24 slots <=> strict fit.
   ix 0: Gromark on the plaintext index, then transpose -> hash join; with err 1 every perm is inserted 24 times, slot t replaced
         by a sentinel label (31) in the canonical partition code, and every primer is looked up 24 times.
   ix 1: transpose first, Gromark on the carved index -> brute force per perm x primer; the drop mask is intersected over the
         violated equal-ct pairs first (fast reject when empty), then over the equal-w / different-ct pairs.
   usage: gm177 CT perms.bin label qlo qhi ix Lmin Lmax base err [primerfile]
   output: H label ix L pa form base err nprim configs strict onlyone ; M label ix L pa form base q primer mask6hex [name] ; END   */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#define N 97
#define FULL 0xFFFFFFu
static const int CI[24]={21,22,23,24,25,26,27,28,29,30,31,32,33,63,64,65,66,67,68,69,70,71,72,73};
static const char*PT="EASTNORTHEASTBERLINCLOCK",*KA="KRYPTOSABCDEFGHIJLMNQUVWXZ";
static int pav[2][24];
/* canonical partition code; slot 'drop' (or -1) gets the sentinel label 31 */
static void canon(const int*x,int drop,uint64_t*a,uint64_t*b){int lab[26];memset(lab,-1,sizeof lab);int n=0;uint64_t A=0,B=0;
  for(int t=0;t<24;t++){uint64_t l;if(t==drop)l=31;else{int v=x[t];if(lab[v]<0)lab[v]=n++;l=lab[v];}
    if(t<12)A|=l<<(5*t);else B|=l<<(5*(t-12));}*a=A;*b=B;}
#define HB 23
static uint64_t *HA,*HBk;static int *Hhead,*nxt;static unsigned char*used;
static long hslot(uint64_t a,uint64_t b){uint64_t h=((a*0x9E3779B97F4A7C15ULL)^(b*0xC2B2AE3D27D4EB4FULL))>>(64-HB);
  while(used[h]&&!(HA[h]==a&&HBk[h]==b))h=(h+1)&((1u<<HB)-1);return (long)h;}
static long hfind(uint64_t a,uint64_t b){long h=hslot(a,b);return used[h]?h:-1;}
static int B_;
static void stream(const int*pr,int L,int*d){for(int i=0;i<L;i++)d[i]=pr[i];for(int i=L;i<N;i++)d[i]=(d[i-L]+d[i-L+1])%B_;}
static int cmpu64(const void*x,const void*y){uint64_t a=*(const uint64_t*)x,b=*(const uint64_t*)y;return a<b?-1:a>b;}
int main(int argc,char**argv){
  setvbuf(stdout,NULL,_IOLBF,0);
  if(argc<11){fprintf(stderr,"usage: gm177 CT perms.bin label qlo qhi ix Lmin Lmax base err [primerfile]\n");return 1;}
  const char*Cs=argv[1];int C[N];if(strlen(Cs)!=N)return 1;for(int i=0;i<N;i++)C[i]=Cs[i]-'A';
  const char*lab=argv[3];long qlo=atol(argv[4]),qhi=atol(argv[5]);int ix=atoi(argv[6]),Lmin=atoi(argv[7]),Lmax=atoi(argv[8]);
  B_=atoi(argv[9]);int err=atoi(argv[10]);
  for(int t=0;t<24;t++){pav[0][t]=PT[t]-'A';pav[1][t]=strchr(KA,PT[t])-KA;}
  FILE*pf=fopen(argv[2],"rb");fseek(pf,0,SEEK_END);long np=ftell(pf)/(2*N);rewind(pf);
  short*P=malloc(np*N*2);if(fread(P,2,np*N,pf)!=(size_t)(np*N))return 2;fclose(pf);if(qhi>np)qhi=np;
  int npr=0,cap=0;int*prs=NULL;int*prL=NULL;char(*prn)[32]=NULL;
  if(argc>11){FILE*f=fopen(argv[11],"r");char nm[64],dg[64];while(fscanf(f,"%63s %63s",nm,dg)==2){if(npr==cap){cap=cap?cap*2:1024;prs=realloc(prs,cap*16*sizeof(int));prL=realloc(prL,cap*sizeof(int));prn=realloc(prn,cap*32);}
      int L=strlen(dg);if(L>16)continue;int okd=1;for(int i=0;i<L;i++){prs[npr*16+i]=dg[i]-'0';if(dg[i]-'0'>=B_)okd=0;}if(!okd)continue;prL[npr]=L;snprintf(prn[npr],32,"%s",nm);npr++;}fclose(f);}
  int usefile=argc>11;int Ls=usefile?0:Lmin,Le=usefile?0:Lmax;
  if(ix==0){
    HA=malloc(sizeof(uint64_t)<<HB);HBk=malloc(sizeof(uint64_t)<<HB);Hhead=malloc(sizeof(int)<<HB);used=calloc(1u<<HB,1);
    int nd=err?24:1;nxt=malloc(sizeof(int)*(qhi-qlo)*nd);
    for(long q=qlo;q<qhi;q++){const short*S=P+q*N;int x[24];for(int t=0;t<24;t++)x[t]=C[S[CI[t]]];
      for(int t=0;t<nd;t++){uint64_t a,b;canon(x,err?t:-1,&a,&b);long h=hslot(a,b);if(!used[h]){used[h]=1;HA[h]=a;HBk[h]=b;Hhead[h]=-1;}
        int id=(int)((q-qlo)*nd+t);nxt[id]=Hhead[h];Hhead[h]=id;}}
    for(int L=Ls;L<=Le;L++){
      long nprim=1;if(!usefile)for(int i=0;i<L;i++)nprim*=B_;else nprim=npr;
      long long fs[2][2]={{0}},fo[2][2]={{0}};
      #pragma omp parallel for schedule(dynamic,4096) reduction(+:fs[:2][:2],fo[:2][:2])
      for(long k=0;k<nprim;k++){int pr[16],LL,d[N];
        if(usefile){LL=prL[k];memcpy(pr,prs+k*16,LL*sizeof(int));}else{LL=L;long z=k;for(int i=LL-1;i>=0;i--){pr[i]=z%B_;z/=B_;}}
        stream(pr,LL,d);
        for(int pa=0;pa<2;pa++)for(int fm=0;fm<2;fm++){int w[24];
          for(int t=0;t<24;t++){int v=fm?d[CI[t]]-pav[pa][t]:pav[pa][t]+d[CI[t]];w[t]=((v%26)+26)%26;}
          uint64_t hit[4096];int nh=0;   /* (perm<<5 | t) */
          for(int t=0;t<nd;t++){uint64_t a,b;canon(w,err?t:-1,&a,&b);long h=hfind(a,b);if(h<0)continue;
            for(int e=Hhead[h];e>=0;e=nxt[e]){if(nh<4096)hit[nh++]=((uint64_t)(e/nd)<<5)|(uint64_t)(e%nd);else{
              #pragma omp critical
              fprintf(stderr,"overflow %s L%d\n",lab,LL);}}}
          if(!nh)continue;qsort(hit,nh,8,cmpu64);
          for(int i=0;i<nh;){uint64_t e=hit[i]>>5;unsigned m=0;while(i<nh&&(hit[i]>>5)==e){m|=1u<<(hit[i]&31);i++;}
            if(!err)m=FULL;
            if(m==FULL)fs[pa][fm]++;else fo[pa][fm]++;
            char ps[20];for(int j=0;j<LL;j++)ps[j]='0'+pr[j];ps[LL]=0;
            #pragma omp critical
            printf("M %s 0 %d %s %s %d %ld %s %06x%s%s\n",lab,LL,pa?"ka":"az",fm?"beau":"vig",B_,qlo+(long)e,ps,m,usefile?" ":"",usefile?prn[k]:"");}
        }
      }
      for(int pa=0;pa<2;pa++)for(int fm=0;fm<2;fm++)printf("H %s 0 %d %s %s %d %d %ld %lld %lld %lld\n",lab,usefile?-1:L,pa?"ka":"az",fm?"beau":"vig",B_,err,nprim,(long long)nprim*(qhi-qlo),fs[pa][fm],fo[pa][fm]);
    }
  } else {
    for(int L=Ls;L<=Le;L++){
      long nprim=1;if(!usefile)for(int i=0;i<L;i++)nprim*=B_;else nprim=npr;
      unsigned char*D=malloc(nprim*N);int*Lk=malloc(nprim*sizeof(int));
      for(long k=0;k<nprim;k++){int pr[16],LL,d[N];if(usefile){LL=prL[k];memcpy(pr,prs+k*16,LL*sizeof(int));}else{LL=L;long z=k;for(int i=LL-1;i>=0;i--){pr[i]=z%B_;z/=B_;}}
        stream(pr,LL,d);for(int i=0;i<N;i++)D[k*N+i]=d[i];Lk[k]=LL;}
      long long fs[2][2]={{0}},fo[2][2]={{0}};
      #pragma omp parallel for schedule(dynamic,64) reduction(+:fs[:2][:2],fo[:2][:2])
      for(long q=qlo;q<qhi;q++){const short*S=P+q*N;int tc[24],ct[24];for(int t=0;t<24;t++){tc[t]=S[CI[t]];ct[t]=C[tc[t]];}
        int ea[300],eb[300],ne=0;for(int a=0;a<24;a++)for(int b=a+1;b<24;b++)if(ct[a]==ct[b]){ea[ne]=a;eb[ne]=b;ne++;}
        for(int pa=0;pa<2;pa++)for(int fm=0;fm<2;fm++){int need[300];
          for(int e=0;e<ne;e++){int r=fm?(pav[pa][ea[e]]-pav[pa][eb[e]]):(pav[pa][eb[e]]-pav[pa][ea[e]]);need[e]=((r%26)+26)%26;}
          for(long k=0;k<nprim;k++){const unsigned char*d=D+k*N;unsigned m=FULL;
            for(int e=0;e<ne;e++){int x=(int)d[tc[ea[e]]]-(int)d[tc[eb[e]]]+26;if(x>=26)x-=26;if(x!=need[e]){if(!err){m=0;break;}m&=(1u<<ea[e])|(1u<<eb[e]);if(!m)break;}}
            if(!m)continue;
            int w[24];for(int t=0;t<24;t++){int v=fm?d[tc[t]]-pav[pa][t]:pav[pa][t]+d[tc[t]];w[t]=((v%26)+26)%26;}
            for(int a=0;a<24&&m;a++)for(int b=a+1;b<24;b++)if(w[a]==w[b]&&ct[a]!=ct[b]){if(!err){m=0;break;}m&=(1u<<a)|(1u<<b);if(!m)break;}
            if(!m)continue;
            if(m==FULL)fs[pa][fm]++;else fo[pa][fm]++;
            char ps[20];for(int i=0;i<Lk[k];i++)ps[i]='0'+d[i];ps[Lk[k]]=0;
            #pragma omp critical
            printf("M %s 1 %d %s %s %d %ld %s %06x%s%s\n",lab,Lk[k],pa?"ka":"az",fm?"beau":"vig",B_,q,ps,m,usefile?" ":"",usefile?prn[k]:"");
          }}
      }
      for(int pa=0;pa<2;pa++)for(int fm=0;fm<2;fm++)printf("H %s 1 %d %s %s %d %d %ld %lld %lld %lld\n",lab,usefile?-1:L,pa?"ka":"az",fm?"beau":"vig",B_,err,nprim,(long long)nprim*(qhi-qlo),fs[pa][fm],fo[pa][fm]);
      free(D);free(Lk);
    }
  }
  printf("END %s %ld %ld\n",lab,qlo,qhi);return 0;}
