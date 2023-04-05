#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  5 09:31:54 2023
提取ePub文件页面并保存为txt
@author: Merlin
"""

import io
import os
import sys
import fitz  # PyMuPDF库

def extract_pages(input_file, start_page, end_page, output_file):
    # 打开输入文件
    doc = fitz.open(input_file)

    # 确保指定的页面范围有效
    if start_page < 0 or end_page >= doc.page_count or start_page > end_page:
        print("无效的页面范围。")
        sys.exit(1)

    # 提取指定范围内的页面文本内容
    extracted_text = ""
    for page_num in range(start_page, end_page + 1):
        page = doc.load_page(page_num)
        extracted_text += page.get_text("text")

    # 将提取的文本内容保存到输出文件
    with io.open(output_file, "w", encoding="utf-8") as f:
        f.write(extracted_text)

    print(f"已成功将页面 {start_page} 到 {end_page} 从 {input_file} 提取至 {output_file}。")

input_file = "/Users/Merlin/Downloads/001.epub"
start_page = 3584  # 页码从0开始，所以减1
end_page = 4144  # 页码从0开始，所以减1
output_file = "/Users/Merlin/Downloads/001output.txt"

extract_pages(input_file, start_page, end_page, output_file)