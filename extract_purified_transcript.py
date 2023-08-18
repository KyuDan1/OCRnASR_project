import os
import re
import datetime


def get_lines_list(text_path):
    with open(text_path, "r") as f:
        lines = f.readlines()
    return lines


def list_to_txt(input_list, filename):
    with open(filename, "w") as file:
        for item in input_list:
            file.write(str(item) + "\n\n")


"""
def get_transcript_txt(input_file, pattern):
    new_lines = []
    result = []
    with open(input_file, "r") as f:
        lines = f.readlines()
    for text in lines:
        if not re.fullmatch(pattern, text):
            new_lines.append(text)
#   for list in new_lines:
#       temp2 = list.rstrip("\n")
#       result.append(temp2)
    return new_lines
"""


def get_transcript_txt(input_file):
    def time_valid(text):
        format = "%H:%M:%S,%f"
        from_time = datetime.datetime.strptime(text[0:12] + "000", format)
        to_time = datetime.datetime.strptime(text[-13:-1] + "000", format)
        return from_time <= to_time

    new_lines = []
    result = []
    with open(input_file, "r") as f:
        paragraphs = f.read().split("\n\n")
    for paragraph in paragraphs:
        if paragraph == "":
            continue
        lines = paragraph.split("\n")
        new_lines.append("")
        if time_valid(lines[1]):
            new_lines.append(lines[1:])
        else:
            new_lines.append("**ERROR**")
    return new_lines[1:]


def remove_duplicate_sentences(list):
    result = list.copy()
    for i in reversed(range(len(list) - 1)):
        if i == 0:
            break
        l = len(result[i - 1])
        if result[i][0:l] == result[i - 1]:
            result[i] = result[i][l:]
    return result


def process_list(input_list):
    result = []
    current_sentence = ""

    for item in input_list:
        # Remove leading/trailing whitespace and check if the item is a number
        cleaned_item = item.strip()
        if not cleaned_item.isdigit():
            current_sentence += cleaned_item + " "
        elif current_sentence:
            result.append(current_sentence)
            current_sentence = ""

    # Append the last sentence if it exists
    if current_sentence:
        result.append(current_sentence)

    return result


# 특정 패턴을 지정합니다.
pattern = r"(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3}\n)|\n"
directory = "transcript"
for filename in os.listdir(directory):
    f = os.path.join(directory, filename)
    # transcripts = get_transcript_txt(f, pattern)
    transcripts = get_transcript_txt(f)
    list_to_txt(
        remove_duplicate_sentences(transcripts),
        f"after_transcript/purified_{filename}",
    )
    # print(transcripts)
    # list_to_txt(transcripts,f'after_transcript/purified_{filename}')
