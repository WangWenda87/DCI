#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab 


# In[19]:


#result_file = 'E:/MIALAB/daily work/new metric/result/filter_Target.csv'


# In[20]:


def get_file(file):
    data = pd.read_csv(file,header=None)
    data = pd.DataFrame(data)
    data.columns = ['model', 'CAPRI label', 'DockQ', 'DCI']
    return data


# In[39]:


def create_label(data, c1, c2, c3):
    capri_label = np.asarray(data['CAPRI label'])
    dq_value = np.asarray(data['DockQ'])
    dci_value = np.asarray(data['DCI'])
    dockq_label = []
    for l in range(len(dq_value)):
        if dq_value[l] > 0 and dq_value[l] <= 0.23:
            dockq_label.append(0)
        elif dq_value[l] > 0.23 and dq_value[l] <= 0.49:
            dockq_label.append(1)
        elif dq_value[l] > 0.49 and dq_value[l] <= 0.8:
            dockq_label.append(2)
        elif dq_value[l] > 0.8 and dq_value[l] <= 1:
            dockq_label.append(3)
    dockq_label = np.asarray(dockq_label,'int64')
    dci_label = []
    for i in range(len(dci_value)):
        if dci_value[i] > 0 and dci_value[i] <= c1:
            dci_label.append(0)
        elif dci_value[i] > c1 and dci_value[i] <= c2:
            dci_label.append(1)
        elif dci_value[i] > c2 and dci_value[i] <= c3:
            dci_label.append(2)
        elif dci_value[i] > c3 and dci_value[i] <= 1:
            dci_label.append(3)
    dci_label = np.asarray(dci_label, 'int64')
    return [capri_label, dockq_label, dci_label]


# In[45]:


def cal_acc_cor(label):
    dim = np.shape(label)[1]
    dq_true_num = 0
    dci_true_num = 0
    for j in range(dim):
        if label[1][j] == label[0][j]:
            dq_true_num = dq_true_num + 1
    for k in range(dim):
        if label[2][k] == label[0][k]:
            dci_true_num = dci_true_num + 1
    acc_dq = dq_true_num / dim
    acc_dci = dci_true_num / dim
    return [acc_dq, acc_dci]


# In[57]:


def optimize_cutoff(data):
    acc_list = []
    for c1 in np.linspace(0.25, 0.5, 26):
        for c2 in np.linspace(0.45, 0.7, 26):
            for c3 in np.linspace(0.6, 0.85, 26):
                if c1 < c2 and c2 < c3 :
                    acc_dci = cal_acc_cor(create_label(data, c1, c2, c3))[1]
                    acc_list.append([float('%.3f' % acc_dci), float('%.2f' % c1), float('%.2f' % c2), float('%.2f' % c3)])
    return acc_list


# In[59]:


def main(file):
    result = get_file(file)
    acc_list = optimize_cutoff(result)
    return acc_list


# In[ ]:


ACC_LIST = main(result_file)

