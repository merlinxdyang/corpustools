#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 26 22:16:14 2023
你现在是Python高级工程师，写一段代码，计算一个语料库的词汇复杂度。
首先计算每个文本的token和type数量并给出TTR，
其次计算词汇密度，词汇密度计算公式为（实词数量/词汇总量）*100。
然后计算词汇丰富性，计算公式为类符树/(SQRT(形符数))。
最后计算学术词汇复杂度，计算公式为（文本中学术词汇数/一般词汇数)*100。
代码要使用tkinter构建一个UI界面，提示选择语料库文件夹的路径，
提示选择输入学术词汇文本，提示选择输入一般词汇文本，还要提示选择输出文件的路径。
输出为excel格式，包含文件名、token、type、TTR、词汇密度、词汇丰富度、学术词汇复杂度。
读取语料库文件夹文件是，如果不是txt或不是utf-8编码的文件就跳过。计算过程中避免除0问题。
@author: Merlin
"""

import os
import tkinter as tk
from tkinter import filedialog
import pandas as pd
import math
from collections import Counter
import nltk
nltk.download("punkt")
from nltk.tokenize import word_tokenize
import tkinter.messagebox

# 计算指标的函数
def calculate_metrics(corpus_file, academic_words_file, general_words_file):
    with open(corpus_file, 'r', encoding='utf-8') as f:
        text = f.read()
    tokens = word_tokenize(text)
    types = set(tokens)
    token_count = len(tokens)
    type_count = len(types)
    TTR = type_count / token_count if token_count > 0 else 0
    
    content_words = [word for word in tokens if word.isalpha()]
    content_word_count = len(content_words)
    lexical_density = (content_word_count / token_count) * 100 if token_count > 0 else 0

    lexical_richness = type_count / math.sqrt(token_count) if token_count > 0 else 0

    with open(academic_words_file, 'r', encoding='utf-8') as f:
        academic_words = set(f.read().split())
    with open(general_words_file, 'r', encoding='utf-8') as f:
        general_words = set(f.read().split())

    academic_word_count = sum([tokens.count(word) for word in academic_words])
    general_word_count = sum([tokens.count(word) for word in general_words])

    academic_complexity = (academic_word_count / general_word_count) * 100 if general_word_count > 0 else 0

    return token_count, type_count, TTR, lexical_density, lexical_richness, academic_complexity

# 计算所有文本指标的函数
def process_files(corpus_dir, academic_words_file, general_words_file, output_file):
    metrics_data = []
    for file in os.listdir(corpus_dir):
        if file.endswith('.txt'):
            try:
                corpus_file = os.path.join(corpus_dir, file)
                metrics = calculate_metrics(corpus_file, academic_words_file, general_words_file)
                metrics_data.append((file, *metrics))
            except UnicodeDecodeError:
                pass

    df = pd.DataFrame(metrics_data, columns=["文件名", "token", "type", "TTR", "词汇密度", "词汇丰富度", "学术词汇复杂度"])
    df.to_excel(output_file, index=False)

# UI界面
def select_directory(title):
    return filedialog.askdirectory(title=title)

def select_file(title):
    return filedialog.askopenfilename(title=title)

def select_output_file(title):
    return filedialog.asksaveasfilename(title=title, defaultextension=".xlsx")



def main():
    corpus_dir = None
    academic_words_file = None
    general_words_file = None
    output_file = None

    def select_corpus_dir():
        nonlocal corpus_dir
        corpus_dir = select_directory("选择语料库文件夹路径")
        corpus_dir_label.config(text=corpus_dir)

    def select_academic_words():
        nonlocal academic_words_file
        academic_words_file = select_file("选择学术词汇文本")
        academic_words_label.config(text=academic_words_file)

    def select_general_words():
        nonlocal general_words_file
        general_words_file = select_file("选择一般词汇文本")
        general_words_label.config(text=general_words_file)

    def select_output():
        nonlocal output_file
        output_file = select_output_file("选择输出文件路径")
        output_file_label.config(text=output_file)

    def process_and_save():
        if not (corpus_dir and academic_words_file and general_words_file and output_file):
            tk.messagebox.showerror("错误", "请先选择所有文件和目录")
        else:
            process_files(corpus_dir, academic_words_file, general_words_file, output_file)
            tk.messagebox.showinfo("完成", "分析完成！")

    root = tk.Tk()
    root.title("词汇复杂度计算器")

    corpus_btn = tk.Button(root, text="选择语料库文件夹", command=select_corpus_dir)
    corpus_btn.grid(row=0, column=0, pady=5)
    corpus_dir_label = tk.Label(root, text="")
    corpus_dir_label.grid(row=0, column=1)

    academic_words_btn = tk.Button(root, text="选择学术词汇文本", command=select_academic_words)
    academic_words_btn.grid(row=1, column=0, pady=5)
    academic_words_label = tk.Label(root, text="")
    academic_words_label.grid(row=1, column=1)

    general_words_btn = tk.Button(root, text="选择一般词汇文本", command=select_general_words)
    general_words_btn.grid(row=2, column=0, pady=5)
    general_words_label = tk.Label(root, text="")
    general_words_label.grid(row=2, column=1)

    output_btn = tk.Button(root, text="选择输出文件路径", command=select_output)
    output_btn.grid(row=3, column=0, pady=5)
    output_file_label = tk.Label(root, text="")
    output_file_label.grid(row=3, column=1)

    process_btn = tk.Button(root, text="开始计算", command=process_and_save)
    process_btn.grid(row=4, column=0, pady=5)

    exit_btn = tk.Button(root, text="退出", command=root.quit)
    exit_btn.grid(row=4, column=1, pady=5)

    root.mainloop()

if __name__ == "__main__":
    main()

