#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 29 15:58:08 2020

@author: hantao.li
"""

import re
CutTime = '''
14:28:05
14:31:13
14:32:04
14:38:04
14:38:37
14:39:04
14:39:26
14:39:58
14:40:10
14:40:47
'''


Pattern = r' |\n'
Timelist_CutTime = list(map(str,re.split(Pattern,CutTime)))  #split the doctor's label time 
Timelist_CutTime = [x for x in Timelist_CutTime if x != '']
Timelist_CutTime = [x for x in Timelist_CutTime if x != '\n']
VedioStartTime = Timelist_CutTime[::2]

