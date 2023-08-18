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


def mean_WER_of(out_dir, str_file):
    out_dir_list = os.listdir(out_dir)
    str_file_list = os.listdir(str_file)

    sum = 0
    cnt = 0
    for o, s in zip(
        list(map((lambda x: out_dir + "/" + x + "/"), out_dir_list)),
        list(map((lambda x: str_file + "/" + x), str_file_list))
        # list(map(lambda x: str_file + "/" + x, str_file_list)),
    ):
        sum += WER_of(o, s)
        cnt += 1
    return sum / cnt


# example
out_dir = "pure_ASR_transcript/audio_1-Orientation/"
str_file = "after_transcript/purified_번역- 1. Orientation.txt"
print(WER_of(out_dir, str_file))
print(mean_WER_of("pure_ASR_transcript", "after_transcript"))
