#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 30 02:54:23 2020

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
import scipy.interpolate as spi
import time
import datetime

######################################################################

PathName = '/Users/hantao.li/Desktop/test/'
EEGstarttime = datetime.datetime(2019,12,11,12,4,0,109000)              #Last bit should be odd
Gaitstarttime = datetime.datetime(2019,12,11,11,48,50,000000)           #Last bit should be even

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

CsvName = ['LShank','RShank','Waist','Arm'] 
EEGName = ['EEG','EMG','ECG']

for C_N in range(0,4):
    
    isExists = os.path.exists(PathName+CsvName[C_N]+'0.csv')
    if isExists:
        data1= pd.read_csv(PathName+CsvName[C_N]+'0.csv',header=None,index_col=False,
                                    names=[CsvName[C_N]+'TIME', CsvName[C_N]+'ACCX',CsvName[C_N]+'ACCY',
                                           CsvName[C_N]+'ACCZ',CsvName[C_N]+'GYROX',CsvName[C_N]+'GYROY',
                                           CsvName[C_N]+'GYROZ','NC'])
        names = [CsvName[C_N]+'TIME', CsvName[C_N]+'ACCX',CsvName[C_N]+'ACCY',
                   CsvName[C_N]+'ACCZ',CsvName[C_N]+'GYROX',CsvName[C_N]+'GYROY',
                    CsvName[C_N]+'GYROZ','NC']
        
        X=data1.index 
        Ytime = (np.array(data1[CsvName[C_N]+'TIME'].values)).tolist()
        time111 = list(range(int(5*len(Ytime))))
        
        kk = 0
        for i in range(0,len(time111)):
            if i%5==0:
                time111[i] = Ytime[kk]
                kk = kk+1
            elif i%5==1: 
                time111[i] = '+.002'
            elif i%5==2:
                time111[i] = '+.004'
            elif i%5==3:
                time111[i] = '+.006'
            elif i%5==4:
                time111[i] = '+.008'     
        
        time = {'OriTIME':time111}
        Dataframe_Gait = pd.DataFrame(time)
                        
        for j1 in range(0,len(names)):
            Y=data1[names[j1]].values 
            x=np.arange(0,len(data1),0.2) 
            ipo3=spi.splrep(X,Y,k=3)        #Make third-order spline difference
            iy3=spi.splev(x,ipo3) 
            ch1 = pd.DataFrame(iy3)
            ch1.rename(columns={0:names[j1]},inplace=True)
            Dataframe_Gait = pd.concat([Dataframe_Gait,ch1],axis=1)
        
        label1 = list(range(len(time111)))
        for k in range(0,len(label1)):
            label1[k]=0        
        
        for i in range(0,len(label1)):
            deltatime = datetime.timedelta(microseconds=i*2000)
            time = Gaitstarttime + deltatime
            strdatetime = str(time)
            strtime = strdatetime[11:23]
            label1[i] = strtime
        
        label1 = {'TIME':label1}
        ch1 = pd.DataFrame(label1)
        Dataframe_Gait = pd.concat([ch1,Dataframe_Gait],axis=1)
        Dataframe_Gait.to_csv(PathName+CsvName[C_N]+'.csv')
   
for E_N in range(0,3):        
        
    data = pd.read_table(PathName + EEGName[E_N] + '.txt',sep=',',header=None)
    data.to_csv(PathName + EEGName[E_N] + '_1000_0.csv', index=None, header=None)
    data = pd.read_csv(PathName + EEGName[E_N] + '_1000_0.csv')
    
    Ytime1 = data['Time'].values
    Ytime1 = np.array(Ytime1)
    Ytime1 = Ytime1.tolist()
    label1 = list(range(len(Ytime1)))
    for k in range(0,len(label1)):
        label1[k]=0
        
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
    
    data.to_csv(PathName + EEGName[E_N] + '_1000.csv')
    
    origin_f = open(PathName + EEGName[E_N] + '_1000.csv', 'r')
    new_f = open(PathName + EEGName[E_N] + '.csv', 'w')
    reader = csv.reader(origin_f)
    writer = csv.writer(new_f)
    
    for i,row in enumerate(reader):
        if (i-2)%2 == 0:
           writer.writerow(row)
    origin_f.close()
    new_f.close()
    os.remove(PathName + EEGName[E_N] + '_1000.csv') 
    os.remove(PathName + EEGName[E_N] + '_1000_0.csv') 
        