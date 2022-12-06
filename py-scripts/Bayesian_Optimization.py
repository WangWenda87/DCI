#!/usr/bin/env python
# coding: utf-8

# In[68]:


from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = "all" 
import os
os.environ['KMP_DUPLICATE_LIB_OK']='True'
import numpy as np
import pandas as pd
from sklearn.datasets import make_classification
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.metrics import make_scorer
from sklearn.metrics import matthews_corrcoef
from bayes_opt import BayesianOptimization

import ipynb_importer
from module import DCI
import config
import warnings
import torch as t
warnings.filterwarnings("ignore")


# In[69]:


all_data = pd.read_csv("/home/wenda/workspace/DCI/dataset/all_data.csv")
all_data = all_data[(all_data['penalty'] >= 0.75)]
all_data = all_data[['model','classification']]
all_data.reset_index(drop=True, inplace=True)


# In[70]:


train_set, test_set = train_test_split(all_data, test_size=0.2, random_state=31)


# In[71]:


def mcc_score(y_true, y_pred):
    return matthews_corrcoef(y_true, y_pred)


# In[72]:


_score = make_scorer(mcc_score, greater_is_better=True)


# In[73]:

def get_input(data, samp = 4000):
    class_dict = dict(data['classification'].value_counts('1'))
    l = []
    for i in class_dict.keys():
        sub_num = round(class_dict[i] * samp)
        sub_data = data[(data['classification'] == i)]
        l.append(sub_data.sample(n = sub_num))
    samp_data = l[0]
    for i in range(1, len(l)):
        samp_data = pd.concat([samp_data, l[i]])
    samp_data.reset_index(drop=True, inplace=True)
    return samp_data


# In[74]:


# temp = get_input(train_set)
# np.asarray(temp['model'])


# In[75]:


def DCI_mcc(w_inter_chain, w_contact, w_noncontact, w_inter_Fnat, w_value):
    _set = get_input(train_set)
    x_train = np.asarray(_set['model'])
    y_train = np.asarray(_set['classification'])
    y_train = [round(float(i)) for i in y_train]
    y_pred = DCI(w_inter_chain = w_inter_chain,
                w_contact = w_contact,
                w_noncontact = w_noncontact,
                w_inter_Fnat = w_inter_Fnat,
                w_value = w_value
                ).predict(x_train)
#    print(y_train)
#    print(y_pred)
    mcc = mcc_score(y_train, y_pred)
    return mcc

#print(DCI_mcc(0.9, 1.5, 0.8, 0.2, 0.7))
# In[76]:


dci_bo = BayesianOptimization(
        DCI_mcc,
        {'w_inter_chain' : (0.79, 0.96),
         'w_contact' : (1.19, 1.81),
         'w_noncontact' : (0.49, 0.91),
         'w_inter_Fnat' : (0.14, 0.36),
         'w_value' : (0.49, 0.86)}
    )
dci_bo.maximize()


# In[6]:


#dci_bo.max

