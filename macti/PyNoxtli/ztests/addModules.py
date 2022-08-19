#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 26 14:21:08 2020

@author: luiggi
"""

import sys
print(sys.path)

sys.path.insert(0, "/home/luiggi/GitSites/pynoxtli/base")
print(sys.path)

#from geo.line import Line

import geo.line #as line
barra = geo.line.Line(1.0)
#barra = line.Line(1.0)

