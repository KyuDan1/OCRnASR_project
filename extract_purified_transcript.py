import os

def get_lines_list(text_path):
    with open(text_path, 'r') as f:
        lines = f.readlines()
    return lines

def list_to_txt(input_list, filename):
    with open(filename, 'w') as file:
        for item in input_list:
            file.write(str(item) + '\n')

def get_transcript_txt(input_text_path):
    arr = get_lines_list(input_text_path)
    temp = []
    for i in range(len(arr)):
        if i%4==2:
            temp.append(arr[i])
        else:
            continue
    
    result=[]
    for list in temp:
        temp2 = list.rstrip("\n")
        result.append(temp2)
    return result


def remove_duplicate_sentences(list):
    result = []
    result.append(list[0])
    for i in range(len(list)-1):
        result.append(list[i+1].replace(list[i],""))
     
    return result


#중복 내용 삭제 후
#list_to_txt(remove_duplicate_sentences(transcripts),deleted_output)


directory = 'transcript'
for filename in os.listdir(directory):
    f = os.path.join(directory,filename)
    transcripts = get_transcript_txt(f)
    list_to_txt(remove_duplicate_sentences(transcripts),f'after_transcript/purified_{filename}')

