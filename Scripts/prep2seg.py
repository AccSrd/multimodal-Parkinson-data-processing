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

import sys
sys.path.append("..")
sys.path.append(".")

from config import settings
import formatting
import function

import pandas as pd
import os
import csv


#Cut the ACC/SC data file
def CutGait(sensor_loc, task_id, CUT_TIME):

    StartTimeRow, EndTimeRow = 0, 0
    StartHour, StartMin, StartSec, EndHour, EndMin, EndSec = function.SplitCutTime(CUT_TIME)
    StartTime = StartHour[task_id-1]+':'+StartMin[task_id-1]+':'+StartSec[task_id-1]+'.002'
    EndTime = EndHour[task_id-1]+':'+EndMin[task_id-1]+':'+EndSec[task_id-1]+'.002'

    col_name = formatting.get_column_name_prep(sensor_loc)
    input_path = os.path.join(settings.DATA_PATH_Preprocessed, sensor_loc + settings.FILE_SUFFIX_Preprocessed)
    mid_path = os.path.join(settings.DATA_PATH_Preprocessed, sensor_loc + settings.FILE_SUFFIX_PreprocessedMid)
    
    #For nonexistent files, write 0 in the corresponding position
    if not os.path.exists(input_path):
        new_f = open(input_path,'w')
        writer = csv.writer(new_f)
        writer.writerow(['0']*len(col_name))
        new_f.close()
        Dataframe = pd.read_csv(input_path, header=None, index_col=False, names=col_name)
        Dataframe = Dataframe.drop([sensor_loc, '?'], axis=1)
        os.remove(input_path) 

        print(f'There is no [{sensor_loc}.csv] for task {task_id}, thus an empty one has been utilized')
        
    else:
        origin_f = open(input_path,'r')
        reader = csv.reader(origin_f)
        column = [row[1] for row in reader]
        
        #Find the start and the end lines of the data
        for j in range(0,len(column)):
            if StartTime in column[j]:
                StartTimeRow = j-1
            if EndTime in column[j]:
                EndTimeRow = j-1
        origin_f.close()

        origin_f = open(input_path,'r')
        new_f = open(mid_path, 'w')
        reader = csv.reader(origin_f)
        writer = csv.writer(new_f)
        
        #Select the part between StartTimeRow and EndTimeRow and save it to the corresponding dataframe
        for i,row in enumerate(reader):
            if ((i >= StartTimeRow) and (i <= EndTimeRow)):
               writer.writerow(row)
               
        origin_f.close()
        new_f.close()       
        
        Dataframe = pd.read_csv(mid_path, header=None, index_col=False, names=col_name)
        Dataframe = Dataframe.drop([sensor_loc, '?'], axis=1)
        
        os.remove(mid_path) 
        function.ZeroDetc(StartTimeRow, EndTimeRow, sensor_loc, task_id)
        
    return Dataframe

#Cut the EEG/EMG data file
def CutEEG(sensor_loc, task_id, CUT_TIME):

    StartTimeRow, EndTimeRow = 0, 0
    StartHour, StartMin, StartSec, EndHour, EndMin, EndSec = function.SplitCutTime(CUT_TIME)
    StartTime = StartHour[task_id-1]+':'+StartMin[task_id-1]+':'+StartSec[task_id-1]+'.002'
    EndTime = EndHour[task_id-1]+':'+EndMin[task_id-1]+':'+EndSec[task_id-1]+'.002'

    col_name = formatting.get_column_name_prep(sensor_loc)
    input_path = os.path.join(settings.DATA_PATH_Preprocessed, sensor_loc + settings.FILE_SUFFIX_Preprocessed)
    mid_path = os.path.join(settings.DATA_PATH_Preprocessed, sensor_loc + settings.FILE_SUFFIX_PreprocessedMid)
    
    # impossible in general
    if not os.path.exists(input_path):
        new_f = open(input_path, 'w')
        writer = csv.writer(new_f)
        writer.writerow(['0']*len(col_name))
        new_f.close()
        Dataframe = pd.read_csv(input_path, header=None, index_col=False, names=col_name)
        if sensor_loc != 'EEG':
            Dataframe = Dataframe.drop([sensor_loc+'TIME'], axis=1)
        Dataframe = Dataframe.drop(['?'], axis=1)
        os.remove(input_path) 
        
        print(f'There is no [{sensor_loc}.csv] for task {task_id}, thus an empty one has been utilized')
        
    #Same method as the ACC/SC cutting
    else:
        origin_f = open(input_path,'r')
        reader = csv.reader(origin_f)
        column = [row[1] for row in reader]
        
        for j in range(0,len(column)):
            if StartTime in column[j]:
                StartTimeRow = j-1
            if EndTime in column[j]:
                EndTimeRow = j-1      
        origin_f.close()

        origin_f = open(input_path,'r')
        new_f = open(mid_path, 'w')
        reader = csv.reader(origin_f)
        writer = csv.writer(new_f)
        
        for i,row in enumerate(reader):
            if ((i >= StartTimeRow) and (i <= EndTimeRow)):
               writer.writerow(row)
               
        origin_f.close()
        new_f.close()       
        
        Dataframe = pd.read_csv(mid_path, header=None, index_col=False, names=col_name) 
        if sensor_loc != 'EEG':
            Dataframe = Dataframe.drop([sensor_loc+'TIME'], axis=1)
        Dataframe = Dataframe.drop(['?'], axis=1)
        Dataframe = Dataframe.loc[:,~Dataframe.columns.str.contains('^Unnamed')]

        os.remove(mid_path) 
        function.ZeroDetc(StartTimeRow, EndTimeRow, sensor_loc, task_id)

    return Dataframe


def CutData(task_id, CUT_TIME):
    TASK_NAME = 'task_' + str(task_id)
    output_path = os.path.join(settings.DATA_PATH_Cut, TASK_NAME + settings.FILE_SUFFIX_CUT)
    
    # The gait files are cut separately and stored in a dataframe
    Dataframe_Gait_LS = CutGait('LShank', task_id, CUT_TIME)
    Dataframe_Gait_RS = CutGait('RShank', task_id, CUT_TIME)
    Dataframe_Gait_WST = CutGait('Waist', task_id, CUT_TIME)
    Dataframe_Gait_ARM = CutGait('Arm', task_id, CUT_TIME)
    Dataframe_Gait = pd.concat([Dataframe_Gait_LS, Dataframe_Gait_RS, Dataframe_Gait_WST, Dataframe_Gait_ARM], axis=1)
    
    Dataframe_Gait = formatting.reformat_col_gait(Dataframe_Gait)
    
    # The EEG and EMG file are cut and stored in a dataframe
    Dataframe_EEG = CutEEG('EEG', task_id, CUT_TIME)
    Dataframe_EMG = CutEEG('EMG', task_id, CUT_TIME)
    
    # Put multimodal data together.
    Dataframe = pd.concat([Dataframe_EEG, Dataframe_EMG, Dataframe_Gait],axis=1)
    Dataframe = Dataframe.fillna(value=0)
    Dataframe = Dataframe.drop(settings.PREP_COLNAME_DROP, axis=1)
    Dataframe = Dataframe.rename(columns={('EEGTIME'): 'TIME'})
    Dataframe.to_csv(output_path)
    
    print(f'{TASK_NAME} Segmented Finished')


def prep2seg(TASK_NUMBER, CUT_TIME):

    if not os.path.exists(settings.DATA_PATH_Cut):
        function.mkdir(settings.DATA_PATH_Cut)

    for task_id in range(1, TASK_NUMBER + 1):
        CutData(task_id, CUT_TIME)
    
    print('============================')
    print('Preprocessed Data -> Segmented Data: Finished')
    print('============================\n')


    