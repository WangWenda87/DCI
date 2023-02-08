#!/usr/bin/env python
# coding: utf-8

# In[1]:


from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = "all" 
import os
os.environ['KMP_DUPLICATE_LIB_OK']='True'
import ipynb_importer
import DCI_map
import per_chain_mask

import numpy as np
import matplotlib.pyplot as plt
import time
import warnings
warnings.filterwarnings("ignore")
import pandas as pd
import torch as t


# In[3]:


def prep_CI(gt, pred):
    DCI = DCI_map.main_for_maps(gt, pred) # 2 optional argument for intra/inter contact cutoff
    
    common_CI = t.mul(DCI['gt_CI_map'], DCI['pred_CI_map'])
    gt_CI = DCI['gt_CI_map']
    return common_CI, gt_CI


# In[4]:


def fraction(m1, m2, mask_matrix):
    m1_mask = t.mul(m1, mask_matrix)
    m2_mask = t.mul(m2, mask_matrix)
    judge_m = m2_mask == 0
    if judge_m.all() == True:
        return "no contacts"
    else:
        frac = m1_mask.sum().item() / m2_mask.sum().item()
        return frac


# In[5]:


def cal_Fnat(gt, pred, is_inter_chain = True):
    l = DCI_map.chain_length(gt)[0]
    mask = DCI_map.inter_chains_mask(l) # intra = 1; inter = 0
    common_CI, gt_CI = prep_CI(gt, pred)
    
    if is_inter_chain == False:
        mask_matrix = mask
        intra_Fnat = fraction(common_CI, gt_CI, mask_matrix)
        return intra_Fnat
    else:
        mask_matrix = t.mul(mask, -1).add(1)
        inter_Fnat = fraction(common_CI, gt_CI, mask_matrix)
        return inter_Fnat


# In[6]:


def main_Fnat(gt, pred):
    intra_Fnat = cal_Fnat(gt, pred, is_inter_chain=False)
    inter_Fnat = cal_Fnat(gt, pred)
    return [intra_Fnat, inter_Fnat]


# In[19]:


# main_Fnat(test_gt, test_pred)


# In[7]:


def per_chain_Fnat(gt, pred):
    gt_mask = per_chain_mask.main_pair_mask(gt)
    pred_mask = per_chain_mask.main_pair_mask(pred)
    common_CI, gt_CI = prep_CI(gt, pred)
    
    if gt_mask.size() != pred_mask.size():
        return "Inconsistent dimensions"
    else:
        dim = gt_mask.size()[-1]
        
        per_chain_F = []
        for d in range(dim):
            mask = gt_mask[:, :, d]
            per_chain_F.append(fraction(common_CI, gt_CI, mask))
        return per_chain_F


# In[8]:


# test_gt = data_path + 'gt_atom.pdb'
# test_pred = data_path + 'predict_atom.pdb'
# temp = per_chain_Fnat(test_gt, test_pred)
# temp


# In[ ]:





# In[ ]:




