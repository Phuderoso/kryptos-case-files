// Cycle 30: M-94 / Bazeries cylinder (25 published M-94 disks, any disk order, any generatrix offset per 25-letter line)
// behind an optional transposition y[i]=X[p[i]]. Exact check against the 24 crib letters + disk injectivity (bipartite matching).
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
static int pos[26][25];      // pos[letter][disk] = index of letter on disk
static char alph[25][27];
static const char *PT_CRIB[2]={"EASTNORTHEAST","BERLINCLOCK"}; static int CRS[2]={21,63};
static int cp[24], cl[24]; static int ncr=0;
static uint32_t cm[25]; static int match_d[25];
static int seen;
static int aug(int c,int *own,uint32_t *vis){ uint32_t m=cm[c]&~*vis; while(m){int d=__builtin_ctz(m); m&=m-1; *vis|=1u<<d;
  if(own[d]<0||aug(own[d],own,vis)){own[d]=c;match_d[c]=d;return 1;}} return 0;}
static int matchable(void){ int own[25]; for(int i=0;i<25;i++)own[i]=-1;
  for(int c=0;c<25;c++){ if(cm[c]==0x1FFFFFFu) continue; uint32_t vis=0; if(!aug(c,own,&vis)) return 0;} return 1;}
int main(int argc,char**argv){
  FILE*f=fopen("m94.txt","r"); for(int d=0;d<25;d++){ if(fscanf(f,"%26s",alph[d])!=1) return 1; for(int k=0;k<26;k++) pos[alph[d][k]-'A'][d]=k;} fclose(f);
  char ct[200]; f=fopen(argv[1],"r"); if(fscanf(f,"%199s",ct)!=1) return 1; fclose(f); int n=strlen(ct);
  int np=1; int16_t *P=NULL; if(argc>2){ f=fopen(argv[2],"rb"); fseek(f,0,SEEK_END); long sz=ftell(f); fseek(f,0,SEEK_SET); np=sz/(2*n); P=malloc(sz); fread(P,2,np*n,f); fclose(f);} 
  for(int k=0;k<2;k++) for(int j=0;PT_CRIB[k][j];j++){ cp[ncr]=CRS[k]+j; cl[ncr]=PT_CRIB[k][j]-'A'; ncr++; }
  long hitperms=0, hitcfg=0, fixedg=0;
  for(int pi=0;pi<np;pi++){
    char y[200]; for(int i=0;i<n;i++) y[i]= P? ct[P[(long)pi*n+i]] : ct[i];
    // mask[line][g][col]
    static uint32_t M[4][26][25];
    for(int l=0;l<4;l++) for(int g=0;g<26;g++) for(int c=0;c<25;c++) M[l][g][c]=0x1FFFFFFu;
    for(int t=0;t<ncr;t++){ int i=cp[t], l=i/25, c=i%25; int p=cl[t], C=y[i]-'A';
      for(int g=1;g<26;g++){ uint32_t m=0; for(int d=0;d<25;d++) if(alph[d][(pos[p][d]+g)%26]-'A'==C) m|=1u<<d; M[l][g][c]&=m; } }
    int hit=0;
    for(int g0=1;g0<26;g0++){ int bad=0; for(int c=21;c<25;c++) if(!M[0][g0][c]) bad=1; if(bad) continue;
     for(int g1=1;g1<26;g1++){ bad=0; for(int c=0;c<9;c++) if(!M[1][g1][c]) bad=1; if(bad) continue;
      for(int g2=1;g2<26;g2++){ bad=0;
        for(int c=0;c<25;c++){ cm[c]=M[0][g0][c]&M[1][g1][c]&M[2][g2][c]; if(!cm[c]) {bad=1;break;} }
        if(bad) continue;
        if(matchable()){ hit=1; hitcfg++; if(g0==g1&&g1==g2) fixedg++;
          if(hitcfg<=20){ printf("HIT perm=%d g=(%d,%d,%d) disks:",pi,g0,g1,g2); for(int c=0;c<25;c++) if(cm[c]!=0x1FFFFFFu) printf(" c%d=%d",c,match_d[c]+1); printf("\n"); } }
      }}}
    if(hit) hitperms++;
  }
  printf("RESULT text=%s perms=%d hitperms=%ld hitconfigs=%ld fixed_offset_hits=%ld\n",argv[1],np,hitperms,hitcfg,fixedg);
}
