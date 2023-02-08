#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# visualize Distance map,Contact-Interface map and two difference maps


# In[1]:


import ipynb_importer
import config
import DCI_map
import per_chain_mask
import mask_to_weight
import os
import numpy as np

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
from PIL import Image


# In[6]:


#%matplotlib auto


# In[2]:


data_path = config.model_config['data_path']
test_gt = data_path + 'gt_atom.pdb'
test_pred = data_path + 'predict_atom.pdb'


# In[8]:


# Map = {'gt_dist_map', 'gt_CI_map', 'pred_dist_map', 'pred_CI_map', 'dist_difference_map', 'CI_difference_map'}

def visual(gt, pred, Map):
    DCI = DCI_map.main_for_maps(gt, pred) # 2 optional argument for intra/inter contact cutoff
    visual_data = DCI[Map]
    plt.matshow(visual_data)
    plt.colorbar()
    plt.show()    


# In[4]:


def visual_all_mask(pdb):
    length = DCI_map.chain_length(pdb)[0]
    MASK = DCI_map.inter_chains_mask(length)
    plt.matshow(MASK)
    plt.show()


# In[1]:


#eg:
#visual_all_mask(test_pred)


# In[3]:


def visual_per_chain_mask(pdb):
    all_pair_mask = per_chain_mask.main_pair_mask(pdb)
    for c in range(all_pair_mask.size()[-1]):
        v_data = all_pair_mask[:, :, c]
        plt.matshow(v_data)
        plt.show()


# In[3]:


def visual_weights(gt, pred):
    weight1 = mask_to_weight.main_weight1(gt, pred)
    weight2 = mask_to_weight.main_weight2(gt, pred)
    plt.matshow(weight1)
    plt.colorbar()
    plt.matshow(weight2)
    plt.colorbar()
    plt.show()

