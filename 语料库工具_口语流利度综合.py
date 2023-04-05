#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 26 10:01:34 2023

@author: Merlin
"""

import os
import speech_recognition as sr
from pydub import AudioSegment
from pydub.silence import split_on_silence
import spacy
import xlsxwriter
import tkinter as tk
from tkinter import filedialog

# Load the English model
nlp = spacy.load("en_core_web_sm")

def transcribe_audio(file_path):
    recognizer = sr.Recognizer()
    with sr.AudioFile(file_path) as source:
        audio = recognizer.record(source)
    try:
        text = recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        text = ""
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        text = ""
    return text

def count_words(text):
    doc = nlp(text)
    return len([token for token in doc if not token.is_punct])

def analyze_speaking_fluency(input_folder, output_xlsx):
    files = os.listdir(input_folder)

    # Create a new Excel workbook and add a worksheet
    workbook = xlsxwriter.Workbook(output_xlsx)
    worksheet = workbook.add_worksheet()

    # Write the headers for the Excel file
    worksheet.write(0, 0, "文件名")
    worksheet.write(0, 1, "时长（秒）")
    worksheet.write(0, 2, "单词总数")
    worksheet.write(0, 3, "每分钟的有效词汇数")
    worksheet.write(0, 4, "暂停次数")

    row = 1

    for file in files:
        if file.endswith(".wav"):
            file_path = os.path.join(input_folder, file)
            sound = AudioSegment.from_wav(file_path)
            pauses = split_on_silence(sound, min_silence_len=500, silence_thresh=-30)
            num_pauses = len(pauses)

            text = transcribe_audio(file_path)
            word_count = count_words(text)
            duration_seconds = len(sound) / 1000
            words_per_minute = (word_count / duration_seconds) * 60 if duration_seconds != 0 else 0

            worksheet.write(row, 0, file)
            worksheet.write(row, 1, duration_seconds)
            worksheet.write(row, 2, word_count)
            worksheet.write(row, 3, words_per_minute)
            worksheet.write(row, 4, num_pauses)

            row += 1

    # Close the Excel workbook
    workbook.close()

def browse_input_folder():
    input_folder = filedialog.askdirectory()
    input_folder_entry.delete(0, tk.END)
    input_folder_entry.insert(0, input_folder)

def browse_output_file():
    output_xlsx = filedialog.asksaveasfilename(defaultextension=".xlsx")
    output_xlsx_entry.delete(0, tk.END)
    output_xlsx_entry.insert(0, output_xlsx)

def start_analysis():
    input_folder = input_folder_entry.get()
    output_xlsx = output_xlsx_entry.get()
    analyze_speaking_fluency(input_folder, output_xlsx)
    tk.messagebox.showinfo("完成", "分析完成！")

app = tk.Tk()
app.title("口语流利度分析工具 V1.0")

input_folder_label = tk.Label(app, text="音频文件夹：")
input_folder_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")
input_folder_entry = tk.Entry(app, width=50)
input_folder_entry.grid(row=0, column=1, padx=5, pady=5)
input_folder_button = tk.Button(app, text="浏览", command=browse_input_folder)
input_folder_button.grid(row=0, column=2, padx=5, pady=5)

output_xlsx_label = tk.Label(app, text="输出文件：")
output_xlsx_label.grid(row=1, column=0, padx=5, pady=5, sticky="e")
output_xlsx_entry = tk.Entry(app, width=50)
output_xlsx_entry.grid(row=1, column=1, padx=5, pady=5)
output_xlsx_button = tk.Button(app, text="浏览", command=browse_output_file)
output_xlsx_button.grid(row=1, column=2, padx=5, pady=5)

start_analysis_button = tk.Button(app, text="开始分析", command=start_analysis)
start_analysis_button.grid(row=2, column=1, padx=5, pady=10)

app.mainloop()

