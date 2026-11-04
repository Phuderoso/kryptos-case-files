/* Cycle 54: split (two-segment) periodic key. Segment 1 [0,b) carries EASTNORTHEAST (21-33), segment 2 [b,97)
   carries BERLINCLOCK (63-73), b in 34..63. Each segment has its own periodic key; p1<=13, p2<=11 make the key fully
   determined by its crib (13/11 consecutive letters cover every residue), so every config gives one exact plaintext.
   Alphabets: 86,731 (AZ, KA, themed keyword alphabets from data/alpha.bin), Quagmire-III style (same alphabet both
   sides of the tableau). Vigenere c=p+k, Beaufort c=k-p (variant = Vigenere with -k, same plaintext). Segments may use
   different variants; with AZ/KA (alphabet ids 0,1) also different alphabets.
   usage: splitkey CT alpha.bin qg.bin [maxalpha]   -> prints count of consistent configs, best scores, top 15 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define N 97
static float *QG; static unsigned char (*AL)[26]; static int NA;
typedef struct{float s; int a1,v1,p1,a2,v2,p2,b; char pt[N+1];} R;
static R top[15]; static int ntop=0;
static void push(R*r){ if(ntop<15){top[ntop++]=*r;} else { int w=0; for(int i=1;i<15;i++) if(top[i].s<top[w].s) w=i; if(r->s>top[w].s) top[w]=*r; } }
int main(int c,char**v){
  const char*ct=v[1]; if(strlen(ct)!=N){fprintf(stderr,"len\n");return 1;}
  FILE*f=fopen(v[2],"rb"); fseek(f,0,2); NA=ftell(f)/26; rewind(f); AL=malloc(NA*26); if(fread(AL,26,NA,f)!=(size_t)NA)return 1; fclose(f);
  if(c>4) NA=atoi(v[4]);
  QG=malloc(4*456976); f=fopen(v[3],"rb"); if(fread(QG,4,456976,f)!=456976)return 1; fclose(f);
  const char*c1="EASTNORTHEAST",*c2="BERLINCLOCK";
  long ncons=0, nscored=0; float best=-1e9;
  /* per alphabet: build decryptions */
  static unsigned char D1[2][14][N], D2[2][12][N]; static int ok1[2][14], ok2[2][12];
  static unsigned char KD1[2][2][14][N], KD2[2][2][12][N]; static int KO1[2][2][14], KO2[2][2][12]; /* AZ/KA cache */
  for(int a=0;a<NA;a++){
    int idx[26]; for(int i=0;i<26;i++) idx[AL[a][i]]=i;
    for(int var=0;var<2;var++){
      for(int p=1;p<=13;p++){ int key[13]; for(int r=0;r<p;r++)key[r]=-1; int ok=1;
        for(int i=0;i<13 && ok;i++){ int pos=21+i; int ci=idx[ct[pos]-'A'], pi=idx[c1[i]-'A']; int k= var==0? (ci-pi+26)%26 : (ci+pi)%26;
          int r=pos%p; if(key[r]<0)key[r]=k; else if(key[r]!=k) ok=0; }
        ok1[var][p]=ok; if(ok){ for(int pos=0;pos<N;pos++){ int ci=idx[ct[pos]-'A'], k=key[pos%p]; int pi= var==0? (ci-k+26)%26 : (k-ci+26)%26; D1[var][p][pos]=AL[a][pi]; } } }
      for(int p=1;p<=11;p++){ int key[11]; for(int r=0;r<p;r++)key[r]=-1; int ok=1;
        for(int i=0;i<11 && ok;i++){ int pos=63+i; int ci=idx[ct[pos]-'A'], pi=idx[c2[i]-'A']; int k= var==0? (ci-pi+26)%26 : (ci+pi)%26;
          int r=pos%p; if(key[r]<0)key[r]=k; else if(key[r]!=k) ok=0; }
        ok2[var][p]=ok; if(ok){ for(int pos=0;pos<N;pos++){ int ci=idx[ct[pos]-'A'], k=key[pos%p]; int pi= var==0? (ci-k+26)%26 : (k-ci+26)%26; D2[var][p][pos]=AL[a][pi]; } } }
    }
    if(a<2){ memcpy(KD1[a],D1,sizeof D1); memcpy(KD2[a],D2,sizeof D2); memcpy(KO1[a],ok1,sizeof ok1); memcpy(KO2[a],ok2,sizeof ok2); }
    int amax = (a==1)?2:1; /* at a==1 also combine AZ x KA cross pairs */
    for(int pass=0; pass<amax; pass++){
      for(int x1=0;x1<(pass?2:1);x1++) for(int x2=0;x2<(pass?2:1);x2++){
        if(pass && x1==x2) continue;
        int a1= pass? x1:a, a2= pass? x2:a;
        for(int v1=0;v1<2;v1++)for(int p1=1;p1<=13;p1++){ int o1= pass? KO1[x1][v1][p1]:ok1[v1][p1]; if(!o1)continue;
          unsigned char*d1= pass? KD1[x1][v1][p1]:D1[v1][p1];
          for(int v2=0;v2<2;v2++)for(int p2=1;p2<=11;p2++){ int o2= pass? KO2[x2][v2][p2]:ok2[v2][p2]; if(!o2)continue;
            unsigned char*d2= pass? KD2[x2][v2][p2]:D2[v2][p2]; if(getenv("STRICT") && (p1==13 || p2==11)) continue; ncons++;
            /* skip same key in both segments (that is the plain periodic case, already excluded) */
            for(int b=34;b<=63;b++){ unsigned char x[N]; memcpy(x,d1,b); memcpy(x+b,d2+b,N-b);
              float s=0; for(int i=0;i+3<N;i++) s+=QG[((x[i]*26+x[i+1])*26+x[i+2])*26+x[i+3]]; s/=(N-3); nscored++;
              if(s>best)best=s;
              if(ntop<15 || s>top[0].s-1){ R r; r.s=s; r.a1=a1;r.v1=v1;r.p1=p1;r.a2=a2;r.v2=v2;r.p2=p2;r.b=b; for(int i=0;i<N;i++)r.pt[i]='A'+x[i]; r.pt[N]=0; push(&r);} }
          } }
      }
    }
  }
  /* sort top */
  for(int i=0;i<ntop;i++)for(int j=i+1;j<ntop;j++) if(top[j].s>top[i].s){R t=top[i];top[i]=top[j];top[j]=t;}
  printf("pairs_consistent=%ld scored=%ld best=%.4f\n",ncons,nscored,best);
  for(int i=0;i<ntop;i++) printf("%.4f a1=%d v1=%d p1=%d a2=%d v2=%d p2=%d b=%d %s\n",top[i].s,top[i].a1,top[i].v1,top[i].p1,top[i].a2,top[i].v2,top[i].p2,top[i].b,top[i].pt);
  return 0; }
