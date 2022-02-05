#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 22 19:08:40 2019

@author: hantao.li
"""
#import csv
import pandas as pd
import numpy as np
#import os
import datetime

filepath = '/Users/hantao.li/Documents/Dongjie/003数据/task/task_5_data.csv'
newfilepath = '/Users/hantao.li/Documents/Dongjie/003数据/task/task_5_data_labeled'

VedioStartTime = '20:09:03'
VedioStartTimeRes = '.200'
#设置视频开始帧对应的真实时间------------------需更改！！！！！-------------
Fnumber_L1 = 3 #--------医生1确认（黄色）（xxx.xlsx)
Fnumber_L2 = 3 #--------医生1疑似（白色）
Fnumber_L3 = 4 #--------医生2（白色）（xxx-副本.xlsx）
#设置每个医生冻结步态数量————————————————————-需更改！！！！！--------------


Fstartmin_L1 = list(range(Fnumber_L1)); Fstartsec_L1 = list(range(Fnumber_L1))
Fendmin_L1 = list(range(Fnumber_L1)); Fendsec_L1 = list(range(Fnumber_L1))
Fstartmin_L2 = list(range(Fnumber_L2)); Fstartsec_L2 = list(range(Fnumber_L2))
Fendmin_L2 = list(range(Fnumber_L2)); Fendsec_L2 = list(range(Fnumber_L2))
Fstartmin_L3 = list(range(Fnumber_L3)); Fstartsec_L3 = list(range(Fnumber_L3))
Fendmin_L3 = list(range(Fnumber_L3)); Fendsec_L3 = list(range(Fnumber_L3))


Fstartmin_L1[0] = 0;  Fstartsec_L1[0] = 0
Fendmin_L1[0]   = 0;  Fendsec_L1[0]   = 13

Fstartmin_L1[1] = 0;  Fstartsec_L1[1] = 20
Fendmin_L1[1]   = 0;  Fendsec_L1[1]   = 39

Fstartmin_L1[2] = 0;  Fstartsec_L1[2] = 56
Fendmin_L1[2]   = 1;  Fendsec_L1[2]   = 0
'''
Fstartmin_L1[3] = 1;  Fstartsec_L1[3] = 1
Fendmin_L1[3]   = 1;  Fendsec_L1[3]   = 8

Fstartmin_L1[4] = 2;  Fstartsec_L1[4] = 35
Fendmin_L1[4]   = 3;  Fendsec_L1[4]   = 26

Fstartmin_L1[5] = 3;  Fstartsec_L1[5] = 47
Fendmin_L1[5]   = 4;  Fendsec_L1[5]   = 3

Fstartmin_L1[6] = 4;  Fstartsec_L1[6] = 13
Fendmin_L1[6]   = 4;  Fendsec_L1[6]   = 38

Fstartmin_L1[7] = 2;  Fstartsec_L1[7] = 3
Fendmin_L1[7]   = 2;  Fendsec_L1[7]   = 10

Fstartmin_L1[8] = 2;  Fstartsec_L1[8] = 13
Fendmin_L1[8]   = 2;  Fendsec_L1[8]   = 19

Fstartmin_L1[9] = 2;  Fstartsec_L1[9] = 49
Fendmin_L1[9]   = 2;  Fendsec_L1[9]   = 57

Fstartmin_L1[10] = 3;  Fstartsec_L1[10] = 0
Fendmin_L1[10]   = 3;  Fendsec_L1[10]   = 6
'''
#############################################

Fstartmin_L2[0] = 0;  Fstartsec_L2[0] = 0
Fendmin_L2[0]   = 0;  Fendsec_L2[0]   = 13

Fstartmin_L2[1] = 0;  Fstartsec_L2[1] = 20
Fendmin_L2[1]   = 0;  Fendsec_L2[1]   = 39

Fstartmin_L2[2] = 0;  Fstartsec_L2[2] = 56
Fendmin_L2[2]   = 1;  Fendsec_L2[2]   = 0
'''
Fstartmin_L2[3] = 1;  Fstartsec_L2[3] = 1
Fendmin_L2[3]   = 1;  Fendsec_L2[3]   = 8

Fstartmin_L2[4] = 2;  Fstartsec_L2[4] = 35
Fendmin_L2[4]   = 3;  Fendsec_L2[4]   = 26

Fstartmin_L2[5] = 3;  Fstartsec_L2[5] = 47
Fendmin_L2[5]   = 4;  Fendsec_L2[5]   = 3

Fstartmin_L2[6] = 4;  Fstartsec_L2[6] = 13
Fendmin_L2[6]   = 4;  Fendsec_L2[6]   = 38

Fstartmin_L2[7] = 2;  Fstartsec_L2[7] = 3
Fendmin_L2[7] = 2;  Fendsec_L2[7] = 10

Fstartmin_L2[8] = 2;  Fstartsec_L2[8] = 13
Fendmin_L2[8] = 2;  Fendsec_L2[8] = 19

Fstartmin_L2[9] = 2;  Fstartsec_L2[9] = 44
Fendmin_L2[9] = 2;  Fendsec_L2[9] = 57

Fstartmin_L2[10] = 3;  Fstartsec_L2[10] = 0
Fendmin_L2[10] = 3;  Fendsec_L2[10] = 6
'''
#############################################

Fstartmin_L3[0] = 0;  Fstartsec_L3[0] = 0
Fendmin_L3[0]   = 0;  Fendsec_L3[0]   = 4

Fstartmin_L3[1] = 0;  Fstartsec_L3[1] = 6
Fendmin_L3[1]   = 0;  Fendsec_L3[1]   = 12

Fstartmin_L3[2] = 0;  Fstartsec_L3[2] = 21
Fendmin_L3[2]   = 0;  Fendsec_L3[2]   = 39

Fstartmin_L3[3] = 0;  Fstartsec_L3[3] = 56
Fendmin_L3[3]   = 0;  Fendsec_L3[3]   = 59
'''
Fstartmin_L3[4] = 2;  Fstartsec_L3[4] = 36
Fendmin_L3[4]   = 3;  Fendsec_L3[4]   = 25

Fstartmin_L3[5] = 3;  Fstartsec_L3[5] = 46
Fendmin_L3[5]   = 4;  Fendsec_L3[5]   = 2

Fstartmin_L3[6] = 4;  Fstartsec_L3[6] = 13
Fendmin_L3[6]   = 4;  Fendsec_L3[6]   = 38

Fstartmin_L3[7] = 2;  Fstartsec_L3[7] = 14
Fendmin_L3[7] = 2;  Fendsec_L3[7] = 19

Fstartmin_L3[8] = 2;  Fstartsec_L3[8] = 47
Fendmin_L3[8] = 2;  Fendsec_L3[8] = 58

Fstartmin_L3[9] = 3;  Fstartsec_L3[9] = 1
Fendmin_L3[9] = 3;  Fendsec_L3[9] = 6

#Fstartmin_L3[10] = 3;  Fstartsec_L3[10] = 0
#Fendmin_L3[10] = 3;  Fendsec_L3[10] = 6
'''
#设置每个冻结步态开始结束时间————————————————需更改！！！！！


VedioStartTime = datetime.datetime.strptime(VedioStartTime, '%H:%M:%S')
#处理视频开始帧时间

data = pd.read_csv(filepath,index_col=0)
Ytime = data['TIME'].values
Ytime = np.array(Ytime)
Ytime = Ytime.tolist()
label1 = list(range(len(Ytime)))
label2 = list(range(len(Ytime)))
label3 = list(range(len(Ytime)))
#将时间戳读入list,创建label1数组

for k in range(0,len(label1)):
    label1[k]=0
    label2[k]=0
    label3[k]=0
#label1初始化
    
for Fnum in range(0,Fnumber_L1):
    Fstarttime = VedioStartTime + datetime.timedelta(minutes=int(Fstartmin_L1[Fnum]),seconds=Fstartsec_L1[Fnum])
    Fstarttime = str(Fstarttime)
    Fstarttime = Fstarttime[11:19]+VedioStartTimeRes
    
    Fendtime = VedioStartTime + datetime.timedelta(minutes=Fendmin_L1[Fnum],seconds=Fendsec_L1[Fnum])
    Fendtime = str(Fendtime)
    Fendtime = Fendtime[11:19]+VedioStartTimeRes
    
    
    
    for i in range(0,len(label1)):
        if Fstarttime in Ytime[i]:
            StarttimeRow = i
        if Fendtime in Ytime[i]:
            EndtimeRow = i
            
    for j in range(0,len(label1)):
        if ((j >= StarttimeRow) and (j <= EndtimeRow)):
            label1[j]=1
        
label1 = {'Label1':label1}
ch1 = pd.DataFrame(label1)
data = pd.concat([data,ch1],axis=1)
#-------------------------------------------------------------
for Fnum in range(0,Fnumber_L2):
    Fstarttime = VedioStartTime + datetime.timedelta(minutes=int(Fstartmin_L2[Fnum]),seconds=Fstartsec_L2[Fnum])
    Fstarttime = str(Fstarttime)
    Fstarttime = Fstarttime[11:19]+VedioStartTimeRes
    
    Fendtime = VedioStartTime + datetime.timedelta(minutes=Fendmin_L2[Fnum],seconds=Fendsec_L2[Fnum])
    Fendtime = str(Fendtime)
    Fendtime = Fendtime[11:19]+VedioStartTimeRes
    
    
    
    for i in range(0,len(label2)):
        if Fstarttime in Ytime[i]:
            StarttimeRow = i
        if Fendtime in Ytime[i]:
            EndtimeRow = i
            
    for j in range(0,len(label2)):
        if ((j >= StarttimeRow) and (j <= EndtimeRow)):
            label2[j]=1
        
label2 = {'Label2':label2}
ch2 = pd.DataFrame(label2)
data = pd.concat([data,ch2],axis=1)
#-------------------------------------------------------------
for Fnum in range(0,Fnumber_L3):
    Fstarttime = VedioStartTime + datetime.timedelta(minutes=int(Fstartmin_L3[Fnum]),seconds=Fstartsec_L3[Fnum])
    Fstarttime = str(Fstarttime)
    Fstarttime = Fstarttime[11:19]+VedioStartTimeRes
    
    Fendtime = VedioStartTime + datetime.timedelta(minutes=Fendmin_L3[Fnum],seconds=Fendsec_L3[Fnum])
    Fendtime = str(Fendtime)
    Fendtime = Fendtime[11:19]+VedioStartTimeRes
    
    
    
    for i in range(0,len(label3)):
        if Fstarttime in Ytime[i]:
            StarttimeRow = i
        if Fendtime in Ytime[i]:
            EndtimeRow = i
            
    for j in range(0,len(label3)):
        if ((j >= StarttimeRow) and (j <= EndtimeRow)):
            label3[j]=1
        
label3 = {'Label3':label3}
ch3 = pd.DataFrame(label3)
data = pd.concat([data,ch3],axis=1)

#data.drop(labels=[0], axis=1,inplace = True)
data.to_csv(newfilepath+'.csv')
data.to_csv(newfilepath+'.txt')
        
