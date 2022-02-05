#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul  4 22:59:27 2020

@author: hantao.li
"""

import re

def SplitLabelTime(Timestr):
    Pattern = r' |-|:|\r\n|\n'
    Timelist = list(map(str,re.split(Pattern,Timestr)))  #split the doctor's label time into m/s 
    Timelist = [int(x) for x in Timelist if x != '']
    return Timelist[::4],Timelist[1::4],Timelist[2::4],Timelist[3::4]

def SplitCutTime(Timestr):
    Pattern = r' |-|:|\r\n|\n'
    Timelist = list(map(str,re.split(Pattern,Timestr)))  #split the cuttime into h/m/s
    Timelist = [x for x in Timelist if x != '']
    return Timelist[::6],Timelist[1::6],Timelist[2::6],Timelist[3::6],Timelist[4::6],Timelist[5::6]

CutTime = '''
12:04:38
12:10:39
12:12:33
12:18:05
12:20:09
12:20:38
12:20:48
12:21:19
'''

CutTime1 = '12:04:38 12:10:39 12:12:33 12:18:05 12:20:09 12:20:38 12:20:48 12:21:19'


xx = '''
00:28-01:02
01:06-01:08
01:29-01:41
01:59-02:30
02:58-03:06
03:25-03:36
03:59-04:11
04:30-04:35
04:39-04:43
05:11-05:13
'''
aa = '1'
aa = '''
'''

print ('------'+aa)
if aa == '\n':
    print ('yes')

x1,x2,x3,x4 = SplitLabelTime(xx)
y1,y2,y3,y4,y5,y6 = SplitCutTime(CutTime)

Pattern = r' '
Timelist_CutTime1 = list(map(str,re.split(Pattern,CutTime1)))  #split the doctor's label time 
VedioStartTime1 = Timelist_CutTime1[::2]

Pattern = r' |\n'
Timelist_CutTime = list(map(str,re.split(Pattern,CutTime)))  #split the doctor's label time
Timelist_CutTime = [x for x in Timelist_CutTime if x != ''] 
VedioStartTime = Timelist_CutTime[::2]
