
import os
import re
import xlsxwriter

# Set the folder where the text files are located
folder = "/Users/Merlin/Desktop/mylab/wo_wu/"

# Set the name of the file containing the keywords
keyword_file = "/Users/Merlin/Desktop/mylab/chinese_sfp.txt"

# Read the keywords from the file
with open(keyword_file, "r") as f:
    keywords = [line.strip() for line in f.readlines()]

# Create a regular expression pattern to match the keywords
pattern = "|".join(keywords)

# Create a new Excel workbook
workbook = xlsxwriter.Workbook("/Users/Merlin/Desktop/mylab/rr.xlsx")


# Create a new worksheet
worksheet = workbook.add_worksheet()

# Create a format for the keyword cells
keyword_format = workbook.add_format({"font_color": "red"})

# Set the column widths
worksheet.set_column(0, 0, 10)  # column A: index
worksheet.set_column(1, 1, 70)  # column B: sentence
worksheet.set_column(2, 2, 20)  # column C: filename

# Write the column headers
worksheet.write(0, 0, "序号")
worksheet.write(0, 1, "包含关键词的句子")
worksheet.write(0, 2, "来源文本文件名")

# Get a list of all the .txt files in the folder
files = [f for f in os.listdir(folder) if f.endswith(".txt")]

# Loop through each file and search for sentences containing the keywords
current_row = 1  # start at row 1, after the header row
for file in files:
    # Open the file and read its contents
    with open(os.path.join(folder, file), "r") as f:
        text = f.read()

    # Split the text into sentences
    sentences = re.split(r"([。？！])", text)

    # Loop through each sentence and search for keywords
    for i in range(0, len(sentences), 2):
        # Get the sentence and the ending punctuation
        sentence = sentences[i]
        punctuation = sentences[i + 1] if i + 1 < len(sentences) else ""

        # Search for keywords in the sentence
        matches = list(re.finditer(pattern, sentence))

        # If there are matches, write the sentence to the Excel worksheet
        if matches:
            # Write the index to the first column
            worksheet.write(current_row, 0, current_row)

            # Write the sentence to the second column, highlighting the keywords
            worksheet.write_rich_string(current_row, 1, sentence, *[keyword_format] * len(matches), punctuation)

            # Write the filename to the third column
            worksheet.write(current_row, 2, file)

            # Increment the row index
            current_row += 1

# Save the Excel workbook
workbook.close()
