'''
这段程序的作用是对一个指定路径下的所有txt文件进行文本清洗，并将清洗后的文本写入新的文件中。具体解释如下：

    1. 导入os和re模块，分别用于操作文件和进行正则表达式匹配。
    2. 获取用户输入的语料库路径，并获取语料库文件夹名称和所在的上一级目录。
    3. 拼接清洁后语料库文件夹的路径，并创建该文件夹。
    4. 遍历语料库文件夹下的所有文件，对于每个txt文件进行以下操作：
        - 拼接文件路径。
        - 尝试以utf-8编码读取文件内容，如果读取失败则跳过该文件。
        - 使用正则表达式进行文本清洗，包括去除两个单词之间的空格、替换非字母、非标点符号的字符为空格、替换数字为空格、将多个空格替换为一个空格。
        - 拼接清洁后的文件名和文件路径，并将清洁后的内容写入文件。
        - 如果文件不是utf-8编码，则将其重命名为ERROR_文件名，并跳过该文件。
    5. 所有txt文件都处理完毕后，输出文本清洁完成的提示。

'''

import os
import re

# 获取用户输入的语料库路径
path = input("请输入语料库路径:")

# 获取语料库文件夹名称
folder_name = os.path.basename(path)

# 获取语料库文件夹所在的上一级目录
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
                # 使用正则表达式清洁文本
                pattern = r'\b(\w) (\w)\b'  # 匹配两个单词之间的空格
                fixed_text = re.sub(pattern, r'\1\2', file_content)  # 将两个单词之间的空格去掉
                cleaned_content = re.sub(r'[^A-Za-z.,!?;:]', ' ', fixed_text)  # 将非字母、非标点符号的字符替换为空格
                cleaned_content = re.sub(r'\d+', '', cleaned_content)  # 将数字替换为空格
                cleaned_content = re.sub(r' +', ' ', cleaned_content)  # 将多个空格替换为一个空格
                # 拼接清洁后的文件名和文件路径
                cleaned_filename = filename + "_cleaned.txt"
                cleaned_file_path = os.path.join(cleaned_path, cleaned_filename)
                # 将清洁后的内容写入文件
                with open(cleaned_file_path, 'w', encoding="utf-8") as f:
                    f.write(cleaned_content)
        # 如果文件不是utf-8编码,则跳过该文件
        except UnicodeDecodeError:
            new_filename = "ERROR_" + filename
            os.rename(file_path, os.path.join(path, new_filename))
            print(f"文件 {filename} 不是 utf-8 编码,已重命名为 {new_filename} 并跳过")
print("文本清洁完成!")
