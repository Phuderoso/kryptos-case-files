/* Cycle 121: seriated Playfair as INNER or OUTER layer under periodic Vig/Beau/variant
   on KA/A–Z.
   Seriation S0 (column / classic ACA): write row-wise width w; Playfair-pair DOWN each
   column with phase ph (0: rows 0-1,2-3,..; 1: rows 1-2,3-4,..); unpaired = holdover
   (mid = PT letter projected onto the 25-letter alphabet).
   Seriation S1 (row-bounded): pair ACROSS each row of width w with phase ph; unpaired
   holdovers at the odd edge of a row. (Even w + ph=0 coincides with ordinary Playfair
   even-alignment on a complete text; N=97 leaves a short last row.)
   Layer order 0: PT → Playfair → mid → outer key → CT  (cycle-82 style)
   Layer order 1: PT → outer key → mid → Playfair → CT
   Exact crib test on fully-known digraphs + holdovers that land on cribs.
   usage: spf121 CT words.txt minchecks [wmin wmax pmax]
   Prints HIT lines (checks>=minchecks) and cons_by_p[order][p] histograms. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define N 97
static const char *KA="KRYPTOSABCDEFGHIJLMNQUVWXZ", *AZ="ABCDEFGHIJKLMNOPQRSTUVWXYZ";
static const char *PTCRIB="EASTNORTHEASTBERLINCLOCK";
static int crib_mask[N];
static void build_crib(char pt[N]){
  memset(pt,0,N); memset(crib_mask,0,sizeof crib_mask);
  for(int i=0;i<13;i++){pt[21+i]=PTCRIB[i]; crib_mask[21+i]=1;}
  for(int i=0;i<11;i++){pt[63+i]=PTCRIB[13+i]; crib_mask[63+i]=1;}
}
static int build_pairs_col(int w, int ph, int P1[], int P2[]){
  int m=0;
  for(int c=0;c<w;c++){
    int col[N], h=0;
    for(int r=0; c+r*w < N; r++) col[h++]=c+r*w;
    for(int i=ph;i+1<h;i+=2){ P1[m]=col[i]; P2[m]=col[i+1]; m++; }
  }
  return m;
}
static int build_pairs_row(int w, int ph, int P1[], int P2[]){
  int m=0;
  for(int start=0; start<N; start+=w){
    int row[N], h=0, end=start+w; if(end>N) end=N;
    for(int i=start;i<end;i++) row[h++]=i;
    for(int i=ph;i+1<h;i+=2){ P1[m]=row[i]; P2[m]=row[i+1]; m++; }
  }
  return m;
}
static void pf_enc_pair(int p1,int p2, int *o1,int *o2){
  int r1=p1/5,c1=p1%5,r2=p2/5,c2=p2%5;
  if(r1==r2){ *o1=r1*5+(c1+1)%5; *o2=r2*5+(c2+1)%5; }
  else if(c1==c2){ *o1=((r1+1)%5)*5+c1; *o2=((r2+1)%5)*5+c2; }
  else { *o1=r1*5+c2; *o2=r2*5+c1; }
}
static void pf_dec_pair(int p1,int p2, int *o1,int *o2){
  int r1=p1/5,c1=p1%5,r2=p2/5,c2=p2%5;
  if(r1==r2){ *o1=r1*5+(c1+4)%5; *o2=r2*5+(c2+4)%5; }
  else if(c1==c2){ *o1=((r1+4)%5)*5+c1; *o2=((r2+4)%5)*5+c2; }
  else { *o1=r1*5+c2; *o2=r2*5+c1; }
}
int main(int argc,char**argv){
  if(argc<4){fprintf(stderr,"usage: spf121 CT words.txt minchecks [wmin wmax pmax]\n"); return 1;}
  const char*ct=argv[1]; FILE*f=fopen(argv[2],"r"); int minc=atoi(argv[3]);
  int wmin=argc>4?atoi(argv[4]):2, wmax=argc>5?atoi(argv[5]):12, pmax=argc>6?atoi(argv[6]):16;
  if(!f|| (int)strlen(ct)!=N){fprintf(stderr,"bad args\n"); return 1;}
  char pt[N]; build_crib(pt);
  int ix[2][26]; for(int t=0;t<2;t++){const char*T=t?AZ:KA; for(int q=0;q<26;q++) ix[t][T[q]-'A']=q;}
  long cons[2][27]={{0},{0}}, tests=0; char wbuf[128];
  int P1[64], P2[64];
  while(fscanf(f,"%127s",wbuf)==1){
   for(int om=0;om<2;om++)for(int fill=0;fill<3;fill++){
    char sq0[25], sq[25]; int pos[26]; int used[26]={0}; int n=0; int drop= om? 'Q'-'A' : 9; used[drop]=1;
    for(char*s=wbuf;*s;s++){int c=*s-'A'; if(c<0||c>25)continue; if(!om&&c==9)c=8; if(!used[c]){used[c]=1; sq0[n++]='A'+c;}}
    const char*rest= fill==1? KA: AZ;
    for(int q=0;q<26;q++){int c=rest[q]-'A'; if(!used[c]){used[c]=1; sq0[n++]='A'+c;}}
    for(int i=0;i<25;i++) sq[i]= fill==2? sq0[(i%5)*5+i/5] : sq0[i];
    for(int i=0;i<26;i++) pos[i]=-1;
    for(int i=0;i<25;i++) pos[sq[i]-'A']=i; if(!om) pos[9]=pos[8]; /* J→I */
    for(int ser=0;ser<2;ser++)for(int ph=0;ph<2;ph++)for(int ww=wmin;ww<=wmax;ww++){
      int np = ser==0? build_pairs_col(ww,ph,P1,P2) : build_pairs_row(ww,ph,P1,P2);
      int paired[N]; memset(paired,0,sizeof paired);
      for(int k=0;k<np;k++){ paired[P1[k]]=1; paired[P2[k]]=1; }

      /* ---- order 0: PT→PF→mid→key→CT ---- */
      {
        int Pos[48], Mid[48], m=0; int bad=0;
        for(int k=0;k<np;k++){
          int a=P1[k], b=P2[k];
          if(!crib_mask[a]||!crib_mask[b]) continue;
          int ca=pt[a]-'A', cb=pt[b]-'A';
          if(pos[ca]<0||pos[cb]<0||pos[ca]==pos[cb]){bad=1; break;}
          int o1,o2; pf_enc_pair(pos[ca],pos[cb],&o1,&o2);
          Pos[m]=a; Mid[m++]=sq[o1]-'A'; Pos[m]=b; Mid[m++]=sq[o2]-'A';
        }
        if(!bad){
          for(int i=0;i<N;i++) if(crib_mask[i] && !paired[i]){
            int ca=pt[i]-'A'; if(pos[ca]<0){bad=1; break;}
            Pos[m]=i; Mid[m++]= (ca==9 && !om) ? 8 : ca;
          }
        }
        if(!bad && m>=8){
          for(int t=0;t<2;t++)for(int mode=0;mode<3;mode++){
            int K[48]; for(int j=0;j<m;j++){int c=ix[t][ct[Pos[j]]-'A'], q=ix[t][Mid[j]]; int k= mode==0? c-q: mode==1? c+q: q-c; K[j]=((k%26)+26)%26;}
            for(int p=1;p<=pmax;p++){ tests++; int kv[26]; for(int r=0;r<p;r++)kv[r]=-1; int ok=1,ch=0;
              for(int j=0;j<m&&ok;j++){int r=Pos[j]%p; if(kv[r]<0)kv[r]=K[j]; else if(kv[r]!=K[j])ok=0; else ch++;}
              if(!ok)continue; cons[0][p]++;
              if(ch>=minc) printf("HIT ord=0 word=%s om=%d fill=%d ser=%d ph=%d w=%d tab=%s mode=%d p=%d checks=%d known=%d\n",
                wbuf,om,fill,ser,ph,ww,t?"AZ":"KA",mode,p,ch,m);}
          }
        }
      }

      /* ---- order 1: PT→key→mid→PF→CT : PF-decrypt CT digraphs → mid; key links mid↔PT ---- */
      {
        int Pos[48], Mid[48], PtL[48], m=0; int bad=0;
        for(int k=0;k<np;k++){
          int a=P1[k], b=P2[k];
          if(!crib_mask[a]||!crib_mask[b]) continue;
          int ca=ct[a]-'A', cb=ct[b]-'A';
          /* CT letters must live in the square (I=J merge maps J; Q-drop: Q cannot appear) */
          if(pos[ca]<0||pos[cb]<0){bad=1; break;}
          if(pos[ca]==pos[cb]){bad=1; break;}
          int o1,o2; pf_dec_pair(pos[ca],pos[cb],&o1,&o2);
          Pos[m]=a; Mid[m]=sq[o1]-'A'; PtL[m]=pt[a]-'A'; if(PtL[m]==9&&!om) PtL[m]=8; m++;
          Pos[m]=b; Mid[m]=sq[o2]-'A'; PtL[m]=pt[b]-'A'; if(PtL[m]==9&&!om) PtL[m]=8; m++;
        }
        if(!bad){
          for(int i=0;i<N;i++) if(crib_mask[i] && !paired[i]){
            /* holdover: mid = CT letter (PF skipped); still need it in alphabet */
            int ca=ct[i]-'A';
            Pos[m]=i; Mid[m]=ca; PtL[m]=pt[i]-'A'; if(PtL[m]==9&&!om) PtL[m]=8; m++;
          }
        }
        if(!bad && m>=8){
          for(int t=0;t<2;t++)for(int mode=0;mode<3;mode++){
            /* mid = Vig(PT, key)  =>  key from mid and PT (not CT) */
            int K[48]; for(int j=0;j<m;j++){int c=ix[t][Mid[j]], q=ix[t][PtL[j]]; int k= mode==0? c-q: mode==1? c+q: q-c; K[j]=((k%26)+26)%26;}
            for(int p=1;p<=pmax;p++){ tests++; int kv[26]; for(int r=0;r<p;r++)kv[r]=-1; int ok=1,ch=0;
              for(int j=0;j<m&&ok;j++){int r=Pos[j]%p; if(kv[r]<0)kv[r]=K[j]; else if(kv[r]!=K[j])ok=0; else ch++;}
              if(!ok)continue; cons[1][p]++;
              if(ch>=minc) printf("HIT ord=1 word=%s om=%d fill=%d ser=%d ph=%d w=%d tab=%s mode=%d p=%d checks=%d known=%d\n",
                wbuf,om,fill,ser,ph,ww,t?"AZ":"KA",mode,p,ch,m);}
          }
        }
      }
    }
   }
  }
  printf("tests=%ld\n",tests);
  printf("cons_ord0_by_p="); for(int p=1;p<=pmax;p++)printf("%ld%s",cons[0][p],p<pmax?",":"\n");
  printf("cons_ord1_by_p="); for(int p=1;p<=pmax;p++)printf("%ld%s",cons[1][p],p<pmax?",":"\n");
  return 0;
}
