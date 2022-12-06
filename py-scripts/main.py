#!/usr/bin/env python
# coding: utf-8

# In[1]:


from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = "all" 
import time
import os
os.environ['KMP_DUPLICATE_LIB_OK']='True'
import ipynb_importer
import DCI_map
import per_chain_mask
import Fnat
import mask_to_weight
import main_value
import config
import warnings
import torch as t
warnings.filterwarnings("ignore")


# In[2]:


# data_path = ''
# test_gt = data_path + 'Target29_0_gt.pdb'
# test_pred = data_path + 'Target29_0_pred.pdb'


# In[8]:


def main_DCI(gt, pred):
    return main_value.weighted(gt, pred)


# In[6]:
import sys
gt = sys.argv[1]
pred = sys.argv[2]
#time_begin = time.time()

print(main_DCI(gt, pred))

#time_end = time.time()
#time = time_end - time_begin
#print('time:', time)

