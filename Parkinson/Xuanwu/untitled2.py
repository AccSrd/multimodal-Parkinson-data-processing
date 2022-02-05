#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May  1 18:08:34 2020

@author: hantao.li
"""

import pandas as pd
import numpy as np
import datetime
import time
import re
import os

######################################################################  

EMGNAME = 'EMG_Ori'
Path_File         = '/Volumes/Work/Parkinson/宣武医院'

Path_Cut          = Path_File + '/4-分段未标注数据'   
Path_Labeled      = Path_File + '/6-标注完成数据_new'


Personnumber = '020'   # xxx or xxx/OFF or xxx/ON       
Tasknumber = 5

CutTime = '''
09:30:07
09:38:46
09:39:48
09:41:06
09:41:43
09:42:50
09:44:36
09:50:50
09:53:17
09:55:57
'''

LabelTime = list(range(Tasknumber))

LabelTime[0] = '''
02:36-02:43
03:23-03:26
04:03-04:19
04:42-04:59
05:02-05:06
05:42-06:13
08:22-08:30
'''

LabelTime[1] = '''
'''

LabelTime[2] = '''
'''

LabelTime[3] = '''
01:00-01:41
01:45-02:13
02:41-02:52
03:17-04:02
05:11-05:34
'''

LabelTime[4] = '''
'''

#LabelTime[5] = '''
#'''

#LabelTime[6] = '''
#'''

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
    Pattern = r' |-|:|\r\n|\n'
    Timelist = list(map(str,re.split(Pattern,Timestr)))  #split the cuttime into h/m/s
    Timelist = [x for x in Timelist if x != '']
    return Timelist[::6],Timelist[1::6],Timelist[2::6],Timelist[3::6],Timelist[4::6],Timelist[5::6]

def SplitLabelTime(Timestr):
    Pattern = r' |-|:|\r\n|\n'
    Timelist = list(map(str,re.split(Pattern,Timestr)))  #split the doctor's label time into m/s 
    Timelist = [int(x) for x in Timelist if x != '']
    return Timelist[::4],Timelist[1::4],Timelist[2::4],Timelist[3::4]

############################################################

EEGName  = ['EEG',EMGNAME]
CsvName  = ['LShank','RShank','Waist','Arm','EEG',EMGNAME]
CriName  = 'LShank'   
DropName = 'RShank'  
  
mkdir(Path_Labeled+'/'+Personnumber)

TaskName = list(range(Tasknumber))
for task in range(0,Tasknumber):
    TaskName[task] = 'task_'+str(task+1)
    
StartHour,StartMin,StartSec,EndHour,EndMin,EndSec = SplitCutTime(CutTime)

Pattern = r' |\n'
Timelist_CutTime = list(map(str,re.split(Pattern,CutTime)))  #split the doctor's label time
Timelist_CutTime = [x for x in Timelist_CutTime if x != ''] 
VedioStartTime = Timelist_CutTime[::2]

############################################################

Task_Time = datetime.datetime.strptime('0:0:0', '%H:%M:%S')
Fog_Time = datetime.datetime.strptime('0:0:0', '%H:%M:%S')



time_start = time.time()
time_point = time.time()


## 6 #######################################################################
time_point = time.time()

for task in range(0,Tasknumber):
    
    DataPath = Path_Cut+'/'+Personnumber+'/task_' + str(task+1) + '_data.txt'
    NewDataPath = Path_Labeled+'/'+Personnumber+'/task_' + str(task+1) + '.txt'        
    
    if LabelTime[task] == '\n':
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