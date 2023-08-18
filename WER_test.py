import natsort
import os
from jiwer import wer


def WER_of(out_dir, str_file):
    def file_to_text(file):
        with open(file, "r") as f:
            return f.read()

    outputs = natsort.natsorted(os.listdir(out_dir))
    # edit part
    new_outputs = []
    for i in outputs:
        new_outputs.append(out_dir + i)
    output = list(map(file_to_text, new_outputs))

    with open(str_file, "r") as f:
        strs = [x for x in f.read().split("\n\n") if x != "**ERROR**"]

    print(output)
    print("\n\n")
    print(" ".join(strs))

    return wer(" ".join(strs), " ".join(output))


def mean_WER_of(out_dir_list, str_file_list):
    sum = 0
    cnt = 0
    for o, s in zip(out_dir_list, str_file_list):
        sum += WER_of(o, s)
        cnt += 1
    return sum / cnt


# example
out_dir = "pure_ASR_transcript/audio_1-Orientation/"
str_file = "after_transcript/purified_번역- 1. Orientation.txt"
print(WER_of(out_dir, str_file))
print(mean_WER_of(os.listdir("pure_ASR_transcript"), os.listdir("after_transcript")))
