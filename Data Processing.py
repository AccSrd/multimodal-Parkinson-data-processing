#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Version.1: Created on Fri May 1, 2020
@author: hantao.li

Version.2: Creat annotation for paper to be published.
Jan 25, 2021, @author: hantao.li

************************************************************************************************
********************       Input Parameters      ***********************************************
************************************************************************************************

Path_File       --> The folder which contains the data file.
(String)            Example: '/Volumes/Work/Parkinson/Xuanwu'
                    
Personnumber    --> The ID of patient data to be processed. If the subject has multi-time experiments, check the name of sub-folders.
(String)            Example: '001' or '007/OFF' or '008/OFF_1', it may be different, thus check it plz.

*Tasknumber     --> The number of tasks to be labeled.
(Integer)           Example: 2

*EEGstarttime/
Gaitstarttime   --> The beginning time-point of the original EEG file and Gait file,
(Datetime)          which indicated in the .vhdr file (MOVE system) or calculated by the recording table (ACC and SC)
                    Example: datetime.datetime(2020,1,1,9,4,4,159000)
                                                                ↑
                    Tips: the last bit in microsecond-level(↑) should be odd in EEGstarttime, should be even in Gaitstarttime

CutTime         --> The beginning and ending time-point in real-world time of each task in the whole data.
(String)            The CutTime is based on video clips. Task_i's cuttime also indicates the time-point of video clips.
                    Example:'''12:04:38
                            12:10:39
                            12:12:33
                            12:18:05'''
                    In this example, it shows that task_1 begins at world time '12:04:38', and ends at '12:10:39', the task_2 begins at world time '12:12:33', and ends at '12:18:05'. It also means that the video of task_1, given to the doctor to label, has the time-point of starting and ending with '12:04:38' and '12:10:39', the length of viedo will 6 min 1 sec.
                    Tips: It should be double the size of Tasknumber.

LabelTime[i]    --> The beginning and ending time-point in the video's time of each task. It is not the real-world time-point.
(String)            Example: LabelTime[0] =  '''00:04:00:21
                                                00:33-00:41'''
                    In this example, it shows that task_1 has 2 FOG epsoids, and FOG occurs when the time-stamp of video are '0:04-0:21' and '0:33-0:41'. The real-world time of it should add the VedioStartTime(12:04:38 in above example)
                    Tips: It should contains i from 0 to Tasknumber-1.
                          If there is no FoG in the task, set the LabelTime empty.

************************************************************************************************
********************         Input Files         ***********************************************
************************************************************************************************

./Path_Raw/Personnumber/ --> The original ACC/SC data file(csv) renamed as LShank0/RShank0/Arm0/Waist0.csv
Data Format: [original time-stamp，data*7], 100Hz

./Path_Preprocessed/Personnumber/ --> The data file output by EEGLAB(txt) renamed as EEG.txt and EMG.txt
Data Format: [TIME,data*25(EEG)/data*5(EMG)],1000Hz

************************************************************************************************
********************         Output Files        ***********************************************
************************************************************************************************

./Path_Preprocessed/Personnumber/ -->
(1) EEG.txt / EMG.txt
Data Format: [NaN,TIME,data*25(EEG)/data*5(EMG)], 500Hz
(2) LShank.csv / RShank.csv / Arm.csv / Waist.csv
Data Format(Arm.csv as exp.): [NaN,TIME,OriTIME,ArmTIME,ArmACCX,ArmACCY,ArmACCZ,ArmGYROX,ArmGYROY,ArmGYROZ,SC(NC in others)], 500Hz

./Path_Cut/Personnumber/          --> task_1_data.txt / task_2_data.txt / ...
Data Format: [NaN,TIME,FP1,FP2,F3,F4,C3,C4,P3,P4,O1,O2,F7,F8,Fz,Cz,Pz,FC1,FC2,CP1,CP2,FC5,FC6,CP5,CP6,EMG1,EMG2,IO,EMG3,EMG4,
              LShankACCX,LShankACCY,LShankACCZ,LShankGYROX,LShankGYROY,LShankGYROZ,NC,RShankACCX,RShankACCY,RShankACCZ,RShankGYROX,
              RShankGYROY,RShankGYROZ,NC,WaistACCX,WaistACCY,WaistACCZ,WaistGYROX,WaistGYROY,WaistGYROZ,NC,ArmACCX,ArmACCY,ArmACCZ,
              ArmGYROX,ArmGYROY,ArmGYROZ,SC]

./Path_Labeled/Personnumber/      --> task_1.txt / task_2.txt / ...
Data Format: [...(Same as above),Label]


Task_Time   --> The length of the whole data of single patient.
FoG_Time    --> The length of the FOG duration in the whole data of single patient.

************************************************************************************************
"""


import pandas as pd
import numpy as np
import scipy.interpolate as spi
import datetime
import time
import re
import os
import csv

"""
************************************************************************************************
************      You need to check these parameters every time you operate      ***************
************************************************************************************************
"""

#The folder which contains the data file.
Path_File     = ''

# xxx or xxx/OFF or xxx/ON
Personnumber  = ''

# The number of task to be labeled
Tasknumber    =

#The beginning time-point of the original EEG file and Gait file
EEGstarttime  = datetime.datetime(2020,1,1,9,4,4,159000)           #Last bit should be odd
Gaitstarttime = datetime.datetime(2020,1,1,8,49,20,000000)         #Last bit should be even

CutTime       = '''
'''

LabelTime     = list(range(Tasknumber))
LabelTime[0]  = '''
'''

LabelTime[1]  = '''
'''

LabelTime[2]  = '''
'''

LabelTime[3]  = '''
'''

LabelTime[4]  = '''
'''

"""
LabelTime[5]  = '''
'''

LabelTime[6]  = '''
'''

"""
#leave the LabelTime array empty if there is no FOG appeared the task

"""
************************************************************************************************
********************           Other Parameters          ***************************************
************************************************************************************************
"""

#According to the EMG.txt filename named by EEGLAB, it does not need to be changed in general
EMGNAME = 'EMG'

#The sub-folder that stores the data files obtained in each step. It can be renamed according to your own needs
Path_Raw          = Path_File + '/1-Raw Data'
Path_Preprocessed = Path_File + '/2-Preprocessed Data'
Path_Cut          = Path_File + '/3-Segmented Data'
Path_Labeled      = Path_File + '/4-Labeled Data'

#According to the Data type (or location of sensor), it does not need to be changed in general
EEGName  = ['EEG',EMGNAME]
CsvName  = ['LShank','RShank','Waist','Arm','EEG',EMGNAME]

#Generally, the time-stamp of the left leg is retained in the gait's Dataframe, and the time stamp of the right leg, arm, and waist are deleted.
#Nevertheless, sometimes the left leg is not recorded. At this time, you need to change CriName and DropName manually.
CriName  = 'LShank'
DropName = 'RShank'


#Other parameters set or calculated in advance
Task_Time = datetime.datetime.strptime('0:0:0', '%H:%M:%S')
Fog_Time = datetime.datetime.strptime('0:0:0', '%H:%M:%S')

mkdir(Path_Preprocessed+'/'+Personnumber)
mkdir(Path_Cut+'/'+Personnumber)
mkdir(Path_Labeled+'/'+Personnumber)

TaskName = list(range(Tasknumber))
for task in range(0,Tasknumber):
    TaskName[task] = 'task_'+str(task+1)

StartHour,StartMin,StartSec,EndHour,EndMin,EndSec = SplitCutTime(CutTime)

#Calculate the start time of each video, that is, the start time of each task
Pattern = r' '
Timelist_CutTime = list(map(str,re.split(Pattern,CutTime)))
VedioStartTime = Timelist_CutTime[::2]

"""
************************************************************************************************
***************************           Functions          ***************************************
************************************************************************************************
"""

#Creat the folder with path
def mkdir(path):
    isExists = os.path.exists(path)
    if not isExists:
        os.makedirs(path)
        print(path + '\n--> Successful, Folder has been Created\n')
        return True
    else:
        print(path + '\n--> Unsuccessful, Directory Already Exists\n')
        return False

#If the trigger line still be 0 after the cutting, it means the error.
def ZeroDetc(StartTimeRow,EndTimeRow,filename,taskname):
    if StartTimeRow == 0:
        print ('----------------------------\n'+taskname+' '+filename+' Can not find the Start Row')
    if EndTimeRow == 0:
        print ('----------------------------\n'+taskname+' '+filename+' Can not find the End Row')

#Split the doctor's label time into m/s
def SplitLabelTime(Timestr):
    Pattern = r' |-|:|\r|\n'
    Timelist = list(map(str,re.split(Pattern,Timestr)))
    Timelist = [int(x) for x in Timelist if x != '']
    Timelist = [int(x) for x in Timelist if x != '\n']
    return Timelist[::4],Timelist[1::4],Timelist[2::4],Timelist[3::4]

#Split the cuttime into h/m/s
def SplitCutTime(Timestr):
    Pattern = r' |-|:|\n'
    Timelist = re.split(Pattern,Timestr)
    Timelist = [int(x) for x in Timelist if x != '']
    Timelist = [int(x) for x in Timelist if x != '\n']
    return Timelist[::6],Timelist[1::6],Timelist[2::6],Timelist[3::6],Timelist[4::6],Timelist[5::6]
  
#Cut the ACC/SC data file
def CutGait(C_N,LastCol):
    StartTimeRow = 0
    EndTimeRow = 0
    
    Col_Name = [CsvName[C_N],CsvName[C_N]+'TIME',CsvName[C_N]+'OriTIME','?',CsvName[C_N]+'ACCX',
    CsvName[C_N]+'ACCY',CsvName[C_N]+'ACCZ',CsvName[C_N]+'GYROX',CsvName[C_N]+'GYROY',
    CsvName[C_N]+'GYROZ',LastCol]
    
    #Check if there have the data file
    isExists = os.path.exists(Path_Preprocessed+'/'+Personnumber+'/'+CsvName[C_N]+'.csv')
    StartTime = StartHour[K]+':'+StartMin[K]+':'+StartSec[K]+'.002'
    EndTime = EndHour[K]+':'+EndMin[K]+':'+EndSec[K]+'.002'
    
    #For nonexistent files, write 0 in the corresponding position
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
        
        #Find the start and the end lines of the data
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
        
        #Select the part between StartTimeRow and EndTimeRow and save it to the corresponding dataframe
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

#Cut the EEG/EMG data file
def CutEEG(C_N,Col_Name):
    StartTimeRow = 0
    EndTimeRow = 0
    
    isExists = os.path.exists(Path_Preprocessed+'/'+Personnumber+'/'+CsvName[C_N]+'.csv')
    #impossible in general
    if not isExists:
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
        
    #Same method as the ACC/SC cutting
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




"""
************************************************************************************************
***********************          Raw --> Preprocessed        ***********************************
************************************************************************************************
Sort out the original data header, and unify the data sampling frequency to 500Hz

Input File      -->
(1) The original ACC/SC data file(csv) renamed as LShank0/RShank0/Arm0/Waist0.csv
Data Format: [original time-stamp，data*7], 100Hz
(2) The data file output by EEGLAB(txt) renamed as EEG.txt and EMG.txt
Data Format: [TIME,data*25(EEG)/data*5(EMG)], 1000Hz

Output File     -->
(1) EEG.txt / EMG.txt
Data Format: [NaN,TIME,data*25(EEG)/data*5(EMG)], 500Hz
(2) LShank.csv / RShank.csv / Arm.csv / Waist.csv
Data Format(Arm.csv as exp.): [NaN,TIME,OriTIME,ArmTIME,ArmACCX,ArmACCY,ArmACCZ,ArmGYROX,ArmGYROY,ArmGYROZ,SC(NC in others)], 500Hz
"""

time_start = time.time()
time_point = time.time()

for C_N in range(0,4):
    #Check whether it exists. If it exists, perform the following operations (add header, interpolate to 500Hz)
    isExists = os.path.exists(Path_Raw+'/'+Personnumber+'/'+CsvName[C_N]+'0.csv')  
    if isExists:
        #The last column of the Arm.csv is SC, not NC
        if CsvName[C_N] == 'Arm':
            names = [CsvName[C_N]+'TIME', CsvName[C_N]+'ACCX',CsvName[C_N]+'ACCY',
                   CsvName[C_N]+'ACCZ',CsvName[C_N]+'GYROX',CsvName[C_N]+'GYROY',
                    CsvName[C_N]+'GYROZ','SC']
            data1= pd.read_csv(Path_Raw+'/'+Personnumber+'/'+CsvName[C_N]+'0.csv',header=None,index_col=False,
                                    names=names)
        #Add headers
        else:
            names = [CsvName[C_N]+'TIME', CsvName[C_N]+'ACCX',CsvName[C_N]+'ACCY',
                   CsvName[C_N]+'ACCZ',CsvName[C_N]+'GYROX',CsvName[C_N]+'GYROY',
                    CsvName[C_N]+'GYROZ','NC']
            data1= pd.read_csv(Path_Raw+'/'+Personnumber+'/'+CsvName[C_N]+'0.csv',header=None,index_col=False,
                                    names=names)

        X=data1.index 
        OriTimeArray = (np.array(data1[CsvName[C_N]+'TIME'].values)).tolist()
        Ori_TimeStamp = list(range(int(5*len(OriTimeArray))))
        
        #Assign OriTime to [original timestamp i; 0.002; 0.004; 0.006; 0.008; original timestamp i+1],
        #to make it correspond to the interpolated data.
        i_time = 0
        for i in range(0,len(Ori_TimeStamp)):
            if i%5==0:
                Ori_TimeStamp[i] = OriTimeArray[i_time]
                i_time = i_time+1
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
               
        #Make third-order spline difference
        for j1 in range(0,len(names)):
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
        
        #Assign the gait time (the correct time after alignment) in the data record table to the timestamp
        for i in range(0,len(List_New_TimeStamp)):
            deltatime = datetime.timedelta(microseconds=i*2000)
            List_New_TimeStamp[i] = str(Gaitstarttime + deltatime)[11:23]
        
        #The interpolated Dataframes are pieced together and then output
        New_TimeStamp = {'TIME':List_New_TimeStamp}
        DataFrame_TimeStamp = pd.DataFrame(New_TimeStamp)
        Dataframe_Gait = pd.concat([DataFrame_TimeStamp,Dataframe_Gait],axis=1)
        Dataframe_Gait.to_csv(Path_Preprocessed+'/'+Personnumber+'/'+CsvName[C_N]+'.csv')
        
for E_N in range(0,len(EEGName)):

    #Read the EEG signal TXT file output by EEGLAB
    data = pd.read_table(Path_Preprocessed+'/'+Personnumber+'/'+EEGName[E_N]+'.txt',sep=',')
    Column_Rawtime = np.array(data['Time'].values).tolist()
    Column_Time = list(range(len(Column_Rawtime)))

    #The time of the EEG .vmrk file (the correct time after alignment) is assigned to the timestamp
    for i in range(0,len(Column_Time)):
        deltatime = datetime.timedelta(microseconds=i*1000)
        strtime = str(EEGstarttime + deltatime)[11:23]
        Column_Time[i] = strtime
    
    DataFrame_Time = pd.DataFrame({'TIME':Column_Time})
    data = pd.concat([DataFrame_Time,data],axis=1)
    data = data.drop(['Time'], axis=1)
    
    #Save the EEG file with correct time stamp as a temporary file, which is 1000Hz
    data.to_csv(Path_Preprocessed+'/'+Personnumber+'/'+EEGName[E_N]+'_1000.csv')
    
    origin_f = open(Path_Preprocessed+'/'+Personnumber+'/'+EEGName[E_N]+'_1000.csv','r')
    new_f = open(Path_Preprocessed+'/'+Personnumber+'/'+EEGName[E_N] +'.csv','w')
    reader = csv.reader(origin_f)
    writer = csv.writer(new_f)
    
    #Save the 1000Hz file in this interlaced way to get the 500Hz file after frequency reduction
    for i,row in enumerate(reader):
        if (i-2)%2 == 0:
           writer.writerow(row)
           
    origin_f.close()
    new_f.close()
    os.remove(Path_Preprocessed+'/'+Personnumber+'/'+EEGName[E_N]+'_1000.csv')

time_end = time.time()
print('============================')
print('Data preprocessing finished，the total time using is %fs' % (time_end - time_start))
print('The time using for single section is %fs' % (time_end - time_point))
print('============================\n')

"""
************************************************************************************************
***********************     Preprocessed --> Segmented       ***********************************
************************************************************************************************
Divided the data into a single piece of data for each task. Put multimodal data together.

Input File      -->
(1) EEG.txt / EMG.txt
Data Format: [NaN,TIME,data*25(EEG)/data*5(EMG)], 500Hz
(2) LShank.csv / RShank.csv / Arm.csv / Waist.csv
Data Format(Arm.csv as exp.): [NaN,TIME,OriTIME,ArmTIME,ArmACCX,ArmACCY,ArmACCZ,ArmGYROX,ArmGYROY,ArmGYROZ,SC(NC in others)], 500Hz

Output File     -->
task_1_data.txt / task_2_data.txt / ...
Data Format: [NaN,TIME,FP1,FP2,F3,F4,C3,C4,P3,P4,O1,O2,F7,F8,Fz,Cz,Pz,FC1,FC2,CP1,CP2,FC5,FC6,CP5,CP6,EMG1,EMG2,IO,EMG3,EMG4,
              LShankACCX,LShankACCY,LShankACCZ,LShankGYROX,LShankGYROY,LShankGYROZ,NC,RShankACCX,RShankACCY,RShankACCZ,RShankGYROX,
              RShankGYROY,RShankGYROZ,NC,WaistACCX,WaistACCY,WaistACCZ,WaistGYROX,WaistGYROY,WaistGYROZ,NC,ArmACCX,ArmACCY,ArmACCZ,
              ArmGYROX,ArmGYROY,ArmGYROZ,SC], 500Hz
"""

time_point = time.time()

#For each task
for K in range(0,Tasknumber):
    
    #The gait files are cut separately and stored in a dataframe
    Dataframe_Gait_LS = CutGait(0,'NC')
    Dataframe_Gait_RS = CutGait(1,'NC')
    Dataframe_Gait_WST = CutGait(2,'NC')
    Dataframe_Gait_ARM = CutGait(3,'SC')
    Dataframe_Gait = pd.concat([Dataframe_Gait_LS,Dataframe_Gait_RS,Dataframe_Gait_WST,Dataframe_Gait_ARM],axis=1)
    
    #Delete the time stamp of the right leg, wrist and waist, leaving only the time stamp of the left leg's file.
    #If the left leg data was not collected, pay attention to change the DropName and CriName!
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
    
    #The EEG file is cut and stored in a dataframe
    Col_Name_EEG = ['?',CsvName[4]+'TIME','FP1','FP2','F3','F4','C3','C4','P3','P4','O1','O2',
                'F7','F8','P7','P8','Fz','Cz','Pz','FC1','FC2','CP1','CP2','FC5','FC6','CP5','CP6']
    Dataframe_EEG = CutEEG(4,Col_Name_EEG)
    
    #The EMG file is cut and stored in a dataframe
    Col_Name_EMG = ['?',CsvName[5]+'TIME','EMG1','EMG2','IO','EMG3','EMG4']
    Dataframe_EMG = CutEEG(5,Col_Name_EMG)
    
    #Put multimodal data together.
    Dataframe = pd.concat([Dataframe_EEG,Dataframe_EMG,Dataframe_Gait],axis=1)
    
    """
    #Output a csv file with all timestamps when you need to check the data

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
    """

    Dataframe = Dataframe.fillna(value=0)
    Dataframe = Dataframe.drop([CsvName[0]+'OriTIME',CsvName[1]+'OriTIME','GaitTIME',
                                CsvName[2]+'OriTIME',CsvName[3]+'OriTIME'],axis=1)
    Dataframe = Dataframe.rename(columns={(EEGName[0]+'TIME'):'TIME'})
    
    Dataframe.to_csv(Path_Cut+'/'+Personnumber+'/'+TaskName[K]+'_data.txt')
    print('----------------------------')
    print(TaskName[K] + ' Segmented Finished')

time_end = time.time()
print('============================')
print('Data segmented finished，the total time using is %fs' % (time_end - time_start))
print('The time using for single section is %fs' % (time_end - time_point))
print('============================\n')

"""
************************************************************************************************
***********************        Segmented --> Labeled         ***********************************
************************************************************************************************
Label the Data with 1(FOG) and 0(FOG-Free.)

Input File      -->
task_1_data.txt / task_2_data.txt / ...
Data Format: [NaN,TIME,FP1,FP2,F3,F4,C3,C4,P3,P4,O1,O2,F7,F8,Fz,Cz,Pz,FC1,FC2,CP1,CP2,FC5,FC6,CP5,CP6,EMG1,EMG2,IO,EMG3,EMG4,
              LShankACCX,LShankACCY,LShankACCZ,LShankGYROX,LShankGYROY,LShankGYROZ,NC,RShankACCX,RShankACCY,RShankACCZ,RShankGYROX,
              RShankGYROY,RShankGYROZ,NC,WaistACCX,WaistACCY,WaistACCZ,WaistGYROX,WaistGYROY,WaistGYROZ,NC,ArmACCX,ArmACCY,ArmACCZ,
              ArmGYROX,ArmGYROY,ArmGYROZ,SC], 500Hz

Output File     -->
task_1.txt / task_2.txt / ...
Data Format: [NaN,TIME,FP1,FP2,F3,F4,C3,C4,P3,P4,O1,O2,F7,F8,Fz,Cz,Pz,FC1,FC2,CP1,CP2,FC5,FC6,CP5,CP6,EMG1,EMG2,IO,EMG3,EMG4,
              LShankACCX,LShankACCY,LShankACCZ,LShankGYROX,LShankGYROY,LShankGYROZ,NC,RShankACCX,RShankACCY,RShankACCZ,RShankGYROX,
              RShankGYROY,RShankGYROZ,NC,WaistACCX,WaistACCY,WaistACCZ,WaistGYROX,WaistGYROY,WaistGYROZ,NC,ArmACCX,ArmACCY,ArmACCZ,
              ArmGYROX,ArmGYROY,ArmGYROZ,SC,Label], 500Hz
"""

time_point = time.time()

for task in range(0,Tasknumber):
    
    DataPath = Path_Cut+'/'+Personnumber+'/task_' + str(task+1) + '_data.txt'
    NewDataPath = Path_Labeled+'/'+Personnumber+'/task_' + str(task+1) + '.txt'        
    
    #If FOG does not appear, that is, labeltime is empty, then label is all 0
    if LabelTime[task] == '\n':
        data = pd.read_csv(DataPath,index_col=0)               
        TimeArray = np.array(data['TIME'].values).tolist()
        Label = [0 for x in range(0,len(TimeArray))]
    
    else:
        Fstartmin,Fstartsec,Fendmin,Fendsec = SplitLabelTime(LabelTime[task])
        
        #import the task data
        data = pd.read_csv(DataPath,index_col=0)
        TimeArray = np.array(data['TIME'].values).tolist()
        Label = [0 for x in range(0,len(TimeArray))]
        
        VedioStartTime[task] = datetime.datetime.strptime(VedioStartTime[task], '%H:%M:%S')
        
        for Fnum in range(0,len(Fstartmin)):
            Fstarttime = str(VedioStartTime[task] + datetime.timedelta(minutes=int(Fstartmin[Fnum]),seconds=Fstartsec[Fnum]))
            Fstarttime = Fstarttime[11:19]+'.002'
            Fendtime = str(VedioStartTime[task] + datetime.timedelta(minutes=Fendmin[Fnum],seconds=(Fendsec[Fnum])))
            Fendtime = Fendtime[11:19]+'.998'
            
            StarttimeRow = EndtimeRow = 0
            
            #Find the location of '1' lebal
            for TimeDetect in range(0,len(Label)):
                if Fstarttime in TimeArray[TimeDetect]:
                    StarttimeRow = TimeDetect-1
                if Fendtime in TimeArray[TimeDetect]:
                    EndtimeRow = TimeDetect
                    
            #If the StarttimeRow and EndtimeRow are not found correctly, an error is reported
            if (StarttimeRow == 0) or (EndtimeRow == 0) or ((EndtimeRow-StarttimeRow) <= 0) :   
                print ('Troubled when labeling the number ' + str(Fnum+1) + ' doctor\'s label')
            
            #Label the lata
            for Labelloc in range(0,len(Label)):
                if ((Labelloc >= StarttimeRow) and (Labelloc <= EndtimeRow)):
                    Label[Labelloc]=1
            
        #The duration of FOG was calculated
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
print('Data labeled finished，the total time using is %fs' % (time_end - time_start))
print('The time using for single section is %fs' % (time_end - time_point))
print('============================\n')
##################################################################################################

#The duration of Tasks was calculated
for K in range(0,len(StartHour)):
    startTime = datetime.datetime.strptime(str(StartHour[K])+':'+str(StartMin[K])+':'+str(StartSec[K]),'%H:%M:%S')
    endTime = datetime.datetime.strptime(str(EndHour[K])+':'+str(EndMin[K])+':'+str(EndSec[K]),'%H:%M:%S')
    delta = endTime - startTime
    Task_Time = Task_Time + delta
print('Time of Task: '+ str(Task_Time)[14:19])
print('Time of FoG: '+ str(Fog_Time)[14:19])
