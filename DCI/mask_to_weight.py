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
import interface_contact_sites
import config

import numpy as np
import matplotlib.pyplot as plt
import time
import warnings
warnings.filterwarnings("ignore")
import pandas as pd
import torch as t
from intervaltree.interval import Interval


# In[2]:


def prep_utils(gt, pred):
    gt_CI_map = DCI_map.main_for_maps(gt, pred)['gt_CI_map']
    mask = per_chain_mask.main_mask(gt)
    length = DCI_map.chain_length(gt)
    fnat = Fnat.per_chain_Fnat(gt, pred)
    
    utils = {}
    utils['native CI map'] = gt_CI_map
    utils['mask'] = mask
    utils['pdb length'] = length[1]
    utils['chains length'] = length[0]
    utils['per-chain Fnat'] = fnat
    return utils


# In[7]:


def inter_chain_weight(mask):
    dim = mask.size()[0]
    intra_weight = float('%.2f' % (1 - config.model_config['inter_chain_weight']))
    inter_weight = config.model_config['inter_chain_weight']
    base = t.ones(dim, dim)
    i1 = t.mul(base, intra_weight).to(t.float64)
    i2 = t.mul(base, inter_weight).to(t.float64)
    med_weight = t.where(mask != 1., mask, i1)
    weight = t.where(med_weight != 0., med_weight, i2)
    return weight


# In[4]:


def contact_weight(gt_CI_map):
    dim = gt_CI_map.size()[0]
    contact_weight = config.model_config['contact_weight']
    noncontact_weight = config.model_config['noncontact_weight']
    base = t.ones(dim, dim)
    c1 = t.mul(base, contact_weight).to(t.float64)
    c2 = t.mul(base, noncontact_weight).to(t.float64)
    med_weight = t.where(gt_CI_map != 1., gt_CI_map, c1)
    weight = t.where(med_weight != 0., med_weight, c2)
    return weight


# In[16]:


def main_weight1(gt, pred):
    utils = prep_utils(gt, pred)
    weight_1 = inter_chain_weight(utils['mask']['inter chain'])
    weight_2 = contact_weight(utils['native CI map'])
    WEIGHT = t.mul(weight_1, weight_2)
    return WEIGHT


# In[3]:


def chain_pair_weight(gt, pred):
    c_p_weight = interface_contact_sites.main_sites(gt, pred)
    c_p_mask = prep_utils(gt, pred)['mask']['chains pair']
    dim = c_p_mask.size()[-1]
    chain_pair_weight = c_p_weight[0] * c_p_mask[:, :, 0]
    for pair in range(1, dim):
        mask = c_p_mask[:, :, pair]
        weight = c_p_weight[pair]
        chain_pair_weight = chain_pair_weight + mask * weight
    return chain_pair_weight


# In[4]:


def main_weight2(gt, pred):
    contact_weight = main_weight1(gt, pred)
    pair_interface_weight = chain_pair_weight(gt, pred)
    WEIGHT = t.add(contact_weight, pair_interface_weight)
    return WEIGHT

