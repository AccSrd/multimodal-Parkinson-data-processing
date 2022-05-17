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

import sys
sys.path.append("..")
sys.path.append(".")

from config import settings
import function

import os
import pandas as pd
import numpy as np
import datetime
import re


def LabelData(task_id, VedioStartTime, LABEL_TIME, Fog_Time):

    TASK_NAME = 'task_' + str(task_id + 1)
    input_path = os.path.join(settings.DATA_PATH_Cut, TASK_NAME + settings.FILE_SUFFIX_CUT)
    output_path = os.path.join(settings.DATA_PATH_Labeled, TASK_NAME + settings.FILE_SUFFIX_LABEL)  
    
    if not os.path.exists(input_path):
        print(f"Wrong Path {input_path} for the data to be labeled")
    else:
        #If FOG does not appear, label is all 0 (e.g. LABEL_TIME[2] here)
        if LABEL_TIME[task_id] == '\n':
            data = pd.read_csv(input_path, index_col=0)               
            time_stamp = np.array(data['TIME'].values).tolist()
            label = [0 for x in range(0,len(time_stamp))]
        
        else:
            Fstartmin, Fstartsec, Fendmin, Fendsec = function.SplitLabelTime(LABEL_TIME[task_id])
            
            #import the task_id data
            data = pd.read_csv(input_path, index_col=0)
            time_stamp = np.array(data['TIME'].values).tolist()
            label = [0 for x in range(0,len(time_stamp))]

            VedioStartTime[task_id] = datetime.datetime.strptime(VedioStartTime[task_id], '%H:%M:%S')

            for Fnum in range(0,len(Fstartmin)):
                Fstarttime = str(VedioStartTime[task_id] + datetime.timedelta(minutes=int(Fstartmin[Fnum]), seconds=int(Fstartsec[Fnum])))
                Fstarttime = Fstarttime[11:19]+'.002'
                Fendtime = str(VedioStartTime[task_id] + datetime.timedelta(minutes=int(Fendmin[Fnum]), seconds=int(Fendsec[Fnum])))
                Fendtime = Fendtime[11:19]+'.998'
                
                StarttimeRow, EndtimeRow = 0, 0
                
                #Find the location of '1' lebal
                for TimeDetect in range(0,len(label)):
                    if Fstarttime in time_stamp[TimeDetect]:
                        StarttimeRow = TimeDetect-1
                    if Fendtime in time_stamp[TimeDetect]:
                        EndtimeRow = TimeDetect
                        
                #If the StarttimeRow and EndtimeRow are not found correctly, an error is reported
                if (StarttimeRow == 0 and EndtimeRow == 0) or ((EndtimeRow-StarttimeRow) <= 0) :   
                    print (f'ERROR when labeling the number {str(Fnum+1)} doctor\'s label in task {task_id+1}')
                
                #Label the lata
                for label_loc in range(0,len(label)):
                    if ((label_loc >= StarttimeRow) and (label_loc <= EndtimeRow)):
                        label[label_loc] = 1
                
            #The duration of FOG was calculated
            for K in range(0,len(Fstartmin)):
                startTime = datetime.datetime.strptime('0:'+str(Fstartmin[K])+':'+str(Fstartsec[K]),'%H:%M:%S')
                endTime = datetime.datetime.strptime('0:'+str(Fendmin[K])+':'+str(Fendsec[K]),'%H:%M:%S')+datetime.timedelta(seconds=1)
                delta = endTime - startTime
                Fog_Time = Fog_Time + delta
        
        Ch_Label = pd.DataFrame({'Label': label})
        data = pd.concat([data,Ch_Label], axis=1)
        data.to_csv(output_path, header = None)

    return Fog_Time
    

def seg2label(TASK_NUMBER, CUT_TIME, LABEL_TIME):

    if not os.path.exists(settings.DATA_PATH_Labeled):
        function.mkdir(settings.DATA_PATH_Labeled)

    # Calculate the start time of each video, that is, the start time of each task
    VIDEO_START_TIME = [x for x in list(map(str, re.split(r' |-|\n', CUT_TIME))) if (x != '')][::2]

    StartHour, StartMin, StartSec, EndHour, EndMin, EndSec = function.SplitCutTime(CUT_TIME)
    Task_Time = datetime.datetime.strptime('0:0:0', '%H:%M:%S')
    Fog_Time = datetime.datetime.strptime('0:0:0', '%H:%M:%S')

    for task_id in range(0, TASK_NUMBER):
        Fog_Time = LabelData(task_id, VIDEO_START_TIME, LABEL_TIME, Fog_Time)

    #The duration of Tasks was calculated
    for K in range(0,len(StartHour)):
        startTime = datetime.datetime.strptime(str(StartHour[K])+':'+str(StartMin[K])+':'+str(StartSec[K]),'%H:%M:%S')
        endTime = datetime.datetime.strptime(str(EndHour[K])+':'+str(EndMin[K])+':'+str(EndSec[K]),'%H:%M:%S')
        delta = endTime - startTime
        Task_Time = Task_Time + delta

    print('============================')
    print('Time of Task: '+ str(Task_Time)[14:19])
    print('Time of FoG: '+ str(Fog_Time)[14:19])
    print('Segmented Data -> Labeled Data: Finished')
    print('============================\n')
    


    