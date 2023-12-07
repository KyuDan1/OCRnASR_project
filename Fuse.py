import csv
import math
import matplotlib.pylab as plt
import os

from natsort import natsorted
import librosa

import ASR_vanilla

import nemo
import nemo.collections.asr as nemo_asr

import Sub

csvfile = "unigram_freq.csv"  # To be changed

total = 588124220187
least = 12711

power_const = -1

eps = 2.2250738585072014e-308

lambda_ocr = 0.1

# ablation
# NF_0 Conventional
# NF_1 least count substitution
# NF_2 NF1+rescaling
NF_MODE = -1
# SOCR_0 Conventional
# SOCR_1 new s_OCR
# SOCR_2 SOCR_1+RF>=1
SOCR_MODE = -1


def frequencyOf(str):
    reader = csv.reader(open(csvfile, newline=""), delimiter=",", quotechar="|")
    reader.__next__()
    for row in reader:
        if row[0] == str:
            return ((int)(row[1])) / total
    return 0


def originalFrequencyOf(str):
    reader = csv.reader(open(csvfile, newline=""), delimiter=",", quotechar="|")
    reader.__next__()
    for row in reader:
        if row[0] == str:
            return int(row[1])
    return least


def nf_dict_from_lf_dict():
    global lf_dict
    global nf_dict

    global rf_dict
    global max_rf

    words = lf_dict.keys()

    _d = {}
    sum = 0

    reader = csv.reader(open(csvfile, newline=""), delimiter=",", quotechar="|")
    reader.__next__()
    for row in reader:
        if row[0] in words:
            _n = int(row[1])
            _d[row[0]] = _n
            sum += _n
    keys = list(_d.keys()).copy()  # OCR words in the corpus

    for w in words:  # OCR words
        if w not in keys:
            if NF_MODE >= 1:
                _d[w] = least
                sum += least
            else:
                _d[w] = 0

    nf_dict = {}
    for w in _d.keys():
        nf_dict[w] = _d[w] / sum if NF_MODE == 2 else _d[w] / total

    if SOCR_MODE == 0:
        # precalculating rfs for OCR words in the corpus
        rf_dict = {}
        for word in lf_dict.keys():
            if word not in keys:
                continue
            upper = lf_dict[word]
            under = nf_dict[word]

            rf_dict[word] = upper / under

        max_rf = max(rf_dict.values())


def txt2dict(path):
    file = open(path, "r")
    text = file.read().lower()
    text = text.replace("\n", " ")
    for sc in Sub.specialcharacters:
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
    # input: string
    # output: {word,LF(word)} dictionary

    text = text.lower()
    text = text.replace("\n", " ")

    # 2023-11-19
    text = Sub.substitute(text)

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

    global lf_dict
    lf_dict = dict
    nf_dict_from_lf_dict()

    return dict


def txts2dict(paths):
    dict = {}
    cnt = 0
    for path in paths:
        file = open(path, "r")
        text = file.read().lower()
        text = text.replace("\n", " ")
        for sc in Sub.specialcharacters:
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
        over = dict[str]  # LF
    under = frequencyOf(str)  # NF
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


def truncated_rf(word):
    # truncated RF; RF=1 whenever LF<NF
    # RF=1 for NF=0

    global lf_dict
    global nf_dict

    global rf_dict
    global max_rf

    if SOCR_MODE == 0:
        if word in rf_dict.keys():
            return rf_dict[word]
        else:
            # not an OCR word or not in the corpus
            if word in lf_dict.keys():
                # not in the corpus
                return max_rf
            else:
                # not an OCR word
                return 0

    # SOCR_MODE>=1

    upper = 0
    under = 0

    if word in lf_dict.keys():
        # OCR word
        upper = lf_dict[word]
        under = nf_dict[word]
    else:
        # not an OCR word
        return 1

    if upper < under and SOCR_MODE == 2:
        ret = 1
    if under == 0:
        ret = 1
    else:
        ret = upper / under

    return ret


def truncated_rf_score(seq):
    # returns the rf score of sequence
    # truncated RF; RF=1 whenever LF<NF

    seq = Sub.substitute(seq.lower().replace("_", " "))
    arr = seq.split(" ")
    cnt = 0
    sum = 0

    for a in arr:
        if a == "":
            continue
        cnt += 1
        sum += (
            (1 - 1 * math.pow(truncated_rf(a), 1 / power_const))
            if SOCR_MODE >= 1
            else math.log(truncated_rf(a) + 1)
        )
    return sum / cnt if cnt > 0 else -1


def fuse(arr, paths):
    ret = []
    dict = txts2dict(paths)
    for score, seq in arr:
        ret.append((score + lambda_ocr * freq_score(seq, dict), seq))
    return ret


def fuse_from_string(arr, str):
    ret = []
    str2dict(str)
    for score, seq in arr:
        # ret.append((score + lambda_ocr * freq_score(seq, dict), seq))
        ret.append((score + lambda_ocr * truncated_rf_score(seq), seq))
    return ret


if __name__ == "__main__":
    if NF_MODE < 0 or NF_MODE > 2:
        NF_MODE = 0
        print("Invalid NF_MODE. Automatically set to 0.")

    if SOCR_MODE < 0 or SOCR_MODE > 2:
        SOCR_MODE = 0
        print("Invalid SOCR_MODE. Automatically set to 0.")

    input_directory = "files_to_process"
    output_directory = "ASR_with_OCR"
    ocr_directory = "OCR_text"
    original_directory = "resampled_splitted_audio"

    for subdirectory in os.listdir(input_directory):
        # Create the output directory if it doesn't exist
        od = os.path.join(output_directory, subdirectory)
        if not os.path.exists(od):
            os.makedirs(od)

        d = os.path.join(input_directory, subdirectory)

        directory = zip(
            natsorted(os.listdir(d)),
            natsorted(os.listdir(os.path.join(ocr_directory, subdirectory))),
        )
        count_file = 0

        for u, o in directory:
            output_dir = os.path.join(od, u) + ".txt"

            audios = natsorted(os.listdir(os.path.join(d, u)))

            lecture_transcript = ""
            cnt = -1
            """
            for line in (
                open(os.path.join(ocr_directory, subdirectory, o), "r")
                .read()
                .split("\n\n")
            ):
                cnt += 1
                if line == "":
                    continue
                if len(audios) <= cnt:
                    continue
                audio = audios[cnt]

                input_file = os.path.join(d, u, audio)

                if not ASR_vanilla.check_wav_file_has_data(input_file):
                    continue

                # seqs = conformer_wav_to_sequence_list(input_file)
                seqs = ASR_vanilla.beam_wav_to_sequence_list(input_file)
                print("!: ", seqs)
                fused = fuse_from_string(seqs, line)
                print("!: ", fused)

                max_str = max(fused, key=lambda x: x[0])[1]
                lecture_transcript += "\n" + max_str[1:].replace("▁", " ")
            """

            str = open(os.path.join(ocr_directory, subdirectory, o), "r").read()
            str2dict(str)
            for audio in audios:
                input_file = os.path.join(d, u, audio)

                if not ASR_vanilla.check_wav_file_has_data(input_file):
                    continue

                # seqs = conformer_wav_to_sequence_list(input_file)
                seqs = ASR_vanilla.beam_wav_to_sequence_list(input_file)

                print("!: ", seqs)

                fused = []

                for score, seq in seqs:
                    # ret.append((score + lambda_ocr * freq_score(seq, dict), seq))
                    fused.append((score + lambda_ocr * truncated_rf_score(seq), seq))

                print("!: ", fused)

                max_str = max(fused, key=lambda x: x[0])[1]
                lecture_transcript += "\n" + max_str[1:].replace("▁", " ")

            ASR_vanilla.save_string_to_txt(
                output_dir,
                lecture_transcript[1:],
            )

        # move files
        os.renames(d, os.path.join(original_directory, subdirectory))

    os.makedirs(input_directory, exist_ok=True)
