/* Cycle 170: Porta behind K3-law decimations and spiral/diagonal routes (IDEAS I-089).
   Model: pt (97) -> Porta substitution with a keyed ordering o[0..25] split in halves H1=o[0..12], H2=o[13..25]
   (split F: o = alphabet; split E: o = alphabet[0::2] + alphabet[1::2]); key value k in 0..12 per letter;
   V1: H1[i] <-> H2[(i+k) mod 13], V2: H1[i] <-> H2[(k-i) mod 13] (both reciprocal); transposition perm
   (perm[j] = carved position holding plaintext letter j); key index j (model A, substitute then transpose)
   or perm[j] (model B, transpose then substitute).
   Stage 1 (key-free, exact): every crib pair (PT[j], CT[perm[j]]) must cross halves. Done per perm with a
   2-colouring of the 24-edge letter graph: a split passes iff on every component it equals the colouring or
   its complement.  Stage 2 on survivors: periodic key L 1..26 (exact consistency per residue class), and
   running keys (every text, every offset) with key value = s*f(letter)+c mod 13, f = (A-Z index)/2 or
   (alphabet index)/2, s = +-1, c free (fixed by the first crib).
   Usage: porta170 CT perms.bin alpha.bin texts.txt [stride offset] > out ; one line per survivor + SUMMARY. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#define N 97
static const char *CRIB1="EASTNORTHEAST", *CRIB2="BERLINCLOCK";
static int cpos[24], cpt[24];
static int nord; static uint8_t (*ord)[26]; static int *ordsrc;           /* derived orderings */
static int nmask; static uint32_t *mask; static int *mstart, *mlist;      /* canonical masks -> orderings */
static int ntext; static char **tname; static uint8_t **ttext; static int *tlen;
static int cmp26(const void*a,const void*b){return memcmp(a,b,26);}
typedef struct {uint32_t m; int o;} MO;
static int cmpmo(const void*a,const void*b){const MO*x=a,*y=b; return x->m<y->m?-1:x->m>y->m?1:x->o-y->o;}
int main(int argc,char**argv){
  if(argc<5){fprintf(stderr,"usage\n");return 1;}
  const char*CT=argv[1]; int stride=argc>5?atoi(argv[5]):1, off=argc>6?atoi(argv[6]):0;
  if(strlen(CT)!=N){fprintf(stderr,"CT length\n");return 1;}
  for(int i=0;i<13;i++){cpos[i]=21+i;cpt[i]=CRIB1[i]-'A';}
  for(int i=0;i<11;i++){cpos[13+i]=63+i;cpt[13+i]=CRIB2[i]-'A';}
  FILE*f=fopen(argv[2],"rb"); fseek(f,0,2); long np=ftell(f)/194; fseek(f,0,0);
  int16_t*P=malloc(np*194); if(fread(P,194,np,f)!=(size_t)np)return 2; fclose(f);
  f=fopen(argv[3],"rb"); fseek(f,0,2); long na=ftell(f)/26; fseek(f,0,0);
  uint8_t*A=malloc(na*26); if(fread(A,26,na,f)!=(size_t)na)return 2; fclose(f);
  /* derived orderings, deduplicated; ordsrc = 2*alpha + split (first occurrence) */
  uint8_t (*tmp)[27]=malloc(na*2*27);
  for(long a=0;a<na;a++){ memcpy(tmp[2*a],A+26*a,26); tmp[2*a][26]=0;
    for(int i=0;i<13;i++){tmp[2*a+1][i]=A[26*a+2*i]; tmp[2*a+1][13+i]=A[26*a+2*i+1];} tmp[2*a+1][26]=1; }
  /* dedupe keeping first source: sort index by content */
  size_t nt=(size_t)na*2; long*idx=malloc(nt*sizeof(long)); for(size_t i=0;i<nt;i++)idx[i]=i;
  /* simple: qsort pairs (content, index) */
  typedef struct {uint8_t c[26]; int i;} CI; CI*ci=malloc(nt*sizeof(CI));
  for(size_t i=0;i<nt;i++){memcpy(ci[i].c,tmp[i],26); ci[i].i=(int)i;}
  int cmpci(const void*a,const void*b){int r=memcmp(((CI*)a)->c,((CI*)b)->c,26); return r?r:((CI*)a)->i-((CI*)b)->i;}
  qsort(ci,nt,sizeof(CI),cmpci);
  ord=malloc(nt*26); ordsrc=malloc(nt*sizeof(int)); nord=0;
  for(size_t i=0;i<nt;i++){ if(i&&!memcmp(ci[i].c,ci[i-1].c,26))continue; memcpy(ord[nord],ci[i].c,26); ordsrc[nord]=ci[i].i; nord++; }
  free(ci); free(tmp); free(idx);
  MO*mo=malloc(nord*sizeof(MO));
  for(int o=0;o<nord;o++){uint32_t m=0; for(int i=0;i<13;i++)m|=1u<<ord[o][i]; if(m&1u) m^=0x3FFFFFFu; mo[o].m=m; mo[o].o=o;}
  qsort(mo,nord,sizeof(MO),cmpmo);
  mask=malloc(nord*4); mstart=malloc((nord+1)*sizeof(int)); mlist=malloc(nord*sizeof(int)); nmask=0;
  for(int i=0;i<nord;i++){ if(!i||mo[i].m!=mo[i-1].m){mask[nmask]=mo[i].m; mstart[nmask]=i; nmask++;} mlist[i]=mo[i].o; }
  mstart[nmask]=nord; free(mo);
  /* texts */
  f=fopen(argv[4],"r"); static char line[4000000]; int cap=64; tname=malloc(cap*8); ttext=malloc(cap*8); tlen=malloc(cap*4); ntext=0;
  while(fgets(line,sizeof line,f)){ char*sp=strchr(line,' '); if(!sp)continue; *sp=0; char*t=sp+1; int L=0; uint8_t*b=malloc(strlen(t)+1);
    for(char*c=t;*c;c++) if(*c>='A'&&*c<='Z') b[L++]=*c-'A';
    tname[ntext]=strdup(line); ttext[ntext]=b; tlen[ntext]=L; ntext++; }
  fclose(f);
  fprintf(stderr,"perms %ld alphabets %ld orderings %d masks %d texts %d\n",np,na,nord,nmask,ntext);
  long long tested_pm=0, surv_pm=0, surv_ord=0, deadself=0, deadodd=0, per_hits[2][2][27]={{{0}}}, rk_hits=0, perm_done=0;
  long long per_hits_ord[27]={0};
  #pragma omp parallel for schedule(dynamic,64) reduction(+:tested_pm,surv_pm,surv_ord,deadself,deadodd,rk_hits,perm_done)
  for(long p=off;p<np;p+=stride){
    const int16_t*pm=P+97*p; int a[24],b[24],self=0; perm_done++;
    for(int i=0;i<24;i++){a[i]=cpt[i]; b[i]=CT[pm[cpos[i]]]-'A'; if(a[i]==b[i])self=1;}
    if(self){deadself++;continue;}
    /* 2-colouring */
    int col[26],comp[26]; for(int i=0;i<26;i++){col[i]=-1;comp[i]=-1;}
    int adjn[26]={0}, adj[26][48];
    for(int i=0;i<24;i++){adj[a[i]][adjn[a[i]]++]=b[i]; adj[b[i]][adjn[b[i]]++]=a[i];}
    int nc=0, odd=0; uint32_t S[26],C1[26];
    for(int s=0;s<26&&!odd;s++){ if(!adjn[s]||col[s]>=0)continue; int q[26],h=0,t=0; q[t++]=s; col[s]=0; comp[s]=nc; S[nc]=0;C1[nc]=0;
      while(h<t){int u=q[h++]; S[nc]|=1u<<u; if(col[u])C1[nc]|=1u<<u;
        for(int e=0;e<adjn[u];e++){int v=adj[u][e]; if(col[v]<0){col[v]=1-col[u];comp[v]=nc;q[t++]=v;} else if(col[v]==col[u]){odd=1;}}}
      nc++; }
    tested_pm+=nmask;
    if(odd){deadodd++;continue;}
    for(int mi=0;mi<nmask;mi++){ uint32_t m=mask[mi]; int ok=1;
      for(int c=0;c<nc;c++){uint32_t r=m&S[c]; if(r!=C1[c]&&r!=(S[c]^C1[c])){ok=0;break;}}
      if(!ok)continue; surv_pm++;
      for(int li=mstart[mi];li<mstart[mi+1];li++){ int o=mlist[li]; surv_ord++; int pos[26]; for(int i=0;i<26;i++)pos[ord[o][i]]=i;
        int kv[2][24];
        for(int i=0;i<24;i++){int ip=pos[a[i]],ic=pos[b[i]]; int h1=ip<13?ip:ic, h2=(ip<13?ic:ip)-13; kv[0][i]=((h2-h1)%13+13)%13; kv[1][i]=(h2+h1)%13;}
        char per[2][2][27]; int minL=99;
        for(int v=0;v<2;v++)for(int md=0;md<2;md++)for(int L=1;L<=26;L++){
          int r[26]; for(int x=0;x<L;x++)r[x]=-1; int ok2=1;
          for(int i=0;i<24;i++){int ix=md?pm[cpos[i]]:cpos[i]; int rr=ix%L; if(r[rr]<0)r[rr]=kv[v][i]; else if(r[rr]!=kv[v][i]){ok2=0;break;}}
          per[v][md][L]=ok2; if(ok2){
            #pragma omp atomic
            per_hits[v][md][L]++;
            if(L<minL)minL=L;}
        }
        /* running keys */
        int nrk=0; char rkdesc[4096]; rkdesc[0]=0;
        for(int t=0;t<(getenv("NORK")?0:ntext);t++){ const uint8_t*T=ttext[t]; int TL=tlen[t];
          for(int fm=0;fm<2;fm++){ int fv[26]; for(int x=0;x<26;x++) fv[x]=fm? pos[x]/2 : x/2;  /* fm1: index in derived ordering */
            for(int v=0;v<2;v++)for(int md=0;md<2;md++){ int ix[24]; int mx=0; for(int i=0;i<24;i++){ix[i]=md?pm[cpos[i]]:cpos[i]; if(ix[i]>mx)mx=ix[i];}
              /* need key letters at t0+idx for idx in 0..96 (whole message) -> t0 <= TL-97 */
              for(int s=0;s<2;s++) for(int t0=0;t0+97<=TL;t0++){
                int c0=((kv[v][0]-(s?-1:1)*fv[T[t0+ix[0]]])%13+13)%13; int i;
                for(i=1;i<24;i++){int need=(((s?-1:1)*fv[T[t0+ix[i]]]+c0)%13+13)%13; if(need!=kv[v][i])break;}
                if(i==24){nrk++; if(strlen(rkdesc)<3800) sprintf(rkdesc+strlen(rkdesc)," RK:%s:f%d:V%d:%c:s%c:c%d:t%d",tname[t],fm,v+1,md?'B':'A',s?'-':'+',c0,t0);}
              }}}
        }
        rk_hits+=nrk;
        #pragma omp critical
        { printf("SURV perm %ld ord %d src_alpha %d split %c minL %d ", p, o, ordsrc[o]/2, (ordsrc[o]&1)?'E':'F', minL);
          for(int i=0;i<26;i++)putchar('A'+ord[o][i]);
          printf(" per");
          for(int v=0;v<2;v++)for(int md=0;md<2;md++){printf(" V%d%c:",v+1,md?'B':'A'); for(int L=1;L<=26;L++) if(per[v][md][L])printf("%d,",L);}
          printf(" rk %d%s\n",nrk,rkdesc); }
      }
    }
  }
  printf("SUMMARY perms %lld masks %d orderings %d perm_mask_tested %lld dead_selfmap %lld dead_oddcycle %lld surv_perm_mask %lld surv_perm_ordering %lld rk_full %lld\n",
    perm_done,nmask,nord,tested_pm,deadself,deadodd,surv_pm,surv_ord,rk_hits);
  for(int v=0;v<2;v++)for(int md=0;md<2;md++){printf("PERIODIC V%d%c",v+1,md?'B':'A'); for(int L=1;L<=26;L++)printf(" %lld",per_hits[v][md][L]); printf("\n");}
  return 0;
}
