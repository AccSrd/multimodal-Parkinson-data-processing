#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 13 13:25:12 2020

@author: hantao.li
"""

import datetime
import pandas as pd
import numpy as np
import csv


PathName = '/Users/hantao.li/Documents/Dongjie/test/'


data = pd.read_table(PathName + 'EEG.txt',sep=',',header=None)
data.to_csv(PathName + 'EEG_1000_0.csv', index=None, header=None)

data = pd.read_csv(PathName + 'EEG_1000_0.csv')

Ytime1 = data['Time'].values
Ytime1 = np.array(Ytime1)
Ytime1 = Ytime1.tolist()
label1 = list(range(len(Ytime1)))
for k in range(0,len(label1)):
    label1[k]=0

EEGstarttime = datetime.datetime(2019,12,11,9,26,16,457000)
#最后一位存奇数!!!!!!

for i in range(0,len(label1)):
    deltatime = datetime.timedelta(microseconds=i*1000)
    time = EEGstarttime + deltatime
    strdatetime = str(time)
    strtime = strdatetime[11:23]
    label1[i] = strtime

label1 = {'TIME':label1}
ch1 = pd.DataFrame(label1)
data = pd.concat([ch1,data],axis=1)
data = data.drop(['Time'], axis=1)

data.to_csv(PathName + 'EEG_1000.csv')

origin_f = open(PathName + 'EEG_1000.csv', 'r')
new_f = open(PathName + 'EEG.csv', 'w')
reader = csv.reader(origin_f)
writer = csv.writer(new_f)

for i,row in enumerate(reader):
    if (i-2)%2 == 0:
       writer.writerow(row)
origin_f.close()
new_f.close()

data500 = pd.read_csv(PathName + 'EEG.csv',index_col=0)