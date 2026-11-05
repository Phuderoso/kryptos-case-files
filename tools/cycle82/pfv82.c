/* Cycle 82: Playfair (keyword 5x5 square; I=J or Q dropped; rest A-Z, rest KA-order, or column-wise) as the inner layer, periodic Vigenere/Beaufort/variant on a
   26-letter KA or A-Z tableau as the outer layer.  Exact crib test: the crib pairs (alignment a=0: pairs start at even
   positions; a=1: odd) give the Playfair output at 22 (a=0) or 20 (a=1) positions; the outer key must be consistent per
   residue mod p.  usage: pfv82 CT words.txt minchecks  -> prints consistent configs with checks>=minchecks, and per-p counts */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
static const char *KA="KRYPTOSABCDEFGHIJLMNQUVWXZ", *AZ="ABCDEFGHIJKLMNOPQRSTUVWXYZ";
static const char *PT="EASTNORTHEASTBERLINCLOCK";
int main(int argc,char**argv){
  const char*ct=argv[1]; FILE*f=fopen(argv[2],"r"); int minc=atoi(argv[3]);
  char pt[97]; memset(pt,0,97); for(int i=0;i<13;i++)pt[21+i]=PT[i]; for(int i=0;i<11;i++)pt[63+i]=PT[13+i];
  int ix[2][26]; for(int t=0;t<2;t++){const char*T=t?AZ:KA; for(int q=0;q<26;q++) ix[t][T[q]-'A']=q;}
  long cons[27]={0}, tests=0; char w[128];
  while(fscanf(f,"%127s",w)==1){
   for(int om=0;om<2;om++)for(int fill=0;fill<3;fill++){
    /* om 0: I=J merged (J dropped); om 1: Q dropped. fill 0: rest A-Z row-wise; 1: rest in KA order; 2: fill 0 written column-wise */
    char sq0[25], sq[25]; int pos[26]; int used[26]={0}; int n=0; int drop= om? 'Q'-'A' : 9; used[drop]=1;
    for(char*s=w;*s;s++){int c=*s-'A'; if(c<0||c>25)continue; if(!om&&c==9)c=8; if(!used[c]){used[c]=1; sq0[n++]='A'+c;}}
    const char*rest= fill==1? KA: AZ;
    for(int q=0;q<26;q++){int c=rest[q]-'A'; if(!used[c]){used[c]=1; sq0[n++]='A'+c;}}
    for(int i=0;i<25;i++) sq[i]= fill==2? sq0[(i%5)*5+i/5] : sq0[i];
    for(int i=0;i<25;i++) pos[sq[i]-'A']=i; if(!om) pos[9]=pos[8];
    for(int a=0;a<2;a++){
      int P[24], M[24], m=0;
      for(int i=0;i<96;i++){ if((i&1)!=a) continue; if(!pt[i]||!pt[i+1]) continue;
        int p1=pos[pt[i]-'A'], p2=pos[pt[i+1]-'A']; int r1=p1/5,c1=p1%5,r2=p2/5,c2=p2%5, o1,o2;
        if(p1==p2) goto skipw; /* doubled letter: cannot occur in these cribs */
        if(r1==r2){o1=r1*5+(c1+1)%5; o2=r2*5+(c2+1)%5;} else if(c1==c2){o1=((r1+1)%5)*5+c1; o2=((r2+1)%5)*5+c2;}
        else {o1=r1*5+c2; o2=r2*5+c1;}
        P[m]=i; M[m++]=sq[o1]-'A'; P[m]=i+1; M[m++]=sq[o2]-'A'; }
      for(int t=0;t<2;t++)for(int mode=0;mode<3;mode++){
        int K[24]; for(int j=0;j<m;j++){int c=ix[t][ct[P[j]]-'A'], q=ix[t][M[j]]; int k= mode==0? c-q: mode==1? c+q: q-c; K[j]=((k%26)+26)%26;}
        for(int p=1;p<=26;p++){ tests++; int kv[26]; for(int r=0;r<p;r++)kv[r]=-1; int ok=1,ch=0;
          for(int j=0;j<m&&ok;j++){int r=P[j]%p; if(kv[r]<0)kv[r]=K[j]; else if(kv[r]!=K[j])ok=0; else ch++;}
          if(!ok)continue; cons[p]++;
          if(ch>=minc) printf("HIT word=%s om=%d fill=%d a=%d tab=%s mode=%d p=%d checks=%d\n",w,om,fill,a,t?"AZ":"KA",mode,p,ch);} }
    }
    skipw:;
   }
  }
  printf("tests=%ld cons_by_p=",tests); for(int p=1;p<=26;p++)printf("%ld%s",cons[p],p<26?",":"\n"); return 0;}
