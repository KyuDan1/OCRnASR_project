import os
import re

def get_lines_list(text_path):
    with open(text_path, 'r') as f:
        lines = f.readlines()
    return lines

def list_to_txt(input_list, filename):
    with open(filename, 'w') as file:
        for item in input_list:
            file.write(str(item) + '\n\n')

    
def get_transcript_txt(input_file, pattern):
    new_lines =[]
    result = []
    with open(input_file, 'r') as f:
        lines = f.readlines()
    for text in lines:
        if not re.fullmatch(pattern, text):
            new_lines.append(text)
    """for list in new_lines:
        temp2 = list.rstrip("\n")
        result.append(temp2)"""
    return new_lines


def remove_duplicate_sentences(list):
    result = []
    result.append(list[0])
    for i in range(len(list)-1):
        result.append(list[i+1].replace(list[i],""))
     
    return result

def process_list(input_list):
    result = []
    current_sentence = ""

    for item in input_list:
        # Remove leading/trailing whitespace and check if the item is a number
        cleaned_item = item.strip()
        if not cleaned_item.isdigit():
            current_sentence += cleaned_item + ' '
        elif current_sentence:
            result.append(current_sentence)
            current_sentence = ""

    # Append the last sentence if it exists
    if current_sentence:
        result.append(current_sentence)

    return result

# 특정 패턴을 지정합니다.
pattern = r'(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3}\n)|\n'
directory = 'transcript'
for filename in os.listdir(directory):
    f = os.path.join(directory,filename)
    transcripts = get_transcript_txt(f,pattern)
    list_to_txt(remove_duplicate_sentences(process_list(transcripts)),f'after_transcript/purified_{filename}')
    #print(transcripts)
    #list_to_txt(transcripts,f'after_transcript/purified_{filename}')

