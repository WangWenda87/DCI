#!/bin/bash

cp $1 order_gt.pdb
if [[ $# -eq 2 ]]
then
	cp $2 order_pred.pdb
elif [[ $3=="-model_chain_order" ]] && [[ $# -eq 4 ]]
then
        order=$(echo $4)
        len=$(echo $order | wc -L)
        for i in $(seq 1 $len)
        do
                chain=$(echo $order | cut -c$i)
                cat $2 | sed -n '/^ATOM.\{17\}'$chain'.*/p' > chain_${i}.pdb
        done
        cat chain_*.pdb > order_pred.pdb
        rm chain_*.pdb
fi
