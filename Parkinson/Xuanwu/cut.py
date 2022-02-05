#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  8 22:39:57 2019

@author: hantao.li
"""

import csv
import pandas as pd
import numpy as np
import os
import scipy.interpolate as spi

def mkdir(path):
    isExists = os.path.exists(path)
    if not isExists:
        os.makedirs(path)
        print(path + ' 创建成功')
        return True
    else:
        print(path + ' 目录已存在')
        return False

def ZeroDetc(StartTimeRow,EndTimeRow,filename,taskname):
    if StartTimeRow == 0:
        print ('----------------------------\n'+taskname+' '+filename+'起始行未找到')
    if EndTimeRow == 0:
        print ('----------------------------\n'+taskname+' '+filename+'结束行未找到')

CsvName = ['LShank','RShank','Waist','EEG','EMG','COF_2_','Arm']        
        

TaskNumber = 1
TaskName = ['task_5']#,'task_5']
PathName = '/Users/hantao.li/Documents/Dongjie/003数据/'

mkdir(PathName+'task')
#--------定义任务数量以及名称----------

StartHour = list(range(TaskNumber)); StartMin = list(range(TaskNumber)); StartSec = list(range(TaskNumber));
EndHour = list(range(TaskNumber)); EndMin = list(range(TaskNumber)); EndSec = list(range(TaskNumber));

StartHour[0] = '20'; StartMin[0] = '08'; StartSec[0] = '53'
EndHour[0]   = '20'; EndMin[0]   = '10'; EndSec[0]   = '14'
'''
StartHour[1] = '20'; StartMin[1] = '03'; StartSec[1] = '40'
EndHour[1]   = '20'; EndMin[1]   = '05'; EndSec[1]   = '38'

StartHour[2] = '20'; StartMin[2] = '07'; StartSec[2] = '05'
EndHour[2]   = '20'; EndMin[2]   = '08'; EndSec[2]   = '31'

StartHour[3] = '20'; StartMin[3] = '09'; StartSec[3] = '13'
EndHour[3]   = '20'; EndMin[3]   = '10'; EndSec[3]   = '14'

StartHour[4] = '14'; StartMin[4] = '51'; StartSec[4] = '03'
EndHour[4  ] = '14'; EndMin[4]   = '51'; EndSec[4]   = '46'
#---------定义任务起始时间----------
'''

#---------确定数据名称------------


for K in range(0,TaskNumber):
    

    C_N = 0
    StartTimeRow = 0
    EndTimeRow = 0
    
    isExists = os.path.exists(PathName+CsvName[C_N]+'.csv')
    if not isExists:
        new_f = open(PathName+CsvName[C_N]+'.csv', 'w')
        writer = csv.writer(new_f)
        writer.writerow(['0','0','0','0','0','0','0','0'])
        new_f.close()
        Dataframe_Butai_1 = pd.read_csv(PathName+CsvName[C_N]+'.csv',
                             header=None,index_col=False,
                            names=[CsvName[C_N]+'TIME', CsvName[C_N]+'ACCX',CsvName[C_N]+'ACCY',
                                   CsvName[C_N]+'ACCZ',CsvName[C_N]+'GYROX',CsvName[C_N]+'GYROY',
                                   CsvName[C_N]+'GYROZ','NC'])
        os.remove(PathName+CsvName[C_N]+'.csv') 
    else:
        origin_f = open(PathName+CsvName[C_N]+'.csv', 'r')
        reader = csv.reader(origin_f)
        
        StartTime = StartHour[K]+'_'+StartMin[K]+'_'+StartSec[K]+'_00'
        EndTime = EndHour[K]+'_'+EndMin[K]+'_'+EndSec[K]+'_00'
        
        column = [row[0] for row in reader]
        
        for j in range(0,len(column)):
            if StartTime in column[j]:
                #print (column[j])
                StartTimeRow = j
            if EndTime in column[j]:
                #print (column[j])
                EndTimeRow = j
        
        origin_f.close()
        #--------------------读取时间戳起始与结束的行-------------------
        
        origin_f = open(PathName+CsvName[C_N]+'.csv', 'r')
        new_f = open(PathName+CsvName[C_N]+'_new.csv', 'w')
        reader = csv.reader(origin_f)
        writer = csv.writer(new_f)
        
        
        for i,row in enumerate(reader):
            if ((i >= StartTimeRow) and (i <= EndTimeRow)):
               writer.writerow(row)
               
        origin_f.close()
        new_f.close()       
        #-------------------将此段数据保存为新csv文件-------------------
        
        Dataframe_Butai_1 = pd.read_csv(PathName+CsvName[C_N]+'_new.csv',
                                 header=None,index_col=False,
                                names=[CsvName[C_N]+'TIME', CsvName[C_N]+'ACCX',CsvName[C_N]+'ACCY',
                                       CsvName[C_N]+'ACCZ',CsvName[C_N]+'GYROX',CsvName[C_N]+'GYROY',
                                       CsvName[C_N]+'GYROZ','NC'])
        Dataframe_Butai_1.to_csv(PathName+CsvName[C_N]+'_new.csv')
        
        #------------------样条插值----------------------------------
        
        data1=pd.read_csv(PathName+CsvName[C_N]+'_new.csv',encoding='gbk')
        names = [CsvName[C_N]+'TIME', CsvName[C_N]+'ACCX',CsvName[C_N]+'ACCY',
                                           CsvName[C_N]+'ACCZ',CsvName[C_N]+'GYROX',CsvName[C_N]+'GYROY',
                                           CsvName[C_N]+'GYROZ','NC']
        #数据准备
        X=data1.index #定义数据点
        Ytime = data1[CsvName[C_N]+'TIME'].values
        Ytime = np.array(Ytime)
        Ytime = Ytime.tolist()
        if len(Ytime)%2==0:
            time111 = list(range(int(2.5*len(Ytime))))
        else:
            time111 = list(range(int(2.5*(len(Ytime)-1)+3)))
        kk = 0
        for i in range(0,len(time111)):
            if i==len(time111)-1:
                time111[i] = 'The Last Timepoint of the Task'
            elif (i%10==0 or (i-2)%10==0 or (i-5)%10==0 or (i-7)%10==0):
                time111[i] = Ytime[kk]
                kk = kk+1
            elif (i+1)%5==0:
                time111[i] = '+.007'
            else:
                time111[i] = '+.005'
                
        time = {CsvName[C_N]+'TIME':time111}
        Dataframe_Butai_1 = pd.DataFrame(time)
                
        #将剩余通道样条插值后拼接到后面
        for j1 in range(1,len(names)):
            Y=data1[names[j1]].values #定义数据点
            x=np.arange(0,len(data1),0.4) #定义观测点
            #进行一阶样条差值
            ipo3=spi.splrep(X,Y,k=3) #源数据点导入，生成参数
            iy3=spi.splev(x,ipo3) #根据观测点和样条参数，生成插值
            ch1 = pd.DataFrame(iy3)
            ch1.rename(columns={0:names[j1]},inplace=True)
            Dataframe_Butai_1 = pd.concat([Dataframe_Butai_1,ch1],axis=1)
        
        os.remove(PathName+CsvName[C_N]+'_new.csv') 
        
        ZeroDetc(StartTimeRow,EndTimeRow,CsvName[C_N],TaskName[K])
    #-------------------将新保存的csv文件读入dataframe-------------(左腿步态)
    
    #-------------------------------------------------
    #-------------------------------------------------
    #-------------------------------------------------
    
    C_N = 1
    StartTimeRow = 0
    EndTimeRow = 0
    
    isExists = os.path.exists(PathName+CsvName[C_N]+'.csv')
    if not isExists:
        new_f = open(PathName+CsvName[C_N]+'.csv', 'w')
        writer = csv.writer(new_f)
        writer.writerow(['0','0','0','0','0','0','0','0'])
        new_f.close()
        Dataframe_Butai_2 = pd.read_csv(PathName+CsvName[C_N]+'.csv',
                             header=None,index_col=False,
                            names=[CsvName[C_N]+'TIME', CsvName[C_N]+'ACCX',CsvName[C_N]+'ACCY',
                                   CsvName[C_N]+'ACCZ',CsvName[C_N]+'GYROX',CsvName[C_N]+'GYROY',
                                   CsvName[C_N]+'GYROZ','NC'])
        os.remove(PathName+CsvName[C_N]+'.csv') 
    else:
        origin_f = open(PathName+CsvName[C_N]+'.csv', 'r')
        reader = csv.reader(origin_f)
        
        column = [row[0] for row in reader]
        
        for j in range(0,len(column)):
            if StartTime in column[j]:
                #print (column[j])
                StartTimeRow = j
            if EndTime in column[j]:
                #print (column[j])
                EndTimeRow = j
        
        origin_f.close()
        #--------------------读取时间戳起始与结束的行-------------------
        
        origin_f = open(PathName+CsvName[C_N]+'.csv', 'r')
        new_f = open(PathName+CsvName[C_N]+'_new.csv', 'w')
        reader = csv.reader(origin_f)
        writer = csv.writer(new_f)
        
        
        for i,row in enumerate(reader):
            if ((i >= StartTimeRow) and (i <= EndTimeRow)):
               writer.writerow(row)
               
        origin_f.close()
        new_f.close()       
        #-------------------将此段数据保存为新csv文件-------------------
        
        Dataframe_Butai_2 = pd.read_csv(PathName+CsvName[C_N]+'_new.csv',
                                 header=None,index_col=False,
                                names=[CsvName[C_N]+'TIME', CsvName[C_N]+'ACCX',CsvName[C_N]+'ACCY',
                                       CsvName[C_N]+'ACCZ',CsvName[C_N]+'GYROX',CsvName[C_N]+'GYROY',
                                       CsvName[C_N]+'GYROZ','NC'])
        Dataframe_Butai_2.to_csv(PathName+CsvName[C_N]+'_new.csv')
        
     #------------------样条插值----------------------------------
        
        data1=pd.read_csv(PathName+CsvName[C_N]+'_new.csv',encoding='gbk')
        names = [CsvName[C_N]+'TIME', CsvName[C_N]+'ACCX',CsvName[C_N]+'ACCY',
                                           CsvName[C_N]+'ACCZ',CsvName[C_N]+'GYROX',CsvName[C_N]+'GYROY',
                                           CsvName[C_N]+'GYROZ','NC']
        #数据准备
        X=data1.index #定义数据点
        Ytime = data1[CsvName[C_N]+'TIME'].values
        Ytime = np.array(Ytime)
        Ytime = Ytime.tolist()
        if len(Ytime)%2==0:
            time111 = list(range(int(2.5*len(Ytime))))
        else:
            time111 = list(range(int(2.5*(len(Ytime)-1)+3)))
        kk = 0
        for i in range(0,len(time111)):
            if i==len(time111)-1:
                time111[i] = 'The Last Timepoint of the Task'
            elif (i%10==0 or (i-2)%10==0 or (i-5)%10==0 or (i-7)%10==0):
                time111[i] = Ytime[kk]
                kk = kk+1
            elif (i+1)%5==0:
                time111[i] = '+.007'
            else:
                time111[i] = '+.005'

        time = {CsvName[C_N]+'TIME':time111}
        Dataframe_Butai_2 = pd.DataFrame(time)
                
        #将剩余通道样条插值后拼接到后面
        for j1 in range(1,len(names)):
            Y=data1[names[j1]].values #定义数据点
            x=np.arange(0,len(data1),0.4) #定义观测点
            #进行一阶样条差值
            ipo3=spi.splrep(X,Y,k=3) #源数据点导入，生成参数
            iy3=spi.splev(x,ipo3) #根据观测点和样条参数，生成插值
            ch1 = pd.DataFrame(iy3)
            ch1.rename(columns={0:names[j1]},inplace=True)
            Dataframe_Butai_2 = pd.concat([Dataframe_Butai_2,ch1],axis=1)
        
        os.remove(PathName+CsvName[C_N]+'_new.csv') 
        ZeroDetc(StartTimeRow,EndTimeRow,CsvName[C_N],TaskName[K])
    #-------------------将新保存的csv文件读入dataframe-------------(右腿步态)
    
    #-------------------------------------------------
    #-------------------------------------------------
    #-------------------------------------------------
    
    C_N = 2
    StartTimeRow = 0
    EndTimeRow = 0
    
    isExists = os.path.exists(PathName+CsvName[C_N]+'.csv')
    if not isExists:
        new_f = open(PathName+CsvName[C_N]+'.csv', 'w')
        writer = csv.writer(new_f)
        writer.writerow(['0','0','0','0','0','0','0','0'])
        new_f.close()
        Dataframe_Butai_3 = pd.read_csv(PathName+CsvName[C_N]+'.csv',
                             header=None,index_col=False,
                            names=[CsvName[C_N]+'TIME', CsvName[C_N]+'ACCX',CsvName[C_N]+'ACCY',
                                   CsvName[C_N]+'ACCZ',CsvName[C_N]+'GYROX',CsvName[C_N]+'GYROY',
                                   CsvName[C_N]+'GYROZ','NC'])
        os.remove(PathName+CsvName[C_N]+'.csv') 
    else:
        origin_f = open(PathName+CsvName[C_N]+'.csv', 'r')
        reader = csv.reader(origin_f)
        
        column = [row[0] for row in reader]
        
        for j in range(0,len(column)):
            if StartTime in column[j]:
                #print (column[j])
                StartTimeRow = j
            if EndTime in column[j]:
                #print (column[j])
                EndTimeRow = j
        
        origin_f.close()
        #--------------------读取时间戳起始与结束的行-------------------
        
        origin_f = open(PathName+CsvName[C_N]+'.csv', 'r')
        new_f = open(PathName+CsvName[C_N]+'_new.csv', 'w')
        reader = csv.reader(origin_f)
        writer = csv.writer(new_f)
        
        
        for i,row in enumerate(reader):
            if ((i >= StartTimeRow) and (i <= EndTimeRow)):
               writer.writerow(row)
               
        origin_f.close()
        new_f.close()       
        #-------------------将此段数据保存为新csv文件-------------------
        
        Dataframe_Butai_3 = pd.read_csv(PathName+CsvName[C_N]+'_new.csv',
                                 header=None,index_col=False,
                                names=[CsvName[C_N]+'TIME', CsvName[C_N]+'ACCX',CsvName[C_N]+'ACCY',
                                       CsvName[C_N]+'ACCZ',CsvName[C_N]+'GYROX',CsvName[C_N]+'GYROY',
                                       CsvName[C_N]+'GYROZ','NC'])
        Dataframe_Butai_3.to_csv(PathName+CsvName[C_N]+'_new.csv')
     #------------------样条插值----------------------------------
        
        data1=pd.read_csv(PathName+CsvName[C_N]+'_new.csv',encoding='gbk')
        names = [CsvName[C_N]+'TIME', CsvName[C_N]+'ACCX',CsvName[C_N]+'ACCY',
                                           CsvName[C_N]+'ACCZ',CsvName[C_N]+'GYROX',CsvName[C_N]+'GYROY',
                                           CsvName[C_N]+'GYROZ','NC']
        #数据准备
        X=data1.index #定义数据点
        Ytime = data1[CsvName[C_N]+'TIME'].values
        Ytime = np.array(Ytime)
        Ytime = Ytime.tolist()
        if len(Ytime)%2==0:
            time111 = list(range(int(2.5*len(Ytime))))
        else:
            time111 = list(range(int(2.5*(len(Ytime)-1)+3)))
        kk = 0
        for i in range(0,len(time111)):
            if i==len(time111)-1:
                time111[i] = 'The Last Timepoint of the Task'
            elif (i%10==0 or (i-2)%10==0 or (i-5)%10==0 or (i-7)%10==0):
                time111[i] = Ytime[kk]
                kk = kk+1
            elif (i+1)%5==0:
                time111[i] = '+.007'
            else:
                time111[i] = '+.005'

        time = {CsvName[C_N]+'TIME':time111}
        Dataframe_Butai_3 = pd.DataFrame(time)
                
        #将剩余通道样条插值后拼接到后面
        for j1 in range(1,len(names)):
            Y=data1[names[j1]].values #定义数据点
            x=np.arange(0,len(data1),0.4) #定义观测点
            #进行一阶样条差值
            ipo3=spi.splrep(X,Y,k=3) #源数据点导入，生成参数
            iy3=spi.splev(x,ipo3) #根据观测点和样条参数，生成插值
            ch1 = pd.DataFrame(iy3)
            ch1.rename(columns={0:names[j1]},inplace=True)
            Dataframe_Butai_3 = pd.concat([Dataframe_Butai_3,ch1],axis=1)
        
        os.remove(PathName+CsvName[C_N]+'_new.csv') 
        ZeroDetc(StartTimeRow,EndTimeRow,CsvName[C_N],TaskName[K])
        #-------------------将新保存的csv文件读入dataframe-------------(腰步态)
    
    C_N = 6
    StartTimeRow = 0
    EndTimeRow = 0
    
    isExists = os.path.exists(PathName+CsvName[C_N]+'.csv')
    if not isExists:
        new_f = open(PathName+CsvName[C_N]+'.csv', 'w')
        writer = csv.writer(new_f)
        writer.writerow(['0','0','0','0','0','0','0','0'])
        new_f.close()
        Dataframe_Butai_4 = pd.read_csv(PathName+CsvName[C_N]+'.csv',
                             header=None,index_col=False,
                            names=[CsvName[C_N]+'TIME', CsvName[C_N]+'ACCX',CsvName[C_N]+'ACCY',
                                   CsvName[C_N]+'ACCZ',CsvName[C_N]+'GYROX',CsvName[C_N]+'GYROY',
                                   CsvName[C_N]+'GYROZ','SC'])
        os.remove(PathName+CsvName[C_N]+'.csv') 
    else:
        origin_f = open(PathName+CsvName[C_N]+'.csv', 'r')
        reader = csv.reader(origin_f)
        
        column = [row[0] for row in reader]
        
        for j in range(0,len(column)):
            if StartTime in column[j]:
                #print (column[j])
                StartTimeRow = j
            if EndTime in column[j]:
                #print (column[j])
                EndTimeRow = j
        
        origin_f.close()
        #--------------------读取时间戳起始与结束的行-------------------
        
        origin_f = open(PathName+CsvName[C_N]+'.csv', 'r')
        new_f = open(PathName+CsvName[C_N]+'_new.csv', 'w')
        reader = csv.reader(origin_f)
        writer = csv.writer(new_f)
        
        
        for i,row in enumerate(reader):
            if ((i >= StartTimeRow) and (i <= EndTimeRow)):
               writer.writerow(row)
               
        origin_f.close()
        new_f.close()       
        #-------------------将此段数据保存为新csv文件-------------------
        
        Dataframe_Butai_4 = pd.read_csv(PathName+CsvName[C_N]+'_new.csv',
                                 header=None,index_col=False,
                                names=[CsvName[C_N]+'TIME', CsvName[C_N]+'ACCX',CsvName[C_N]+'ACCY',
                                       CsvName[C_N]+'ACCZ',CsvName[C_N]+'GYROX',CsvName[C_N]+'GYROY',
                                       CsvName[C_N]+'GYROZ','SC'])
        Dataframe_Butai_4.to_csv(PathName+CsvName[C_N]+'_new.csv')
         #------------------样条插值----------------------------------
        
        data1=pd.read_csv(PathName+CsvName[C_N]+'_new.csv',encoding='gbk')
        names = [CsvName[C_N]+'TIME', CsvName[C_N]+'ACCX',CsvName[C_N]+'ACCY',
                                           CsvName[C_N]+'ACCZ',CsvName[C_N]+'GYROX',CsvName[C_N]+'GYROY',
                                           CsvName[C_N]+'GYROZ','SC']
        #数据准备
        X=data1.index #定义数据点
        Ytime = data1[CsvName[C_N]+'TIME'].values
        Ytime = np.array(Ytime)
        Ytime = Ytime.tolist()
        if len(Ytime)%2==0:
            time111 = list(range(int(2.5*len(Ytime))))
        else:
            time111 = list(range(int(2.5*(len(Ytime)-1)+3)))
        kk = 0
        for i in range(0,len(time111)):
            if i==len(time111)-1:
                time111[i] = 'The Last Timepoint of the Task'
            elif (i%10==0 or (i-2)%10==0 or (i-5)%10==0 or (i-7)%10==0):
                time111[i] = Ytime[kk]
                kk = kk+1
            elif (i+1)%5==0:
                time111[i] = '+.007'
            else:
                time111[i] = '+.005'

        time = {CsvName[C_N]+'TIME':time111}
        Dataframe_Butai_4 = pd.DataFrame(time)
                
        #将剩余通道样条插值后拼接到后面
        for j1 in range(1,len(names)):
            Y=data1[names[j1]].values #定义数据点
            x=np.arange(0,len(data1),0.4) #定义观测点
            #进行一阶样条差值
            ipo3=spi.splrep(X,Y,k=3) #源数据点导入，生成参数
            iy3=spi.splev(x,ipo3) #根据观测点和样条参数，生成插值
            ch1 = pd.DataFrame(iy3)
            ch1.rename(columns={0:names[j1]},inplace=True)
            Dataframe_Butai_4 = pd.concat([Dataframe_Butai_4,ch1],axis=1)
        
        os.remove(PathName+CsvName[C_N]+'_new.csv') 
        ZeroDetc(StartTimeRow,EndTimeRow,CsvName[C_N],TaskName[K])
    #-------------------将新保存的csv文件读入dataframe-------------(手臂步态)
    
    Dataframe_Butai = pd.concat([Dataframe_Butai_1,Dataframe_Butai_2,Dataframe_Butai_3,Dataframe_Butai_4],axis=1)
    Trans = Dataframe_Butai[CsvName[1]+'TIME']
    Dataframe_Butai.drop(labels=[CsvName[1]+'TIME'], axis=1,inplace = True)
    Dataframe_Butai.insert(1, CsvName[1]+'TIME', Trans)
    Trans = Dataframe_Butai[CsvName[2]+'TIME']
    Dataframe_Butai.drop(labels=[CsvName[2]+'TIME'], axis=1,inplace = True)
    Dataframe_Butai.insert(2, CsvName[2]+'TIME', Trans)
    Trans = Dataframe_Butai[CsvName[6]+'TIME']
    Dataframe_Butai.drop(labels=[CsvName[6]+'TIME'], axis=1,inplace = True)
    Dataframe_Butai.insert(3, CsvName[6]+'TIME', Trans)
    
    #==========================步态完成========================
    
    C_N = 3
    StartTimeRow = 0
    EndTimeRow = 0
    
    isExists = os.path.exists(PathName+CsvName[C_N]+'.csv')
    if not isExists:
        new_f = open(PathName+CsvName[C_N]+'.csv', 'w')
        writer = csv.writer(new_f)
        writer.writerow(['0','0','0','0','0','0','0','0','0','0'])
        new_f.close()
        Dataframe_Butai_Naodian = pd.read_csv(PathName+CsvName[C_N]+'.csv',
                             header=None,index_col=False,
                            names=['EEG_CH1(FZ)','EEG_CH2(FCZ)','EEG_CH3(T3)','EEG_CH4(T4)','EEG_CH5(P4)',
                                   'EEG_CH6(CZ)','EEG_CH7(O1)','EEG_CH8(O2)','NC',CsvName[C_N]+'TIME'])
        os.remove(PathName+CsvName[C_N]+'.csv') 
    else:
        origin_f = open(PathName+CsvName[C_N]+'.csv', 'r')
        reader = csv.reader(origin_f)
        
        StartTime = StartHour[K]+':'+StartMin[K]+':'+StartSec[K]+'.000'
        EndTime = EndHour[K]+':'+EndMin[K]+':'+EndSec[K]+'.000'
        
        column = [row[9] for row in reader]
        
        for j in range(0,len(column)):
            if StartTime in column[j]:
                #print (column[j])
                StartTimeRow = j
            if EndTime in column[j]:
                #print (column[j])
                EndTimeRow = j
        EndTimeRow = EndTimeRow+2
        
        origin_f.close()
        #--------------------读取时间戳起始与结束的行-------------------
        
        origin_f = open(PathName+CsvName[C_N]+'.csv', 'r')
        new_f = open(PathName+CsvName[C_N]+'_new.csv', 'w')
        reader = csv.reader(origin_f)
        writer = csv.writer(new_f)
        
        
        for i,row in enumerate(reader):
            if ((i >= StartTimeRow) and (i <= EndTimeRow)):
               writer.writerow(row)
               
        origin_f.close()
        new_f.close()       
        #-------------------将此段数据保存为新csv文件-------------------
        
        Dataframe_Naodian = pd.read_csv(PathName+CsvName[C_N]+'_new.csv',
                                 header=None,index_col=False,
                                names=['EEG_CH1(FZ)','EEG_CH2(FCZ)','EEG_CH3(T3)','EEG_CH4(T4)','EEG_CH5(P4)',
                                       'EEG_CH6(CZ)','EEG_CH7(O1)','EEG_CH8(O2)','NC',CsvName[C_N]+'TIME'])
        Dataframe_Naodian.to_csv(PathName+CsvName[C_N]+'_new.csv')
        os.remove(PathName+CsvName[C_N]+'_new.csv') 
        ZeroDetc(StartTimeRow,EndTimeRow,CsvName[C_N],TaskName[K])
    #-------------------将新保存的csv文件读入dataframe-------------(脑电)

    #==========================脑电完成========================
    
    C_N = 4
    StartTimeRow = 0
    EndTimeRow = 0
    
    isExists = os.path.exists(PathName+CsvName[C_N]+'.csv')
    if not isExists:
        new_f = open(PathName+CsvName[C_N]+'.csv', 'w')
        writer = csv.writer(new_f)
        writer.writerow(['0','0','0','0','0','0','0','0','0','0'])
        new_f.close()
        Dataframe_Jidian = pd.read_csv(PathName+CsvName[C_N]+'.csv',
                             header=None,index_col=False,
                            names=['EMG_CH1(TAL)','EMG_CH2(GSL)','EMG_CH3(TAR)','EMG_CH4(GSR)',
                                   'NC','NC','ECG_CH1','ECG_CH2',CsvName[C_N]+'原始TIME',CsvName[C_N]+'TIME'])
        os.remove(PathName+CsvName[C_N]+'.csv') 
    else:
        origin_f = open(PathName+CsvName[C_N]+'.csv', 'r')
        reader = csv.reader(origin_f)
        
        StartTime = StartHour[K]+':'+StartMin[K]+':'+StartSec[K]+'.000'
        EndTime = EndHour[K]+':'+EndMin[K]+':'+EndSec[K]+'.000'
        
        column = [row[9] for row in reader]
        
        for j in range(0,len(column)):
            if StartTime in column[j]:
                #print (column[j])
                StartTimeRow = j
            if EndTime in column[j]:
                #print (column[j])
                EndTimeRow = j
                
        #StartTimeRow = StartTimeRow-1
        EndTimeRow = EndTimeRow+2
        
        origin_f.close()
        #--------------------读取时间戳起始与结束的行-------------------
        
        origin_f = open(PathName+CsvName[C_N]+'.csv', 'r')
        new_f = open(PathName+CsvName[C_N]+'_new.csv', 'w')
        reader = csv.reader(origin_f)
        writer = csv.writer(new_f)
        
        
        for i,row in enumerate(reader):
            if ((i >= StartTimeRow) and (i <= EndTimeRow)):
               writer.writerow(row)
               
        origin_f.close()
        new_f.close()       
        #-------------------将此段数据保存为新csv文件-------------------
        
        Dataframe_Jidian = pd.read_csv(PathName+CsvName[C_N]+'_new.csv',
                                 header=None,index_col=False,
                                names=['EMG_CH1(TAL)','EMG_CH2(GSL)','EMG_CH3(TAR)','EMG_CH4(GSR)',
                                       'NC','NC','ECG_CH1','ECG_CH2',CsvName[C_N]+'原始TIME',CsvName[C_N]+'TIME'])
        Dataframe_Jidian.to_csv(PathName+CsvName[C_N]+'_new.csv')
        os.remove(PathName+CsvName[C_N]+'_new.csv') 
        ZeroDetc(StartTimeRow,EndTimeRow,CsvName[C_N],TaskName[K])
    #-------------------将新保存的csv文件读入dataframe-------------(肌电)
    
    #==========================肌电完成========================
    
    C_N = 5
    StartTimeRow = 0
    EndTimeRow = 0
    
    isExists = os.path.exists(PathName+CsvName[C_N]+'.csv')
    if not isExists:
        new_f = open(PathName+CsvName[C_N]+'.csv', 'w')
        writer = csv.writer(new_f)
        writer.writerow(['0','0','0'])
        new_f.close()
        Dataframe_Zudi = pd.read_csv(PathName+CsvName[C_N]+'.csv',
                             header=None,index_col=False,
                            names=['COFL','COFR',CsvName[C_N]+'TIME'])
        os.remove(PathName+CsvName[C_N]+'.csv') 
    else:
        origin_f = open(PathName+CsvName[C_N]+'.csv', 'r')
        reader = csv.reader(origin_f)
            
        StartTime = StartHour[K]+':'+StartMin[K]+':'+StartSec[K]+'.00'
        EndTime = EndHour[K]+':'+EndMin[K]+':'+EndSec[K]+'.00'
        column = [row[2] for row in reader]
        
        for j in range(0,len(column)):
            if StartTime in column[j]:
                #print (column[j])
                StartTimeRow = j
            if EndTime in column[j]:
                #print (column[j])
                EndTimeRow = j
        
        origin_f.close()
        #--------------------读取时间戳起始与结束的行-------------------
        
        origin_f = open(PathName+CsvName[C_N]+'.csv', 'r')
        new_f = open(PathName+CsvName[C_N]+'_new.csv', 'w')
        reader = csv.reader(origin_f)
        writer = csv.writer(new_f)
        
        
        for i,row in enumerate(reader):
            if ((i >= StartTimeRow) and (i <= EndTimeRow)):
               writer.writerow(row)
               
        origin_f.close()
        new_f.close()       
        #-------------------将此段数据保存为新csv文件-------------------
        
        Dataframe_Zudi = pd.read_csv(PathName+CsvName[C_N]+'_new.csv',
                                 header=None,index_col=False,
                                names=['COFL','COFR',CsvName[C_N]+'TIME'])
        Dataframe_Zudi.to_csv(PathName+CsvName[C_N]+'_new.csv')
        
         #------------------样条插值----------------------------------
        
        data1=pd.read_csv(PathName+CsvName[C_N]+'_new.csv',encoding='gbk')
        names = ['COFL','COFR',CsvName[C_N]+'TIME']
        #数据准备
        X=data1.index #定义数据点
        Ytime = data1[CsvName[C_N]+'TIME'].values
        Ytime = np.array(Ytime)
        Ytime = Ytime.tolist()
        if len(Ytime)%2==0:
            time111 = list(range(int(2.5*len(Ytime))))
        else:
            time111 = list(range(int(2.5*(len(Ytime)-1)+3)))
        kk = 0
        for i in range(0,len(time111)):
            if i==len(time111)-1:
                time111[i] = 'The Last Timepoint of the Task'
            elif (i%10==0 or (i-2)%10==0 or (i-5)%10==0 or (i-7)%10==0):
                time111[i] = Ytime[kk]
                kk = kk+1
            elif (i+1)%5==0:
                time111[i] = '+.007'
            else:
                time111[i] = '+.005'

        time = {CsvName[C_N]+'TIME':time111}
        Dataframe_Zudi = pd.DataFrame(time)
                
        #将剩余通道样条插值后拼接到后面
        for j1 in range(0,len(names)-1):
            Y=data1[names[j1]].values #定义数据点
            x=np.arange(0,len(data1),0.4) #定义观测点
            #进行一阶样条差值
            ipo3=spi.splrep(X,Y,k=3) #源数据点导入，生成参数
            iy3=spi.splev(x,ipo3) #根据观测点和样条参数，生成插值
            ch1 = pd.DataFrame(iy3)
            ch1.rename(columns={0:names[j1]},inplace=True)
            Dataframe_Zudi = pd.concat([Dataframe_Zudi,ch1],axis=1)
            
        Trans = Dataframe_Zudi[CsvName[5]+'TIME']
        Dataframe_Zudi.drop(labels=[CsvName[5]+'TIME'], axis=1,inplace = True)
        Dataframe_Zudi.insert(2, CsvName[5]+'TIME', Trans)
        os.remove(PathName+CsvName[C_N]+'_new.csv') 
        ZeroDetc(StartTimeRow,EndTimeRow,CsvName[C_N],TaskName[K])
    #-------------------将新保存的csv文件读入dataframe-------------(足底压力)
    
    #==========================足底压力完成========================
    
    
    Dataframe = pd.concat([Dataframe_Jidian,Dataframe_Naodian,Dataframe_Zudi,Dataframe_Butai],axis=1)
    
    Trans = Dataframe[CsvName[3]+'TIME']
    Dataframe.drop(labels=[CsvName[3]+'TIME'], axis=1,inplace = True)
    Dataframe.insert(0, CsvName[3]+'TIME', Trans)
    Trans = Dataframe[CsvName[4]+'TIME']
    Dataframe.drop(labels=[CsvName[4]+'TIME'], axis=1,inplace = True)
    Dataframe.insert(1, CsvName[4]+'TIME', Trans)
    Trans = Dataframe[CsvName[4]+'原始TIME']
    Dataframe.drop(labels=[CsvName[4]+'原始TIME'], axis=1,inplace = True)
    Dataframe.insert(2, CsvName[4]+'原始TIME', Trans)
    Trans = Dataframe[CsvName[5]+'TIME']
    Dataframe.drop(labels=[CsvName[5]+'TIME'], axis=1,inplace = True)
    Dataframe.insert(3, CsvName[5]+'TIME', Trans)
    Trans = Dataframe[CsvName[0]+'TIME']
    Dataframe.drop(labels=[CsvName[0]+'TIME'], axis=1,inplace = True)
    Dataframe.insert(4, CsvName[0]+'TIME', Trans)
    Trans = Dataframe[CsvName[1]+'TIME']
    Dataframe.drop(labels=[CsvName[1]+'TIME'], axis=1,inplace = True)
    Dataframe.insert(5, CsvName[1]+'TIME', Trans)
    Trans = Dataframe[CsvName[2]+'TIME']
    Dataframe.drop(labels=[CsvName[2]+'TIME'], axis=1,inplace = True)
    Dataframe.insert(6, CsvName[2]+'TIME', Trans)
    
    Dataframe.to_csv(PathName+'task/'+TaskName[K]+'.csv')
    
    for k in range(0,len(CsvName)):
        if k != 3:
            del Dataframe[CsvName[k]+'TIME']
    del Dataframe[CsvName[4]+'原始TIME']
    
    Dataframe = Dataframe.fillna(value=0)
    Dataframe = Dataframe.rename(columns={CsvName[3]+'TIME':'TIME'})
    
    Dataframe.to_csv(PathName+'task/'+TaskName[K]+'_data.csv')
    Dataframe.to_csv(PathName+'task/'+TaskName[K]+'_data.txt')
    

