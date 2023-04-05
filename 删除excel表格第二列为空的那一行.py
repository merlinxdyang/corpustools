#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan  6 22:57:51 2023

@author: Merlin
"""


import pandas as pd

# 读取 xlsx 文件并删除第二列为空的行
df = pd.read_excel('/Users/Merlin/Desktop/mylab/rr.xlsx', sheet_name='Sheet1')
print(df.columns)
# 删除第二列为空的行
df.dropna(subset=[df.columns[1]], inplace=True)


# 保存新的 xlsx 文件
df.to_excel('/Users/Merlin/Desktop/mylab/rrnew.xlsx', index=False)