#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 30 02:54:23 2020

@author: hantao.li

Function : Timestamping the original data output by Accdata;
Convert the original data file to 500Hz

*******************Input Files********************************
format of files --> LShank0.csv RShank0.csv...
Gait0.csv

*******************Input**************************************
PathName --> The folder which contains the data file
EEGstarttime --> The time of the first frame of EEGLAB file, which is .vmrk file time
Gaitstarttime --> The gait synchronization time on the record sheet

*******************Output*************************************
format of files --> LShank.csv RShank.csv...
Gait.csv --> [TIME,OriTIME,ACCX,ACCY,ACCZ,GYROX,GYROY,GYROZ,NC/SC]
"""

import os
import numpy as np
import pandas as pd
import scipy.interpolate as spi
import datetime

######################################################################

PathName = '/Users/hantao.li/Desktop/test'
Gaitstarttime = datetime.datetime(2019,12,11,11,48,50,000000)           #Last bit should be even(000000)

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

for C_N in range(0,4):
    
    isExists = os.path.exists(PathName +'/'+CsvName[C_N]+'0.csv')
    if isExists:
        if C_N < 3: 
            data1= pd.read_csv(PathName+'/'+CsvName[C_N]+'0.csv',header=None,index_col=False,
                                        names=[CsvName[C_N]+'TIME', CsvName[C_N]+'ACCX',CsvName[C_N]+'ACCY',
                                               CsvName[C_N]+'ACCZ',CsvName[C_N]+'GYROX',CsvName[C_N]+'GYROY',
                                               CsvName[C_N]+'GYROZ','NC'])
            names = [CsvName[C_N]+'TIME', CsvName[C_N]+'ACCX',CsvName[C_N]+'ACCY',
                       CsvName[C_N]+'ACCZ',CsvName[C_N]+'GYROX',CsvName[C_N]+'GYROY',
                        CsvName[C_N]+'GYROZ','NC']
        else:
            data1= pd.read_csv(PathName+'/'+CsvName[C_N]+'0.csv',header=None,index_col=False,
                                        names=[CsvName[C_N]+'TIME', CsvName[C_N]+'ACCX',CsvName[C_N]+'ACCY',
                                               CsvName[C_N]+'ACCZ',CsvName[C_N]+'GYROX',CsvName[C_N]+'GYROY',
                                               CsvName[C_N]+'GYROZ','SC'])
            names = [CsvName[C_N]+'TIME', CsvName[C_N]+'ACCX',CsvName[C_N]+'ACCY',
                       CsvName[C_N]+'ACCZ',CsvName[C_N]+'GYROX',CsvName[C_N]+'GYROY',
                        CsvName[C_N]+'GYROZ','SC']
        X=data1.index 
        Ytime = (np.array(data1[CsvName[C_N]+'TIME'].values)).tolist()
        Ori_TimeStamp = list(range(int(5*len(Ytime))))
        
        kk = 0
        for i in range(0,len(Ori_TimeStamp)):
            if i%5==0:
                Ori_TimeStamp[i] = Ytime[kk]
                kk = kk+1
            elif i%5==1: 
                Ori_TimeStamp[i] = '+.002'
            elif i%5==2:
                Ori_TimeStamp[i] = '+.004'
            elif i%5==3:
                Ori_TimeStamp[i] = '+.006'
            elif i%5==4:
                Ori_TimeStamp[i] = '+.008'     
        
        OriTIME = {'OriTIME':Ori_TimeStamp}
        Dataframe_Gait = pd.DataFrame(OriTIME)
                        
        for j1 in range(0,len(names)):#Make third-order spline difference
            Y=data1[names[j1]].values 
            x=np.arange(0,len(data1),0.2) 
            ipo3=spi.splrep(X,Y,k=3)        
            iy3=spi.splev(x,ipo3) 
            ch1 = pd.DataFrame(iy3)
            ch1.rename(columns={0:names[j1]},inplace=True)
            Dataframe_Gait = pd.concat([Dataframe_Gait,ch1],axis=1)
        
        List_New_TimeStamp = list(range(len(Ori_TimeStamp)))
        for k in range(0,len(List_New_TimeStamp)):
            List_New_TimeStamp[k]=0        
        
        for i in range(0,len(List_New_TimeStamp)):
            deltatime = datetime.timedelta(microseconds=i*2000)
            List_New_TimeStamp[i] = str(Gaitstarttime + deltatime)[11:23]
        
        New_TimeStamp = {'TIME':List_New_TimeStamp}
        DataFrame_TimeStamp = pd.DataFrame(New_TimeStamp)
        Dataframe_Gait = pd.concat([DataFrame_TimeStamp,Dataframe_Gait],axis=1)
        
        Dataframe_Gait.to_csv(PathName+'/'+CsvName[C_N]+'.csv')
   
