'''
能够实现Range软件同等功能的代码
Developed by Merlin
With the aid of ChatGPT
'''

import os
import re
import tkinter as tk
from tkinter import filedialog


def calculate_word_coverage():
    corpus_dir = corpus_dir_entry.get()
    gsl1000_path = gsl1000_path_entry.get()
    gsl2000_path = gsl2000_path_entry.get()
    awl_path = awl_path_entry.get()
    output_path = output_path_entry.get()

    gsl_awl_dict = {}
    with open(gsl1000_path) as f:
        for line in f:
            word = line.strip()
            gsl_awl_dict[word] = 1
    with open(gsl2000_path) as f:
        for line in f:
            word = line.strip()
            gsl_awl_dict[word] = 2
    with open(awl_path) as f:
        for line in f:
            word = line.strip()
            gsl_awl_dict[word] = 3

    gsl1000_words = {}
    gsl2000_words = {}
    awl_words = {}
    other_words = {}

    for filename in os.listdir(corpus_dir):
        file_path = os.path.join(corpus_dir, filename)
        with open(file_path, 'r') as f:
            text = f.read().lower()
            text = re.sub(r'\W', r' ', text)
            words = text.split()

            for word in words:
                if word not in gsl_awl_dict:
                    other_words[word] = other_words.get(word, 0) + 1
                elif gsl_awl_dict[word] == 1:
                    gsl1000_words[word] = gsl1000_words.get(word, 0) + 1
                elif gsl_awl_dict[word] == 2:
                    gsl2000_words[word] = gsl2000_words.get(word, 0) + 1
                elif gsl_awl_dict[word] == 3:
                    awl_words[word] = awl_words.get(word, 0) + 1

    gsl1000_freq_total = sum(gsl1000_words.values())
    gsl2000_freq_total = sum(gsl2000_words.values())
    awl_freq_total = sum(awl_words.values())
    other_freq_total = sum(other_words.values())

    gsl1000_num_of_words = len(gsl1000_words)
    gsl2000_num_of_words = len(gsl2000_words)
    awl_num_of_words = len(awl_words)
    other_num_of_words = len(other_words)

    freq_total = gsl1000_freq_total + gsl2000_freq_total + awl_freq_total + other_freq_total
    num_of_words_total = gsl1000_num_of_words + gsl2000_num_of_words + awl_num_of_words + other_num_of_words

    file_out = open(output_path, 'w')

    file_out.write('RESULTS OF WORD ANALYSIS\n\n')
    file_out.write('Total No. of word types in corpus: ' + str(num_of_words_total) + '\n\n')
    file_out.write('Total No. of GSL1000 word types : ' + str(gsl1000_num_of_words) + '\n\n')
    file_out.write('Total No. of GSL2000 word types : ' + str(gsl2000_num_of_words) + '\n')
    file_out.write('Total No. of AWL word types : ' + str(awl_num_of_words) + '\n')
    file_out.write('Total No. of other word types : ' + str(other_num_of_words) + '\n')

    # Recognizing_gsl_words.py,part 4-2
    file_out.write('\n\n')
    file_out.write('Total word frequency of Great Expectations: ' + str(freq_total) + '\n\n')

    file_out.write('Total frequency of GSL1000 words: ' + str(gsl1000_freq_total) + '\n')
    file_out.write('Frequency percentage of GSL1000 words: ' + str(gsl1000_freq_total / float(freq_total)) + '\n\n')

    file_out.write('Total frequency of GSL2000 words: ' + str(gsl2000_freq_total) + '\n')
    file_out.write('Frequency percentage of GSL2000 words: ' + str(gsl2000_freq_total / float(freq_total)) + '\n\n')

    file_out.write('Total frequency of AWL words: ' + str(awl_freq_total) + '\n')
    file_out.write('Frequency percentage of AWL words: ' + str(awl_freq_total / float(freq_total)) + '\n\n')

    file_out.write('Total frequency of other words: ' + str(other_freq_total) + '\n')
    file_out.write('Frequency percentage of other words: ' + str(other_freq_total / float(freq_total)) + '\n')

    # Recognizing_gsl_awl_words.py, Part 4-3

    # write out the GSL1000 words
    file_out.write('\n\n')
    file_out.write('##########\n')
    file_out.write('Words in GSL1000\n\n')
    for word in sorted(gsl1000_words.keys()):
        file_out.write(word + '\t' + str(gsl1000_words[word]) + '\n')

    # write out the GSL2000 words
    file_out.write('\n\n')
    file_out.write('##########\n')
    file_out.write('Words in GSL2000\n\n')
    for word in sorted(gsl2000_words.keys()):
        file_out.write(word + '\t' + str(gsl2000_words[word]) + '\n')

    # write out the AWL words
    file_out.write('\n\n')
    file_out.write('##########\n')
    file_out.write('Words in AWL\n\n')
    for word in sorted(awl_words.keys()):
        file_out.write(word + '\t' + str(awl_words[word]) + '\n')

    # write out other words
    file_out.write('\n\n')
    file_out.write('##########\n')
    file_out.write('Other words\n\n')
    for word in sorted(other_words.keys()):
        file_out.write(word + '\t' + str(other_words[word]) + '\n')

    file_out.close()

    tk.messagebox.showinfo("Word Coverage Analysis", "Word coverage analysis complete. Results written to {}".format(output_path))


root = tk.Tk()
root.title("Word Coverage Analysis")

corpus_dir_label = tk.Label(root, text="Corpus Directory:")
corpus_dir_label.grid(row=0, column=0, padx=5, pady=5)
corpus_dir_entry = tk.Entry(root, width=50)
corpus_dir_entry.grid(row=0, column=1, padx=5, pady=5)
corpus_dir_button = tk.Button(root, text="Browse", command=lambda: corpus_dir_entry.insert(tk.END, filedialog.askdirectory()))
corpus_dir_button.grid(row=0, column=2, padx=5, pady=5)

gsl1000_path_label = tk.Label(root, text="GSL1000 Word List:")
gsl1000_path_label.grid(row=1, column=0, padx=5, pady=5)
gsl1000_path_entry = tk.Entry(root, width=50)
gsl1000_path_entry.grid(row=1, column=1, padx=5, pady=5)
gsl1000_path_button = tk.Button(root, text="Browse", command=lambda: gsl1000_path_entry.insert(tk.END, filedialog.askopenfilename()))
gsl1000_path_button.grid(row=1, column=2, padx=5, pady=5)

gsl2000_path_label = tk.Label(root, text="GSL2000 Word List:")
gsl2000_path_label.grid(row=2, column=0, padx=5, pady=5)
gsl2000_path_entry = tk.Entry(root, width=50)
gsl2000_path_entry.grid(row=2, column=1, padx=5, pady=5)
gsl2000_path_button = tk.Button(root, text="Browse", command=lambda: gsl2000_path_entry.insert(tk.END, filedialog.askopenfilename()))
gsl2000_path_button.grid(row=2, column=2, padx=5, pady=5)

awl_path_label = tk.Label(root, text="AWL Word List:")
awl_path_label.grid(row=3, column=0, padx=5, pady=5)
awl_path_entry = tk.Entry(root, width=50)
awl_path_entry.grid(row=3, column=1, padx=5, pady=5)
awl_path_button = tk.Button(root, text="Browse", command=lambda: awl_path_entry.insert(tk.END, filedialog.askopenfilename()))
awl_path_button.grid(row=3, column=2, padx=5, pady=5)

output_path_label = tk.Label(root, text="Output File:")
output_path_label.grid(row=4, column=0, padx=5, pady=5)
output_path_entry = tk.Entry(root, width=50)
output_path_entry.grid(row=4, column=1, padx=5, pady=5)
output_path_button = tk.Button(root, text="Browse", command=lambda: output_path_entry.insert(tk.END, filedialog.asksaveasfilename(defaultextension=".txt")))
output_path_button.grid(row=4, column=2, padx=5, pady=5)

analyze_button = tk.Button(root, text="Start Analysis", command=calculate_word_coverage)
analyze_button.grid(row=5, column=1, padx=5, pady=5)

root.mainloop()
