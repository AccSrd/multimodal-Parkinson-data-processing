#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 26 23:54:03 2020

@author: hantao.li
"""

#宣武医院 label
import pandas as pd
import numpy as np
import datetime
import re
import os

def mkdir(path):
    isExists = os.path.exists(path)
    if not isExists:
        os.makedirs(path)
        print(path + ' 创建成功')
        return True
    else:
        print(path + ' 目录已存在')
        return False

######################################################################
path = '/Volumes/Work/Parkinson/宣武医院/原始数据/006-lixinli/Data/task'    
tasknumber = 5           #original data path
datapath = path + '/task_' + str(tasknumber) + '_data.txt'
newdatapath = path + '/label/task_' + str(tasknumber) + '.txt'      #the new data path
VedioStartTime = '10:56:21'               
Fnumber = 4
LabelTime = '''
00:15-00:17 00:35-00:39 00:58-01:04 01:22-01:25
'''


######################################################################

mkdir(path+'/label')

Pattern = r' |-|:'
Timelist = list(map(int,re.split(Pattern,LabelTime)))  #split the doctor's label time 
Fstartmin = Timelist[::4]
Fstartsec = Timelist[1::4]
Fendmin   = Timelist[2::4]
Fendsec   = Timelist[3::4]

data = pd.read_csv(datapath,index_col=0)               #import the task data
Ytime = np.array(data['TIME'].values).tolist()
Label = [0 for x in range(0,len(Ytime))]

VedioStartTime = datetime.datetime.strptime(VedioStartTime, '%H:%M:%S')

for Fnum in range(0,Fnumber):
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

data.to_csv(newdatapath)
    