// Cycle 30b: other layer order: plaintext transposed first, then M-94. Crib at plaintext index i sits at carved index j with p[j]=i
// (and, via the family's inverses, the other convention too). Exact check: per-line offsets 1..25 (recursive, pruned) + disk matching.
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
static int pos[26][25]; static char alph[25][27];
static const char *PT_CRIB[2]={"EASTNORTHEAST","BERLINCLOCK"}; static int CRS[2]={21,63};
static int cp[24], cl[24]; static int ncr=0;
static uint32_t M[4][26][25]; static int lines[4], nl; static uint32_t cm[25]; static int match_d[25];
static long hitcfg=0; static int curpi; static int G[4];
static int aug(int c,int *own,uint32_t *vis){ uint32_t m=cm[c]&~*vis; while(m){int d=__builtin_ctz(m); m&=m-1; *vis|=1u<<d;
  if(own[d]<0||aug(own[d],own,vis)){own[d]=c;match_d[c]=d;return 1;}} return 0;}
static int matchable(void){ int own[25]; for(int i=0;i<25;i++)own[i]=-1;
  for(int c=0;c<25;c++){ if(cm[c]==0x1FFFFFFu) continue; uint32_t vis=0; if(!aug(c,own,&vis)) return 0;} return 1;}
static void rec(int k, uint32_t *acc){
  if(k==nl){ memcpy(cm,acc,sizeof cm); if(matchable()){ hitcfg++; if(hitcfg<=200){printf("HIT perm=%d g:",curpi); for(int t=0;t<nl;t++) printf(" L%d=%d",lines[t],G[t]); printf("\n");} } return; }
  int l=lines[k];
  for(int g=1;g<26;g++){ uint32_t a2[25]; int bad=0; for(int c=0;c<25;c++){ a2[c]=acc[c]&M[l][g][c]; if(!a2[c]){bad=1;break;} }
    if(bad) continue; G[k]=g; rec(k+1,a2); }
}
int main(int argc,char**argv){
  FILE*f=fopen("m94.txt","r"); for(int d=0;d<25;d++){ if(fscanf(f,"%26s",alph[d])!=1) return 1; for(int k=0;k<26;k++) pos[alph[d][k]-'A'][d]=k;} fclose(f);
  char ct[200]; f=fopen(argv[1],"r"); if(fscanf(f,"%199s",ct)!=1) return 1; fclose(f); int n=strlen(ct);
  f=fopen(argv[2],"rb"); fseek(f,0,SEEK_END); long sz=ftell(f); fseek(f,0,SEEK_SET); int np=sz/(2*n); int16_t*P=malloc(sz); fread(P,2,(long)np*n,f); fclose(f);
  for(int k=0;k<2;k++) for(int j=0;PT_CRIB[k][j];j++){ cp[ncr]=CRS[k]+j; cl[ncr]=PT_CRIB[k][j]-'A'; ncr++; }
  long hitperms=0;
  for(int pi=0;pi<np;pi++){ curpi=pi; int inv[200]; for(int j=0;j<n;j++) inv[P[(long)pi*n+j]]=j;
    for(int l=0;l<4;l++) for(int g=0;g<26;g++) for(int c=0;c<25;c++) M[l][g][c]=0x1FFFFFFu;
    int used[4]={0};
    for(int t=0;t<ncr;t++){ int j=inv[cp[t]], l=j/25, c=j%25, p=cl[t], C=ct[j]-'A'; used[l]=1;
      for(int g=1;g<26;g++){ uint32_t m=0; for(int d=0;d<25;d++) if(alph[d][(pos[p][d]+g)%26]-'A'==C) m|=1u<<d; M[l][g][c]&=m; } }
    nl=0; for(int l=0;l<4;l++) if(used[l]) lines[nl++]=l;
    long before=hitcfg; uint32_t acc[25]; for(int c=0;c<25;c++) acc[c]=0x1FFFFFFu; rec(0,acc); if(hitcfg>before) hitperms++;
  }
  printf("RESULT text=%s perms=%d hitperms=%ld hitconfigs=%ld\n",argv[1],np,hitperms,hitcfg);
}
