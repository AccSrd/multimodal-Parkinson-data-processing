#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 25 01:59:46 2019

@author: hantao.li
"""

import csv
origin_f = open('/Users/hantao.li/Documents/Dongjie/002/jidian/jidian.csv', 'r')
new_f = open('/Users/hantao.li/Documents/Dongjie/002/jidian/jidian_200.csv', 'w')
reader = csv.reader(origin_f)
writer = csv.writer(new_f)
for i,row in enumerate(reader):
    if ((i)%10 != 4 and (i-9)%10 != 0):# or (i-5)%10 == 0 or (i-7)%10 == 0):        #数据第0、2、5、7、10、12....行
       writer.writerow(row)
origin_f.close()
new_f.close()