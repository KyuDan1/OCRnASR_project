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

# 주어진 텍스트 파일의 경로와 변환한 시간 정보를 저장할 파일의 경로
input_text_path = 'transcript/번역- 1. Orientation.txt'
output_time_info_path = 'before_transcript/01.txt'


transcripts = get_transcript_txt(input_text_path)

#중복 내용 삭제 전
list_to_txt(transcripts,output_time_info_path)

def remove_duplicate_sentences(list):
    result = []
    result.append(list[0])
    for i in range(len(list)-1):
        result.append(list[i+1].replace(list[i],""))
     
    return result

deleted_output = 'after_transcript/01.txt'

#중복 내용 삭제 후
list_to_txt(remove_duplicate_sentences(transcripts),deleted_output)
