import os

def get_lines_list(text_path):
    with open(text_path, 'r') as f:
        lines = f.readlines()
    return lines


def list_to_txt(input_list, filename):
    with open(filename, 'w') as file:
        for item in input_list:
            file.write(str(item) + '\n')


def get_timing_txt(input_text_path,output_time_info_path):
    arr = get_lines_list(input_text_path)
    temp = []
    for i in range(len(arr)-1):
        if i%4==1:
            temp.append(arr[i])
        else:
            continue
    
    result=[]
    for list in temp:
        temp2 = list.rstrip("\n").replace(",",":")
        result.append(temp2)

    list_to_txt(result, output_time_info_path)

# 주어진 텍스트 파일의 경로와 변환한 시간 정보를 저장할 파일의 경로
#input_text_path = 'transcript/번역- 1. Orientation.txt'
#output_time_info_path = 'time_info/01.txt'
#get_timing_txt(input_text_path,output_time_info_path)

directory = 'transcript'
for filename in os.listdir(directory):
    f = os.path.join(directory,filename)
    get_timing_txt(f,f'time_info/time_infor_{filename}')
    
