import re
import os

def timing (input_filename):
    # 파일 읽기
    with open(input_filename, 'r') as f:
        content = f.read()

    # transcript 내용 분리
    before_sections = re.split(r'\d+\n\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3}\n', content)[1:]
    sections=[]
    for list in before_sections:
        temp = list.rstrip("\n\n")
        sections.append(temp)

    #시간 정보 분리
    pattern = r'\d{2}:\d{2}:\d{2},\d{3}'
    matches = re.findall(pattern, content)
    #시간:분:초:세부초
    hmss = [re.split(r':|,',i) for i in matches]
    #print(hmss)

    diff = [int(hmss[i+1][2])-int(hmss[i][2]) for i in range(len(hmss)-1)]
    new_diff = []
    for i in diff:
        if i <0:
            new_diff.append(i+60)
        else:
            new_diff.append(i)

    #print(new_diff)
    return(max(diff))
    
directory = 'transcript'
timings = []
for filename in os.listdir(directory):
    f = os.path.join(directory,filename)
    timings.append(timing(f))

print(max(timings))
#52초

'''
결론:
일정한 간격(30초)으로 음성파일을 split 하는 것이 현재 있는 transcipt 파일의 형식으로는 불가하다.
따라서 자막에 있는 시간으로 음성파일을 split하는 것이 최선일 것.
'''

