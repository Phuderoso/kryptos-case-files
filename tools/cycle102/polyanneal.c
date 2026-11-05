/* Cycle 102: anneal the free part of the many-to-one map f for each crib-consistent cycle-101 configuration
   (periodic shift key fixed, transposition fixed, cribs hard). Reads CONS lines from stdin.
   Usage: ./polyanneal CT qg.bin restarts < survivors.txt */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define N 97
static const char*AL[2]={"ABCDEFGHIJKLMNOPQRSTUVWXYZ","KRYPTOSABCDEFGHIJLMNQUVWXZ"};
int ix[2][26],crib[N]; float*QG;
static unsigned rs=987654321u; static inline unsigned rnd(){rs^=rs<<13;rs^=rs>>17;rs^=rs<<5;return rs;}
static float score(const int*x){float s=0;for(int i=0;i+3<N;i++)s+=QG[((x[i]*26+x[i+1])*26+x[i+2])*26+x[i+3]];return s/(N-3);}
int main(int argc,char**argv){ const char*CT=argv[1]; int R=atoi(argv[3]);
 QG=malloc(4*456976); FILE*q=fopen(argv[2],"rb"); fread(QG,4,456976,q); fclose(q);
 const char*a="EASTNORTHEAST",*b="BERLINCLOCK"; for(int i=0;i<N;i++)crib[i]=-1;
 for(int i=0;i<13;i++)crib[21+i]=a[i]-65; for(int i=0;i<11;i++)crib[63+i]=b[i]-65;
 for(int t=0;t<2;t++)for(int k=0;k<26;k++)ix[t][AL[t][k]-65]=k;
 char line[512],file[64],key[32]; long n; int inv,t,kp,m,L;
 while(fgets(line,512,stdin)){ if(sscanf(line,"CONS %63s n=%ld inv=%d t=%d kp=%d m=%d L=%d key=%31s",file,&n,&inv,&t,&kp,&m,&L,key)!=8) continue;
  int s[N],S[N]; if(!strcmp(file,"identity")){for(int i=0;i<N;i++)s[i]=i;} else { FILE*fp=fopen(file,"rb"); short buf[N]; fseek(fp,n*194,0); fread(buf,2,N,fp); fclose(fp);
    for(int i=0;i<N;i++)S[i]=buf[i]; if(!inv)for(int i=0;i<N;i++)s[i]=S[i]; else for(int i=0;i<N;i++)s[S[i]]=i; }
  int x[N],add[N]; for(int i=0;i<N;i++){ int c=ix[t][CT[s[i]]-65]; int kk=key[(kp?s[i]:i)%L]-65; if(m==0){x[i]=(c-kk+26)%26;add[i]=0;} else {x[i]=c;add[i]=kk;} }
  int g[26],fixed[26],used[26]={0}; for(int k=0;k<26;k++){g[k]=-1;fixed[k]=0;} int ok=1;
  for(int i=0;i<N;i++){ used[x[i]]=1; if(crib[i]>=0){ int y=(ix[t][crib[i]]-add[i]+26)%26; if(g[x[i]]<0){g[x[i]]=y;fixed[x[i]]=1;} else if(g[x[i]]!=y) ok=0; } }
  if(!ok){printf("INCONSISTENT %s",line);continue;}
  int nfree=0; for(int k=0;k<26;k++) if(used[k]&&!fixed[k]) nfree++;
  float bs=-99; int bg[26]; int p[N];
  for(int r=0;r<R;r++){ int h[26]; for(int k=0;k<26;k++) h[k]=fixed[k]?g[k]:(int)(rnd()%26);
   #define DEC for(int i=0;i<N;i++) p[i]=AL[t][(h[x[i]]+add[i])%26]-65;
   DEC; float cur=score(p); int imp=1;
   while(imp){imp=0; for(int k=0;k<26;k++){ if(fixed[k]||!used[k])continue; int old=h[k],bv=old;
     for(int v=0;v<26;v++){ if(v==old)continue; h[k]=v; DEC; float sc=score(p); if(sc>cur+1e-6){cur=sc;bv=v;imp=1;} } h[k]=bv; DEC; } }
   if(cur>bs){bs=cur;memcpy(bg,h,sizeof h);} }
  memcpy(g,bg,sizeof g); { int*h=g; DEC; }
  printf("%.3f free=%d %s n=%ld inv=%d t=%d kp=%d m=%d L=%d key=%s ",bs,nfree,file,n,inv,t,kp,m,L,key); for(int i=0;i<N;i++)putchar(65+p[i]); putchar('\n'); }
}
