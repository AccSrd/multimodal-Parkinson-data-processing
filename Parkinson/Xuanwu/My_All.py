#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May  1 18:08:34 2020

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

TPYE = 1 #1-宣武数据库；2-毕设       

EMGNAME = 'EMG_Ori'
Path_File         = '/Volumes/Work/Parkinson/宣武医院'

if TPYE == 2:
    EMGNAME = 'EMG_10H'
    Path_File     = '/Volumes/Work/毕设/database'

Path_Raw          = Path_File + '/2-冻结步态原始数据文件、视频'
Path_Preprocessed = Path_File + '/3-预处理后数据文件' 
Path_Cut          = Path_File + '/4-分段未标注数据'   
Path_Labeled      = Path_File + '/6-标注完成数据'


Personnumber = '008'   # xxx or xxx/OFF or xxx/ON       
Tasknumber = 5

EEGstarttime  = datetime.datetime(2020,1,1,9,4,4,159000)           #Last bit should be odd
Gaitstarttime = datetime.datetime(2020,1,1,8,49,20,000000)           #Last bit should be even

CutTime = '09:05:12 09:09:16 09:09:49 09:13:11 09:14:00 09:14:21 09:14:43 09:15:05 09:15:16 09:15:35'

LabelTime = list(range(Tasknumber))
LabelTime[0] = ''


LabelTime[1] = ''


LabelTime[2] = ''


LabelTime[3] = ''


LabelTime[4] = ''


#LabelTime[5] = ''


#LabelTime[6] = ''
#empty if none


######################################################################

def mkdir(path):
    isExists = os.path.exists(path)
    if not isExists:
        os.makedirs(path)
        print(path + '\n--> Successful, Folder has been Created\n')
        return True
    else:
        print(path + '\n--> Unsuccessful, Directory Already Exists\n')
        return False

def ZeroDetc(StartTimeRow,EndTimeRow,filename,taskname):
    if StartTimeRow == 0:
        print ('----------------------------\n'+taskname+' '+filename+' Can not find the Start Row')
    if EndTimeRow == 0:
        print ('----------------------------\n'+taskname+' '+filename+' Can not find the End Row')

def SplitCutTime(Timestr):
    Pattern = r' |-|:'
    Timelist = re.split(Pattern,Timestr)  #split the cuttime into h/m/s
    return Timelist[::6],Timelist[1::6],Timelist[2::6],Timelist[3::6],Timelist[4::6],Timelist[5::6]

def SplitLabelTime(Timestr):
    Pattern = r' |-|:'
    Timelist = list(map(int,re.split(Pattern,Timestr)))  #split the doctor's label time into m/s 
    return Timelist[::4],Timelist[1::4],Timelist[2::4],Timelist[3::4]

############################################################

EEGName  = ['EEG',EMGNAME]
CsvName  = ['LShank','RShank','Waist','Arm','EEG',EMGNAME]
CriName  = 'LShank'   
DropName = 'RShank'  
  
mkdir(Path_Preprocessed+'/'+Personnumber)
mkdir(Path_Cut+'/'+Personnumber)
mkdir(Path_Labeled+'/'+Personnumber)

TaskName = list(range(Tasknumber))
for task in range(0,Tasknumber):
    TaskName[task] = 'task_'+str(task+1)
    
StartHour,StartMin,StartSec,EndHour,EndMin,EndSec = SplitCutTime(CutTime)

Pattern = r' '
Timelist_CutTime = list(map(str,re.split(Pattern,CutTime)))  #split the doctor's label time 
VedioStartTime = Timelist_CutTime[::2]

############################################################

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
        print('----------------------------')
        print('There is no [' + CsvName[C_N] + '.csv] for ' + TaskName[K])
        
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
        print('----------------------------')
        print('There is no [' + CsvName[C_N] + '].csv for ' + TaskName[K])
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

Task_Time = datetime.datetime.strptime('0:0:0', '%H:%M:%S')
Fog_Time = datetime.datetime.strptime('0:0:0', '%H:%M:%S')



time_start = time.time()
time_point = time.time()

## 3 #######################################################################

for C_N in range(0,4):
    isExists = os.path.exists(Path_Raw+'/'+Personnumber+'/'+CsvName[C_N]+'0.csv')
    if isExists:
        if CsvName[C_N] == 'Arm':
            names = [CsvName[C_N]+'TIME', CsvName[C_N]+'ACCX',CsvName[C_N]+'ACCY',
                   CsvName[C_N]+'ACCZ',CsvName[C_N]+'GYROX',CsvName[C_N]+'GYROY',
                    CsvName[C_N]+'GYROZ','SC']
            data1= pd.read_csv(Path_Raw+'/'+Personnumber+'/'+CsvName[C_N]+'0.csv',header=None,index_col=False,
                                    names=names)
        else:
            names = [CsvName[C_N]+'TIME', CsvName[C_N]+'ACCX',CsvName[C_N]+'ACCY',
                   CsvName[C_N]+'ACCZ',CsvName[C_N]+'GYROX',CsvName[C_N]+'GYROY',
                    CsvName[C_N]+'GYROZ','NC']
            data1= pd.read_csv(Path_Raw+'/'+Personnumber+'/'+CsvName[C_N]+'0.csv',header=None,index_col=False,
                                    names=names)

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
        Dataframe_Gait.to_csv(Path_Preprocessed+'/'+Personnumber+'/'+CsvName[C_N]+'.csv')
        
for E_N in range(0,len(EEGName)):        
        
    data = pd.read_table(Path_Preprocessed+'/'+Personnumber+'/'+EEGName[E_N]+'.txt',sep=',')
    Column_Rawtime = np.array(data['Time'].values).tolist()
    Column_Time = list(range(len(Column_Rawtime)))

    for i in range(0,len(Column_Time)):
        deltatime = datetime.timedelta(microseconds=i*1000)
        strtime = str(EEGstarttime + deltatime)[11:23]
        Column_Time[i] = strtime
    
    DataFrame_Time = pd.DataFrame({'TIME':Column_Time})
    data = pd.concat([DataFrame_Time,data],axis=1)
    data = data.drop(['Time'], axis=1)
    
    data.to_csv(Path_Preprocessed+'/'+Personnumber+'/'+EEGName[E_N]+'_1000.csv')
    
    origin_f = open(Path_Preprocessed+'/'+Personnumber+'/'+EEGName[E_N]+'_1000.csv','r')
    new_f = open(Path_Preprocessed+'/'+Personnumber+'/'+EEGName[E_N] +'.csv','w')
    reader = csv.reader(origin_f)
    writer = csv.writer(new_f)
    
    for i,row in enumerate(reader):
        if (i-2)%2 == 0:
           writer.writerow(row)
           
    origin_f.close()
    new_f.close()
    os.remove(Path_Preprocessed+'/'+Personnumber+'/'+EEGName[E_N]+'_1000.csv') 

time_end = time.time()
print('============================')
print('数据预处理完成，用时为 %fs' % (time_end - time_start))
print('单段用时为 %fs' % (time_end - time_point))
print('============================\n')
##################################################################################################
time_point = time.time()

for K in range(0,Tasknumber):    #For each task
    
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
    
    if EMGNAME == 'EMG_Ori':    
        Col_Name_EMG = ['?',CsvName[5]+'TIME','EMG1','EMG2','IO','EMG3','EMG4']
    elif EMGNAME == 'EMG_10H':
        Col_Name_EMG = ['?',CsvName[5]+'TIME','EMG1','EMG2','EMG3']
    Dataframe_EMG = CutEEG(5,Col_Name_EMG)

    Dataframe = pd.concat([Dataframe_EEG,Dataframe_EMG,Dataframe_Gait],axis=1)
    
    #Output a .csv file with all timestamps when you need to check the data
    '''
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
    '''

    Dataframe = Dataframe.fillna(value=0)
    Dataframe = Dataframe.drop([CsvName[0]+'OriTIME',CsvName[1]+'OriTIME','GaitTIME',
                                CsvName[2]+'OriTIME',CsvName[3]+'OriTIME'],axis=1)
    Dataframe = Dataframe.rename(columns={(EEGName[0]+'TIME'):'TIME'})
    
    Dataframe.to_csv(Path_Cut+'/'+Personnumber+'/'+TaskName[K]+'_data.txt')
    print('----------------------------')
    print(TaskName[K] + ' 裁切完成')

time_end = time.time()
print('============================')
print('数据裁切完成，总用时为 %fs' % (time_end - time_start))
print('单段用时为 %fs' % (time_end - time_point))
print('============================\n')
##################################################################################################

## 6 #######################################################################
time_point = time.time()

for task in range(0,Tasknumber):
    
    DataPath = Path_Cut+'/'+Personnumber+'/task_' + str(task+1) + '_data.txt'
    NewDataPath = Path_Labeled+'/'+Personnumber+'/task_' + str(task+1) + '.txt'        
    
    if LabelTime[task] == '':
        data = pd.read_csv(DataPath,index_col=0)               
        Ytime = np.array(data['TIME'].values).tolist()
        Label = [0 for x in range(0,len(Ytime))]
    
    else:
        Fstartmin,Fstartsec,Fendmin,Fendsec = SplitLabelTime(LabelTime[task])
        
        data = pd.read_csv(DataPath,index_col=0)               #import the task data
        Ytime = np.array(data['TIME'].values).tolist()
        Label = [0 for x in range(0,len(Ytime))]
        
        VedioStartTime[task] = datetime.datetime.strptime(VedioStartTime[task], '%H:%M:%S')
        
        for Fnum in range(0,len(Fstartmin)):
            Fstarttime = str(VedioStartTime[task] + datetime.timedelta(minutes=int(Fstartmin[Fnum]),seconds=Fstartsec[Fnum]))
            Fstarttime = Fstarttime[11:19]+'.002'
            Fendtime = str(VedioStartTime[task] + datetime.timedelta(minutes=Fendmin[Fnum],seconds=(Fendsec[Fnum])))
            Fendtime = Fendtime[11:19]+'.998'
            
            StarttimeRow = EndtimeRow = 0
            
            for TimeDetect in range(0,len(Label)):             #Find the location of '1' lebal
                if Fstarttime in Ytime[TimeDetect]:
                    StarttimeRow = TimeDetect-1
                if Fendtime in Ytime[TimeDetect]:
                    EndtimeRow = TimeDetect
                    
            if (StarttimeRow == 0) or (EndtimeRow == 0) or ((EndtimeRow-StarttimeRow) <= 0) :   
                print ('Troubled when labeling the number ' + str(Fnum+1) + ' doctor\'s label')
                
            for Labelloc in range(0,len(Label)):               # label the lata
                if ((Labelloc >= StarttimeRow) and (Labelloc <= EndtimeRow)):
                    Label[Labelloc]=1
            
        for K in range(0,len(Fstartmin)):
            startTime = datetime.datetime.strptime('0:'+str(Fstartmin[K])+':'+str(Fstartsec[K]),'%H:%M:%S')
            endTime = datetime.datetime.strptime('0:'+str(Fendmin[K])+':'+str(Fendsec[K]),'%H:%M:%S')+datetime.timedelta(seconds=1)
            delta = endTime - startTime
            Fog_Time = Fog_Time + delta
        
    Ch_Label = pd.DataFrame({'Label':Label})
    data = pd.concat([data,Ch_Label],axis=1)
    data.to_csv(NewDataPath,header = None)
    #data.to_csv(Path_Labeled+'/'+Personnumber+'/task_' + str(task+1) + '.csv')

time_end = time.time()
print('============================')
print('数据标注完成，总用时为 %fs' % (time_end - time_start))
print('单段用时为 %fs' % (time_end - time_point))
print('============================\n')
##################################################################################################

for K in range(0,len(StartHour)):
    startTime = datetime.datetime.strptime(str(StartHour[K])+':'+str(StartMin[K])+':'+str(StartSec[K]),'%H:%M:%S')
    endTime = datetime.datetime.strptime(str(EndHour[K])+':'+str(EndMin[K])+':'+str(EndSec[K]),'%H:%M:%S')
    delta = endTime - startTime
    Task_Time = Task_Time + delta
print('Time of Task: '+ str(Task_Time)[14:19])
print('Time of FoG: '+ str(Fog_Time)[14:19])