#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 28 15:10:18 2020

@author: Hantao.Li

Function : label the data of XuanWu Hospital

*******************Input**************************************
InputPath --> The folder which contains the data file
Tasknumber --> The number of task to be labeled 
VedioStartTime --> Time corresponding to the first frame of the task video file, format-->hh:mm:ss
LabelTime --> The time period given by doctor, format-->00:25-00:28 00:45-00:55.......
If there is no FoG in the task, set the LabelTime as ''

*******************Output*************************************
(Inputpath)/label/task_(Tasknmber).txt
format-->[data,label]
"""

import pandas as pd
import numpy as np
import datetime
import re
import os

######################################################################
        
InputPath = '/Volumes/Work/Parkinson/宣武医院/4-分段未标注数据'   
OutputPath = '/Volumes/Work/Parkinson/宣武医院/6-标注完成数据'
Personnumber = '020 E'   # xxx or xxx/OFF
Tasknumber = 5
VedioStartTime = '09:53:17'
LabelTime = '01:25-01:49'

#empty if none

######################################################################

def mkdir(path):
    isExists = os.path.exists(path)
    if not isExists:
        os.makedirs(path)
        print(path + ' --> Folder Created Successfully')
        return True
    else:
        print(path + ' --> Unsuccessful, Directory Already Exists')
        return False


DataPath = InputPath+'/'+Personnumber+'/task_' + str(Tasknumber) + '_data.txt'
NewDataPath = OutputPath+'/'+Personnumber+'/task_' + str(Tasknumber) + '.txt'      
mkdir(OutputPath+'/'+Personnumber)

if LabelTime == '':
    data = pd.read_csv(DataPath,index_col=0)               
    Ytime = np.array(data['TIME'].values).tolist()
    Label = [0 for x in range(0,len(Ytime))]

else:
    Pattern = r' |-|:'
    Timelist = list(map(int,re.split(Pattern,LabelTime)))  #split the doctor's label time 
    Fstartmin = Timelist[::4]
    Fstartsec = Timelist[1::4]
    Fendmin   = Timelist[2::4]
    Fendsec   = Timelist[3::4]
    
    data = pd.read_csv(DataPath,index_col=0)               #import the task data
    Ytime = np.array(data['TIME'].values).tolist()
    Label = [0 for x in range(0,len(Ytime))]
    
    VedioStartTime = datetime.datetime.strptime(VedioStartTime, '%H:%M:%S')
    
    for Fnum in range(0,int(len(Timelist)/4)):
        Fstarttime = str(VedioStartTime + datetime.timedelta(minutes=int(Fstartmin[Fnum]),seconds=Fstartsec[Fnum]))
        Fstarttime = Fstarttime[11:19]+'.002'
        Fendtime = str(VedioStartTime + datetime.timedelta(minutes=Fendmin[Fnum],seconds=(Fendsec[Fnum])))
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
        
Ch_Label = pd.DataFrame({'Label':Label})
data = pd.concat([data,Ch_Label],axis=1)

data.to_csv(NewDataPath)
    