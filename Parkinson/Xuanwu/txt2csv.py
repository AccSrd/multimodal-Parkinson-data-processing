#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 18 00:39:41 2019

@author: hantao.li
"""

import os
import numpy as np  
import pandas as pd  



#将txt存为csv
data = pd.read_table(r"/Users/hantao.li/Documents/Dongjie/003/jidian/jidian.txt",sep=', ',header=None)
data.to_csv('/Users/hantao.li/Documents/Dongjie/003/jidian/jidian_0.csv',index=None, header=None)