#!/bin/bash

perl scripts/fix_numbering.pl $2 $1 > data/fixed1.txt
sed -i '/.\{26\}X.*/d' $2.fixed
cat $2.fixed | sed -s '/^.\{15\}T.*/g' | awk NF > data/pred.pdb

perl scripts/fix_numbering.pl $1 $2 > data/fixed2.txt
sed -i '/.\{26\}X.*/d' $1.fixed
cat $1.fixed | sed -s '/^.\{16\}B.*/g' | awk NF > data/gt.pdb
rm $1.fixed
#rm data/fixed*txt
