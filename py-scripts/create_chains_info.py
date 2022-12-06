#!/usr/bin/env python
# coding: utf-8

# In[1]:


import ipynb_importer
import DCI_map
import per_chain_mask
import config
import numpy as np

from Bio.PDB.PDBParser import PDBParser
import matplotlib.pyplot as plt
import os
os.environ['KMP_DUPLICATE_LIB_OK']='True'
import time
import numpy as np

import warnings
warnings.filterwarnings("ignore")
import pandas as pd
from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = "all" 

import torch as t


# In[2]:


def get_chain_ID(pdb_path):
    parser = PDBParser()
    structure = parser.get_structure('X', pdb_path)
    model = structure[0]
    chain_ID = []
    for chain in model:
        c = str(chain)[-2] #<Chain id=L> --> L
        chain_ID.append(c)
    return chain_ID
#get_chain_ID(test_data)

def get_name(pdb_path):
    global_info = {}
    #pdb name :
    full_name = str(pdb_path)
    file_name = full_name.split("/")[-1]
    p_name = file_name.split(".")[0]
    pdb_name = p_name.split("_", 1)[1]
    return pdb_name

# In[10]:


def generate_info(gt, pred):
    global_pdb = gt
    global_info = {}
    #pdb name :
    global_info['gt name'] = get_name(gt)
    global_info['pred name'] = get_name(pred)
    #pdb length : 
    all_length = DCI_map.chain_length(gt)[1]
    global_info['pdb length'] = all_length
    
    #per chain length :
    per_chain_length = DCI_map.chain_length(gt)[0]
    global_info['per chain length'] = per_chain_length
    
    #chains number : 
    chains_num = len(per_chain_length)
    global_info['chains number'] = chains_num
    
    #chain_dict
    chain_ID = get_chain_ID(global_pdb)
    chain_dict = {}
    for i in range(chains_num):
        ID = chain_ID[i]
        num = i + 1
        chain_dict[ID] = num
    global_info['chain dict'] = chain_dict
    
    return global_info

# In[11]:
import sys
gt = sys.argv[1]
pred = sys.argv[2]
info_list = generate_info(gt, pred)

print('*' * 18 + ' DCI Result ' + '*' * 18)
print("ground truth :", info_list['gt name'] + '.pdb')
print("predicted model :", info_list['pred name'] + '.pdb')
print("all length :", info_list['pdb length'])
print("number of chains :", info_list['chains number'])
print("per chain length (equivalent) :")
i = 0
for k in info_list['chain dict'].keys():
    print(' '*20 + k + '(' + str(info_list['per chain length'][i]) + ' residues)')
    i = i + 1
# In[ ]:




