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


def prep_utils(gt, pred):
    gt_CI_map = DCI_map.main_for_maps(gt, pred)['gt_CI_map']
    mask = per_chain_mask.main_mask(gt)
    length = DCI_map.chain_length(gt)
    
    utils = {}
    utils['native CI map'] = gt_CI_map
    utils['mask'] = mask
    utils['pdb length'] = length[1]
    utils['chains length'] = length[0]
    return utils


# In[3]:


def cal_interface_counts(utils):
    mask = utils['mask']['chains pair']
    CI_map = utils['native CI map']
    dim = mask.size()[-1]
    interface_counts = []
    for pair in range(dim):
        sub_mask = mask[:, :, pair]
        sub_interface = t.mul(sub_mask, CI_map)
        interface_num = int(sub_interface.sum().item() / 2)
        interface_counts.append(interface_num)
    interface_counts = t.tensor(interface_counts)
    return interface_counts


# In[4]:


def cal_contact_counts(utils):
    mask = utils['mask']['chains pair']
    CI_map = utils['native CI map']
    dim = mask.size()[-1]
    contact_counts = []
    for con in range(dim):
        sub_mask = mask[:, :, con]
        d = sub_mask.size()[0]
        for i in range(d):
            for j in range(i+1, d):
                sub_mask[i, j] = 0
        sub_contact = t.mul(sub_mask, CI_map)
        chain_1 = t.sum(sub_contact, 0)
        chain_2 = t.sum(sub_contact, 1)
        contacts = len(t.nonzero(chain_1)) + len(t.nonzero(chain_2))
        contact_counts.append(contacts)
    contact_counts = t.tensor(contact_counts)
    return contact_counts


# In[5]:


def cal_all_sites(utils):
    chains_length = utils['chains length']
    l = len(chains_length)
    all_sites = []
    if l == 2:
        all_sites.append(int(chains_length[0] * chains_length[1]))
        all_sites = t.tensor(all_sites)
    else:
        c = int(l * (l - 1) / 2)
        for i in range(c - 1):
            for j in range(i + 1, c):
                all_sites.append(int(chains_length[i] * chains_length[j]))
        all_sites = t.tensor(all_sites)
    return all_sites


# In[6]:


def main_interface_sites(gt, pred):
    utils = prep_utils(gt, pred)
    counts = cal_interface_counts(utils)
    #print(counts)
    all_sites = cal_all_sites(utils)
    per_chain_pair_weight = t.div(counts * counts, all_sites)
    return per_chain_pair_weight


# In[7]:


def main_contact_sites(gt, pred):
    utils = prep_utils(gt, pred)
    counts = cal_contact_counts(utils)
    #print(counts)
    all_sites = cal_all_sites(utils)
    per_chain_contact_weight = t.div(counts * counts, all_sites)
    return per_chain_contact_weight


# In[8]:


def main_sites(gt, pred):
    interface_sites = main_interface_sites(gt, pred)
    contact_sites = main_contact_sites(gt, pred)
    main_sites = t.add(interface_sites, contact_sites)
    return main_sites


# In[14]:


# data_path = config.model_config['data_path']
# test_gt = data_path + 'gt_atom.pdb'
# test_pred = data_path + 'predict_atom.pdb'


# In[15]:


#main_contact_sites(test_gt, test_pred)


# In[16]:


#main_sites(test_gt, test_pred)


# In[ ]:




