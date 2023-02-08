#!/bin/bash

gt_name=$(echo $1 | rev | cut -d'/' -f1 | rev | cut -d'.' -f1)
pred_name=$(echo $2 | rev | cut -d'/' -f1 | rev | cut -d'.' -f1)
if [[ $# -eq 2 ]]
then
        ./scripts/data.sh $1 $2
elif [[ $3=="-model_chain_order" ]] && [[ $# -eq 4 ]]
then
        ./scripts/data.sh $1 $2 $3 $4
fi
mv gt.pdb gt_${gt_name}.pdb
mv predict.pdb pred_${pred_name}.pdb
./DCI/main.py gt_${gt_name}.pdb pred_${pred_name}.pdb > result.txt
./DCI/create_chains_info.py gt_${gt_name}.pdb pred_${pred_name}.pdb > DCI_result.txt

penalty=$(awk -F',' '{print $2}' penalty.csv)
echo "penalty of structure-loss : $penalty" >> DCI_result.txt
sed -i 's/^.//' result.txt
sed -i 's/.$//' result.txt
DCI_score=$(cat result.txt | awk -F',' '{print $1}')
intra_Fnat=$(cat result.txt | awk -F', ' '{print $2}')
inter_Fnat=$(cat result.txt | awk -F', ' '{print $3}')
w_diff_value=$(cat result.txt | awk -F', ' '{print $4}')

echo "Intra Fnat : $intra_Fnat" >> DCI_result.txt
echo "Inter Fnat : $inter_Fnat" >> DCI_result.txt
echo "Difference Value : $w_diff_value" >> DCI_result.txt
echo "" >> DCI_result.txt
echo "DCI score(no penalty) : $DCI_score" >> DCI_result.txt
echo "DCI score(with penalty) : $(awk 'BEGIN{printf "%.3f\n",('$penalty'*'$DCI_score')}')" >> DCI_result.txt

rm result.txt
rm *pdb
rm penalty.csv
