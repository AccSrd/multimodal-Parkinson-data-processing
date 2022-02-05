#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul  1 13:53:57 2020

@author: hantao.li
"""

#import urllib,urllib2
import tkinter #导入TKinter模块
import re
import os
import datetime
import pandas as pd
import numpy as np

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
    return Timelist[::4],Timelist[1::4],Timelist[2::4],Timelist[3::4]
    #return Timelist

def GetTaskNumber():
    TaskNumber = TaskNum.get()
    print ('TaskNumber ='+ TaskNumber)
    
def GetPersonNumber():
    PersonNumber = PersonNum.get()
    print ('PersonNumber ='+ PersonNumber)

def GetLabelTime():
  user=user_text.get() #获取文本框内容
  startmin,Fstartsec,Fendmin,Fendsec = SplitLabelTime(user)
  return startmin,Fstartsec,Fendmin,Fendsec
  
def Label(Tasknumber,VedioStartTime,LabelTime):
    for task in range(0,Tasknumber):
        
        DataPath = Path_Cut+'/'+Personnumber+'/task_' + str(task+1) + '_data.txt'
        NewDataPath = Path_Labeled+'/'+Personnumber+'/task_' + str(task+1) + '.txt'        
        
        if LabelTime[task] == '':
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
'''
    #time_end = time.time()
    print('============================')
    print('数据标注完成，总用时为 %fs' % (time_end - time_start))
    print('单段用时为 %fs' % (time_end - time_point))
    print('============================\n')
'''


Path_File     = '/Users/hantao.li/Desktop/test/ALL'
Path_Cut          = Path_File + '/4-分段未标注数据'   
Path_Labeled      = Path_File + '/6-标注完成数据'
TaskNumber = 0
Personnumber = ''

#mkdir(Path_Labeled+'/'+Personnumber)

Labelwindow=tkinter.Tk() #创建Tk对象
Labelwindow.title("Label") #设置窗口标题
Labelwindow.geometry("300x300") #设置窗口尺寸

l1=tkinter.Label(Labelwindow,text="用户名") #标签
l1.pack()


TaskNum = tkinter.Spinbox(Labelwindow, from_=0, to=10,)
TaskNum.pack()
tkinter.Button(Labelwindow,text="确定任务数量",command=GetTaskNumber).pack() #command绑定获取文本框内容方法

PersonNum = tkinter.Entry()
PersonNum.pack()
tkinter.Button(Labelwindow,text="确定人物标号",command=GetPersonNumber).pack() #command绑定获取文本框内容方法


user_text=tkinter.Entry() #创建文本框
user_text.pack()
tkinter.Button(Labelwindow,text="确定标签时间",command=GetLabelTime).pack() #command绑定获取文本框内容方法

text = tkinter.Text(Labelwindow, width=20, height=5)
text.pack()

xx = TaskNum.get()

Labelwindow.mainloop() #进入主循环

print (xx)