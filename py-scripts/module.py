#!/usr/bin/env python
# coding: utf-8

# In[1]:


from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = "all" 
import os
os.environ['KMP_DUPLICATE_LIB_OK']='True'
import numpy as np
import pandas as pd
from sklearn.metrics import make_scorer
import ipynb_importer
import main
import config
import warnings
import torch as t
warnings.filterwarnings("ignore")


# In[2]:


class DCI_score:
    gt_path = '/extendplus/wander_W/database/gt/'
    pred_path = '/extendplus/wander_W/database/pred/'
    def __init__(self, w_inter_chain, w_contact, w_noncontact, w_inter_Fnat, w_value):
        self.inter_chain = w_inter_chain
        self.contact = w_contact
        self.noncontact = w_noncontact
        self.inter_Fnat = w_inter_Fnat
        self.value = w_value
        
        self.cal = main.main_DCI
        
    def single_dci(self, pdb):
        config.model_config['inter_chain_weight'] = self.inter_chain
        config.model_config['contact_weight'], config.model_config['noncontact_weight'] = self.contact, self.noncontact
        config.model_config['inter_Fnat_weight'] = self.inter_Fnat
        config.model_config['value_weight'] = self.value
        gt = self.gt_path + pdb + '.pdb'
        pred = self.pred_path + pdb + '.pdb'
        return self.cal(gt, pred)

# In[11]:


#改成 x_train y_train的输入
class DCI(DCI_score):
    def __init__(self, w_inter_chain, w_contact, w_noncontact, w_inter_Fnat, w_value):
        super(DCI, self).__init__(w_inter_chain, w_contact, w_noncontact, w_inter_Fnat, w_value)
        self.full_parameter_ = {
            'w_inter_chain' : w_inter_chain,
            'w_contact' : w_contact,
            'w_noncontact' : w_noncontact,
            'w_inter_Fnat' : w_inter_Fnat,
            'w_value' : w_value
        }
        
    def y_to_label(self, data):
        return data
    def x_to_label(self, data):
        data_v = np.empty(shape = len(data), dtype = int)
        for i in range(len(data)):
            if data[i] > 0 and data[i] <= 0.25:
                data_v[i] = 0
            elif data[i] > 0.25 and data[i] <= 0.5:
                data_v[i] = 1
            elif data[i] > 0.5 and data[i] <= 0.75:
                data_v[i] = 2
            elif data[i] > 0.75 and data[i] <= 1:
                data_v[i] = 3
        return data_v
    def fit(self, X, y):
        if len(X) != len(y):
            return "The data dimension is incorrect!"
        dci_value = np.empty(shape=len(X))
        #sub_value = np.empty(shape=(len(X), 3))
        for i in range(len(X)):
            #sub_value[i, :] = DCI.single_dci(self, X[i])[1:4]
            dci_value[i] = DCI.single_dci(self, X[i])[0]
            #break
        #self.sub_value = sub_value
        self.DCI_value = dci_value
        self.train_label = self.x_to_label(dci_value)
        self.real_label = self.y_to_label(y)
        return self
    def get_params(self, deep = False):
        return self.full_parameter_
    def predict(self, X):
        dci_pred = np.empty(shape=len(X))
        for i in range(len(X)):
            dci_pred[i] = DCI.single_dci(self, X[i])[0]
        pred_label = self.x_to_label(dci_pred)
        return pred_label


# In[9]:


# temp = DCI(0.05, 0.95, 1.5, 0.67, 0.1, 0.35, 0.65).fit(x_train, y_train)

