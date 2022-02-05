#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 22 10:42:37 2019

@author: hantao.li
"""
import csv

new_f = open('/Users/hantao.li/Documents/trytrytry.csv', 'w')
writer = csv.writer(new_f)
writer.writerow(['0','0','0','0','0','0','0','0'])
new_f.close()