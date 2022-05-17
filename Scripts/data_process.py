#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Version.1: Created on Fri May 1, 2020
@author: hantao.li

Version.2: Creat annotation for paper to be published.
Jan 25, 2021, @author: hantao.li

Version.3: Reformat the python program.
May 1, 2022, @author: hantao.li

************************************************************************************************
********************       Input Parameters      ***********************************************
************************************************************************************************

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

./Sample Data/1-Raw Data/ --> The original ACC/SC data file(csv) renamed as LShank0/RShank0/Arm0/Waist0.csv
Data Format: [original time-stamp, data*7], 100Hz

./Sample Data/1-Raw Data/ --> The data file output by EEGLAB(txt) renamed as EEG.txt and EMG.txt
Data Format: [TIME,data*25(EEG)/data*5(EMG)],1000Hz

************************************************************************************************
********************         Output Files        ***********************************************
************************************************************************************************

./Sample Data/2-Preprocessed Data -->
(1) EEG.csv / EMG.csv
Data Format: [NaN,TIME,data*25(EEG)/data*5(EMG)], 500Hz
(2) LShank.csv / RShank.csv / Arm.csv / Waist.csv
Data Format(Arm.csv as exp.): [NaN,TIME,OriTIME,ArmTIME,ArmACCX,ArmACCY,ArmACCZ,ArmGYROX,ArmGYROY,ArmGYROZ,SC(NC in others)], 500Hz

./Sample Data/3-Segmented Data --> task_1_data.txt / task_2_data.txt / ...
Data Format: [NaN,TIME,FP1,FP2,F3,F4,C3,C4,P3,P4,O1,O2,F7,F8,Fz,Cz,Pz,FC1,FC2,CP1,CP2,FC5,FC6,CP5,CP6,EMG1,EMG2,IO,EMG3,EMG4,
              LShankACCX,LShankACCY,LShankACCZ,LShankGYROX,LShankGYROY,LShankGYROZ,NC,RShankACCX,RShankACCY,RShankACCZ,RShankGYROX,
              RShankGYROY,RShankGYROZ,NC,WaistACCX,WaistACCY,WaistACCZ,WaistGYROX,WaistGYROY,WaistGYROZ,NC,ArmACCX,ArmACCY,ArmACCZ,
              ArmGYROX,ArmGYROY,ArmGYROZ,SC]

./Sample Data/4-Labeled Data --> task_1.txt / task_2.txt / ...
Data Format: [...(Same as above),Label]


Task_Time   --> The length of the whole data of single patient.
FoG_Time    --> The length of the FOG duration in the whole data of single patient.

************************************************************************************************
"""

import datetime
import sys
sys.path.append("..")
sys.path.append(".")

from raw2prep import raw2prep
from prep2seg import prep2seg
from seg2label import seg2label


# The beginning time-point of the original EEG file and Gait file
START_TIME_EEG  = datetime.datetime(2020,1,1,9,30,25,159000)           # Last bit should be odd
START_TIME_ACC = datetime.datetime(2020,1,1,9,30,25,150000)            # Last bit should be even

TASK_NUMBER = 3
CUT_TIME = '''
09:30:26
09:30:29
09:30:31
09:30:33
09:30:34
09:30:35
'''

LABEL_TIME = list(range(TASK_NUMBER))
LABEL_TIME[0] = '''
00:00-00:02
'''

LABEL_TIME[1] = '''
00:01-00:01
'''

LABEL_TIME[2] = '''
'''

if __name__ == '__main__':
    raw2prep(START_TIME_EEG, START_TIME_ACC)
    prep2seg(TASK_NUMBER, CUT_TIME)
    seg2label(TASK_NUMBER, CUT_TIME, LABEL_TIME)
