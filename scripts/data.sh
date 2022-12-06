#!/bin/bash

SAVE_PATH=.
mkdir ./data

gt_name=$(echo $1 | rev | cut -d'/' -f1 | rev | cut -d'.' -f1)
pred_name=$(echo $2 | rev | cut -d'/' -f1 | rev | cut -d'.' -f1)

if [[ $# -eq 2 ]]
then
	./scripts/order.sh $1 $2
elif [[ $3=="-model_chain_order" ]] && [[ $# -eq 4 ]]
then
	./scripts/order.sh $1 $2 $3 $4
fi
sed -n '/^ATOM.*CA.*/p' order_gt.pdb > data/gt_atom.pdb
l1=$(awk 'END{print NR}' data/gt_atom.pdb)
cat data/gt_atom.pdb | cut -c22 | uniq | awk '{if($0!=" ") print}' > data/chain_gt.txt
l=$(awk 'END{print NR}' data/chain_gt.txt)
for i in $(seq 1 $l)
do
	chain=$(sed -n ''$i'p' data/chain_gt.txt)
	sed -n '/^.\{21\}'$chain'.*/p' data/gt_atom.pdb > data/gt_$i.pdb
done
sed -n '/^ATOM.*CA.*/p' order_pred.pdb > data/pred_atom.pdb
cat data/pred_atom.pdb | cut -c22 | uniq | awk '{if($0!=" ") print}' > data/chain_pred.txt
ll=$(awk 'END{print NR}' data/chain_pred.txt)
for j in $(seq 1 $ll)
do
	chain=$(sed -n ''$j'p' data/chain_pred.txt)
	sed -n '/^.\{21\}'$chain'.*/p' data/pred_atom.pdb > data/pred_$j.pdb
	./scripts/atom_align.sh data/gt_$j.pdb data/pred_$j.pdb
	mv data/gt.pdb data/gt_chain_$j.pdb
	mv data/pred.pdb data/pred_chain_$j.pdb
done
cat data/gt_chain_*.pdb > $SAVE_PATH/gt.pdb
cat data/pred_chain_*.pdb > $SAVE_PATH/predict.pdb
l2=$(awk 'END{print NR}' $SAVE_PATH/gt.pdb)
penalty=$(awk 'BEGIN{printf "%.3f\n",('$l2'/'$l1')}')
echo $gt_name,$penalty > $SAVE_PATH/penalty.csv
rm -r ./data
