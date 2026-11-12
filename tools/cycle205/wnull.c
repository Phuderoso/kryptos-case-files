/* Cycle 205, I-259 null: does "some letter forms a centred, inset-corner rectangle in rows of some width (3..48),
   with a 5th occurrence within one cell of the grid centre" (the K4 W pattern), optionally with EQ alternating-group
   balance and matching frequency shapes, occur in permutations of K4 (letter counts kept)?
   Definitions identical to wrect.c (reproduces glthr counts 26,734 / 775 / 650). 1-indexed positions. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
static const char *K4="OBKRUOXOGHULBSOLIFBBWFLRVQQPRNGKSSOTWTQSJQSSEKZZWATJKLUDIAWINFBNYPVTTMZFPKWGDKZXTJCDIGKUHUAUEKCAR";
static uint64_t s[2]; static inline uint64_t rotl(uint64_t x,int k){return (x<<k)|(x>>(64-k));}
static uint64_t nx(void){uint64_t s0=s[0],s1=s[1],r=s0+s1; s1^=s0; s[0]=rotl(s0,55)^s1^(s1<<14); s[1]=rotl(s1,36); return r;}
static int symrect(int a,int b,int d,int e,int c,int *inset_cen,int *any_sym){ /* returns via flags */
  *inset_cen=0; *any_sym=0; if(b-a!=e-d) return 0;
  for(int w=3;w<=48;w++){ int ra=(a-1)/w, rb=(b-1)/w, rd=(d-1)/w, re=(e-1)/w;
    if(ra!=rb||rd!=re||ra==rd) continue; if((a-1)%w!=(d-1)%w) continue; int R=97/w; if(a+e!=R*w+1) continue;
    *any_sym=1; if(c>0){ int n=R*w, ctr=(n+1)/2, cr=(ctr-1)/w, rc=(c-1)/w, dc=(c-1)%w-(ctr-1)%w; if(dc<0)dc=-dc;
      if(rc==cr&&dc<=1&&(a-1)/w==1&&(a-1)%w==1) *inset_cen=1; } }
  return *any_sym; }
static int shape_eq(const char *t,int *p){ /* 5 separators p[0..4] 1-idx; groups A=s1,s3,s5 B=s2,s4,s6; equal freq-shape */
  int ca[26]={0},cb[26]={0}; int bnd[7]={0,p[0],p[1],p[2],p[3],p[4],98};
  for(int g=0;g<6;g++) for(int q=bnd[g]+1;q<bnd[g+1];q++){ if(g%2==0) ca[t[q-1]-'A']++; else cb[t[q-1]-'A']++; }
  int ha[100]={0},hb[100]={0}; for(int i=0;i<26;i++){ha[ca[i]]++;hb[cb[i]]++;} for(int i=1;i<100;i++) if(ha[i]!=hb[i]) return 0; return 1; }
int main(int argc,char**argv){ long N=atol(argv[1]); s[0]=0x2052052052052052ULL^atol(argv[2]); s[1]=0x9E3779B97F4A7C15ULL;
  char t[98]; long c_sym=0,c_ic=0,c_eqsym=0,c_eqsym_shape=0,c_ic_eq=0,c_ic_eq_shape=0, c_icS5=0;
  for(int mode=0; mode<2; mode++){ long Nn = mode==0?1:N;
  for(long it=0;it<Nn;it++){ memcpy(t,K4,98); if(mode==1){ if(argc>3&&atoi(argv[3])==1){ for(int i=0;i<97;i++) t[i]='A'+nx()%26; } else for(int i=96;i>0;i--){ int j=nx()%(i+1); char x=t[i]; t[i]=t[j]; t[j]=x; } }
    int f_sym=0,f_ic=0,f_eqsym=0,f_eqsh=0,f_iceq=0,f_iceqsh=0;
    for(int L=0;L<26;L++){ int pos[97],n=0; for(int i=0;i<97;i++) if(t[i]=='A'+L) pos[n++]=i+1; if(n<4) continue;
      for(int i0=0;i0<n;i0++)for(int i1=i0+1;i1<n;i1++)for(int i2=i1+1;i2<n;i2++)for(int i3=i2+1;i3<n;i3++){
        int a=pos[i0],b=pos[i1],d=pos[i2],e=pos[i3]; int ic,as; symrect(a,b,d,e,0,&ic,&as); if(!as) continue; f_sym=1;
        for(int k=0;k<n;k++){ int c=pos[k]; if(c<=b||c>=d) continue; symrect(a,b,d,e,c,&ic,&as); int p5[5]={a,b,c,d,e};
          int eq=(n==5)&&(a+c+e-b-d==49); int sh= eq && shape_eq(t,p5);
          if(ic) f_ic=1; if(eq) f_eqsym=1; if(sh) f_eqsh=1; if(ic&&eq) f_iceq=1; if(ic&&sh) f_iceqsh=1; } } }
    if(mode==0){ printf("K4 itself: sym=%d inset+centre=%d eq&sym(5-letter)=%d eq&sym&shape=%d ic&eq=%d ic&eq&shape=%d\n",f_sym,f_ic,f_eqsym,f_eqsh,f_iceq,f_iceqsh); continue; }
    c_sym+=f_sym; c_ic+=f_ic; c_eqsym+=f_eqsym; c_eqsym_shape+=f_eqsh; c_ic_eq+=f_iceq; c_ic_eq_shape+=f_iceqsh; } }
  printf("N=%ld any-letter: sym %ld | inset+centre %ld | eq&sym(5-occ letter) %ld | eq&sym&shape %ld | inset+centre&eq %ld | inset+centre&eq&shape %ld\n",N,c_sym,c_ic,c_eqsym,c_eqsym_shape,c_ic_eq,c_ic_eq_shape); }
