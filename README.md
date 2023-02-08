# DCI

#### Description
$\qquad$DCI-score, a new evaluation strategy for protein complex which only bases on distance map and CI (contact-interface) map, it can give a global assessment for complex structure, DCI-score ranges from 0 to 1, the value is higher when the two structures are more similar.

#### Software Architecture
$\qquad$The code is located in two folders, in which the shell scripts in the "scripts" folder is used for the pre-processing of the initial input files and the integration of the calculation results, python scripts in the "DCI" folder are used for the calculation of the DCI-score. In addition, two pairs of complex structures are stored in "examples" to test the operation of the program.

#### Installation

1.  clone & install  
$\qquad\qquad$git clone https://gitee.com/WendaWang/DCI-score.git  
to install the Python packages used in this program, please run:  
$\qquad\qquad$pip install -r py-scripts/requirements.txt  
2.  run  
The common format for running the program is:  
$\qquad\qquad$bash scripts/run.sh <gt> <model> -model_chain_order <model_chain_order>  
$\qquad$ where <gt> is the pdb file of ground truth (refer structure), <model> is the pdb file of predicted model, and <model_chain_order> is the correct order of predicted model chain based on ground truth.   
    For example complex 7AC9 in "examples" folder, the order of the three chains in ground truth is "H L I", which should correspond to "D B C" in predicted model, respectively, while the 7AC9_finetune.pdb file is in the order "B C D", so the parameter <model_chain_order> should be "DBC". You can test 7AC9 by running:  
$\qquad\qquad$bash scripts/run.sh examples/7AC9.pdb examples/7AC9_finetune.pdb -model_chain_order DBC  
$\qquad$if the chains' order of ground truth and predicted model is already correct (like 2VDU in "examples" folder), then the <-model_chian_order> parameter is not required, just run:  
$\qquad\qquad$bash scripts/run.sh <gt> <model>  
3.  result  
$\qquad$You will get a txt file with evaluation results. The Result file first shows some basic structure information such as the names of the two structures, the length of the ground truth (refer structure), the equivalent length of each chain. And then, it includes the three constituent subunits of DCI-score: inter-Fnat, intra-Fnat and difference value. Finally, in terms of the DCI-score results, we provide the results of the two calculation strategies in the result file. If you need to consider the loss of ground truth’s length due to the incomplete predicted structure, please choose the DCI(penalty) in the result file, otherwise, please choose the DCI(no penalty). The specific penalty value is shown at “penalty of structure-loss” in the result file.  
#### Contribution

1.  Fork the repository
2.  Create Feat_xxx branch
3.  Commit your code
4.  Create Pull Request

#### Gitee Feature

1.  You can use Readme\_XXX.md to support different languages, such as Readme\_en.md, Readme\_zh.md
2.  Gitee blog [blog.gitee.com](https://blog.gitee.com)
3.  Explore open source project [https://gitee.com/explore](https://gitee.com/explore)
4.  The most valuable open source project [GVP](https://gitee.com/gvp)
5.  The manual of Gitee [https://gitee.com/help](https://gitee.com/help)
6.  The most popular members  [https://gitee.com/gitee-stars/](https://gitee.com/gitee-stars/)
