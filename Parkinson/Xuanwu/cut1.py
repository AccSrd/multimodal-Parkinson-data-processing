#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  8 22:39:57 2019

@author: hantao.li
"""

import csv
import pandas as pd
import os

TaskNumber = 5
TaskName = ['task_1','task_2_1','task_2_2','task_3','task_4']
PathName = '/Users/hantao.li/Documents/Dongjie/002数据/'
#--------定义任务数量以及名称----------

StartHour = list(range(TaskNumber)); StartMin = list(range(TaskNumber)); StartSec = list(range(TaskNumber));
EndHour = list(range(TaskNumber)); EndMin = list(range(TaskNumber)); EndSec = list(range(TaskNumber));

StartHour[0] = '15'; StartMin[0] = '13'; StartSec[0] = '55'
EndHour[0] = '15'; EndMin[0] = '17'; EndSec[0] = '32'

StartHour[1] = '15'; StartMin[1] = '20'; StartSec[1] = '01'
EndHour[1] = '15'; EndMin[1] = '22'; EndSec[1] = '34'

StartHour[2] = '15'; StartMin[2] = '22'; StartSec[2] = '33'
EndHour[2] = '15'; EndMin[2] = '24'; EndSec[2] = '51'

StartHour[3] = '15'; StartMin[3] = '25'; StartSec[3] = '28'
EndHour[3] = '15'; EndMin[3] = '26'; EndSec[3] = '11'

StartHour[4] = '15'; StartMin[4] = '26'; StartSec[4] = '29'
EndHour[4] = '15'; EndMin[4] = '27'; EndSec[4] = '10'
#---------定义任务起始时间----------

CsvName = ['GAIT_L','GAIT_R','GAIT_U','EEG','EMG','Fscan']
#---------确定数据名称------------


for K in range(0,TaskNumber):
    
    StartTimeRow = 0
    EndTimeRow = 0
    
    C_N = 0
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
                            names=[CsvName[C_N]+'TIME', CsvName[C_N]+'1',CsvName[C_N]+'2',CsvName[C_N]+'3',
                                   CsvName[C_N]+'4',CsvName[C_N]+'5',CsvName[C_N]+'6',CsvName[C_N]+'7'])
    Dataframe_Butai_1.to_csv(PathName+CsvName[C_N]+'_new.csv')
    os.remove(PathName+CsvName[C_N]+'_new.csv') 
    #-------------------将新保存的csv文件读入dataframe-------------(步态1)
    
    #-------------------------------------------------
    #-------------------------------------------------
    #-------------------------------------------------
    
    C_N = 1
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
                            names=[CsvName[C_N]+'TIME', CsvName[C_N]+'1',CsvName[C_N]+'2',CsvName[C_N]+'3',
                                   CsvName[C_N]+'4',CsvName[C_N]+'5',CsvName[C_N]+'6',CsvName[C_N]+'7'])
    Dataframe_Butai_2.to_csv(PathName+CsvName[C_N]+'_new.csv')
    os.remove(PathName+CsvName[C_N]+'_new.csv') 
    #-------------------将新保存的csv文件读入dataframe-------------(步态2)
    
    #-------------------------------------------------
    #-------------------------------------------------
    #-------------------------------------------------
    
    C_N = 2
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
                            names=[CsvName[C_N]+'TIME', CsvName[C_N]+'1',CsvName[C_N]+'2',CsvName[C_N]+'3',
                                   CsvName[C_N]+'4',CsvName[C_N]+'5',CsvName[C_N]+'6',CsvName[C_N]+'7'])
    Dataframe_Butai_3.to_csv(PathName+CsvName[C_N]+'_new.csv')
    os.remove(PathName+CsvName[C_N]+'_new.csv') 
    #-------------------将新保存的csv文件读入dataframe-------------(步态3)
        
    Dataframe_Butai = pd.concat([Dataframe_Butai_1,Dataframe_Butai_2,Dataframe_Butai_3],axis=1)
    Trans = Dataframe_Butai[CsvName[1]+'TIME']
    Dataframe_Butai.drop(labels=[CsvName[1]+'TIME'], axis=1,inplace = True)
    Dataframe_Butai.insert(1, CsvName[1]+'TIME', Trans)
    Trans = Dataframe_Butai[CsvName[2]+'TIME']
    Dataframe_Butai.drop(labels=[CsvName[2]+'TIME'], axis=1,inplace = True)
    Dataframe_Butai.insert(2, CsvName[2]+'TIME', Trans)
    
    #==========================步态完成========================
    
    C_N = 3
    StartTimeRow = 0
    EndTimeRow = 0
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
                            names=[CsvName[C_N]+'1',CsvName[C_N]+'2',CsvName[C_N]+'3',
                                   CsvName[C_N]+'4',CsvName[C_N]+'5',CsvName[C_N]+'6',CsvName[C_N]+'7',
                                   CsvName[C_N]+'8',CsvName[C_N]+'9',CsvName[C_N]+'TIME'])
    Dataframe_Naodian.to_csv(PathName+CsvName[C_N]+'_new.csv')
    os.remove(PathName+CsvName[C_N]+'_new.csv') 
    #-------------------将新保存的csv文件读入dataframe-------------(脑电)

    #==========================脑电完成========================
    
    C_N = 4
    
#    origin_f = open(PathName+CsvName[C_N]+'_250.csv', 'r')
#    new_f = open(PathName+CsvName[C_N]+'.csv', 'w')
#    reader = csv.reader(origin_f)
#    writer = csv.writer(new_f)
#    for i,row in enumerate(reader):
#        if ((i)%10 == 0 or (i-2)%10 == 0 or (i-5)%10 == 0 or (i-7)%10 == 0):        #数据第0、2、5、7、10、12....行
#           writer.writerow(row)
#    origin_f.close()
#    new_f.close()
    #----------------------250HZ-100HZ------------------------
    
    StartTimeRow = 0
    EndTimeRow = 0
    
    origin_f = open(PathName+CsvName[C_N]+'.csv', 'r')
    reader = csv.reader(origin_f)
    
    StartTime = StartHour[K]+':'+StartMin[K]+':'+StartSec[K]+'.00'
    EndTime = EndHour[K]+':'+EndMin[K]+':'+EndSec[K]+'.00'
    
    column = [row[9] for row in reader]
    
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
    
    Dataframe_Jidian = pd.read_csv(PathName+CsvName[C_N]+'_new.csv',
                             header=None,index_col=False,
                            names=[CsvName[C_N]+'1',CsvName[C_N]+'2',CsvName[C_N]+'3',
                                   CsvName[C_N]+'4',CsvName[C_N]+'5',CsvName[C_N]+'6',CsvName[C_N]+'7',
                                   CsvName[C_N]+'8',CsvName[C_N]+'原始TIME',CsvName[C_N]+'TIME'])
    Dataframe_Jidian.to_csv(PathName+CsvName[C_N]+'_new.csv')
    os.remove(PathName+CsvName[C_N]+'_new.csv') 
    #-------------------将新保存的csv文件读入dataframe-------------(肌电)
    
    #==========================肌电完成========================
    
    C_N = 5
    
    StartTimeRow = 0
    EndTimeRow = 0
    
    origin_f = open(PathName+CsvName[C_N]+'.csv', 'r')
    reader = csv.reader(origin_f)

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
                            names=[CsvName[C_N]+'_L',CsvName[C_N]+'_R',CsvName[C_N]+'TIME'])
    Dataframe_Zudi.to_csv(PathName+CsvName[C_N]+'_new.csv')
    os.remove(PathName+CsvName[C_N]+'_new.csv') 
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
    
    for k in range(0,6):
        if k != 3:
            del Dataframe[CsvName[k]+'TIME']
    del Dataframe[CsvName[4]+'原始TIME']
    
    Dataframe = Dataframe.rename(columns={CsvName[3]+'TIME':'TIME'})
    
    Dataframe.to_csv(PathName+'task/'+TaskName[K]+'_data.csv')
    

