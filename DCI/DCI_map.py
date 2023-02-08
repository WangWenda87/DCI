#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os

from Bio.PDB.PDBParser import PDBParser
from Bio.PDB import NeighborSearch
from Bio.PDB import Selection
from Bio.PDB import StructureAlignment
from Bio.Cluster import distancematrix
from Bio.Align import MultipleSeqAlignment

import matplotlib.pyplot as plt
os.environ['KMP_DUPLICATE_LIB_OK']='True'
import time
import numpy as np
from Bio.Cluster import kmedoids
import warnings
warnings.filterwarnings("ignore")
import pandas as pd
from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = "all" 

import torch as t


# In[2]:


def dist_map(pdb_path):
    parser = PDBParser()
    structure = parser.get_structure('X', pdb_path)
    atoms = structure.get_atoms()
    ATOM = []
    for atom in atoms:
        ATOM.append(atom.get_coord())
    dist_map = distancematrix(ATOM)
    dist_map = [np.sqrt(3 * i) for i in list(dist_map)]
    m = np.zeros(shape = (len(dist_map), len(dist_map)))
    for i in range(len(dist_map)):
        for j in range(len(dist_map)):
           # if i == j:
           #     m[i][j] = 0
            if i < j:
                m[i][j] = dist_map[j][i]
            elif i > j:
                m[i][j] = dist_map[i][j]
    m = t.from_numpy(m)
    return m


# In[3]:


def chain_length(pdb_path):
    parser = PDBParser()
    structure = parser.get_structure('X', pdb_path)
    model = structure[0]
    chain_len = []
    for chain in model:
        atoms = chain.get_atoms()
        i = 0
        for atom in atoms:
            i = i + 1
        chain_len.append(i)
    all_length = sum(chain_len)
    return chain_len, all_length


# In[4]:


def inter_chains_mask(length):
    dim = sum(length)
    refer = [0]
    for l in range(len(length)):
        re = sum(length[:(l + 1)])
        refer.append(re)
    chain_mask = np.zeros(shape = (dim, dim))
    for i in range(dim):
        for j in range(dim):
            for r in range(len(refer) - 1):
                sub_re = [refer[r], refer[r + 1]]
                if (i >= sub_re[0] and j >= sub_re[0] and i < sub_re[1] and j < sub_re[1]):
                    chain_mask[i, j] = 1
    chain_mask = t.from_numpy(chain_mask)
    return chain_mask


# In[5]:


def interface(d, cutoff):
    k = np.empty(len(d))
    k[d < cutoff] = 1
    k[d > cutoff] = 0
    return k


# In[7]:


def judge_contact(pdb_path, intra_cutoff, inter_cutoff):
    d_map = dist_map(pdb_path)
    c_length = chain_length(pdb_path)
    c_mask = inter_chains_mask(c_length[0])
    
    dim = d_map.size()[0]
    c = np.empty(shape = (dim, dim))
    #print(d_map[c_mask == 1])
    c[c_mask == 1] = interface(d_map[c_mask == 1], cutoff=intra_cutoff)
    c[(c_mask == 0)] = interface(d_map[(c_mask == 0)], cutoff=inter_cutoff)
    c = t.from_numpy(c)
    return c


# In[8]:


def get_two_maps(pdb_path, intra_cutoff, inter_cutoff):
    distance_map = dist_map(pdb_path)
    contact_map = judge_contact(pdb_path, intra_cutoff, inter_cutoff)
    return distance_map, contact_map
def get_difference_map(gt_result, pred_result):
    dist_diff_map = abs(gt_result[0] - pred_result[0])
    con_diff_map = abs(gt_result[1] - pred_result[1])
    return dist_diff_map, con_diff_map


# In[29]:


# def sequence_one_hot(seq: str) -> t.Tensor:
#     tokens_dict_regular_order = {'ALA': 0, 'CYS': 1, 'ASP': 2, 'GLU': 3, 'PHE': 4,
#                                      'GLY': 5, 'HIS': 6, 'ILE': 7, 'LYS': 8, 'LEU': 9,
#                                      'MET': 10, 'ASN': 11, 'PRO': 12, 'GLN': 13,
#                                      'ARG': 14, 'SER': 15, 'THR': 16, 'VAL': 17,
#                                      'TRP': 18, 'TYR': 19, 'X': 20}
#     one_hot = []
#     for aa in seq:
#         one_hot.append(tokens_dict_regular_order[aa])
#     one_hot = t.from_numpy(np.asarray(one_hot))
#     return one_hot


# In[30]:


# def res_matrix(pdb_path):
#     parser = PDBParser()
#     structure = parser.get_structure('X', pdb_path)
#     Res = structure.get_residues()
#     R = []
#     for res in Res:
#         R.append(res.get_resname())
#     R = sequence_one_hot(R)
#     temp = []
#     for i in range(len(R)):
#         for j in range(len(R)):
#              temp.append([R[i].item(), R[j].item()])
#     temp = np.asarray(temp)
#     r = t.tensor(temp).view(len(R), len(R), 2)
#     return r


# In[31]:


# def compare_gt_pred(gt, pred):
#     res_ma1 = res_matrix(gt)
#     res_ma2 = res_matrix(pred)
#     compare_matrix = res_ma1 - res_ma2 == 0
#     if t.all(compare_matrix) == True:
#         return "completely same"
#     else:
#         return "different"


# In[9]:


def main_for_maps(gt, pred, intra_cutoff = 6, inter_cutoff = 8):
    # compare if predict model is same as ground truth:
    #compare_res = compare_gt_pred(gt, pred)
    
    #get distance map and CI map for each structure:
    gt_maps = get_two_maps(gt, intra_cutoff, inter_cutoff)
    pred_maps = get_two_maps(pred, intra_cutoff, inter_cutoff)
    
    #get difference maps between gt and model:
    difference_maps = get_difference_map(gt_maps, pred_maps)
    
    maps_result = {}
   # maps_result['model_compare'] = compare_res
    maps_result['gt_dist_map'] = gt_maps[0]
    maps_result['gt_CI_map'] = gt_maps[1]
    maps_result['pred_dist_map'] = pred_maps[0]
    maps_result['pred_CI_map'] = pred_maps[1]
    maps_result['dist_difference_map'] = difference_maps[0]
    maps_result['CI_difference_map'] = difference_maps[1]
    return maps_result


# In[ ]:




