# -*- coding: utf-8 -*-
"""
Created on Thu May 23 01:44:22 2024

@author: ispar
"""

from PyQt5 import uic
with open("Hakkinda.py", "w", encoding="utf-8") as fout:
    uic.compileUi("Hakkinda.ui",fout)
    