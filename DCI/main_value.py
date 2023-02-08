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
import Fnat
import mask_to_weight
import config

import numpy as np
import matplotlib.pyplot as plt
import time
import warnings
warnings.filterwarnings("ignore")
import pandas as pd
import torch as t
from interval import Interval


# In[2]:


#method 1


# In[3]:


def mul_weight_map1(gt, pred):
    d_d_map = DCI_map.main_for_maps(gt, pred)['dist_difference_map']
    weight_matrix = mask_to_weight.main_weight1(gt, pred)
    mul_matrix = t.mul(d_d_map, weight_matrix)
    return mul_matrix


# In[4]:


#method 2


# In[5]:


def mul_weight_map2(gt, pred):
    d_d_map = DCI_map.main_for_maps(gt, pred)['dist_difference_map']
    weight_matrix = mask_to_weight.main_weight2(gt, pred)
    mul_matrix = t.mul(d_d_map, weight_matrix)
    return mul_matrix


# In[6]:


# me1 = mul_weight_map1(test_gt, test_pred)
# me2 = mul_weight_map2(test_gt, test_pred)
# plt.matshow(me1)
# plt.colorbar()
# plt.matshow(me2)
# plt.colorbar()
# plt.show()


# In[7]:


def normalize_to_value(matrix):
    v = 1 / (1 + matrix.mean()).item()
    value = '%.3f' % v
    return float(value)


# In[10]:


def weighted(gt, pred):
    fnat = Fnat.main_Fnat(gt, pred)
    intra_fnat = fnat[0]
    intra_fnat = float('%.3f' % intra_fnat)
    inter_fnat = fnat[1]
    inter_fnat = float('%.3f' % inter_fnat)
    value = normalize_to_value(mul_weight_map1(gt, pred)) #method 1
    #value = normalize_to_value(mul_weight_map2(gt, pred)) #method 2
    V = t.tensor((intra_fnat, inter_fnat, value))
    weights = t.tensor((1 - config.model_config['inter_Fnat_weight'] - config.model_config['value_weight'], config.model_config['inter_Fnat_weight'], config.model_config['value_weight']))
    fv = sum(t.mul(V, weights)).item()
    final_value = float('%.3f' % fv)
    return final_value, intra_fnat, inter_fnat, value


# In[ ]:




