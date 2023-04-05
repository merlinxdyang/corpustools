#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan  7 11:20:32 2023
所有文件和文件夹的路径都是/User/lujing/。
将wo_wu文件夹下所有txt文件中的关键词作出标注。
关键词保存在chinese_sfp.txt中，
每一行包括关键词和它的拼音，用逗号分隔，
如“吧, ba”。
标注的方法是在关键词出现的地方加上SFP和这个关键词的拼音，
例如关键词是“吧”，那么在文本中“吧”出现的地方标注为：吧_SFP_ba 。
@author: Merlin
"""

import os
import re


# 需要标注的文件夹
folder_path = '/Users/Merlin/Desktop/mylab/wo_wu'

# 关键词文件路径
keywords_file_path = '/Users/Merlin/Desktop/mylab/chinese_sfp.txt'


# 读取关键词文件
with open(keywords_file_path, 'r') as f:
    keywords = [line.strip().split(',') for line in f]

# 拼音到关键词的映射，使用拼音做为 key
pinyin_to_keyword = {}

# 对于每一个关键词，使用拼音作为 key 存储到拼音到关键词的映射中
for keyword, pinyin in keywords:
    pinyin_to_keyword[pinyin] = keyword

# 遍历文件夹中的所有文件
for file_name in os.listdir(folder_path):
    # 只处理 txt 文件
    if file_name.endswith('.txt'):
        file_path = os.path.join(folder_path, file_name)
        # 读取文件内容
        with open(file_path, 'r') as f:
            file_content = f.read()
        
        # 对于文件中的每一个关键词
        for pinyin, keyword in pinyin_to_keyword.items():
            # 使用正则表达式替换关键词
            file_content = re.sub(keyword, f'{keyword}_SFP_{pinyin}', file_content)
        
        # 将修改后的文件内容写回文件
        with open(file_path, 'w') as f:
            f.write(file_content)
