import scipy.interpolate as spi
import pandas as pd
import numpy as np
import re
import os

def spline(X, Dataframe_Gait, csv_data, col):

    Y = csv_data[col].values 
    x = np.arange(0,len(csv_data), 0.2) 
    ipo3 = spi.splrep(X, Y,k=3)
    iy3 = spi.splev(x, ipo3) 
    ch1 = pd.DataFrame(iy3)
    ch1.rename(columns={0:col}, inplace=True)
    Dataframe_Gait = pd.concat([Dataframe_Gait, ch1], axis=1)

    return Dataframe_Gait

#Split the doctor's label time into m/s
def SplitLabelTime(Timestr):
    Pattern = r' |-|:|\r|\n'
    Timelist = list(map(str,re.split(Pattern, Timestr)))
    Timelist = [str(int(x)) for x in Timelist if (x != '' and x != '\n')]
    return Timelist[::4],Timelist[1::4],Timelist[2::4],Timelist[3::4]

def SplitCutTime(Timestr: str):
    """
    Split the cuttime into h/m/s

    Args:
        Timestr(str): format should be hh:mm:ss e.g. 10:21:23
    """
    Pattern = r' |-|:|\n'
    Timelist = re.split(Pattern, Timestr)
    Timelist = [str(int(x)) for x in Timelist if (x != '' and x != '\n')]
    return Timelist[::6],Timelist[1::6],Timelist[2::6],Timelist[3::6],Timelist[4::6],Timelist[5::6]

#If the trigger line still be 0 after the cutting, it means the error.
def ZeroDetc(StartTimeRow, EndTimeRow, filename, taskname):
    if StartTimeRow == 0:
        print (f'----------------------------\n task {taskname} for {filename} Can not find the Start Row')
    if EndTimeRow == 0:
        print (f'----------------------------\n task {taskname} for {filename} Can not find the End Row')

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