"""
************************************************************************************************
***********************          Raw --> Preprocessed        ***********************************
************************************************************************************************
Sort out the original txt_data header, and unify the txt_data sampling frequency to 500Hz

Input File      -->
(1) The original ACC/SC txt_data file(csv) renamed as LShank0/RShank0/Arm0/Waist0.csv
Data Format: [original time-stamp，data*7], 100Hz
(2) The txt_data file output by EEGLAB(txt) renamed as EEG.txt and EMG.txt
Data Format: [TIME,txt_data*25(EEG)/txt_data*5(EMG)], 1000Hz

Output File     -->
(1) EEG.txt / EMG.txt
Data Format: [NaN,TIME,txt_data*25(EEG)/txt_data*5(EMG)], 500Hz
(2) LShank.csv / RShank.csv / Arm.csv / Waist.csv
Data Format(Arm.csv as exp.): [NaN,TIME,OriTIME,ArmTIME,ArmACCX,ArmACCY,ArmACCZ,ArmGYROX,ArmGYROY,ArmGYROZ,SC(NC in others)], 500Hz
"""


import sys
sys.path.append("..")
sys.path.append(".")

from config import settings
import formatting
import function

import os
import csv
import pandas as pd
import numpy as np
import datetime


def prep_acc_data(sensor_loc, Gaitstarttime):

    # Check whether it exists. If it exists, perform the following operations (add header, interpolate to 500Hz)
    file_path = os.path.join(settings.DATA_PATH_Raw, sensor_loc + settings.FILE_SUFFIX_ACC_Raw)
    output_path = os.path.join(settings.DATA_PATH_Preprocessed, sensor_loc + settings.FILE_SUFFIX_Preprocessed)

    if not os.path.exists(file_path):
        print(f"Wrong Path {file_path} for the Gait data: {sensor_loc}")
    else:
        names = formatting.get_column_name_raw(sensor_loc)
        csv_data = pd.read_csv(file_path, header=None, index_col=False, names=names)
        
        ori_timeStamp = (np.array(csv_data[sensor_loc+'TIME'].values)).tolist()
        suffix_timeStamp = list(range(int(5*len(ori_timeStamp))))
        
        # Assign OriTime to [original timestamp i; 0.002; 0.004; 0.006; 0.008; original timestamp i+1],
        # to make it correspond to the interpolated txt_data.
        i_time = -1
        for i in range(0,len(suffix_timeStamp)):
            if i%5 == 0: i_time += 1
            suffix_timeStamp[i] = formatting.get_time_suffix(i, ori_timeStamp[i_time]) 
        
        OriTIME = {'OriTIME':suffix_timeStamp}
        Dataframe_Gait = pd.DataFrame(OriTIME)
        
        idx = csv_data.index 
        for col in names:
            Dataframe_Gait = function.spline(idx, Dataframe_Gait, csv_data, col)
        
        lst_new_timeStamp = list(range(len(suffix_timeStamp)))
        for k in range(0,len(lst_new_timeStamp)): lst_new_timeStamp[k] = 0        
        
        # Assign the gait time (the correct time after alignment) in the txt_data record table to the timestamp
        for i in range(0,len(lst_new_timeStamp)):
            deltatime = datetime.timedelta(microseconds=i*2000)
            lst_new_timeStamp[i] = str(Gaitstarttime + deltatime)[11:23]
        
        # The interpolated Dataframes are pieced together and then output
        new_timeStamp = {'TIME':lst_new_timeStamp}
        DataFrame_TimeStamp = pd.DataFrame(new_timeStamp)
        Dataframe_Gait = pd.concat([DataFrame_TimeStamp, Dataframe_Gait], axis=1)
        Dataframe_Gait.to_csv(output_path)

        print(f"Finish R->P in Gait data: {sensor_loc} for {file_path}")


def prep_eeg_data(sensor_name, EEGstarttime):

    # Check whether it exists. If it exists, perform the following operations (downsampling to 500Hz)
    file_path = os.path.join(settings.DATA_PATH_Raw, sensor_name + settings.FILE_SUFFIX_EEG_Raw)
    mid_path = os.path.join(settings.DATA_PATH_Preprocessed, sensor_name + settings.FILE_SUFFIX_EEG_Mid)
    output_path = os.path.join(settings.DATA_PATH_Preprocessed, sensor_name + settings.FILE_SUFFIX_Preprocessed)

    if not os.path.exists(file_path):
        print(f"Wrong Path {file_path} for the Gait data: {sensor_name}")
    else:
        # Read the EEG/EMG signal .txt file output by EEGLAB
        txt_data = pd.read_table(file_path, sep=',')
        ori_timeStamp = np.array(txt_data['Time'].values).tolist()
        new_timeStamp = list(range(len(ori_timeStamp)))

        # The time of the EEG .vmrk file (the correct time after alignment) is assigned to the timestamp
        for i in range(0,len(new_timeStamp)):
            deltatime = datetime.timedelta(microseconds=i*1000)
            new_timeStamp[i] = str(EEGstarttime + deltatime)[11:23]
        
        DataFrame_TimeStamp = pd.DataFrame({'TIME':new_timeStamp})
        txt_data = pd.concat([DataFrame_TimeStamp, txt_data],axis=1)
        txt_data = txt_data.drop(['Time'], axis=1)
        
        # Save the EEG file with correct time stamp as a temporary file, which is 1000Hz
        # If you do not want to delete the temporary file, you can change here
        txt_data.to_csv(mid_path)
        csv_data = open(mid_path, 'r')
        os.remove(mid_path)

        new_csv_data = open(output_path, 'w')
        reader = csv.reader(csv_data)
        writer = csv.writer(new_csv_data)
        
        # Save the 1000Hz file in this interlaced way to get the 500Hz file after frequency reduction
        for i,row in enumerate(reader):
            if (i-2)%2 == 0:
                writer.writerow(row)
            
        csv_data.close()
        new_csv_data.close()

        print(f"Finish R->P in EEG data: {sensor_name} for {file_path}")


def raw2prep(START_TIME_EEG, START_TIME_ACC):

    if not os.path.exists(settings.DATA_PATH_Preprocessed):
        function.mkdir(settings.DATA_PATH_Preprocessed)
    
    for s_loc in settings.SENSOR_NAME_ACC:
        prep_acc_data(s_loc, START_TIME_ACC)

    for s_name in settings.SENSOR_NAME_EEG:
        prep_eeg_data(s_name, START_TIME_EEG)

    print('============================')
    print('Raw Data -> Preprocessed Data: Finished')
    print('============================\n')
