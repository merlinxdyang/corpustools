
import os
import re
import tkinter as tk
from tkinter import filedialog

def clean_corpus():
    global file_path  # 声明全局变量
    # 获取用户选择的语料库路径
    path = file_path.get()
    if not path:
        return

    # 获取语料库文件夹名称和所在的上一级目录
    folder_name = os.path.basename(path)
    parent_dir = os.path.dirname(path)

    # 拼接清洁后语料库文件夹的路径
    cleaned_path = os.path.join(parent_dir, folder_name + "_cleaned")

    # 创建清洁后语料库文件夹
    os.mkdir(cleaned_path)

    # 遍历语料库文件夹下的所有文件
    for filename in os.listdir(path):
        # 判断文件是否为TXT文件
        if filename.endswith(".txt"):
            # 拼接文件路径
            file_path = os.path.join(path, filename)
            # 尝试以utf-8编码读取文件内容
            try:
                with open(file_path, encoding="utf-8") as f:
                    # 读取文件内容
                    file_content = f.read()
                    # 使用正则表达式进行文本清洗
                    pattern = r'\b(\w) (\w)\b' # 匹配两个单词之间的空格
                    fixed_text = re.sub(pattern, r'\1\2', file_content) # 将两个单词之间的空格去掉
                    cleaned_content = re.sub(r'[^A-Za-z.,!?;:]', ' ', fixed_text) # 将非字母、非标点符号的字符替换为空格
                    cleaned_content = re.sub(r'\d+', '', cleaned_content) # 将数字替换为空格
                    cleaned_content = re.sub(r' +', ' ', cleaned_content) # 将多个空格替换为一个空格
                # 拼接清洁后文件的路径
                cleaned_filename = filename + "cleaned.txt"
                cleaned_file_path = os.path.join(cleaned_path, cleaned_filename)
                # 将清洁后的内容写入文件
                with open(cleaned_file_path, mode="w", encoding="utf-8") as f:
                    f.write(cleaned_content)
            except UnicodeDecodeError:
                new_filename = "ERROR" + filename
                os.rename(file_path, os.path.join(path, new_filename))

    # 弹出提示框，提示用户清洁完成
    tk.messagebox.showinfo(title="提示", message="语料库清洁完成！")

def select_folder_path():
    global file_path  # 声明全局变量
    # 弹出文件选择对话框，获取用户选择的文件夹路径
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        # 更新文本框的内容，显示用户选择的文件夹路径
        file_path.set(folder_selected)

# 创建窗口
window = tk.Tk()
window.title("选择语料库文件夹，然后清洁。By Merlin")
window.geometry("400x200")

# 创建文件路径文本框和选择文件夹按钮
file_path = tk.StringVar()
file_path_label = tk.Label(window, text="请选择语料库路径：")
file_path_label.pack()
file_path_entry = tk.Entry(window, textvariable=file_path)
file_path_entry.pack()

# 将按钮的高度调整为标准大小
select_folder_button = tk.Button(window, text="选择文件夹", command=select_folder_path, height=1)
select_folder_button.pack()

# 创建选择文件夹按钮和清洁语料库按钮之间的空行
empty_label = tk.Label(window, height=1)

empty_label.pack()
# 创建清洁语料库按钮
clean_corpus_button = tk.Button(window, text="清洁语料库", command=clean_corpus, height=1)
clean_corpus_button.pack()

# 进入消息循环
window.mainloop()
