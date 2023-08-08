import csv
import math
import matplotlib.pylab as plt

csvfile = 'C:/Users/skyba/vscode-workspace/unigram_freq.csv' #To be changed
total = 588124220187
    
def frequencyOf(str):
    
    reader = csv.reader(open(csvfile, newline=''),delimiter=',',quotechar='|')
    reader.__next__()
    for row in reader:
        if(row[0] == str): return ((int)(row[1]))/total
    return 0

#print(frequencyOf('the'))

specialcharacters = ['!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.', '/', ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^', '', '`', '{', '|', '}', '~', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0']

def txt2dict(path):
    file = open(path,'r')
    text = file.read().lower()
    text = text.replace('\n',' ')
    for sc in specialcharacters:
        text = text.replace(sc,' ')
    arr = text.split(' ')
    dict = {}
    cnt = 0
    for x in arr:
        if x == '': continue
        cnt += 1
        if x in dict:
            dict[x]=dict[x]+1
        else:
            dict[x]=1
    for key,value in dict.items():
        dict[key] = value/cnt
    return dict

def txts2dict(paths):
    dict = {}
    cnt = 0
    for path in paths:
        file = open(path,'r')
        text = file.read().lower()
        text = text.replace('\n',' ')
        for sc in specialcharacters:
            text = text.replace(sc,'')
        arr = text.split(' ')
        
        
        for x in arr:
            if x == '': continue
            cnt += 1
            if x in dict:
                dict[x]=dict[x]+1
            else:
                dict[x]=1
    for key,value in dict.items():
        dict[key] = value/cnt
    return dict

#print(txt2dict('C:/Users/skyba/vscode-workspace/text.txt'))

def rational_weight(x):
    val = 1-2/(x+1)
    return val if val > 0 else 0

eps = 2.2250738585072014e-308

def relative_frequency(str,dict,weight):
    freq = 0
    over = 0
    if str in dict:
        over = dict[str]
    under = frequencyOf(str)
    if under == 0:
        #under = eps
        return -1
    freq = over/under
    return weight(freq)
"""
def test_temp(str):
    print(str + ': ',relative_frequency(str,txt2dict('C:/Users/skyba/vscode-workspace/text.txt'),rational_weight))   
"""
def test_temp(str):
    print(str + ': ',relative_frequency(str,txt2dict('C:/Users/skyba/vscode-workspace/text.txt'), lambda x : x))   

def test_temp_2():
    dict = {}
    ref = txt2dict('C:/Users/skyba/vscode-workspace/text.txt')
    for i in ref.keys():
        dict[i] = relative_frequency(i,ref, lambda x : x)
    #print(dict)
    return dict

def test_temp_3():
    dict = test_temp_2()

    for key,value in dict.items():
        if value != -1: dict[key] = math.log(value+1)

    list = sorted(dict.items(),key=lambda x:x[1])

    x, y = zip(*list)
    plt.xticks(rotation=45)
    plt.plot(x, y)
    plt.show()

lambda_ocr=0.1

def freq_score(seq,dict):
    # returns the word frequency score of sequence
    seq = seq.replace('_',' ')
    arr = seq.split(' ')
    cnt = 0
    sum = 0
    for a in arr:
        if a == '': continue
        cnt += 1
        sum += relative_frequency(a,dict,lambda x : x)
    return sum/cnt if cnt > 0 else -1
    
def fuse(arr,paths):
    ret = []
    dict = txts2dict(paths)
    for score,seq in arr:
        ret.append(score+lambda_ocr*freq_score(seq,dict),seq)
    return ret