#!/usr/bin/env python
# coding: utf-8

# In[86]:


from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = "all" 
import os
os.environ['KMP_DUPLICATE_LIB_OK']='True'
import ipynb_importer
import DCI_map
import config

import numpy as np
import matplotlib.pyplot as plt
import time
import warnings
warnings.filterwarnings("ignore")
import pandas as pd
import torch as t
from interval import Interval


# In[87]:


def create_Interval(length):
    all_Interval = []
    st = 0
    for l in range(len(length)):
        ed = sum(length[:(l + 1)]) - 1
        all_Interval.append(Interval(st, ed))
        st = sum(length[:(l + 1)])
    return all_Interval


# In[88]:


def chain_label(iv, num):
    for i in range(len(iv)):
        if num in iv[i]:
            label = i + 1
    return label


# In[89]:


def create_pair_label(pdb):
    length = DCI_map.chain_length(pdb)[0]
    all_length = DCI_map.chain_length(pdb)[1]
    all_Interval = create_Interval(length)
    PL = np.empty(shape = (all_length, all_length, 2))
    
    for i in range(all_length):
        for j in range(all_length):
            i_label = chain_label(all_Interval, i)
            j_label = chain_label(all_Interval, j)
            pair_label = (i_label, j_label)
            PL[i, j, :] = pair_label
    PL = t.from_numpy(PL)
    return PL


# In[90]:


def per_chain_mask(pair_label, r_chain, l_chain):
    chains_num = t.max(pair_label).item()
    dim = pair_label.size()[0]
    Chain_Mask = np.zeros(shape = (dim, dim))
    if r_chain % 1 != 0 or l_chain % 1 != 0:
        return "Please input an integer"
    elif r_chain > chains_num or l_chain > chains_num:
        return "An error occurred while specifying the chain number"
    r0 = pair_label[:, :, 0] == r_chain
    l1 = pair_label[:, :, 1] == l_chain
    r1 = pair_label[:, :, 1] == r_chain
    l0 = pair_label[:, :, 0] == l_chain
    Chain_Mask[r0.mul(l1)] = 1
    Chain_Mask[r1.mul(l0)] = 1
    return Chain_Mask


# In[91]:


def inter_chain_mask(pdb):
    l = DCI_map.chain_length(pdb)[0]
    inter_chain_mask = DCI_map.inter_chains_mask(l)
    return inter_chain_mask


# In[92]:


def main_pair_mask(pdb):
    pair_label = create_pair_label(pdb)
    chains_num = int(t.max(pair_label).item())
    c = int(chains_num * (chains_num - 1) / 2)
    dim = pair_label.size()[0]
    ALL_MASK = np.empty(shape = (dim, dim, c))
    i = 0
    for c1 in range(1, chains_num):
        for c2 in range(c1 + 1, chains_num + 1):
            ALL_MASK[:, :, i] = per_chain_mask(pair_label, c1, c2)
            i = i + 1
    ALL_MASK = t.from_numpy(ALL_MASK)
    return ALL_MASK


# In[93]:


def main_mask(pdb):
    mask_inter = inter_chain_mask(pdb)
    mask_all = main_pair_mask(pdb)
    MASK = {}
    MASK['inter chain'] = mask_inter
    MASK['chains pair'] = mask_all
    return MASK


# inter chain : 1 means intra-chain residues and 0 means inter-chain residues.
# 
# chains pair : [length,length,$C^2_n$],eg:[0,1,0] means chain1-chain3 contact,[0,0,0] means intra-chain contact.
