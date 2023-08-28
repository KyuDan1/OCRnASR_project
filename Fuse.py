import csv
import math
import matplotlib.pylab as plt
import os

from natsort import natsorted
import librosa

import ASR_vanilla

import nemo
import nemo.collections.asr as nemo_asr

csvfile = "unigram_freq.csv"  # To be changed
total = 588124220187

eps = 2.2250738585072014e-308

lambda_ocr = 0.1

specialcharacters = [
    "!",
    '"',
    "#",
    "$",
    "%",
    "&",
    "'",
    "(",
    ")",
    "*",
    "+",
    ",",
    "-",
    ".",
    "/",
    ":",
    ";",
    "<",
    "=",
    ">",
    "?",
    "@",
    "[",
    "\\",
    "]",
    "^",
    "`",
    "{",
    "|",
    "}",
    "~",
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
    "0",
]


def frequencyOf(str):
    reader = csv.reader(open(csvfile, newline=""), delimiter=",", quotechar="|")
    reader.__next__()
    for row in reader:
        if row[0] == str:
            return ((int)(row[1])) / total
    return 0


def txt2dict(path):
    file = open(path, "r")
    text = file.read().lower()
    text = text.replace("\n", " ")
    for sc in specialcharacters:
        text = text.replace(sc, " ")
    arr = text.split(" ")
    dict = {}
    cnt = 0
    for x in arr:
        if x == "":
            continue
        cnt += 1
        if x in dict:
            dict[x] = dict[x] + 1
        else:
            dict[x] = 1
    for key, value in dict.items():
        dict[key] = value / cnt
    return dict


def str2dict(text):
    text = text.lower()
    text = text.replace("\n", " ")
    for sc in specialcharacters:
        text = text.replace(sc, " ")
    arr = text.split(" ")
    dict = {}
    cnt = 0
    for x in arr:
        if x == "":
            continue
        cnt += 1
        if x in dict:
            dict[x] = dict[x] + 1
        else:
            dict[x] = 1
    for key, value in dict.items():
        dict[key] = value / cnt
    return dict


def txts2dict(paths):
    dict = {}
    cnt = 0
    for path in paths:
        file = open(path, "r")
        text = file.read().lower()
        text = text.replace("\n", " ")
        for sc in specialcharacters:
            text = text.replace(sc, "")
        arr = text.split(" ")

        for x in arr:
            if x == "":
                continue
            cnt += 1
            if x in dict:
                dict[x] = dict[x] + 1
            else:
                dict[x] = 1
    for key, value in dict.items():
        dict[key] = value / cnt
    return dict


def rational_weight(x):
    val = 1 - 2 / (x + 1)
    return val if val > 0 else 0


def relative_frequency(str, dict, weight):
    freq = 0
    over = 0
    if str in dict:
        over = dict[str]
    under = frequencyOf(str)
    if under == 0:
        # under = eps
        return weight(1) if over == 0 else -1
    freq = over / under
    return weight(freq)


def relative_frequency_dict(arr_str, dict_ref, weight, handle_overflow=True):
    ret = {}
    for str in arr_str:
        if str == "":
            continue
        ret[str] = relative_frequency(str, dict_ref, weight)
    if handle_overflow:
        maxval = 0
        for value in relative_frequency_dict(
            dict_ref.keys(), dict_ref, weight, False
        ).values():
            if maxval < value:
                maxval = value
        for key, value in ret.items():
            if value == -1:
                # overflow
                ret[key] = maxval
    return ret


"""
def test_temp(str):
    print(str + ': ',relative_frequency(str,txt2dict('C:/Users/skyba/vscode-workspace/text.txt'),rational_weight))   
"""


def test_temp(str):
    print(
        str + ": ",
        relative_frequency(
            str, txt2dict("C:/Users/skyba/vscode-workspace/text.txt"), lambda x: x
        ),
    )


def test_temp_2():
    dict = {}
    ref = txt2dict("C:/Users/skyba/vscode-workspace/text.txt")
    # return relative_frequency_dict(ref.keys(), ref, lambda x: x)
    return relative_frequency_dict(ref.keys(), ref, lambda x: math.log(x + 1))


def test_temp_3():
    dict = test_temp_2()

    """
    for key, value in dict.items():
        if value != -1:
            dict[key] = math.log(value + 1)
    """

    list = sorted(dict.items(), key=lambda x: x[1])

    x, y = zip(*list)
    plt.xticks(rotation=45)
    plt.plot(x, y)
    plt.show()


def freq_score(seq, dict):
    # returns the word frequency score of sequence
    seq = seq.replace("_", " ")
    arr = seq.split(" ")
    cnt = 0
    sum = 0

    rfd = relative_frequency_dict(arr, dict, lambda x: math.log(x + 1))

    for a in arr:
        if a == "":
            continue
        cnt += 1
        sum += rfd[a]  # relative_frequency(a, dict, lambda x: x)
    return sum / cnt if cnt > 0 else -1


def fuse(arr, paths):
    ret = []
    dict = txts2dict(paths)
    for score, seq in arr:
        ret.append((score + lambda_ocr * freq_score(seq, dict), seq))
    return ret


def fuse_from_string(arr, str):
    ret = []
    dict = str2dict(str)
    for score, seq in arr:
        ret.append((score + lambda_ocr * freq_score(seq, dict), seq))
    return ret


if __name__ == "__main__":

    upper_directory = "resampled_splitted_audio"
    output_directory = "ASR_with_OCR"
    ocr_directory = "OCR_text"

    # Create the output directory if it doesn't exist
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    directory = zip(
        natsorted(os.listdir(upper_directory)), natsorted(os.listdir(ocr_directory))
    )
    count_file = 0

    for u, o in directory:
        audios = natsorted(os.listdir(os.path.join(upper_directory, u)))

        cnt = 0

        for line in open(os.path.join(ocr_directory, o), "r").read().split("\n\n"):
            cnt += 1
            if(line==""): continue
            if(len(audios)<=cnt): continue
            audio = audios[cnt-1]
            if not ASR_vanilla.check_wav_file_has_data(os.path.join(upper_directory, u, audio)):
                continue

            input_file = os.path.join(upper_directory, u, audio)
            output_dir = os.path.join(output_directory, u)

            # Create the output subdirectory if it doesn't exist
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)

            #seqs = conformer_wav_to_sequence_list(input_file)
            seqs=ASR_vanilla.beam_wav_to_sequence_list(input_file)
            print("!: ", seqs)
            fused = fuse_from_string(seqs, line)
            print("!: ",fused)

            max_str = max(fused, key=lambda x: x[0])[1]

            ASR_vanilla.save_string_to_txt(
                output_dir + "/ASR_with_OCR_" + f"{audio}".replace("wav", "txt"),
                max_str[1:].replace("▁"," "),
            )
