import natsort
import os
from jiwer import wer
import Fuse


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


def batch_WER(file1, file2):
    str1 = open(file1, "r").read().replace("\n", " ").replace("  ", " ")
    str2 = open(file2, "r").read().replace("\n", " ").replace("  ", " ")

    str1 = Fuse.substitute(str1.lower())
    str2 = Fuse.substitute(str2.lower())

    batch_wer = wer(str1, str2)
    print("WER of ", file1, ": ", batch_wer)
    return batch_wer


def mean_batch_WER(dir1, dir2):
    dir1_list = natsort.natsorted(os.listdir(dir1))
    dir2_list = natsort.natsorted(os.listdir(dir2))

    sum = 0
    cnt = 0
    for f1, f2 in zip(dir1_list, dir2_list):
        sum += batch_WER(os.path.join(dir1, f1), os.path.join(dir2, f2))
        cnt += 1

    print("mean WER of ", dir1, ": ", sum / cnt)

    return sum / cnt


if __name__ == "__main__":
    """
    write_filename = "WER"

    # print(WER_of(out_dir, str_file))

    mean_WER_of(
        "pure_ASR_transcript",
        "after_transcript",
        os.path.join(write_filename, "pure.txt"),
    )
    mean_WER_of(
        "ASR_with_OCR", "after_transcript", os.path.join(write_filename, "with_OCR.txt")
    )

    compare(
        os.path.join(write_filename, "pure.txt"),
        os.path.join(write_filename, "with_OCR.txt"),
    )
    """

    # mean_batch_WER("pure_ASR_transcript", "after_transcript")
    # mean_batch_WER("ASR_with_OCR", "after_transcript")

    input_directory = "files_to_process"
    pure_directory = "pure_ASR_transcript"
    fused_directory = "ASR_with_OCR"
    ref_directory = "after_transcript"

    for subdirectory in os.listdir(input_directory):
        print(f"WER of lecture {subdirectory}:")
        mean_batch_WER(
            os.path.join(input_directory, subdirectory),
            os.path.join(ref_directory, subdirectory),
        )
        mean_batch_WER(
            os.path.join(fused_directory, subdirectory),
            os.path.join(ref_directory, subdirectory),
        )
        print("")

        # move files
        os.renames(
            os.path.join(input_directory, subdirectory),
            os.path.join(pure_directory, subdirectory),
        )

    os.makedirs(input_directory, exist_ok=True)
