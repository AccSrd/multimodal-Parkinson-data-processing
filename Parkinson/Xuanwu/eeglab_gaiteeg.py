#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 14 13:18:16 2020

@author: hantao.li
"""
import os
import csv
import numpy as np
import pandas as pd
import scipy.interpolate as spi
import time
import datetime

def mkdir(path):
    isExists = os.path.exists(path)
    if not isExists:
        os.makedirs(path)
        print(path + ' 创建成功')
        return True
    else:
        print(path + ' 目录已存在')
        return False
CsvName = ['LShank','RShank','Waist','Arm'] 

#============================================================================
'''
'''
PathName = '/Volumes/Work/Parkinson/宣武医院/原始数据/020-陈大蕙/data'
#EEGstarttime = datetime.datetime(2019,12,11,12,4,0,109000) #最后一位奇数
Gaitstarttime = datetime.datetime(2019,12,11,9,14,0,000000) #最后一位偶数
'''
'''
#============================================================================


for k in range(0,4):
    
    C_N = k
#    starttime = time.time()
    
#导入数据
    isExists = os.path.exists(PathName + '/' + CsvName[C_N] + '0.csv')
    if isExists:
    
        data1= pd.read_csv(PathName +'/'+ CsvName[C_N]+'0.csv',header=None,index_col=False,
                                    names=[CsvName[C_N]+'TIME', CsvName[C_N]+'ACCX',CsvName[C_N]+'ACCY',
                                           CsvName[C_N]+'ACCZ',CsvName[C_N]+'GYROX',CsvName[C_N]+'GYROY',
                                           CsvName[C_N]+'GYROZ','NC'])
        
        
        names = [CsvName[C_N]+'TIME', CsvName[C_N]+'ACCX',CsvName[C_N]+'ACCY',
                   CsvName[C_N]+'ACCZ',CsvName[C_N]+'GYROX',CsvName[C_N]+'GYROY',
                    CsvName[C_N]+'GYROZ','NC']
        
                #数据准备
        X=data1.index #定义数据点
        Ytime = data1[CsvName[C_N]+'TIME'].values
        Ytime = np.array(Ytime)
        Ytime = Ytime.tolist()
        
        
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
                        
                #将剩余通道样条插值后拼接到后面
        for j1 in range(0,len(names)):
            Y=data1[names[j1]].values #定义数据点
            x=np.arange(0,len(data1),0.2) #定义观测点
                    #进行一阶样条差值
            ipo3=spi.splrep(X,Y,k=3) #源数据点导入，生成参数
            iy3=spi.splev(x,ipo3) #根据观测点和样条参数，生成插值
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
        
        #Trans = Dataframe_Zudi['TIME']
        #Dataframe_Zudi.drop(labels=['TIME'], axis=1,inplace = True)
        #Dataframe_Zudi.insert(0,'TIME', Trans)
        Dataframe_Gait.to_csv(PathName + '/' +CsvName[C_N]+'.csv')
#        elapsed = (time.time() - starttime)
#        print(CsvName[C_N]+'已处理完成，用时：'+elapsed)
        
     
        '''
        
#starttime = time.time()        
        
data = pd.read_table(PathName + 'EEG.txt',sep=',',header=None)
data.to_csv(PathName + 'EEG_1000_0.csv', index=None, header=None)

data = pd.read_csv(PathName + 'EEG_1000_0.csv')

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
os.remove(PathName + 'EEG_1000.csv') 
os.remove(PathName + 'EEG_1000_0.csv') 
#print('EEG已处理完成，用时：'+elapsed)
'''