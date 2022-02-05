#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 28 14:41:14 2020

@author: hantao.li
"""

import pandas as pd
import numpy as np
import scipy.interpolate as spi
import datetime
import time
import re
import os
import csv

######################################################################
Path_File         = '/Users/hantao.li/Desktop/test/ALL'
Path_Raw          = Path_File + '/2-冻结步态原始数据文件、视频'
Path_Preprocessed = Path_File + '/3-预处理后数据文件' 
Path_Cut          = Path_File + '/4-分段未标注数据'   
Path_Labeled      = Path_File + '/6-标注完成数据'
Personnumber = '001'   # xxx or xxx/OFF
Tasknumber = 2

EEGstarttime  = datetime.datetime(2020,1,1,12,20,5,109000)           #Last bit should be odd
Gaitstarttime = datetime.datetime(2020,1,1,12,20,5,000000)           #Last bit should be even

CutTime = '12:20:09 12:20:29 12:20:10 12:20:20'

LabelTime = list(range(Tasknumber))
LabelTime[0] = '00:01-00:02 00:09-00:11'
LabelTime[1] = '00:02-00:03 00:05-00:06'
#empty if none

######################################################################

EEGName = ['EEG','EMG_Ori']
CsvName  = ['LShank','RShank','Waist','Arm','EEG','EMG_Ori']
CriName  = 'LShank'   
DropName = 'RShank'  

TaskName = list(range(Tasknumber))
for task in range(0,Tasknumber):
    TaskName[task] = 'task_'+str(task+1)



def mkdir(path):
    isExists = os.path.exists(path)
    if not isExists:
        os.makedirs(path)
        print(path + '\n--> Folder Created Successfully')
        return True
    else:
        print(path + '\n--> Unsuccessful, Directory Already Exists')
        return False

def ZeroDetc(StartTimeRow,EndTimeRow,filename,taskname):
    if StartTimeRow == 0:
        print ('----------------------------\n'+taskname+' '+filename+' Can not find the Start Row')
    if EndTimeRow == 0:
        print ('----------------------------\n'+taskname+' '+filename+' Can not find the End Row')

def SplitCutTime(Timestr):
    Pattern = r' |-|:'
    Timelist = re.split(Pattern,Timestr)  #split the cut time into h/m/s
    return Timelist[::6],Timelist[1::6],Timelist[2::6],Timelist[3::6],Timelist[4::6],Timelist[5::6]

StartHour,StartMin,StartSec,EndHour,EndMin,EndSec = SplitCutTime(CutTime)

def CutGait(C_N,LastCol):
    StartTimeRow = 0
    EndTimeRow = 0
    
    Col_Name = [CsvName[C_N],CsvName[C_N]+'TIME',CsvName[C_N]+'OriTIME','?',CsvName[C_N]+'ACCX',
    CsvName[C_N]+'ACCY',CsvName[C_N]+'ACCZ',CsvName[C_N]+'GYROX',CsvName[C_N]+'GYROY',
    CsvName[C_N]+'GYROZ',LastCol]
    
    isExists = os.path.exists(Path_Preprocessed+'/'+Personnumber+'/'+CsvName[C_N]+'.csv')     #Check if there have the data file
    StartTime = StartHour[K]+':'+StartMin[K]+':'+StartSec[K]+'.002'
    EndTime = EndHour[K]+':'+EndMin[K]+':'+EndSec[K]+'.002'
    
    if not isExists:
        new_f = open(Path_Preprocessed+'/'+Personnumber+'/'+CsvName[C_N]+'.csv','w')
        writer = csv.writer(new_f)
        writer.writerow(['0']*len(Col_Name))
        new_f.close()
        Dataframe = pd.read_csv(Path_Preprocessed+'/'+Personnumber+'/'+CsvName[C_N]+'.csv',
                                header=None,index_col=False,names=Col_Name)
        Dataframe = Dataframe.drop([CsvName[C_N],'?'], axis=1)
        os.remove(Path_Preprocessed+'/'+Personnumber+'/'+CsvName[C_N]+'.csv') 
        print('There is no ' + CsvName[C_N] + ' for ' + TaskName[K])
        
    else:
        origin_f = open(Path_Preprocessed+'/'+Personnumber+'/'+CsvName[C_N]+'.csv','r')
        reader = csv.reader(origin_f)
        column = [row[1] for row in reader]
        for j in range(0,len(column)):       #Find the start and the end lines of the data
            if StartTime in column[j]:
                StartTimeRow = j-1
            if EndTime in column[j]:
                EndTimeRow = j-1
        origin_f.close()
        
        origin_f = open(Path_Preprocessed+'/'+Personnumber+'/'+CsvName[C_N]+'.csv', 'r')
        new_f = open(Path_Preprocessed+'/'+Personnumber+'/'+CsvName[C_N]+'_new.csv', 'w')
        reader = csv.reader(origin_f)
        writer = csv.writer(new_f)
        
        
        for i,row in enumerate(reader):
            if ((i >= StartTimeRow) and (i <= EndTimeRow)):
               writer.writerow(row)
               
        origin_f.close()
        new_f.close()       
        
        Dataframe = pd.read_csv(Path_Preprocessed+'/'+Personnumber+'/'+CsvName[C_N]+'_new.csv',
                                 header=None,index_col=False,names=Col_Name)
        Dataframe = Dataframe.drop([CsvName[C_N],'?'], axis=1)
        
        #Dataframe.to_csv(Path_Preprocessed+'/'+Personnumber+'/'+CsvName[C_N]+'_new.csv')  #??????
        os.remove(Path_Preprocessed+'/'+Personnumber+'/'+CsvName[C_N]+'_new.csv') 
        ZeroDetc(StartTimeRow,EndTimeRow,CsvName[C_N],TaskName[K])
        
    return Dataframe

def CutEEG(C_N,Col_Name):
    StartTimeRow = 0
    EndTimeRow = 0
    
    isExists = os.path.exists(Path_Preprocessed+'/'+Personnumber+'/'+CsvName[C_N]+'.csv')
    if not isExists:     #norm impossible
        new_f = open(Path_Preprocessed+'/'+Personnumber+'/'+CsvName[C_N]+'.csv', 'w')
        writer = csv.writer(new_f)
        writer.writerow(['0']*len(Col_Name))
        new_f.close()
        Dataframe = pd.read_csv(Path_Preprocessed+'/'+Personnumber+'/'+CsvName[C_N]+'.csv',
                             header=None,index_col=False,names=Col_Name)
        if CsvName[C_N] != 'EEG':
            Dataframe = Dataframe.drop([CsvName[C_N]+'TIME'], axis=1)
        Dataframe = Dataframe.drop(['?'], axis=1)
        os.remove(Path_Preprocessed+'/'+Personnumber+'/'+CsvName[C_N]+'.csv') 
        print('There is no ' + CsvName[C_N] + ' for ' + TaskName[K])
    else:
        origin_f = open(Path_Preprocessed+'/'+Personnumber+'/'+CsvName[C_N]+'.csv','r')
        reader = csv.reader(origin_f)
        
        StartTime = StartHour[K]+':'+StartMin[K]+':'+StartSec[K]+'.002'
        EndTime = EndHour[K]+':'+EndMin[K]+':'+EndSec[K]+'.002'
        
        column = [row[1] for row in reader]
        
        for j in range(0,len(column)):
            if StartTime in column[j]:
                StartTimeRow = j-1
            if EndTime in column[j]:
                EndTimeRow = j-1      
        origin_f.close()
        
        origin_f = open(Path_Preprocessed+'/'+Personnumber+'/'+CsvName[C_N]+'.csv', 'r')
        new_f = open(Path_Preprocessed+'/'+Personnumber+'/'+CsvName[C_N]+'_new.csv', 'w')
        reader = csv.reader(origin_f)
        writer = csv.writer(new_f)
        
        
        for i,row in enumerate(reader):
            if ((i >= StartTimeRow) and (i <= EndTimeRow)):
               writer.writerow(row)
               
        origin_f.close()
        new_f.close()       
        
        Dataframe = pd.read_csv(Path_Preprocessed+'/'+Personnumber+'/'+CsvName[C_N]+'_new.csv',
                                 header=None,index_col=False,names=Col_Name) 
        if CsvName[C_N] != 'EEG':
            Dataframe = Dataframe.drop([CsvName[C_N]+'TIME'], axis=1)
        Dataframe = Dataframe.drop(['?'], axis=1)
        Dataframe = Dataframe.loc[:,~Dataframe.columns.str.contains('^Unnamed')]
        #Dataframe.to_csv(Path_Preprocessed+'/'+Personnumber+'/'+CsvName[C_N]+'_new.csv')
        os.remove(Path_Preprocessed+'/'+Personnumber+'/'+CsvName[C_N]+'_new.csv') 
        ZeroDetc(StartTimeRow,EndTimeRow,CsvName[C_N],TaskName[K])

    return Dataframe


mkdir(Path_Preprocessed+'/'+Personnumber)
mkdir(Path_Cut+'/'+Personnumber)
mkdir(Path_Labeled+'/'+Personnumber)


for K in range(0,Tasknumber):    #For each task
    '''
    C_N = 0    #LShank
    StartTimeRow = 0
    EndTimeRow = 0
    
    isExists = os.path.exists(Path_Preprocessed+'/'+Personnumber+'/'+CsvName[C_N]+'.csv')     #Check if there have the data file
    StartTime = StartHour[K]+':'+StartMin[K]+':'+StartSec[K]+'.002'
    EndTime = EndHour[K]+':'+EndMin[K]+':'+EndSec[K]+'.002'
    
    if not isExists:
        new_f = open(Path_Preprocessed+'/'+Personnumber+'/'+CsvName[C_N]+'.csv','w')
        writer = csv.writer(new_f)
        writer.writerow(['0','0','0','0','0','0','0','0','0'])
        new_f.close()
        Dataframe_Gait_LS = pd.read_csv(Path_Preprocessed+'/'+Personnumber+'/'+CsvName[C_N]+'.csv',
                             header=None,index_col=False,
                            names=[CsvName[C_N]+'TIME', CsvName[C_N]+'OriTIME',
                                   CsvName[C_N]+'ACCX',CsvName[C_N]+'ACCY',
                                   CsvName[C_N]+'ACCZ',CsvName[C_N]+'GYROX',CsvName[C_N]+'GYROY',
                                   CsvName[C_N]+'GYROZ','NC'])
        os.remove(Path_Preprocessed+'/'+Personnumber+'/'+CsvName[C_N]+'.csv') 
        print('There is no ' + CsvName[C_N])
    else:
        origin_f = open(Path_Preprocessed+'/'+Personnumber+'/'+CsvName[C_N]+'.csv','r')
        reader = csv.reader(origin_f)
        column = [row[1] for row in reader]
        for j in range(0,len(column)):       #Find the start and the end lines of the data
            if StartTime in column[j]:
                StartTimeRow = j-1
            if EndTime in column[j]:
                EndTimeRow = j-1
        origin_f.close()
        
        origin_f = open(Path_Preprocessed+'/'+Personnumber+'/'+CsvName[C_N]+'.csv', 'r')
        new_f = open(Path_Preprocessed+'/'+Personnumber+'/'+CsvName[C_N]+'_new.csv', 'w')
        reader = csv.reader(origin_f)
        writer = csv.writer(new_f)
        
        
        for i,row in enumerate(reader):
            if ((i >= StartTimeRow) and (i <= EndTimeRow)):
               writer.writerow(row)
               
        origin_f.close()
        new_f.close()       
        #-------------------将此段数据保存为新csv文件-------------------
        
        Dataframe_Gait_LS = pd.read_csv(Path_Preprocessed+'/'+Personnumber+'/'+CsvName[C_N]+'_new.csv',
                                 header=None,index_col=False,
                                names=[CsvName[C_N],CsvName[C_N]+'TIME',CsvName[C_N]+'OriTIME','?',
                                       CsvName[C_N]+'ACCX',CsvName[C_N]+'ACCY',
                                       CsvName[C_N]+'ACCZ',CsvName[C_N]+'GYROX',CsvName[C_N]+'GYROY',
                                       CsvName[C_N]+'GYROZ','NC'])
        Dataframe_Gait_LS = Dataframe_Gait_LS.drop([CsvName[C_N],'?'], axis=1)
        
        #Dataframe_Gait_LS.to_csv(Path_Preprocessed+'/'+Personnumber+'/'+CsvName[C_N]+'_new.csv')  #??????
        os.remove(Path_Preprocessed+'/'+Personnumber+'/'+CsvName[C_N]+'_new.csv') 
        ZeroDetc(StartTimeRow,EndTimeRow,CsvName[C_N],TaskName[K])

    #-------------------将新保存的csv文件读入dataframe-------------(左腿步态)
    
    #-------------------------------------------------
    #-------------------------------------------------
    #-------------------------------------------------
    
    C_N = 1    #RShank
    StartTimeRow = 0
    EndTimeRow = 0
    
    isExists = os.path.exists(Path_Preprocessed+'/'+Personnumber+'/'+CsvName[C_N]+'.csv')     #Check if there have the data file
    StartTime = StartHour[K]+':'+StartMin[K]+':'+StartSec[K]+'.002'
    EndTime = EndHour[K]+':'+EndMin[K]+':'+EndSec[K]+'.002'
    
    if not isExists:
        new_f = open(Path_Preprocessed+'/'+Personnumber+'/'+CsvName[C_N]+'.csv','w')
        writer = csv.writer(new_f)
        writer.writerow(['0','0','0','0','0','0','0','0','0'])
        new_f.close()
        Dataframe_Gait_RS = pd.read_csv(Path_Preprocessed+'/'+Personnumber+'/'+CsvName[C_N]+'.csv',
                             header=None,index_col=False,
                            names=[CsvName[C_N]+'TIME', CsvName[C_N]+'OriTIME',
                                   CsvName[C_N]+'ACCX',CsvName[C_N]+'ACCY',
                                   CsvName[C_N]+'ACCZ',CsvName[C_N]+'GYROX',CsvName[C_N]+'GYROY',
                                   CsvName[C_N]+'GYROZ','NC'])
        os.remove(Path_Preprocessed+'/'+Personnumber+'/'+CsvName[C_N]+'.csv') 
        print('There is no ' + CsvName[C_N])
    else:
        origin_f = open(Path_Preprocessed+'/'+Personnumber+'/'+CsvName[C_N]+'.csv','r')
        reader = csv.reader(origin_f)
        column = [row[1] for row in reader]
        for j in range(0,len(column)):       #Find the start and the end lines of the data
            if StartTime in column[j]:
                StartTimeRow = j-1
            if EndTime in column[j]:
                EndTimeRow = j-1
        origin_f.close()
        
        origin_f = open(Path_Preprocessed+'/'+Personnumber+'/'+CsvName[C_N]+'.csv', 'r')
        new_f = open(Path_Preprocessed+'/'+Personnumber+'/'+CsvName[C_N]+'_new.csv', 'w')
        reader = csv.reader(origin_f)
        writer = csv.writer(new_f)
        
        
        for i,row in enumerate(reader):
            if ((i >= StartTimeRow) and (i <= EndTimeRow)):
               writer.writerow(row)
               
        origin_f.close()
        new_f.close()       
        #-------------------将此段数据保存为新csv文件-------------------
        
        Dataframe_Gait_RS = pd.read_csv(Path_Preprocessed+'/'+Personnumber+'/'+CsvName[C_N]+'_new.csv',
                                 header=None,index_col=False,
                                names=[CsvName[C_N],CsvName[C_N]+'TIME',CsvName[C_N]+'OriTIME','?',
                                       CsvName[C_N]+'ACCX',CsvName[C_N]+'ACCY',
                                       CsvName[C_N]+'ACCZ',CsvName[C_N]+'GYROX',CsvName[C_N]+'GYROY',
                                       CsvName[C_N]+'GYROZ','NC'])
        Dataframe_Gait_RS = Dataframe_Gait_RS.drop([CsvName[C_N],'?'], axis=1)
        #Dataframe_Gait_RS.to_csv(Path_Preprocessed+'/'+Personnumber+'/'+CsvName[C_N]+'_new.csv')  #??????
        os.remove(Path_Preprocessed+'/'+Personnumber+'/'+CsvName[C_N]+'_new.csv') 
        ZeroDetc(StartTimeRow,EndTimeRow,CsvName[C_N],TaskName[K])
    #-------------------将新保存的csv文件读入dataframe-------------(右腿步态)
    
    #-------------------------------------------------
    #-------------------------------------------------
    #-------------------------------------------------
    
    C_N = 2    #Waist    
    StartTimeRow = 0
    EndTimeRow = 0
    
    isExists = os.path.exists(Path_Preprocessed+'/'+Personnumber+'/'+CsvName[C_N]+'.csv')     #Check if there have the data file
    StartTime = StartHour[K]+':'+StartMin[K]+':'+StartSec[K]+'.002'
    EndTime = EndHour[K]+':'+EndMin[K]+':'+EndSec[K]+'.002'
    
    if not isExists:
        new_f = open(Path_Preprocessed+'/'+Personnumber+'/'+CsvName[C_N]+'.csv','w')
        writer = csv.writer(new_f)
        writer.writerow(['0','0','0','0','0','0','0','0','0'])
        new_f.close()
        Dataframe_Gait_WST = pd.read_csv(Path_Preprocessed+'/'+Personnumber+'/'+CsvName[C_N]+'.csv',
                             header=None,index_col=False,
                            names=[CsvName[C_N]+'TIME', CsvName[C_N]+'OriTIME',
                                   CsvName[C_N]+'ACCX',CsvName[C_N]+'ACCY',
                                   CsvName[C_N]+'ACCZ',CsvName[C_N]+'GYROX',CsvName[C_N]+'GYROY',
                                   CsvName[C_N]+'GYROZ','NC'])
        os.remove(Path_Preprocessed+'/'+Personnumber+'/'+CsvName[C_N]+'.csv') 
        print('There is no ' + CsvName[C_N])
    else:
        origin_f = open(Path_Preprocessed+'/'+Personnumber+'/'+CsvName[C_N]+'.csv','r')
        reader = csv.reader(origin_f)
        column = [row[1] for row in reader]
        for j in range(0,len(column)):       #Find the start and the end lines of the data
            if StartTime in column[j]:
                StartTimeRow = j-1
            if EndTime in column[j]:
                EndTimeRow = j-1
        origin_f.close()
        
        origin_f = open(Path_Preprocessed+'/'+Personnumber+'/'+CsvName[C_N]+'.csv', 'r')
        new_f = open(Path_Preprocessed+'/'+Personnumber+'/'+CsvName[C_N]+'_new.csv', 'w')
        reader = csv.reader(origin_f)
        writer = csv.writer(new_f)
        
        
        for i,row in enumerate(reader):
            if ((i >= StartTimeRow) and (i <= EndTimeRow)):
               writer.writerow(row)
               
        origin_f.close()
        new_f.close()       
        #-------------------将此段数据保存为新csv文件-------------------
        
        Dataframe_Gait_WST = pd.read_csv(Path_Preprocessed+'/'+Personnumber+'/'+CsvName[C_N]+'_new.csv',
                                 header=None,index_col=False,
                                names=[CsvName[C_N],CsvName[C_N]+'TIME',CsvName[C_N]+'OriTIME','?',
                                       CsvName[C_N]+'ACCX',CsvName[C_N]+'ACCY',
                                       CsvName[C_N]+'ACCZ',CsvName[C_N]+'GYROX',CsvName[C_N]+'GYROY',
                                       CsvName[C_N]+'GYROZ','NC'])
        Dataframe_Gait_WST = Dataframe_Gait_WST.drop([CsvName[C_N],'?'], axis=1)
        #Dataframe_Gait_WST.to_csv(Path_Preprocessed+'/'+Personnumber+'/'+CsvName[C_N]+'_new.csv')  #??????
        os.remove(Path_Preprocessed+'/'+Personnumber+'/'+CsvName[C_N]+'_new.csv') 
        ZeroDetc(StartTimeRow,EndTimeRow,CsvName[C_N],TaskName[K])
        #-------------------将新保存的csv文件读入dataframe-------------(腰步态)
    
    C_N = 3 #Arm
    StartTimeRow = 0
    EndTimeRow = 0
    
    isExists = os.path.exists(Path_Preprocessed+'/'+Personnumber+'/'+CsvName[C_N]+'.csv')     #Check if there have the data file
    StartTime = StartHour[K]+':'+StartMin[K]+':'+StartSec[K]+'.002'
    EndTime = EndHour[K]+':'+EndMin[K]+':'+EndSec[K]+'.002'
    
    if not isExists:
        new_f = open(Path_Preprocessed+'/'+Personnumber+'/'+CsvName[C_N]+'.csv','w')
        writer = csv.writer(new_f)
        writer.writerow(['0','0','0','0','0','0','0','0','0'])
        new_f.close()
        Dataframe_Gait_ARM = pd.read_csv(Path_Preprocessed+'/'+Personnumber+'/'+CsvName[C_N]+'.csv',
                             header=None,index_col=False,
                            names=[CsvName[C_N]+'TIME', CsvName[C_N]+'OriTIME',
                                   CsvName[C_N]+'ACCX',CsvName[C_N]+'ACCY',
                                   CsvName[C_N]+'ACCZ',CsvName[C_N]+'GYROX',CsvName[C_N]+'GYROY',
                                   CsvName[C_N]+'GYROZ','NC'])
        os.remove(Path_Preprocessed+'/'+Personnumber+'/'+CsvName[C_N]+'.csv') 
        print('There is no ' + CsvName[C_N])
    else:
        origin_f = open(Path_Preprocessed+'/'+Personnumber+'/'+CsvName[C_N]+'.csv','r')
        reader = csv.reader(origin_f)
        column = [row[1] for row in reader]
        for j in range(0,len(column)):       #Find the start and the end lines of the data
            if StartTime in column[j]:
                StartTimeRow = j-1
            if EndTime in column[j]:
                EndTimeRow = j-1
        origin_f.close()
        
        origin_f = open(Path_Preprocessed+'/'+Personnumber+'/'+CsvName[C_N]+'.csv', 'r')
        new_f = open(Path_Preprocessed+'/'+Personnumber+'/'+CsvName[C_N]+'_new.csv', 'w')
        reader = csv.reader(origin_f)
        writer = csv.writer(new_f)
        
        
        for i,row in enumerate(reader):
            if ((i >= StartTimeRow) and (i <= EndTimeRow)):
               writer.writerow(row)
               
        origin_f.close()
        new_f.close()       
        #-------------------将此段数据保存为新csv文件-------------------
        
        Dataframe_Gait_ARM = pd.read_csv(Path_Preprocessed+'/'+Personnumber+'/'+CsvName[C_N]+'_new.csv',
                                 header=None,index_col=False,
                                names=[CsvName[C_N],CsvName[C_N]+'TIME',CsvName[C_N]+'OriTIME','?',
                                       CsvName[C_N]+'ACCX',CsvName[C_N]+'ACCY',
                                       CsvName[C_N]+'ACCZ',CsvName[C_N]+'GYROX',CsvName[C_N]+'GYROY',
                                       CsvName[C_N]+'GYROZ','NC'])
        Dataframe_Gait_ARM = Dataframe_Gait_ARM.drop([CsvName[C_N],'?'], axis=1)
        #Dataframe_Gait_ARM.to_csv(Path_Preprocessed+'/'+Personnumber+'/'+CsvName[C_N]+'_new.csv')  #??????
        os.remove(Path_Preprocessed+'/'+Personnumber+'/'+CsvName[C_N]+'_new.csv') 
        ZeroDetc(StartTimeRow,EndTimeRow,CsvName[C_N],TaskName[K])
    #-------------------将新保存的csv文件读入dataframe-------------(手臂步态)
    
    '''
    Dataframe_Gait_LS = CutGait(0,'NC')
    Dataframe_Gait_RS = CutGait(1,'NC')
    Dataframe_Gait_WST = CutGait(2,'NC')
    Dataframe_Gait_ARM = CutGait(3,'SC')
    
    Dataframe_Gait = pd.concat([Dataframe_Gait_LS,Dataframe_Gait_RS,Dataframe_Gait_WST,Dataframe_Gait_ARM],axis=1)
    Trans = Dataframe_Gait[CsvName[1]+'OriTIME']
    Dataframe_Gait.drop(labels=[CsvName[1]+'OriTIME'], axis=1,inplace = True)
    Dataframe_Gait.insert(1, CsvName[1]+'OriTIME', Trans)
    Trans = Dataframe_Gait[CsvName[2]+'OriTIME']
    Dataframe_Gait.drop(labels=[CsvName[2]+'OriTIME'], axis=1,inplace = True)
    Dataframe_Gait.insert(2, CsvName[2]+'OriTIME', Trans)
    Trans = Dataframe_Gait[CsvName[3]+'OriTIME']
    Dataframe_Gait.drop(labels=[CsvName[3]+'OriTIME'], axis=1,inplace = True)
    Dataframe_Gait.insert(3, CsvName[3]+'OriTIME', Trans)
    Dataframe_Gait = Dataframe_Gait.rename(columns={CriName+'TIME':'GaitTIME'})
    
    Dataframe_Gait = Dataframe_Gait.drop([DropName+'TIME',CsvName[2]+'TIME',CsvName[3]+'TIME'],axis=1)
    
    #==========================步态完成========================
    Col_Name_EEG = ['?',CsvName[4]+'TIME','FP1','FP2','F3','F4','C3','C4','P3','P4','O1','O2',
                'F7','F8','P7','P8','Fz','Cz','Pz','FC1','FC2','CP1','CP2','FC5','FC6','CP5','CP6']
    Dataframe_EEG = CutEEG(4,Col_Name_EEG)
    
    Col_Name_EMG = ['?',CsvName[5]+'TIME','EMG1','EMG2','IO','EMG3','EMG4']
    Dataframe_EMG = CutEEG(5,Col_Name_EMG)
    
    '''
    C_N = 4     #EEG
    StartTimeRow = 0
    EndTimeRow = 0
    
    Col_Name = ['?',CsvName[C_N]+'TIME','FP1','FP2','F3','F4','C3','C4','P3','P4','O1','O2',
                'F7','F8','P7','P8','Fz','Cz','Pz','FC1','FC2','CP1','CP2','FC5','FC6','CP5','CP6']
    
    isExists = os.path.exists(Path_Preprocessed+'/'+Personnumber+'/'+CsvName[C_N]+'.csv')
    if not isExists:#impossible
        new_f = open(Path_Preprocessed+'/'+Personnumber+'/'+CsvName[C_N]+'.csv', 'w')
        writer = csv.writer(new_f)
        writer.writerow(['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0',
                         '0','0','0','0','0','0','0'])
        new_f.close()
        Dataframe_EEG = pd.read_csv(Path_Preprocessed+'/'+Personnumber+'/'+CsvName[C_N]+'.csv',
                             header=None,index_col=False,names=Col_Name)
        os.remove(Path_Preprocessed+'/'+Personnumber+'/'+CsvName[C_N]+'.csv') 
    else:
        origin_f = open(Path_Preprocessed+'/'+Personnumber+'/'+CsvName[C_N]+'.csv','r')
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
        
        origin_f = open(Path_Preprocessed+'/'+Personnumber+'/'+CsvName[C_N]+'.csv', 'r')
        new_f = open(Path_Preprocessed+'/'+Personnumber+'/'+CsvName[C_N]+'_new.csv', 'w')
        reader = csv.reader(origin_f)
        writer = csv.writer(new_f)
        
        
        for i,row in enumerate(reader):
            if ((i >= StartTimeRow) and (i <= EndTimeRow)):
               writer.writerow(row)
               
        origin_f.close()
        new_f.close()       
        #-------------------将此段数据保存为新csv文件-------------------
        
        Dataframe_EEG = pd.read_csv(Path_Preprocessed+'/'+Personnumber+'/'+CsvName[C_N]+'_new.csv',
                                 header=None,index_col=False,names=Col_Name)        
        Dataframe_EEG = Dataframe_EEG.drop(['?'], axis=1)
        Dataframe_EEG = Dataframe_EEG.loc[:,~Dataframe_EEG.columns.str.contains('^Unnamed')]
        #Dataframe_EEG.to_csv(Path_Preprocessed+'/'+Personnumber+'/'+CsvName[C_N]+'_new.csv')
        os.remove(Path_Preprocessed+'/'+Personnumber+'/'+CsvName[C_N]+'_new.csv') 
        ZeroDetc(StartTimeRow,EndTimeRow,CsvName[C_N],TaskName[K])
    #-------------------将新保存的csv文件读入dataframe-------------(脑电)

    #==========================脑电完成========================

    C_N = 5     #EMG
    StartTimeRow = 0
    EndTimeRow = 0
    
    Col_Name = ['?',CsvName[C_N]+'TIME','EMG1','EMG2','IO','EMG3','EMG4']
    
    isExists = os.path.exists(Path_Preprocessed+'/'+Personnumber+'/'+CsvName[C_N]+'.csv')
    if not isExists:#impossible
        new_f = open(Path_Preprocessed+'/'+Personnumber+'/'+CsvName[C_N]+'.csv', 'w')
        writer = csv.writer(new_f)
        writer.writerow(['0','0','0','0','0','0','0'])
        new_f.close()
        Dataframe_EMG = pd.read_csv(Path_Preprocessed+'/'+CsvName[C_N]+'.csv',
                             header=None,index_col=False,names=Col_Name)
        os.remove(Path_Preprocessed+'/'+Personnumber+'/'+CsvName[C_N]+'.csv') 
    else:
        origin_f = open(Path_Preprocessed+'/'+Personnumber+'/'+CsvName[C_N]+'.csv','r')
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
        
        origin_f = open(Path_Preprocessed+'/'+Personnumber+'/'+CsvName[C_N]+'.csv', 'r')
        new_f = open(Path_Preprocessed+'/'+Personnumber+'/'+CsvName[C_N]+'_new.csv', 'w')
        reader = csv.reader(origin_f)
        writer = csv.writer(new_f)
        
        
        for i,row in enumerate(reader):
            if ((i >= StartTimeRow) and (i <= EndTimeRow)):
               writer.writerow(row)
               
        origin_f.close()
        new_f.close()       
        #-------------------将此段数据保存为新csv文件-------------------
        
        Dataframe_EMG = pd.read_csv(Path_Preprocessed+'/'+Personnumber+'/'+CsvName[C_N]+'_new.csv',
                                 header=None,index_col=False,names=Col_Name)
                        
        Dataframe_EMG = Dataframe_EMG.drop(['?'], axis=1)
        Dataframe_EMG = Dataframe_EMG.loc[:,~Dataframe_EMG.columns.str.contains('^Unnamed')]
        #Dataframe_EMG.to_csv(Path_Preprocessed+'/'+Personnumber+'/'+CsvName[C_N]+'_new.csv')
        os.remove(Path_Preprocessed+'/'+Personnumber+'/'+CsvName[C_N]+'_new.csv') 
        ZeroDetc(StartTimeRow,EndTimeRow,CsvName[C_N],TaskName[K])
        
        #==========================肌电完成========================
    '''
    
    Dataframe = pd.concat([Dataframe_EEG,Dataframe_EMG,Dataframe_Gait],axis=1)
    
    
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
    
    Trans = Dataframe[CsvName[3]+'OriTIME']
    Dataframe.drop(labels=[CsvName[3]+'OriTIME'], axis=1,inplace = True)
    Dataframe.insert(5, CsvName[3]+'OriTIME', Trans)

    Dataframe = Dataframe.fillna(value=0)
    Dataframe.to_csv(Path_Cut+'/'+Personnumber+'/'+TaskName[K]+'.csv')
    

    Dataframe = Dataframe.fillna(value=0)
    Dataframe = Dataframe.drop([CsvName[0]+'OriTIME',CsvName[1]+'OriTIME','GaitTIME',
                                CsvName[2]+'OriTIME',CsvName[3]+'OriTIME'],axis=1)
    Dataframe = Dataframe.rename(columns={'EEGTIME':'TIME'})
    
    Dataframe.to_csv(Path_Cut+'/'+Personnumber+'/'+TaskName[K]+'_data.txt')




