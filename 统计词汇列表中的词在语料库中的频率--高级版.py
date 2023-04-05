#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
#读取文件夹wjj下的所有txt汉语文本，
#根据stp.txt文件中的关键词，统计每个关键词在每个文本中的出现频率。
#输出结果保存在ff.exls文件中，
#结果显示为：序号、关键词、总频率数、归一化频率数，在每个txt文件中的频率数。

Created on Sun Mar 19 23:08:41 2023

@author: Merlin
"""

import os
import re
from collections import defaultdict
from openpyxl import Workbook

BASE_PATH = '/Users/Merlin/Desktop/mylab/chuanxin/'

def read_txt_files(folder_path):
    return [f for f in os.listdir(folder_path) if f.endswith('.txt')]

def read_keywords(filepath):
    with open(filepath) as f:
        return [line.strip() for line in f]

def count_keyword_occurrences(txt_files, keywords, folder_path):
    counts = defaultdict(lambda: defaultdict(int))
    for txt_file in txt_files:
        try:
            with open(os.path.join(folder_path, txt_file), encoding='utf-8') as f:
                text = f.read()
                for keyword in keywords:
                    counts[keyword][txt_file] = len(re.findall(keyword, text))
        except UnicodeDecodeError:
            print(f"注意：文件'{txt_file}' 不是UTF-8格式，已跳过。")
    return counts

def save_results_to_excel(keywords, counts, output_path):
    wb = Workbook()
    ws = wb.active

    ws.append(['序号', '关键词', '总频率数', '归一化频率数', '在每个txt文件中的频率数', 'Types', 'Tokens', 'TTR', 'file counts'])

    for i, keyword in enumerate(keywords):
        total_count = sum(counts[keyword].values())
        normalized_count = total_count / len(txt_files)
        types = len(counts[keyword])
        tokens = total_count
        ttr = types / tokens if tokens != 0 else 0
        ws.append([i+1, keyword, total_count, normalized_count, ', '.join(str(count) for count in counts[keyword].values()), types, tokens, ttr, len(txt_files)])

    wb.save(output_path)
    
txt_files = read_txt_files(os.path.join(BASE_PATH, 'ss'))
keywords = read_keywords(os.path.join(BASE_PATH, 'quedingbiaoji.txt'))
counts = count_keyword_occurrences(txt_files, keywords, os.path.join(BASE_PATH, 'ss'))
save_results_to_excel(keywords, counts, os.path.join(BASE_PATH, 'output_ss.xlsx')) 