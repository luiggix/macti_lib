# -*- coding: utf-8 -*-
"""
Created on Thu Jul  4 00:08:15 2019

@author: luiggi
"""

import numpy as np

aa = np.array([1,2,3])

print(aa)

aW = aa[0]
aa[0] = 0
print(aa)
print(aW)