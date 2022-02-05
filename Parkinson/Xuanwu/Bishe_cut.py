#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 28 14:36:15 2020

@author: hantao.li

Function : Cut the data into single task
If you want to view files with the original time, Uncomment the code in the last.

*******************Input Files********************************
format of files --> EEG.csv EMG.csv ECG.csv LShank.csv RShank.csv...
EEG.csv --> [TIME,25Channels]
EMG.csv --> [TIME,EMG1,EMG2,EMG4]
Gait.csv --> [TIME,OriTIME,ACCX,ACCY,ACCZ,GYROX,GYROY,GYROZ,NC/SC]

*******************Input**************************************
PathName --> The folder which contains the data file
Tasknumber --> The number of task to be cut
TaskName --> Name of tasks 
CutTime --> World time corresponding to tasks, format-->12:04:38 12:10:39 12:12:33 12:18:05.......
CriName,DropName --> The time stamp of GaitTIME used in the task_X.csv file. Normally L/R. 
If there is no LShank data, please change it to R/L.

*******************Output*************************************
(PathName)/task/task_(Tasknmber)_data.txt
format-->[Number,Time,EEG,EMG,LShank,RShank,Waist,Arm]
"""

import csv
import pandas as pd
import os
import time
import re

######################################################################

TaskNumber = 5
TaskName = ['task_1','task_2','task_3','task_4','task_5']#,'task_6','task_7']
PathName = '/Volumes/Work/Parkinson/宣武医院/3-预处理后数据文件/020 E/'
OutputPath = '/Volumes/Work/Parkinson/宣武医院/4-分段未标注数据/020 E'
CutTime = '09:30:07 09:38:46 09:39:48 09:41:06 09:41:43 09:42:50 09:44:36 09:50:50 09:53:17 09:55:57'

######################################################################

CsvName  = ['LShank','RShank','Waist','EEG_ICA','Arm','EMG']
CriName  = 'LShank'   
DropName = 'RShank'  

def mkdir(path):
    isExists = os.path.exists(path)
    if not isExists:
        os.makedirs(path)
        print(path + ' --> Folder Created Successfully')
        return True
    else:
        print(path + ' --> Unsuccessful, Directory Already Exists')
        return False

def ZeroDetc(StartTimeRow,EndTimeRow,filename,taskname):
    if StartTimeRow == 0:
        print ('----------------------------\n'+taskname+' '+filename+' Can not find the Start Row')
    if EndTimeRow == 0:
        print ('----------------------------\n'+taskname+' '+filename+' Can not find the End Row')
'''
def CutGait(C_N):
    starttime = time.time()  
    StartTimeRow = 0
    EndTimeRow = 0
    isExists = os.path.exists(PathName+CsvName[C_N]+'.csv')     #Check if there have the data file
    StartTime = StartHour[K]+':'+StartMin[K]+':'+StartSec[K]+'.002'
    EndTime = EndHour[K]+':'+EndMin[K]+':'+EndSec[K]+'.002'
    
    if not isExists:
        new_f = open(PathName+CsvName[C_N]+'.csv', 'w')
        writer = csv.writer(new_f)
        writer.writerow(['0','0','0','0','0','0','0','0','0'])
        new_f.close()
        Dataframe_Butai_1 = pd.read_csv(PathName+CsvName[C_N]+'.csv',
                             header=None,index_col=False,
                            names=[CsvName[C_N]+'TIME', CsvName[C_N]+'OriTIME',
                                   CsvName[C_N]+'ACCX',CsvName[C_N]+'ACCY',
                                   CsvName[C_N]+'ACCZ',CsvName[C_N]+'GYROX',CsvName[C_N]+'GYROY',
                                   CsvName[C_N]+'GYROZ','NC'])
        os.remove(PathName+CsvName[C_N]+'.csv') 
    else:
        origin_f = open(PathName+CsvName[C_N]+'.csv', 'r')
        reader = csv.reader(origin_f)
        column = [row[1] for row in reader]
        for j in range(0,len(column)):       #Fine the start and end lines of the data
            if StartTime in column[j]:
                StartTimeRow = j-1
            if EndTime in column[j]:
                EndTimeRow = j-1
        origin_f.close()
        
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
    '''   



StartTime00 = time.time() 
mkdir(OutputPath)

Pattern = r' |-|:'
Timelist = re.split(Pattern,CutTime)  #split the cut time in to h/m/s
StartHour = Timelist[::6]
StartMin = Timelist[1::6]
StartSec = Timelist[2::6]
EndHour = Timelist[3::6]
EndMin = Timelist[4::6]
EndSec = Timelist[5::6]


for K in range(0,TaskNumber):    #For each task
    
    taskstarttime = time.time()  
    
    C_N = 0
    starttime = time.time()  
    StartTimeRow = 0
    EndTimeRow = 0
    
    isExists = os.path.exists(PathName+CsvName[C_N]+'.csv')     #Check if there have the data file
    StartTime = StartHour[K]+':'+StartMin[K]+':'+StartSec[K]+'.002'
    EndTime = EndHour[K]+':'+EndMin[K]+':'+EndSec[K]+'.002'
    
    if not isExists:
        new_f = open(PathName+CsvName[C_N]+'.csv', 'w')
        writer = csv.writer(new_f)
        writer.writerow(['0','0','0','0','0','0','0','0','0'])
        new_f.close()
        Dataframe_Butai_1 = pd.read_csv(PathName+CsvName[C_N]+'.csv',
                             header=None,index_col=False,
                            names=[CsvName[C_N]+'TIME', CsvName[C_N]+'OriTIME',
                                   CsvName[C_N]+'ACCX',CsvName[C_N]+'ACCY',
                                   CsvName[C_N]+'ACCZ',CsvName[C_N]+'GYROX',CsvName[C_N]+'GYROY',
                                   CsvName[C_N]+'GYROZ','NC'])
        os.remove(PathName+CsvName[C_N]+'.csv') 
    else:
        origin_f = open(PathName+CsvName[C_N]+'.csv', 'r')
        reader = csv.reader(origin_f)
        column = [row[1] for row in reader]
        for j in range(0,len(column)):       #Fine the start and end lines of the data
            if StartTime in column[j]:
                StartTimeRow = j-1
            if EndTime in column[j]:
                EndTimeRow = j-1
        origin_f.close()
        
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
                                names=[CsvName[C_N],CsvName[C_N]+'TIME',CsvName[C_N]+'OriTIME','?',
                                       CsvName[C_N]+'ACCX',CsvName[C_N]+'ACCY',
                                       CsvName[C_N]+'ACCZ',CsvName[C_N]+'GYROX',CsvName[C_N]+'GYROY',
                                       CsvName[C_N]+'GYROZ','NC'])
        Dataframe_Butai_1 = Dataframe_Butai_1.drop([CsvName[C_N],'?'], axis=1)
        
        Dataframe_Butai_1.to_csv(PathName+CsvName[C_N]+'_new.csv')
        os.remove(PathName+CsvName[C_N]+'_new.csv') 
        
        ZeroDetc(StartTimeRow,EndTimeRow,CsvName[C_N],TaskName[K])
        elapsed = (time.time() - starttime)
        print(CsvName[C_N]+'已处理完成，用时：'+str(elapsed))
    #-------------------将新保存的csv文件读入dataframe-------------(左腿步态)
    
    #-------------------------------------------------
    #-------------------------------------------------
    #-------------------------------------------------
    
    C_N = 1
    starttime = time.time()  
    StartTimeRow = 0
    EndTimeRow = 0
    
    isExists = os.path.exists(PathName+CsvName[C_N]+'.csv')
    if not isExists:
        new_f = open(PathName+CsvName[C_N]+'.csv', 'w')
        writer = csv.writer(new_f)
        writer.writerow(['0','0','0','0','0','0','0','0','0'])
        new_f.close()
        Dataframe_Butai_2 = pd.read_csv(PathName+CsvName[C_N]+'.csv',
                             header=None,index_col=False,
                            names=[CsvName[C_N]+'TIME', CsvName[C_N]+'OriTIME',
                                   CsvName[C_N]+'ACCX',CsvName[C_N]+'ACCY',
                                   CsvName[C_N]+'ACCZ',CsvName[C_N]+'GYROX',CsvName[C_N]+'GYROY',
                                   CsvName[C_N]+'GYROZ','NC'])
        os.remove(PathName+CsvName[C_N]+'.csv') 
    else:
        origin_f = open(PathName+CsvName[C_N]+'.csv', 'r')
        reader = csv.reader(origin_f)
        
        column = [row[1] for row in reader]
        
        for j in range(0,len(column)):
            if StartTime in column[j]:
                #print (column[j])
                StartTimeRow = j-1
            if EndTime in column[j]:
                #print (column[j])
                EndTimeRow = j-1
        
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
                                names=[CsvName[C_N],CsvName[C_N]+'TIME',CsvName[C_N]+'OriTIME','?',
                                       CsvName[C_N]+'ACCX',CsvName[C_N]+'ACCY',
                                       CsvName[C_N]+'ACCZ',CsvName[C_N]+'GYROX',CsvName[C_N]+'GYROY',
                                       CsvName[C_N]+'GYROZ','NC'])
    
        Dataframe_Butai_2 = Dataframe_Butai_2.drop([CsvName[C_N],'?'], axis=1)
        
        Dataframe_Butai_2.to_csv(PathName+CsvName[C_N]+'_new.csv')
        os.remove(PathName+CsvName[C_N]+'_new.csv') 
        
        ZeroDetc(StartTimeRow,EndTimeRow,CsvName[C_N],TaskName[K])
        elapsed = (time.time() - starttime)
        print(CsvName[C_N]+'已处理完成，用时：'+str(elapsed))
    #-------------------将新保存的csv文件读入dataframe-------------(右腿步态)
    
    #-------------------------------------------------
    #-------------------------------------------------
    #-------------------------------------------------
    
    C_N = 2
    starttime = time.time()  
    StartTimeRow = 0
    EndTimeRow = 0
    
    isExists = os.path.exists(PathName+CsvName[C_N]+'.csv')
    if not isExists:
        new_f = open(PathName+CsvName[C_N]+'.csv', 'w')
        writer = csv.writer(new_f)
        writer.writerow(['0','0','0','0','0','0','0','0','0'])
        new_f.close()
        Dataframe_Butai_3 = pd.read_csv(PathName+CsvName[C_N]+'.csv',
                             header=None,index_col=False,
                            names=[CsvName[C_N]+'TIME', CsvName[C_N]+'OriTIME',
                                   CsvName[C_N]+'ACCX',CsvName[C_N]+'ACCY',
                                   CsvName[C_N]+'ACCZ',CsvName[C_N]+'GYROX',CsvName[C_N]+'GYROY',
                                   CsvName[C_N]+'GYROZ','NC'])
        os.remove(PathName+CsvName[C_N]+'.csv') 
    else:
        origin_f = open(PathName+CsvName[C_N]+'.csv', 'r')
        reader = csv.reader(origin_f)
        
        column = [row[1] for row in reader]
        
        for j in range(0,len(column)):
            if StartTime in column[j]:
                #print (column[j])
                StartTimeRow = j-1
            if EndTime in column[j]:
                #print (column[j])
                EndTimeRow = j-1
        
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
                                names=[CsvName[C_N],CsvName[C_N]+'TIME',CsvName[C_N]+'OriTIME','?',
                                       CsvName[C_N]+'ACCX',CsvName[C_N]+'ACCY',
                                       CsvName[C_N]+'ACCZ',CsvName[C_N]+'GYROX',CsvName[C_N]+'GYROY',
                                       CsvName[C_N]+'GYROZ','NC'])
        Dataframe_Butai_3 = Dataframe_Butai_3.drop([CsvName[C_N],'?'], axis=1)
    
        Dataframe_Butai_3.to_csv(PathName+CsvName[C_N]+'_new.csv')
        os.remove(PathName+CsvName[C_N]+'_new.csv') 
        
        ZeroDetc(StartTimeRow,EndTimeRow,CsvName[C_N],TaskName[K])
        elapsed = (time.time() - starttime)
        print(CsvName[C_N]+'已处理完成，用时：'+str(elapsed))
        #-------------------将新保存的csv文件读入dataframe-------------(腰步态)
    
    C_N = 4
    starttime = time.time()  
    StartTimeRow = 0
    EndTimeRow = 0
    
    isExists = os.path.exists(PathName+CsvName[C_N]+'.csv')
    if not isExists:
        new_f = open(PathName+CsvName[C_N]+'.csv', 'w')
        writer = csv.writer(new_f)
        writer.writerow(['0','0','0','0','0','0','0','0','0'])
        new_f.close()
        Dataframe_Butai_4 = pd.read_csv(PathName+CsvName[C_N]+'.csv',
                             header=None,index_col=False,
                            names=[CsvName[C_N]+'TIME', CsvName[C_N]+'OriTIME',
                                   CsvName[C_N]+'ACCX',CsvName[C_N]+'ACCY',
                                   CsvName[C_N]+'ACCZ',CsvName[C_N]+'GYROX',CsvName[C_N]+'GYROY',
                                   CsvName[C_N]+'GYROZ','SC'])
        os.remove(PathName+CsvName[C_N]+'.csv') 
    else:
        origin_f = open(PathName+CsvName[C_N]+'.csv', 'r')
        reader = csv.reader(origin_f)
        
        column = [row[1] for row in reader]
        
        for j in range(0,len(column)):
            if StartTime in column[j]:
                #print (column[j])
                StartTimeRow = j-1
            if EndTime in column[j]:
                #print (column[j])
                EndTimeRow = j-1
        
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
                                names=[CsvName[C_N],CsvName[C_N]+'TIME',CsvName[C_N]+'OriTIME','?',
                                       CsvName[C_N]+'ACCX',CsvName[C_N]+'ACCY',
                                       CsvName[C_N]+'ACCZ',CsvName[C_N]+'GYROX',CsvName[C_N]+'GYROY',
                                       CsvName[C_N]+'GYROZ','SC'])
    
        Dataframe_Butai_4 = Dataframe_Butai_4.drop([CsvName[C_N],'?'], axis=1)
        Dataframe_Butai_4.to_csv(PathName+CsvName[C_N]+'_new.csv')
        os.remove(PathName+CsvName[C_N]+'_new.csv') 
        
        ZeroDetc(StartTimeRow,EndTimeRow,CsvName[C_N],TaskName[K])
        elapsed = (time.time() - starttime)
        print(CsvName[C_N]+'已处理完成，用时：'+str(elapsed))
    #-------------------将新保存的csv文件读入dataframe-------------(手臂步态)
    
    Dataframe_Butai = pd.concat([Dataframe_Butai_1,Dataframe_Butai_2,Dataframe_Butai_3,Dataframe_Butai_4],axis=1)
    Trans = Dataframe_Butai[CsvName[1]+'OriTIME']
    Dataframe_Butai.drop(labels=[CsvName[1]+'OriTIME'], axis=1,inplace = True)
    Dataframe_Butai.insert(1, CsvName[1]+'OriTIME', Trans)
    Trans = Dataframe_Butai[CsvName[2]+'OriTIME']
    Dataframe_Butai.drop(labels=[CsvName[2]+'OriTIME'], axis=1,inplace = True)
    Dataframe_Butai.insert(2, CsvName[2]+'OriTIME', Trans)
    Trans = Dataframe_Butai[CsvName[4]+'OriTIME']
    Dataframe_Butai.drop(labels=[CsvName[4]+'OriTIME'], axis=1,inplace = True)
    Dataframe_Butai.insert(3, CsvName[4]+'OriTIME', Trans)
    Dataframe_Butai = Dataframe_Butai.rename(columns={CriName+'TIME':'GaitTIME'})
    
    Dataframe_Butai = Dataframe_Butai.drop([DropName+'TIME',CsvName[2]+'TIME',CsvName[4]+'TIME'],axis=1)
    
    #==========================步态完成========================
    
    C_N = 3
    starttime = time.time()  
    StartTimeRow = 0
    EndTimeRow = 0
    
    isExists = os.path.exists(PathName+CsvName[C_N]+'.csv')
    if not isExists:#impossible
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
        
        StartTime = StartHour[K]+':'+StartMin[K]+':'+StartSec[K]+'.002'
        EndTime = EndHour[K]+':'+EndMin[K]+':'+EndSec[K]+'.002'
        
        column = [row[1] for row in reader]
        
        for j in range(0,len(column)):
            if StartTime in column[j]:
                #print (column[j])
                StartTimeRow = j-1
            if EndTime in column[j]:
                #print (column[j])
                EndTimeRow = j-1
        
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
                               names=['?',CsvName[C_N]+'TIME','FP1','FP2','F3','F4','C3','C4','P3','P4',
                                       'O1','O2','F7','F8','P7','P8',
                                      'Fz','Cz','Pz','FC1','FC2','CP1','CP2',
                                       'FC5','FC6','CP5','CP6'])
                        
        Dataframe_Naodian = Dataframe_Naodian.drop(['?'], axis=1)
        Dataframe_Naodian=Dataframe_Naodian.loc[:,~Dataframe_Naodian.columns.str.contains('^Unnamed')]
        Dataframe_Naodian.to_csv(PathName+CsvName[C_N]+'_new.csv')
        os.remove(PathName+CsvName[C_N]+'_new.csv') 
        ZeroDetc(StartTimeRow,EndTimeRow,CsvName[C_N],TaskName[K])
        elapsed = (time.time() - starttime)
        print(CsvName[C_N]+'已处理完成，用时：'+str(elapsed))
    #-------------------将新保存的csv文件读入dataframe-------------(脑电)

    #==========================脑电完成========================
    C_N = 5
    starttime = time.time()  
    StartTimeRow = 0
    EndTimeRow = 0
    
    isExists = os.path.exists(PathName+CsvName[C_N]+'.csv')
    if not isExists:#impossible
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
        
        StartTime = StartHour[K]+':'+StartMin[K]+':'+StartSec[K]+'.002'
        EndTime = EndHour[K]+':'+EndMin[K]+':'+EndSec[K]+'.002'
        
        column = [row[1] for row in reader]
        
        for j in range(0,len(column)):
            if StartTime in column[j]:
                #print (column[j])
                StartTimeRow = j-1
            if EndTime in column[j]:
                #print (column[j])
                EndTimeRow = j-1
        
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
                               names=['?',CsvName[C_N]+'TIME','EMG1','EMG2','IO','EMG3','EMG4'])
                        
        Dataframe_Jidian = Dataframe_Jidian.drop(['?',CsvName[C_N]+'TIME'], axis=1)
    
        Dataframe_Jidian=Dataframe_Jidian.loc[:,~Dataframe_Jidian.columns.str.contains('^Unnamed')]
        Dataframe_Jidian.to_csv(PathName+CsvName[C_N]+'_new.csv')
        os.remove(PathName+CsvName[C_N]+'_new.csv') 
        ZeroDetc(StartTimeRow,EndTimeRow,CsvName[C_N],TaskName[K])
        
        #==========================肌电完成========================
    
    
    Dataframe = pd.concat([Dataframe_Naodian,Dataframe_Jidian,Dataframe_Butai],axis=1)
    
    Trans = Dataframe['GaitTIME']
    Dataframe.drop(labels=['GaitTIME'], axis=1,inplace = True)
    Dataframe.insert(1, 'GaitTIME', Trans)
    
    Trans = Dataframe[CsvName[0]+'OriTIME']
    Dataframe.drop(labels=[CsvName[0]+'OriTIME'], axis=1,inplace = True)
    Dataframe.insert(2, CsvName[0]+'OriTIME', Trans)
    
    Trans = Dataframe[CsvName[1]+'OriTIME']
    Dataframe.drop(labels=[CsvName[1]+'OriTIME'], axis=1,inplace = True)
    Dataframe.insert(3, CsvName[1]+'OriTIME', Trans)
    
    Trans = Dataframe[CsvName[2]+'OriTIME']
    Dataframe.drop(labels=[CsvName[2]+'OriTIME'], axis=1,inplace = True)
    Dataframe.insert(4, CsvName[2]+'OriTIME', Trans)
    
    Trans = Dataframe[CsvName[4]+'OriTIME']
    Dataframe.drop(labels=[CsvName[4]+'OriTIME'], axis=1,inplace = True)
    Dataframe.insert(5, CsvName[4]+'OriTIME', Trans)

    #Dataframe = Dataframe.fillna(value=0)
    #Dataframe.to_csv(PathName+'task/'+TaskName[K]+'.csv')

    Dataframe = Dataframe.fillna(value=0)
    Dataframe = Dataframe.drop([CsvName[0]+'OriTIME',CsvName[1]+'OriTIME','GaitTIME',
                                CsvName[2]+'OriTIME',CsvName[4]+'OriTIME'],axis=1)
    Dataframe = Dataframe.rename(columns={'EEG_ICATIME':'TIME'})
    
    Dataframe.to_csv(OutputPath+'/'+TaskName[K]+'_data.txt')


    elapsed = (time.time() - taskstarttime)
    print('--------------------------------------')
    print(TaskName[K]+'已处理完成，用时：'+str(elapsed))
    print('======================================')
    
elapsed = (time.time() - StartTime00)
print('======================================')
print('数据裁切已完成，用时：'+str(elapsed))
print('======================================')
print('======================================')

