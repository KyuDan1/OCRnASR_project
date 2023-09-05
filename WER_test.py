import natsort
import os
from jiwer import wer


def WER_of(out_dir, str_file, write_filename):
    with open(write_filename, "a") as txtfile:

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

        # print(" ".join(output), "\n\n", " ".join(strs))

        print("WER of ", out_dir, ": ", wer(" ".join(strs), " ".join(output)))
        txtfile.write(str(wer(" ".join(strs), " ".join(output))) + "\n")

        return wer(" ".join(strs), " ".join(output))


def mean_WER_of(out_dir, str_file, write_filename):
    out_dir_list = natsort.natsorted(os.listdir(out_dir))
    str_file_list = natsort.natsorted(os.listdir(str_file))

    sum = 0
    cnt = 0
    for o, s in zip(
        list(map((lambda x: out_dir + "/" + x + "/"), out_dir_list)),
        list(map((lambda x: str_file + "/" + x), str_file_list))
        # list(map(lambda x: str_file + "/" + x, str_file_list)),
    ):
        sum += WER_of(o, s, write_filename)
        cnt += 1

    print("mean WER of ", out_dir, ": ", sum / cnt)

    return sum / cnt


def read_file_to_list(file_path):
    lines = []
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            lines.append(line.strip())  # 각 줄의 양쪽 공백 및 개행 문자 제거 후 리스트에 추가
    return lines


def compare(pure_txtfile, OCR_txtfile):
    pure = []
    OCR = []
    percent = []
    pure = read_file_to_list(pure_txtfile)
    OCR = read_file_to_list(OCR_txtfile)
    for pure_wer, OCR_wer in zip(pure, OCR):
        ratio = ((float(OCR_wer) - float(pure_wer)) / float(pure_wer)) * 100
        percent.append(ratio)
    for i, pure_wer, OCR_wer, per in zip(range(len(pure)), pure, OCR, percent):
        print(
            # 소수 넷째 자리까지 나타냄.
            f"[{i}] pure: {float(pure_wer):.4f}   OCR: {float(OCR_wer):.4f} ---> {per:.4f} % changed"
        )


if __name__ == "__main__":
    write_filename = "WER"

    # print(WER_of(out_dir, str_file))
    mean_WER_of(
        "pure_ASR_transcript",
        "after_transcript",
        os.path.join(write_filename, "pure.txt"),
    )
    """mean_WER_of(
        "ASR_with_OCR", "after_transcript", os.path.join(write_filename, "with_OCR.txt")
    )"""
    """
    compare(
        os.path.join(write_filename, "pure.txt"),
        os.path.join(write_filename, "with_OCR.txt"),
    )
    """
