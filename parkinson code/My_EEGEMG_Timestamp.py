#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 13 17:17:59 2020

@author: hantao.li

Function : Timestamping the original data output by EEG Lab;
Convert the original data file to 500Hz

*******************Input Files********************************
format of files --> EEG.txt EMG.txt ECG.txt LShank0.csv RShank0.csv...
EEG.txt --> [Number,25Channels]
EMG.txt --> [Number,EMG1,EMG2,EMG4]
ECG.txt --> [Number,EMG3]
Gait0.csv --> [TIME,OriTIME,ACCX,ACCY,ACCZ,GYROX,GYROY,GYROZ,NC/SC]

*******************Input**************************************
PathName --> The folder which contains the data file
Tasknumber --> The number of task to be cut
EEGstarttime --> The time of the first frame of EEGLAB file, which is .vmrk file time
Gaitstarttime --> The gait synchronization time on the record sheet

*******************Output*************************************
format of files --> EEG.csv EMG.csv ECG.csv LShank.csv RShank.csv...
EEG.csv --> [TIME,25Channels]
EMG.csv --> [TIME,EMG1,EMG2,EMG4]
ECG.csv --> [TIME,EMG3]
Gait.csv --> [TIME,OriTIME,ACCX,ACCY,ACCZ,GYROX,GYROY,GYROZ,NC/SC]
"""

import os
import csv
import numpy as np
import pandas as pd
import datetime

######################################################################

PathName = '/Users/hantao.li/Desktop/test/'
EEGstarttime = datetime.datetime(2020,1,11,9,29,53,97000)              #Last bit should be odd

######################################################################

def mkdir(path):
    isExists = os.path.exists(path)
    if not isExists:
        os.makedirs(path)
        print(path + 'Folder Created Successfully')
        return True
    else:
        print(path + 'Unsuccessful, Directory Already Exists')
        return False

    
def Label_EEG(EEGName):
    data = pd.read_table(PathName + EEGName + '.txt',sep=',',header=None)
    data.to_csv(PathName + EEGName + '_1000_0.csv', index=None, header=None)
    data = pd.read_csv(PathName + EEGName + '_1000_0.csv')
    
    Ytime1 = data['Time'].values
    Ytime1 = np.array(Ytime1)
    Ytime1 = Ytime1.tolist()
    label1 = list(range(len(Ytime1)))
    for k in range(0,len(label1)):
        label1[k]=0
        
    for i in range(0,len(label1)):
        deltatime = datetime.timedelta(microseconds=i*1000)
        strdatetime = str(EEGstarttime + deltatime)
        strtime = strdatetime[11:23]
        label1[i] = strtime
    
    label1 = {'TIME':label1}
    ch1 = pd.DataFrame(label1)
    data = pd.concat([ch1,data],axis=1)
    data = data.drop(['Time'], axis=1)
    
    data.to_csv(PathName + EEGName + '_1000.csv')
    
    origin_f = open(PathName + EEGName + '_1000.csv', 'r')
    new_f = open(PathName + EEGName + '.csv', 'w')
    reader = csv.reader(origin_f)
    writer = csv.writer(new_f)
    
    for i,row in enumerate(reader):
        if (i-2)%2 == 0:
           writer.writerow(row)
    origin_f.close()
    new_f.close()
    os.remove(PathName + EEGName + '_1000.csv') 
    os.remove(PathName + EEGName + '_1000_0.csv') 

Label_EEG('EMG')