#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 12 17:10:46 2020

@author: hantao.li
"""

import os
import numpy as np  
import pandas as pd  



#将txt存为csv
data = pd.read_table(r"/Volumes/Backup Plus/学校/北航/冻结步态原始数据/宣武医院/002-caoguifeng/002.txt",sep=',',header=None)
data.to_csv('/Volumes/Backup Plus/学校/北航/冻结步态原始数据/宣武医院/002-caoguifeng/002.csv',index=None, header=None)