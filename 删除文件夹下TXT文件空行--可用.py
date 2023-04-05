#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan  6 21:31:28 2023
删除文件夹下所有txt文件中的空行
@author: Merlin
"""


import os 

# 遍历文件夹
def remove_empty_line(path):
    files = os.listdir(path)
    for file in files:
        file_path = os.path.join(path, file)
        # 判断文件是否是文件夹
        if os.path.isdir(file_path):
            remove_empty_line(file_path)
        # 判断文件是否是txt文件
        elif os.path.splitext(file_path)[1] == '.txt':
            # 读取文件
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            # 写入文件
            with open(file_path, 'w', encoding='utf-8') as f_w:
                for line in lines:
                    # 判断行是否为空
                    if line.strip() != '':
                        f_w.write(line)

# 程序入口
if __name__ == '__main__':
    # 文件夹路径
    path = '/Users/Merlin/Desktop/mylab/wo_wu'
    remove_empty_line(path)