/* Cycle 171 (IDEAS I-096): Porta behind K3-law decimations / spiral-diagonal routes (or any perms file) under ONE error.
   Same model as porta170.c (cycle 170, case 158): keyed ordering o (173,431 orderings from alpha.bin, splits F/E),
   halves H1=o[0..12], H2=o[13..25]; V1: H1[i]<->H2[(i+k)%13], V2: H1[i]<->H2[(k-i)%13]; model A (key index j) or
   B (key index perm[j]).  One error = one wrong crib letter or one wrong carved letter at a crib position, i.e. one of
   the 24 crib pairs (PT[j], CT[perm[j]]) is arbitrary.  Stage 1 (key-free, exact): a mask (half set) passes iff at most
   one crib pair fails to cross halves; if exactly one fails, it is the forced error d.  Self-mapped pairs (PT = CT) never
   cross: >= 2 of them kill the perm, 1 forces d.  Stage 2 per surviving ordering:
     periodic L 1..26: d forced -> strict consistency of the other 23 key values; d free -> consistent after removing at
     most one value (one residue class may hold exactly one dissenting value).
     running keys (texts, fm, s, c0 as cycle 170): at most one of the 24 key equations fails (d forced: the 23 others hold);
     c0 tried from each of the first two usable constraints.
   Expectations (I-097): for every survivor and (V, model, L) the chance probability of the periodic test is summed:
     d forced: 13^-c (c = 23 - distinct residues), d free: 13^-c24 + sum_i 13^-c(i) (union bound, c(i) = checks without i).
   Usage: porta171 CT perms.bin alpha.bin texts.txt [stride offset]   env NORK=1 skips running keys, RKFREE=1 runs
   running keys only for d-free survivors. Prints FIT lines (periodic L <= LMAX(23) or RK) + SUMMARY + PERIODIC rows. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <math.h>
#define N 97
static const char *CRIB1="EASTNORTHEAST", *CRIB2="BERLINCLOCK";
static int cpos[24], cpt[24];
static int nord; static uint8_t (*ord)[26]; static int *ordsrc;
static int nmask; static uint32_t *mask; static int *mstart, *mlist;
static int ntext; static char **tname; static uint8_t **ttext; static int *tlen;
typedef struct {uint32_t m; int o;} MO;
static int cmpmo(const void*a,const void*b){const MO*x=a,*y=b; return x->m<y->m?-1:x->m>y->m?1:x->o-y->o;}
typedef struct {uint8_t c[26]; int i;} CI;
static int cmpci(const void*a,const void*b){int r=memcmp(((CI*)a)->c,((CI*)b)->c,26); return r?r:((CI*)a)->i-((CI*)b)->i;}
/* periodic consistency with key values kv (kv<0 = dropped), at most `allow` dissenting value (only when no drop) */
static int per_ok(const int*ix,const int*kv,int L,int allow){
  int cnt[26][13]; int tot[26]; memset(cnt,0,sizeof cnt); memset(tot,0,sizeof tot);
  for(int i=0;i<24;i++){ if(kv[i]<0)continue; int r=ix[i]%L; cnt[r][kv[i]]++; tot[r]++; }
  int miss=0; for(int r=0;r<L;r++){ if(!tot[r])continue; int mx=0; for(int k=0;k<13;k++) if(cnt[r][k]>mx)mx=cnt[r][k]; miss+=tot[r]-mx; if(miss>allow)return 0; }
  return 1;
}
static int checks(const int*ix,const int*kv,int L,int skip){ int seen[26]={0},n=0,d=0;
  for(int i=0;i<24;i++){ if(i==skip||kv[i]<0)continue; n++; int r=ix[i]%L; if(!seen[r]){seen[r]=1;d++;} } return n-d; }
int main(int argc,char**argv){
  if(argc<5){fprintf(stderr,"usage\n");return 1;}
  const char*CT=argv[1]; int stride=argc>5?atoi(argv[5]):1, off=argc>6?atoi(argv[6]):0; int LMAX=getenv("LMAX")?atoi(getenv("LMAX")):23;
  int NORK=getenv("NORK")!=NULL, RKFREE=getenv("RKFREE")!=NULL;
  if(strlen(CT)!=N){fprintf(stderr,"CT length\n");return 1;}
  for(int i=0;i<13;i++){cpos[i]=21+i;cpt[i]=CRIB1[i]-'A';}
  for(int i=0;i<11;i++){cpos[13+i]=63+i;cpt[13+i]=CRIB2[i]-'A';}
  FILE*f=fopen(argv[2],"rb"); fseek(f,0,2); long np=ftell(f)/194; fseek(f,0,0);
  int16_t*P=malloc(np*194); if(fread(P,194,np,f)!=(size_t)np)return 2; fclose(f);
  f=fopen(argv[3],"rb"); fseek(f,0,2); long na=ftell(f)/26; fseek(f,0,0);
  uint8_t*A=malloc(na*26); if(fread(A,26,na,f)!=(size_t)na)return 2; fclose(f);
  size_t nt=(size_t)na*2; CI*ci=malloc(nt*sizeof(CI));
  for(long a=0;a<na;a++){ memcpy(ci[2*a].c,A+26*a,26); ci[2*a].i=2*a;
    for(int i=0;i<13;i++){ci[2*a+1].c[i]=A[26*a+2*i]; ci[2*a+1].c[13+i]=A[26*a+2*i+1];} ci[2*a+1].i=2*a+1; }
  qsort(ci,nt,sizeof(CI),cmpci);
  ord=malloc(nt*26); ordsrc=malloc(nt*sizeof(int)); nord=0;
  for(size_t i=0;i<nt;i++){ if(i&&!memcmp(ci[i].c,ci[i-1].c,26))continue; memcpy(ord[nord],ci[i].c,26); ordsrc[nord]=ci[i].i; nord++; }
  free(ci);
  MO*mo=malloc(nord*sizeof(MO));
  for(int o=0;o<nord;o++){uint32_t m=0; for(int i=0;i<13;i++)m|=1u<<ord[o][i]; if(m&1u) m^=0x3FFFFFFu; mo[o].m=m; mo[o].o=o;}
  qsort(mo,nord,sizeof(MO),cmpmo);
  mask=malloc(nord*4); mstart=malloc((nord+1)*sizeof(int)); mlist=malloc(nord*sizeof(int)); nmask=0;
  for(int i=0;i<nord;i++){ if(!i||mo[i].m!=mo[i-1].m){mask[nmask]=mo[i].m; mstart[nmask]=i; nmask++;} mlist[i]=mo[i].o; }
  mstart[nmask]=nord; free(mo);
  f=fopen(argv[4],"r"); static char line[4000000]; int cap=64; tname=malloc(cap*8); ttext=malloc(cap*8); tlen=malloc(cap*4); ntext=0;
  while(fgets(line,sizeof line,f)){ char*sp=strchr(line,' '); if(!sp)continue; *sp=0; char*t=sp+1; int L=0; uint8_t*b=malloc(strlen(t)+1);
    for(char*c=t;*c;c++) if(*c>='A'&&*c<='Z') b[L++]=*c-'A';
    tname[ntext]=strdup(line); ttext[ntext]=b; tlen[ntext]=L; ntext++; }
  fclose(f);
  fprintf(stderr,"perms %ld alphabets %ld orderings %d masks %d texts %d\n",np,na,nord,nmask,ntext);
  long long perm_done=0,dead2self=0,sp_free=0,sp_forced=0,so_free=0,so_forced=0,rk_fits=0,rk_free_ord=0,rk_forced_ord=0;
  static long long ph[2][2][27]; static double pe[2][2][27];
  #pragma omp parallel for schedule(dynamic,1) reduction(+:perm_done,dead2self,sp_free,sp_forced,so_free,so_forced,rk_fits,rk_free_ord,rk_forced_ord)
  for(long p=off;p<np;p+=stride){
    const int16_t*pm=P+97*p; int a[24],b[24],nself=0,dself=-1; perm_done++;
    uint32_t ea[24],eb[24];
    for(int i=0;i<24;i++){a[i]=cpt[i]; b[i]=CT[pm[cpos[i]]]-'A'; if(a[i]==b[i]){nself++;dself=i;} ea[i]=a[i]; eb[i]=b[i];}
    if(nself>=2){dead2self++;continue;}
    long long lh[2][2][27]={{{0}}}; double le[2][2][27]={{{0}}};
    for(int mi=0;mi<nmask;mi++){ uint32_t m=mask[mi]; int bad=0,d=-1;
      for(int i=0;i<24;i++){ if(!(((m>>ea[i])^(m>>eb[i]))&1u)){ bad++; d=i; if(bad>1)break; } }
      if(bad>1)continue;
      if(bad==1) sp_forced++; else sp_free++;
      for(int li=mstart[mi];li<mstart[mi+1];li++){ int o=mlist[li]; int pos[26]; for(int i=0;i<26;i++)pos[ord[o][i]]=i;
        if(d>=0) so_forced++; else so_free++;
        int kv[2][24];
        for(int i=0;i<24;i++){ if(i==d){kv[0][i]=kv[1][i]=-1;continue;} int ip=pos[a[i]],ic=pos[b[i]]; int h1=ip<13?ip:ic, h2=(ip<13?ic:ip)-13; kv[0][i]=((h2-h1)%13+13)%13; kv[1][i]=(h2+h1)%13;}
        char fitL[2][2][27]; int anyfit=0;
        for(int v=0;v<2;v++)for(int md=0;md<2;md++){ int ix[24]; for(int i=0;i<24;i++)ix[i]=md?pm[cpos[i]]:cpos[i];
          for(int L=1;L<=26;L++){ int ok=per_ok(ix,kv[v],L,d>=0?0:1); fitL[v][md][L]=ok; if(ok){lh[v][md][L]++; if(L<=LMAX)anyfit=1;}
            double e; if(d>=0) e=pow(13.0,-checks(ix,kv[v],L,-1)); else { e=pow(13.0,-checks(ix,kv[v],L,-1)); for(int s=0;s<24;s++) e+=pow(13.0,-checks(ix,kv[v],L,s)); if(e>1)e=1; }
            le[v][md][L]+=e; } }
        int nrk=0; char rkdesc[2048]; rkdesc[0]=0;
        if(!NORK && !(RKFREE && d>=0)){
          if(d>=0) rk_forced_ord++; else rk_free_ord++;
          for(int t=0;t<ntext;t++){ const uint8_t*T=ttext[t]; int TL=tlen[t];
            for(int fm=0;fm<2;fm++){ int fv[26]; for(int x=0;x<26;x++) fv[x]=fm? pos[x]/2 : x/2;
              uint8_t *G=malloc(TL); for(int x=0;x<TL;x++) G[x]=fv[T[x]];
              for(int v=0;v<2;v++)for(int md=0;md<2;md++){ int ix[24]; for(int i=0;i<24;i++)ix[i]=md?pm[cpos[i]]:cpos[i];
                int us[24],nu=0; for(int i=0;i<24;i++) if(kv[v][i]>=0) us[nu++]=i;
                int allow=(d>=0)?0:1;
                for(int s=0;s<2;s++){ /* constraint i holds iff (kv_i - sg*G[t0+ix_i]) mod 13 == c0 ; table R[k][g] */
                  uint8_t R[13][13]; for(int k=0;k<13;k++)for(int g=0;g<13;g++) R[k][g]=(uint8_t)(((k-(s?-1:1)*g)%13+26)%13);
                  const uint8_t *Ru[24]; int ixu[24]; for(int u=0;u<nu;u++){Ru[u]=R[kv[v][us[u]]]; ixu[u]=ix[us[u]];}
                  for(int t0=0;t0+97<=TL;t0++){ const uint8_t*Gt=G+t0;
                    int c0=Ru[0][Gt[ixu[0]]], c1=Ru[1][Gt[ixu[1]]];
                    if(c0!=c1 && !allow) continue;
                    int cand[2]={c0,c1}, ncand=(c0==c1)?1:2;
                    for(int cc=0;cc<ncand;cc++){ int c=cand[cc]; int mis=0,mi2=-1;
                      for(int u=0;u<nu;u++){ if(Ru[u][Gt[ixu[u]]]!=c){mis++;mi2=us[u]; if(mis>allow)break;} }
                      if(mis<=allow){ nrk++; if(strlen(rkdesc)<1800) sprintf(rkdesc+strlen(rkdesc)," RK:%s:f%d:V%d:%c:s%c:c%d:t%d:miss%d",tname[t],fm,v+1,md?'B':'A',s?'-':'+',c,t0,d>=0?d:mi2); break; }
                    }}}}
              free(G);}}
          rk_fits+=nrk; }
        if(anyfit||nrk){
          #pragma omp critical
          { printf("FIT perm %ld ord %d src_alpha %d split %c d %d ",p,o,ordsrc[o]/2,(ordsrc[o]&1)?'E':'F',d);
            for(int i=0;i<26;i++)putchar('A'+ord[o][i]); printf(" per");
            for(int v=0;v<2;v++)for(int md=0;md<2;md++){printf(" V%d%c:",v+1,md?'B':'A'); for(int L=1;L<=26;L++) if(fitL[v][md][L])printf("%d,",L);}
            printf(" rk %d%s\n",nrk,rkdesc); }
        }
      }
    }
    #pragma omp critical
    { for(int v=0;v<2;v++)for(int md=0;md<2;md++)for(int L=1;L<=26;L++){ph[v][md][L]+=lh[v][md][L]; pe[v][md][L]+=le[v][md][L];} }
  }
  printf("SUMMARY perms %lld masks %d orderings %d dead_2self %lld surv_mask_free %lld surv_mask_forced %lld surv_ord_free %lld surv_ord_forced %lld rk_ord_free %lld rk_ord_forced %lld rk_fits %lld\n",
    perm_done,nmask,nord,dead2self,sp_free,sp_forced,so_free,so_forced,rk_free_ord,rk_forced_ord,rk_fits);
  for(int v=0;v<2;v++)for(int md=0;md<2;md++){printf("PERIODIC V%d%c",v+1,md?'B':'A'); for(int L=1;L<=26;L++)printf(" %lld",ph[v][md][L]); printf("\n");
    printf("EXPECT V%d%c",v+1,md?'B':'A'); for(int L=1;L<=26;L++)printf(" %.3g",pe[v][md][L]); printf("\n");}
  return 0;
}
