#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 25 00:51:29 2019

@author: hantao.li
"""

import csv
origin_f = open('/Users/hantao.li/Documents/Dongjie/003/naodian/naodian_1000.csv', 'r')
new_f = open('/Users/hantao.li/Documents/Dongjie/003/naodian/naodian_250.csv', 'w')
reader = csv.reader(origin_f)
writer = csv.writer(new_f)
for i,row in enumerate(reader):
    if (i-1)%4 == 0:
       writer.writerow(row)
origin_f.close()
new_f.close()