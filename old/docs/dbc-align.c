
#include <stdio.h>

#include "dbc.h"
#include "mmo/talent/util/spell.c"
#include "dbcutil.h"


int main(int argc, char** argv) {
  dbc* dbc1;
  dbc* dbc2;

  int i,j,k;
  int cl;
  char buf[4096];
  char buf2[4096];
  int m;
  int zm;
  int nmap;
  int mbest;
  int mwhich;
  unsigned int* map1;
  unsigned int* map2;
  char* filename1 = "11723/dbfilesclient/Spell.dbc";
  char* filename2 = "C:/Program Files/World of Warcraft Beta/Data/enUS/DBFilesClient/Spell.dbc";
  int pos = 0;
  int postrack = 0;
  char insstr[32];
  char lastline[256];
  int lastmwhich = -2;
  int noff = 0;

  if(argc > 1) filename1 = argv[1];
  if(argc > 2) filename2 = argv[2];

  dbc2 = loaddbc(filename1);
  dbc1 = loaddbc(filename2);

  printf("size: %d/%d vs %d/%d%s\n", dbc2->sn, dbc2->n, dbc1->sn, dbc1->n, (dbc2->sn == dbc1->sn) ? "" : " *************************");

  m = 0;
  for(i=0;i<dbc1->n;i++) {
    if(dbc1->d[i][0] > m) m = dbc1->d[i][0];
  }
  for(i=0;i<dbc2->n;i++) {
    if(dbc2->d[i][0] > m) m = dbc2->d[i][0];
  }

  map1 = (unsigned int*)calloc(m,sizeof(int));
  map2 = (unsigned int*)calloc(m,sizeof(int));

  for(i=0,j=0,k=0;i<dbc1->n && j<dbc2->n;) {
    if(dbc1->d[i][0] == dbc2->d[j][0]) {
      map1[k] = i++;
      map2[k] = j++;
      k++;
    } else if(dbc1->d[i][0] < dbc2->d[j][0]) {
      i++;
    } else {
      j++;
    }
  }
  nmap = k;

  for(i=1;i<dbc1->sn;i++) {
    mbest = 0;
    zm = 0;

    for(k=0;k<nmap;k++) {
      if(dbc1->d[map1[k]][i] == 0) zm++;
//      if(dbc1->d[map1[k]][i] == 0 && dbc2->d[map2[k]][i] == 0) zm++;
    }

    for(j=1;j<dbc2->sn;j++) {    // compare dbc1 column i vs dbc2 column j using rows in mapX[0..nmap]
      m = 0;
      for(k=0;k<nmap;k++) {
        if(dbc1->d[map1[k]][i] == dbc2->d[map2[k]][j]) m++;
      }
//printf("@ %d : %d %d   %d %d %d\n", j, m, mbest, pos, mwhich, lastmwhich);
      if(m > mbest || (m > 0 && m == mbest && j == lastmwhich+1) || (m > 0 && m == mbest && j+noff == i)) { //pos-mwhich)) {
        mbest = m;
        mwhich = j;
      }
    }
//printf("%d %d %d\n", pos, mwhich, lastmwhich);

    if(mbest > 0) {    // redo zm's for target if we have a target
      zm = 0;

      for(k=0;k<nmap;k++) {
        if(dbc1->d[map1[k]][i] == 0 && dbc2->d[map2[k]][mwhich] == 0) zm++;
      }
    }

#if 0
if(i == 12) {
//mwhich = i;
  for(k=0;k<nmap;k++) {
    printf("%08x %08x\n", dbc1->d[map1[k]][i], dbc2->d[map2[k]][mwhich]);
  }
}
#endif

    pos++;
    sprintf(insstr, "");
    if(pos == mwhich || zm == nmap || zm == mbest) {
    } else if(100.0*(mbest-zm)/(nmap-zm) > 25.0) {
      if(pos > mwhich) {
        sprintf(insstr, "+%d here", pos-mwhich);
        noff += pos-mwhich;
      } else {
        sprintf(insstr, "-%d here", mwhich-pos);
        noff -= mwhich-pos;
      }
      if(zm == nmap || zm == mbest) {} else { pos = mwhich; }
    }

    if(i > 1) printf("%s %s\n", lastline, insstr);

//    if(zm == nmap || zm == mbest) {
//printf("%d %d  %d %d\n", zm, nmap, zm, mbest);
    if(zm == nmap || zm == mbest) {
      sprintf(lastline, "match 1:%3d <=> %s  : %6.2f%%", i, (zm==nmap)?"<nul>":"<ins>", (zm==nmap)?100.0:0.0);
    } else {
      sprintf(lastline, "match 1:%3d <=> 2:%3d  : %6.2f%%", i, mwhich, 100.0*(mbest-zm)/(nmap-zm));
      lastmwhich = mwhich;
    }
  }

//printf("noff = %d\n", noff);
      noff = (dbc1->sn - dbc2->sn) - noff;
//printf("noff = %d\n", noff);
      if(noff > 0) {
        sprintf(insstr, "+%d here", noff);
      } else if(noff < 0) {
        sprintf(insstr, "%d here", noff);
      } else insstr[0] = 0;

  printf("%s %s\n", lastline, insstr);

}
