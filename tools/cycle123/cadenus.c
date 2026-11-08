/* Cycle 123: Cadenus-style rotated-column transposition + periodic tableau key, exact crib test.
   Geometry (width w, ragged, 97 letters): text written row-wise; column c has L_c=ceil((97-c)/w) cells;
   each column rotated up by an ARBITRARY s_c in [0,L_c); columns placed in slot pi[c];
   read by rows (ROW = Cadenus, holes in the short last row skipped) or by columns (COL).
   dir 0: plaintext is written into the grid (ct[geom(i)] = enc(pt[i]))
   dir 1: ciphertext is written into the grid (pt position = geom(ct position)), i.e. sigma inverse.
   Substitution: tableau AZ or KA, Vig (k=c-p) or Beau (k=c+p) [variant == Vig consistency],
   key residue: model A = plaintext index mod p, model B = ciphertext index mod p. p = 1..PMAX.
   A survivor = all 24 crib letters consistent. Survivors are fully decrypted (unknown key residues
   filled by quadgram coordinate ascent) and scored (mean log10 quadgram).
   usage: cadenus CT orders.txt PMAX qg.bin label   (orders.txt lines: w pi[0..w-1] [name]) */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define N 97
static float *QG; static int ct[N]; static const char *KA="KRYPTOSABCDEFGHIJLMNQUVWXZ";
static int kai[26];
static const int CRP[24]={21,22,23,24,25,26,27,28,29,30,31,32,33,63,64,65,66,67,68,69,70,71,72,73};
static const char *CRS="EASTNORTHEASTBERLINCLOCK";
static int crl[24];
static int w,pi_[32],L[32],hs,slotoff[32],longbefore[32];
static int ncol_cribs[32],colcrib[32][24],corder[32];
static int postab[24][32]; /* pos of crib t (its paired other-side index) for rotation s */
static int dirg,model,alpha,beau,P;
static int key[32],keyset[32];
static int rot[32];
static long nsurv=0; static char label[256]; static char oname[64];
static long cnt_cfg[2][2][2][4][32];
static int place(int c,int rr,int mode){ int k=pi_[c];
  if(mode==1) return slotoff[k]+rr; /* COL */
  if(rr<hs) return rr*w+k; return w*hs+longbefore[k]; }
static int inv_place_mode; static int whereinv[N]; /* readout pos -> (c, rr) */
static int MODE;
static int lt(int x){return alpha?kai[x]:x;}
static float score(int*x){float s=0;for(int i=0;i+3<N;i++)s+=QG[((x[i]*26+x[i+1])*26+x[i+2])*26+x[i+3]];return s/(N-3);}
static void full_and_report(void){
  /* build sigma: pt index i -> ct index */
  int sig[N];
  if(dirg==0){ for(int i=0;i<N;i++){int c=i%w,r=i/w;int rr=(r-rot[c]+L[c])%L[c]; sig[i]=place(c,rr,MODE);} }
  else { for(int j=0;j<N;j++){int c=j%w,r=j/w;int rr=(r-rot[c]+L[c])%L[c]; sig[place(c,rr,MODE)]=j;} }
  int kk[32],ks[32]; memcpy(kk,key,sizeof kk); memcpy(ks,keyset,sizeof ks);
  int pt[N];
  for(int it=0;it<3;it++){
    for(int res=0;res<P;res++){ if(ks[res]==1) continue; float best=-1e9;int bv=0;
      for(int v=0;v<26;v++){ kk[res]=v;
        for(int i=0;i<N;i++){int rs=model==0? i%P : sig[i]%P; int cv=lt(ct[sig[i]]); int k=ks[rs]==1||rs==res||it>0?kk[rs]:0;
          int pv= beau? (k-cv+26)%26 : (cv-k+26)%26; pt[i]=alpha?(KA[pv]-'A'):pv;}
        float s=score(pt); if(s>best){best=s;bv=v;} }
      kk[res]=bv; if(ks[res]==0) ks[res]=2; }
  }
  for(int i=0;i<N;i++){int rs=model==0? i%P : sig[i]%P; int cv=lt(ct[sig[i]]); int k=kk[rs];
    int pv= beau? (k-cv+26)%26 : (cv-k+26)%26; pt[i]=alpha?(KA[pv]-'A'):pv;}
  float s=score(pt); int known=0; for(int r=0;r<P;r++) if(keyset[r]==1) known++;
  char buf[N+1]; for(int i=0;i<N;i++) buf[i]='A'+pt[i]; buf[N]=0;
  printf("SURV %s w=%d %s %s dir=%d model=%c %s %s p=%d known=%d/%d score=%.3f order=%s rot=",label,w,oname,MODE?"COL":"ROW",dirg,model?'B':'A',alpha?"KA":"AZ",beau?"Beau":"Vig",P,known,P,s,"");
  for(int c=0;c<w;c++) printf("%d%s",rot[c],c<w-1?",":"");
  printf(" key="); for(int r=0;r<P;r++) printf("%c",keyset[r]==1? (alpha?KA[kk[r]]:'A'+kk[r]) : ('a'+ (alpha?KA[kk[r]]-'A':kk[r])));
  printf(" pt=%s\n",buf);
}
static void bt(int d){
  if(d==w){ nsurv++; cnt_cfg[MODE][dirg][model][alpha*2+beau][P]++; if(nsurv<=200000) full_and_report(); return; }
  int c=corder[d];
  for(int s=0;s<L[c];s++){
    int undo[24],nu=0,ok=1;
    for(int q=0;q<ncol_cribs[c];q++){ int t=colcrib[c][q]; int pos=postab[t][s];
      /* dir0: t is pt crib at CRP[t], ct at pos. dir1: crib grid index is ct position... handled in postab */
      int ptpos=CRP[t], ctpos=pos;
      int res= model==0? ptpos%P : ctpos%P;
      int cv=lt(ct[ctpos]), pv=lt(crl[t]);
      int k= beau? (cv+pv)%26 : (cv-pv+26)%26;
      if(keyset[res]){ if(key[res]!=k){ok=0;break;} }
      else { keyset[res]=1; key[res]=k; undo[nu++]=res; }
    }
    if(ok){ rot[c]=s; bt(d+1); }
    for(int q=0;q<nu;q++) keyset[undo[q]]=0;
  }
}
int main(int argc,char**argv){
  if(argc<6){fprintf(stderr,"usage\n");return 1;}
  for(int i=0;i<N;i++) ct[i]=argv[1][i]-'A';
  for(int i=0;i<26;i++) kai[KA[i]-'A']=i;
  for(int t=0;t<24;t++) crl[t]=CRS[t]-'A';
  int PMAX=atoi(argv[3]); strncpy(label,argv[5],255);
  QG=malloc(sizeof(float)*456976); FILE*f=fopen(argv[4],"rb"); fread(QG,4,456976,f); fclose(f);
  FILE*of=fopen(argv[2],"r"); char line[512]; long norders=0;
  while(fgets(line,sizeof line,of)){
    char *p=line; int n; if(sscanf(p,"%d%n",&w,&n)!=1) continue; p+=n;
    for(int c=0;c<w;c++){sscanf(p,"%d%n",&pi_[c],&n);p+=n;}
    oname[0]=0; sscanf(p,"%63s",oname); norders++;
    hs=N/w; for(int c=0;c<w;c++) L[c]=(N-c+w-1)/w;
    int inv[32]; for(int c=0;c<w;c++) inv[pi_[c]]=c;
    int o=0,lb=0; for(int k=0;k<w;k++){ slotoff[k]=o; o+=L[inv[k]]; longbefore[k]=lb; if(L[inv[k]]>hs) lb++; }
    for(MODE=0;MODE<2;MODE++) for(dirg=0;dirg<2;dirg++){
      /* build per-column crib lists and postab */
      for(int c=0;c<w;c++) ncol_cribs[c]=0;
      for(int t=0;t<24;t++){ int i=CRP[t];
        if(dirg==0){ int c=i%w,r=i/w; colcrib[c][ncol_cribs[c]++]=t; for(int s=0;s<L[c];s++) postab[t][s]=place(c,(r-s+L[c])%L[c],MODE); }
        else { /* pt pos i is a readout position: find slot/row */
          int c=-1,rr=-1;
          for(int cc=0;cc<w&&c<0;cc++) for(int r2=0;r2<L[cc];r2++) if(place(cc,r2,MODE)==i){c=cc;rr=r2;break;}
          colcrib[c][ncol_cribs[c]++]=t; for(int s=0;s<L[c];s++){ int r=(rr+s)%L[c]; postab[t][s]=r*w+c; } }
      }
      /* column order: most cribs first */
      for(int c=0;c<w;c++) corder[c]=c;
      for(int a=0;a<w;a++) for(int b=a+1;b<w;b++) if(ncol_cribs[corder[b]]>ncol_cribs[corder[a]]){int x=corder[a];corder[a]=corder[b];corder[b]=x;}
      for(model=0;model<2;model++) for(alpha=0;alpha<2;alpha++) for(beau=0;beau<2;beau++) for(P=1;P<=PMAX;P++){
        memset(keyset,0,sizeof keyset); bt(0); }
    }
  }
  fprintf(stderr,"%s orders=%ld survivors=%ld\n",label,norders,nsurv);
  printf("TOTAL %s orders=%ld survivors=%ld\n",label,norders,nsurv);
  for(int m=0;m<2;m++)for(int d=0;d<2;d++)for(int mo=0;mo<2;mo++)for(int ab=0;ab<4;ab++)for(int p=1;p<=PMAX;p++) if(cnt_cfg[m][d][mo][ab][p])
    printf("COUNT %s %s dir=%d model=%c %s p=%d n=%ld\n",label,m?"COL":"ROW",d,mo?'B':'A',(const char*[]){"AZ-Vig","AZ-Beau","KA-Vig","KA-Beau"}[ab],p,cnt_cfg[m][d][mo][ab][p]);
  return 0;
}
