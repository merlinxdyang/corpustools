#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  5 11:33:06 2023

@author: Merlin
"""

import re

inp_file = '/Users/Merlin/Library/Rime/custom_phrase.txt'
out_file = '/Users/Merlin/Library/Rime/custom_phrase_new.txt'

with open(inp_file, 'r', encoding='utf-8') as f, open(out_file, 'w', encoding='utf-8') as f_out:
    lines = f.readlines()
    new_lines = []
    for line in lines:
        words = re.split(' +', line.strip()) # 使用正则分割成words列表
        new_words = [] # 存储无重复单词的列表
        [new_words.append(w) for w in words if w not in new_words]
        new_line = ' '.join(new_words)
        if new_line:
            new_lines.append(new_line)
    f_out.write('\n'.join(new_lines))

print('删除重复词并删除空行完成!')