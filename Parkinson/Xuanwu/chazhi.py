#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 21 17:50:43 2019

@author: hantao.li
"""

#import csv
#import pandas as pd
#import os
#import matplotlib.pyplot as plt

import numpy as np
import pandas as pd
import scipy.interpolate as spi


TaskNumber = 1
TaskName = ['task_1']#,'task_2_1','task_2_2','task_3','task_4']
CsvName = ['LShank','RShank','Waist','EEG_200','EMG_200','COF','Arm']
PathName = '/Users/hantao.li/Documents/Dongjie/test/'
C_N=5
#导入数据
data1= pd.read_csv('/Users/hantao.li/Documents/LStest.csv',header=None,
                   index_col=False,names=['TIME','R','ASD','adsf','ads','adsfs','as','dfds'])
names = ['R','ASD','adsf','ads','adsfs','as','dfds']
        #数据准备
X=data1.index #定义数据点
Ytime = data1['TIME'].values
Ytime = np.array(Ytime)
Ytime = Ytime.tolist()

#if len(Ytime)%2==0:
time111 = list(range(int(5*len(Ytime))))
#else:
#    time111 = list(range(int(2.5*(len(Ytime)-1)+3)))
kk = 0
for i in range(0,len(time111)):
#    if i==len(time111)-1:
#        time111[i] = 'The Last Timepoint of the Task'
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
        '''
    elif (i%10==0 or (i-2)%10==0 or (i-5)%10==0 or (i-7)%10==0):
        time111[i] = Ytime[kk]
        kk = kk+1
    elif (i+1)%5==0:
        time111[i] = '+.007'
    else:
        time111[i] = '+.005'
                '''
time = {'TIME':time111}
Dataframe_Zudi = pd.DataFrame(time)
                
        #将剩余通道样条插值后拼接到后面
for j1 in range(0,len(names)):
    Y=data1[names[j1]].values #定义数据点
    x=np.arange(0,len(data1),0.2) #定义观测点
            #进行一阶样条差值
    ipo3=spi.splrep(X,Y,k=3) #源数据点导入，生成参数
    iy3=spi.splev(x,ipo3) #根据观测点和样条参数，生成插值
    ch1 = pd.DataFrame(iy3)
    ch1.rename(columns={0:names[j1]},inplace=True)
    Dataframe_Zudi = pd.concat([Dataframe_Zudi,ch1],axis=1)

            
Trans = Dataframe_Zudi['TIME']
Dataframe_Zudi.drop(labels=['TIME'], axis=1,inplace = True)
Dataframe_Zudi.insert(0,'TIME', Trans)
Dataframe_Zudi.to_csv('/Users/hantao.li/Documents/LStest_.csv')
  
##作图
#fig,(ax1)=plt.subplots(1,1,figsize=(10,12))
#ax1.plot(x,iy1,'r.',label='插值点')
#ax1.set_ylim(Y.min()-10,Y.max()+10)
#ax1.set_ylabel('指数')
#ax1.set_title('线性插值')
#ax1.legend()


#Dataframe = pd.read_csv('/Users/hantao.li/Documents/chazhi.csv',header=None,index_col=False)

#ZeroData = pd.Series(['0',0,0,0,0,0,0,0],index=[0,1,2,3,'123213',5,6,7])
#Dataframe.append(ZeroData,ignore_index=True)
#Dataframe.to_csv('/Users/hantao.li/Documents/chazhi_1.csv')