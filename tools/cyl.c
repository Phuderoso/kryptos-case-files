// Cycle 31: generalized Bazeries/Jefferson cylinder. D disks (file, one alphabet per line, D<=32).
// Cylinder of n distinct disks (any choice + order), message starts at disk phase s, offset g (1..25) chosen per n-letter line.
// Exact test vs the 24 crib letters, then bipartite matching (distinct disks). Prints hits per (n,s).
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
static int D, pos[26][32]; static char alph[32][27];
static const char *PC[2]={"EASTNORTHEAST","BERLINCLOCK"}; static int CS[2]={21,63};
static int cp[24], cl[24], ncr=0, n;
static uint32_t M[26][26][32]; static int lines[26], nl; static uint32_t cm[32]; static int used[32];
static uint32_t ALL; static uint32_t TB[26][26][26];
static int aug(int c,int *own,uint32_t *vis){ uint32_t m=cm[c]&~*vis; while(m){int d=__builtin_ctz(m); m&=m-1; *vis|=1u<<d;
  if(own[d]<0||aug(own[d],own,vis)){own[d]=c;return 1;}} return 0;}
static int matchable(void){ int own[32]; for(int i=0;i<32;i++)own[i]=-1;
  for(int c=0;c<n;c++){ if(!used[c]) continue; uint32_t vis=0; if(!aug(c,own,&vis)) return 0;} return 1;}
static long hits; static int gsel[26];
static void dfs(int k){
  if(k==nl){ if(matchable()) hits++; return; }
  int l=lines[k]; uint32_t save[32]; memcpy(save,cm,sizeof(uint32_t)*n);
  for(int g=1;g<26;g++){ int bad=0;
    for(int c=0;c<n;c++){ cm[c]=save[c]&M[l][g][c]; if(!cm[c]){bad=1;break;} }
    if(!bad){ gsel[k]=g; dfs(k+1); }
  }
  memcpy(cm,save,sizeof(uint32_t)*n);
}
int main(int argc,char**argv){
  FILE*f=fopen(argv[1],"r"); D=0; while(D<32 && fscanf(f,"%26s",alph[D])==1){ for(int k=0;k<26;k++) pos[alph[D][k]-'A'][D]=k; D++;} fclose(f);
  ALL=(D==32)?0xFFFFFFFFu:((1u<<D)-1);
  char ct[200]; f=fopen(argv[2],"r"); if(fscanf(f,"%199s",ct)!=1) return 1; fclose(f);
  int nmin=atoi(argv[3]), nmax=atoi(argv[4]); int L=strlen(ct);
  int np=1; int16_t *P=NULL; if(argc>5){ FILE*g=fopen(argv[5],"rb"); fseek(g,0,SEEK_END); long sz=ftell(g); fseek(g,0,SEEK_SET); np=sz/(2*L); P=malloc(sz); if(fread(P,2,(long)np*L,g)){} fclose(g);} 
  for(int k=0;k<2;k++) for(int j=0;PC[k][j];j++){ cp[ncr]=CS[k]+j; cl[ncr]=PC[k][j]-'A'; ncr++; }
  long tot=0; int cells=0, hitcells=0;
  for(int p=0;p<26;p++) for(int g=1;g<26;g++) for(int d=0;d<D;d++) TB[p][alph[d][(pos[p][d]+g)%26]-'A'][g]|=1u<<d;
  setvbuf(stdout,NULL,_IOLBF,0);
  char orig[200]; strcpy(orig,ct); long hitperms=0;
  for(int pi=0;pi<np;pi++){ if(P) for(int i=0;i<L;i++) ct[i]=orig[P[(long)pi*L+i]]; int hc0=hitcells;
  for(n=nmin;n<=nmax && n<=D;n++) for(int s=0;s<n;s++){
    int lmax=(97+s)/n+1; for(int l=0;l<=lmax&&l<26;l++) for(int g=0;g<26;g++) for(int c=0;c<n;c++) M[l][g][c]=ALL;
    int has[26]={0};
    memset(used,0,sizeof used);
    for(int t=0;t<ncr;t++){ int i=cp[t]+s, l=i/n, c=i%n, p=cl[t], C=ct[cp[t]]-'A'; has[l]=1; used[c]=1;
      for(int g=1;g<26;g++) M[l][g][c]&=TB[p][C][g]; }
    nl=0; for(int l=0;l<26;l++) if(has[l]) lines[nl++]=l;
    for(int c=0;c<n;c++) cm[c]=ALL;
    hits=0; dfs(0); cells++; if(hits){ hitcells++; if(hitcells<=30) printf("HIT perm=%d n=%d s=%d configs=%ld\n",pi,n,s,hits);} tot+=hits;
  }
  if(hitcells>hc0) hitperms++; }
  printf("RESULT disks=%s text=%s perms=%d hitperms=%ld cells=%d hitcells=%d configs=%ld\n",argv[1],argv[2],np,hitperms,cells,hitcells,tot);
}
