#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 28 15:52:05 2020

@author: hantao.li

对未标注数据标注三种标签,对于重合标签，优先级为3>4>2>1>0
0 - 无
1 - 正常行走
2 - 冻结步态前5s
3 - 冻结步态
4 - 条带线索行走
"""

import pandas as pd
import numpy as np
import datetime
import time
import re
import os

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
    
def SplitLabelTime(Timestr):
    Pattern = r' |-|:|\r|\n'
    Timelist = list(map(str,re.split(Pattern,Timestr)))  #split the doctor's label time into m/s 
    Timelist = [int(x) for x in Timelist if x != '']
    Timelist = [int(x) for x in Timelist if x != '\n']
    return Timelist[::4],Timelist[1::4],Timelist[2::4],Timelist[3::4] 

def SplitCutTime(Timestr):
    Pattern = r' |-|:|\n'
    Timelist = re.split(Pattern,Timestr)  #split the cuttime into h/m/s
    Timelist = [int(x) for x in Timelist if x != '']
    Timelist = [int(x) for x in Timelist if x != '\n']
    return Timelist[::6],Timelist[1::6],Timelist[2::6],Timelist[3::6],Timelist[4::6],Timelist[5::6]
    

# 需要手动更改 ##################################
Path_File         = '/Volumes/Backup Plus'
Path_Cut          = Path_File + '/4-分段未标注数据'   
Path_Labeled      = Path_File + '/8-三段标注完成数据(冻结前2s)'

subject = 8       #选取患者
CutTime = '''
12:13:46
12:19:59
12:21:03
12:27:18
12:27:48
12:29:00
12:29:24
12:30:05
'''
###############################################

#                 0     1     2       3       4       5         6         7  
Path_subject = ['003','005','006','007/OFF','008','009/OFF','010/OFF','015/OFF_1',
#                   8         9    10    11
                '015/OFF_2','016','017','019']   # xxx or xxx/OFF or xxx/ON    
Path_task = [4,4,5,5,4,4,4,5,4,6,5,5]
Personnumber = Path_subject[subject]
Tasknumber = Path_task[subject]

LabelTime_NormalWalk = list(range(Tasknumber))
LabelTime_BeforeFOG = list(range(Tasknumber))
LabelTime_FOG = list(range(Tasknumber))
LabelTime_Strip = list(range(Tasknumber))

Pattern = r' |\n'
Timelist_CutTime = list(map(str,re.split(Pattern,CutTime)))  #split the doctor's label time 
Timelist_CutTime = [x for x in Timelist_CutTime if x != '']
Timelist_CutTime = [x for x in Timelist_CutTime if x != '\n']
VedioStartTime = Timelist_CutTime[::2]

Task_Time = datetime.datetime.strptime('0:0:0', '%H:%M:%S')
NormalWalk_Time = datetime.datetime.strptime('0:0:0', '%H:%M:%S')
BeforeFog_Time = datetime.datetime.strptime('0:0:0', '%H:%M:%S')
Fog_Time = datetime.datetime.strptime('0:0:0', '%H:%M:%S')
Strip_Time = datetime.datetime.strptime('0:0:0', '%H:%M:%S')

# TASK1 ########################################
LabelTime_NormalWalk[0] = '''
00:03-00:08
00:41-00:46
00:51-01:03
02:02-02:06
04:16-04:22
05:13-05:20
05:41-05:49
05:55-06:01
'''

LabelTime_BeforeFOG[0] = '''
00:30-00:32
01:04-01:07
02:08-02:10
02:20-02:22
03:17-03:19
04:24-04:26
04:52-04:54
05:22-05:24
'''

LabelTime_FOG[0] = '''
00:11-00:22
00:32-00:37
01:07-01:58
02:10-02:13
02:22-03:07
03:19-03:21
03:25-03:55
03:59-04:12
04:26-04:31
04:54-05:09
05:24-05:36
'''

LabelTime_Strip[0] = '''
04:12-04:16
04:37-04:43
'''

# TASK2 ########################################
LabelTime_NormalWalk[1] = '''
00:03-00:07
00:37-00:42
00:53-00:59
01:42-02:08
03:43-03:49
04:46-04:51
05:13-05:23
05:49-06:02
'''

LabelTime_BeforeFOG[1] = '''
00:20-00:22
01:01-01:03
02:25-02:27
03:51-03:53
04:53-04:55
05:25-05:27
'''

LabelTime_FOG[1] = '''
00:11-00:13
00:22-00:33
01:03-01:08
01:12-01:38
02:27-03:24
03:28-03:37
03:53-04:26
04:55-05:09
05:27-05:45
'''

LabelTime_Strip[1] = '''
03:37-03:43
04:41-04:46
'''

# TASK3 ########################################
LabelTime_NormalWalk[2] = '''
'''

LabelTime_BeforeFOG[2] = '''
'''

LabelTime_FOG[2] = '''
00:05-00:41
00:47-00:53
'''

LabelTime_Strip[2] = '''
'''

# TASK4 ########################################
LabelTime_NormalWalk[3] = '''
'''

LabelTime_BeforeFOG[3] = '''
00:23-00:25
'''

LabelTime_FOG[3] = '''
00:04-00:20
00:25-00:27
'''

LabelTime_Strip[3] = '''
'''

'''
# TASK5 ########################################
LabelTime_NormalWalk[4] = '''
'''

LabelTime_BeforeFOG[4] = '''
'''

LabelTime_FOG[4] = '''
'''

LabelTime_Strip[4] = '''
'''


# TASK6 ########################################
LabelTime_NormalWalk[5] = '''
'''

LabelTime_BeforeFOG[5] = '''
'''

LabelTime_FOG[5] = '''
'''

LabelTime_Strip[5] = '''
'''
'''

#empty if none

## Label #######################################################################
time_point = time.time()
mkdir(Path_Labeled+'/'+Personnumber)
StartHour,StartMin,StartSec,EndHour,EndMin,EndSec = SplitCutTime(CutTime)
errorcode = 0;

for task in range(0,Tasknumber):
    
    DataPath = Path_Cut+'/'+Personnumber+'/task_' + str(task+1) + '_data.txt'
    NewDataPath = Path_Labeled+'/'+Personnumber+'/task_' + str(task+1) + '.txt'        
    
    VedioStartTime[task] = datetime.datetime.strptime(VedioStartTime[task], '%H:%M:%S')
    
    if LabelTime_NormalWalk[task] == '\n':                     #如果正常行走为空，建立全0Label
        data = pd.read_csv(DataPath,index_col=0)               
        Ytime = np.array(data['TIME'].values).tolist()
        Label = [0 for x in range(0,len(Ytime))]
    
    else:                     #正常行走不为空，建立1Label+0底色
        Fstartmin,Fstartsec,Fendmin,Fendsec = SplitLabelTime(LabelTime_NormalWalk[task])

        data = pd.read_csv(DataPath,index_col=0)               #import the task data
        Ytime = np.array(data['TIME'].values).tolist()
        Label = [0 for x in range(0,len(Ytime))]
        
        
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
                print ('Troubled when labeling the number ' + str(Fnum+1) + ' doctor\'s label in normal walk')
                errorcode = 1
                
            for Labelloc in range(0,len(Label)):               # label the lata
                if ((Labelloc >= StarttimeRow) and (Labelloc <= EndtimeRow)):
                    Label[Labelloc] = 1
            
        for K in range(0,len(Fstartmin)):
            startTime = datetime.datetime.strptime('0:'+str(Fstartmin[K])+':'+str(Fstartsec[K]),'%H:%M:%S')
            endTime = datetime.datetime.strptime('0:'+str(Fendmin[K])+':'+str(Fendsec[K]),'%H:%M:%S')+datetime.timedelta(seconds=1)
            delta = endTime - startTime
            NormalWalk_Time = NormalWalk_Time + delta
            
####################################################        
    if LabelTime_BeforeFOG[task] != '\n':                     #如果前5s不为空,建立2Label
    
        Fstartmin,Fstartsec,Fendmin,Fendsec = SplitLabelTime(LabelTime_BeforeFOG[task])
        
        for Fnum in range(0,len(Fstartmin)):
            Fstarttime = str(VedioStartTime[task] + datetime.timedelta(minutes=int(Fstartmin[Fnum]),seconds=Fstartsec[Fnum]))
            Fstarttime = Fstarttime[11:19]+'.002'
            Fendtime = str(VedioStartTime[task] + datetime.timedelta(minutes=Fendmin[Fnum],seconds=(Fendsec[Fnum])))
            Fendtime = Fendtime[11:19]+'.998'
            
            StarttimeRow = EndtimeRow = 0
            
            for TimeDetect in range(0,len(Label)):             #Find the location of '2' lebal
                if Fstarttime in Ytime[TimeDetect]:
                    StarttimeRow = TimeDetect-1
                if Fendtime in Ytime[TimeDetect]:
                    EndtimeRow = TimeDetect
                    
            if (StarttimeRow == 0) or (EndtimeRow == 0) or ((EndtimeRow-StarttimeRow) <= 0) :   
                print ('Troubled when labeling the number ' + str(Fnum+1) + ' doctor\'s label in before fog')
                errorcode = 1
                
            for Labelloc in range(0,len(Label)):               # label the lata
                if ((Labelloc >= StarttimeRow) and (Labelloc <= EndtimeRow)):
                    Label[Labelloc] = 2
            
        for K in range(0,len(Fstartmin)):
            startTime = datetime.datetime.strptime('0:'+str(Fstartmin[K])+':'+str(Fstartsec[K]),'%H:%M:%S')
            endTime = datetime.datetime.strptime('0:'+str(Fendmin[K])+':'+str(Fendsec[K]),'%H:%M:%S')
            delta = endTime - startTime
            BeforeFog_Time = BeforeFog_Time + delta
            
####################################################        
    if LabelTime_Strip[task] != '\n':                     #如果条带线索不为空,建立4Label
    
        Fstartmin,Fstartsec,Fendmin,Fendsec = SplitLabelTime(LabelTime_Strip[task])
        
        for Fnum in range(0,len(Fstartmin)):
            Fstarttime = str(VedioStartTime[task] + datetime.timedelta(minutes=int(Fstartmin[Fnum]),seconds=Fstartsec[Fnum]))
            Fstarttime = Fstarttime[11:19]+'.002'
            Fendtime = str(VedioStartTime[task] + datetime.timedelta(minutes=Fendmin[Fnum],seconds=(Fendsec[Fnum])))
            Fendtime = Fendtime[11:19]+'.998'
            
            StarttimeRow = EndtimeRow = 0
            
            for TimeDetect in range(0,len(Label)):             #Find the location of '2' lebal
                if Fstarttime in Ytime[TimeDetect]:
                    StarttimeRow = TimeDetect-1
                if Fendtime in Ytime[TimeDetect]:
                    EndtimeRow = TimeDetect
                    
            if (StarttimeRow == 0) or (EndtimeRow == 0) or ((EndtimeRow-StarttimeRow) <= 0) :   
                print ('Troubled when labeling the number ' + str(Fnum+1) + ' doctor\'s label in before fog')
                errorcode = 1
                
            for Labelloc in range(0,len(Label)):               # label the lata
                if ((Labelloc >= StarttimeRow) and (Labelloc <= EndtimeRow)):
                    Label[Labelloc] = 4
            
        for K in range(0,len(Fstartmin)):
            startTime = datetime.datetime.strptime('0:'+str(Fstartmin[K])+':'+str(Fstartsec[K]),'%H:%M:%S')
            endTime = datetime.datetime.strptime('0:'+str(Fendmin[K])+':'+str(Fendsec[K]),'%H:%M:%S')
            delta = endTime - startTime
            Strip_Time = Strip_Time + delta
            
####################################################
    if LabelTime_FOG[task] != '\n':                     #如果冻结不为空,建立3Label
    
        Fstartmin,Fstartsec,Fendmin,Fendsec = SplitLabelTime(LabelTime_FOG[task])
        
        for Fnum in range(0,len(Fstartmin)):
            Fstarttime = str(VedioStartTime[task] + datetime.timedelta(minutes=int(Fstartmin[Fnum]),seconds=Fstartsec[Fnum]))
            Fstarttime = Fstarttime[11:19]+'.002'
            Fendtime = str(VedioStartTime[task] + datetime.timedelta(minutes=Fendmin[Fnum],seconds=(Fendsec[Fnum])))
            Fendtime = Fendtime[11:19]+'.998'
            
            StarttimeRow = EndtimeRow = 0
            
            for TimeDetect in range(0,len(Label)):             #Find the location of '2' lebal
                if Fstarttime in Ytime[TimeDetect]:
                    StarttimeRow = TimeDetect-1
                if Fendtime in Ytime[TimeDetect]:
                    EndtimeRow = TimeDetect
                    
            if (StarttimeRow == 0) or (EndtimeRow == 0) or ((EndtimeRow-StarttimeRow) <= 0) :   
                print ('Troubled when labeling the number ' + str(Fnum+1) + ' doctor\'s label in before fog')
                errorcode = 1
                
            for Labelloc in range(0,len(Label)):               # label the lata
                if ((Labelloc >= StarttimeRow) and (Labelloc <= EndtimeRow)):
                    Label[Labelloc] = 3
            
        for K in range(0,len(Fstartmin)):
            startTime = datetime.datetime.strptime('0:'+str(Fstartmin[K])+':'+str(Fstartsec[K]),'%H:%M:%S')
            endTime = datetime.datetime.strptime('0:'+str(Fendmin[K])+':'+str(Fendsec[K]),'%H:%M:%S')+datetime.timedelta(seconds=1)
            delta = endTime - startTime
            Fog_Time = Fog_Time + delta
            
        
    Ch_Label = pd.DataFrame({'Label':Label})
    data = pd.concat([data,Ch_Label],axis=1)
    data.to_csv(NewDataPath,header = None)

time_end = time.time()
print('============================')
print('数据标注完成，总用时为 %fs' % (time_end - time_point))
print('============================\n')
##################################################################################################

for K in range(0,len(StartHour)):
    startTime = datetime.datetime.strptime(str(StartHour[K])+':'+str(StartMin[K])+':'+str(StartSec[K]),'%H:%M:%S')
    endTime = datetime.datetime.strptime(str(EndHour[K])+':'+str(EndMin[K])+':'+str(EndSec[K]),'%H:%M:%S')
    delta = endTime - startTime
    Task_Time = Task_Time + delta

if errorcode == 0:
    print('Time of Task: '+ str(Task_Time)[14:19])
    print('Time of FoG: '+ str(Fog_Time)[14:19])
    print('Time of BeforeFoG: '+ str(BeforeFog_Time)[14:19])
    print('Time of Normal Walk: '+ str(NormalWalk_Time)[14:19])
    print('Time of Walk on strips: '+ str(Strip_Time)[14:19])
else:
    print('Some problems have happend, please check it!')
