#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 13 16:51:10 2020

@author: hantao.li
"""

import csv
import pandas as pd
import numpy as np
import os
import time
import datetime
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

StartTime00 = time.time() 
CsvName = ['LShank','RShank','Waist','EEG','Arm']
CriName = 'LShank'   #在task_x.csv文件当做GaitTIME的时间戳，默认为左腿，若无左腿文件请更改为右腿 
DropName = 'RShank'  #默认为右腿，若将右腿作为CriName,请更改为左腿

TaskNumber = 1
TaskName = ['task_1']#,'task_2','task_3','task_4','task_5']#,'task_6','task_7']
PathName = '/Volumes/Backup Plus/冻结步态原始数据/宣武医院/012-zhaobingjv/Data/'

mkdir(PathName+'task')
#--------定义任务数量以及名称----------

StartHour = list(range(TaskNumber)); StartMin = list(range(TaskNumber)); StartSec = list(range(TaskNumber));
EndHour = list(range(TaskNumber)); EndMin = list(range(TaskNumber)); EndSec = list(range(TaskNumber));

StartHour[0] = '10'; StartMin[0] = '49'; StartSec[0] = '55'
EndHour[0]   = '11'; EndMin[0]   = '23'; EndSec[0]   = '19'
'''
StartHour[1] = '11'; StartMin[1] = '04'; StartSec[1] = '04'
EndHour[1]   = '11'; EndMin[1]   = '14'; EndSec[1]   = '48'

StartHour[2] = '11'; StartMin[2] = '16'; StartSec[2] = '48'
EndHour[2]   = '11'; EndMin[2]   = '18'; EndSec[2]   = '08'

StartHour[3] = '11'; StartMin[3] = '19'; StartSec[3] = '10'
EndHour[3]   = '11'; EndMin[3]   = '20'; EndSec[3]   = '29'

StartHour[4] = '11'; StartMin[4] = '23'; StartSec[4] = '03'
EndHour[4]   = '11'; EndMin[4]   = '27'; EndSec[4]   = '53'

StartHour[5] = '11'; StartMin[5] = '30'; StartSec[5] = '12'
EndHour[5]   = '11'; EndMin[5]   = '30'; EndSec[5]   = '38'

StartHour[6] = '11'; StartMin[6] = '30'; StartSec[6] = '42'
EndHour[6]   = '11'; EndMin[6]   = '31'; EndSec[6]   = '07'
#---------定义任务起始时间----------

'''
#---------确定数据名称------------


for K in range(0,TaskNumber):
    
    taskstarttime = time.time()  
    
    C_N = 0
    starttime = time.time()  
    StartTimeRow = 0
    EndTimeRow = 0
    
    isExists = os.path.exists(PathName+CsvName[C_N]+'.csv')
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
                                       'O1','O2','F7','F8','EMG1','EMG2','P7','P8',
                                      'Fz','Cz','Pz','IO','FC1','FC2','CP1','CP2',
                                       'FC5','FC6','CP5','CP6','EMG3','EMG4','TP9','TP10'])
                        
        Dataframe_Naodian = Dataframe_Naodian.drop(['?'], axis=1)
        Dataframe_Naodian=Dataframe_Naodian.loc[:,~Dataframe_Naodian.columns.str.contains('^Unnamed')]
        Dataframe_Naodian.to_csv(PathName+CsvName[C_N]+'_new.csv')
        os.remove(PathName+CsvName[C_N]+'_new.csv') 
        ZeroDetc(StartTimeRow,EndTimeRow,CsvName[C_N],TaskName[K])
        elapsed = (time.time() - starttime)
        print(CsvName[C_N]+'已处理完成，用时：'+str(elapsed))
    #-------------------将新保存的csv文件读入dataframe-------------(脑电)

    #==========================脑电完成========================
    
    #断点0-------------------------------------------------------------------
    elapsed = (time.time() - taskstarttime)
    print('--------------------------------------')
    print('断点0用时：'+str(elapsed))    
    
    Dataframe = pd.concat([Dataframe_Naodian,Dataframe_Butai],axis=1)
    
    #断点1-------------------------------------------------------------------
    elapsed = (time.time() - taskstarttime)
    print('--------------------------------------')
    print('断点1用时：'+str(elapsed))    
    
    
    #------------
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
    #-----------
    #断点2-------------------------------------------------------------------
    elapsed = (time.time() - taskstarttime)
    print('--------------------------------------')
    print('断点2用时：'+str(elapsed))    


    #---------
    Dataframe = Dataframe.fillna(value=0)
    Dataframe.to_csv(PathName+'task/'+TaskName[K]+'.csv')
    #----------
    #断点3-------------------------------------------------------------------
    elapsed = (time.time() - taskstarttime)
    print('--------------------------------------')
    print('断点3用时：'+str(elapsed))    


    
    Dataframe = Dataframe.fillna(value=0)
    Dataframe = Dataframe.drop([CsvName[0]+'OriTIME',CsvName[1]+'OriTIME','GaitTIME',
                                CsvName[2]+'OriTIME',CsvName[4]+'OriTIME'],axis=1)
    Dataframe = Dataframe.rename(columns={'EEGTIME':'TIME'})
    #断点4-------------------------------------------------------------------
    elapsed = (time.time() - taskstarttime)
    print('--------------------------------------')
    print('断点4用时：'+str(elapsed))    
    
    
    
    Dataframe.to_csv(PathName+'task/'+TaskName[K]+'_data.csv')
    Dataframe.to_csv(PathName+'task/'+TaskName[K]+'_data.txt')
    #断点5-------------------------------------------------------------------
    elapsed = (time.time() - taskstarttime)
    print('--------------------------------------')
    print('断点5用时：'+str(elapsed))    



    elapsed = (time.time() - taskstarttime)
    print('--------------------------------------')
    print(TaskName[K]+'已处理完成，用时：'+str(elapsed))
    print('======================================')
    
elapsed = (time.time() - StartTime00)
print('======================================')
print('数据裁切已完成，用时：'+str(elapsed))
print('======================================')
print('======================================')

