#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 23 23:39:13 2019

@author: hantao.li
"""

import pandas as pd
import scipy
from scipy import io

features_struct = scipy.io.loadmat('/Users/hantao.li/Documents/Dongjie/003/naodian/naodian_0.mat')
features = features_struct['Record']
dfdata = pd.DataFrame(features)
datapath1 = '/Users/hantao.li/Documents/Dongjie/003/naodian/naodian_1000.csv'
dfdata.to_csv(datapath1, index=False)
