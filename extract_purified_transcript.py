import os
import re

error_code = "**ERROR**"
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
]

time_format = [
    "0",
    "0",
    ":",
    "0",
    "0",
    ":",
    "0",
    "0",
    ",",
    "0",
    "0",
    "0",
]


def get_lines_list(text_path):
    with open(text_path, "r") as f:
        lines = f.readlines()
    return lines


def list_to_txt(input_list, filename):
    with open(filename, "w") as file:
        file.write("\n".join(input_list))


"""
def get_transcript_txt(input_file, pattern):
    new_lines = []
    result = []
    with open(input_file, "r") as f:
        lines = f.readlines()
    for text in lines:
        if not re.fullmatch(pattern, text):
            new_lines.append(text)
#   for list in new_lines:
#       temp2 = list.rstrip("\n")
#       result.append(temp2)
    return new_lines
"""


def get_transcript_txt(input_file):
    def time_valid(text):
        def format_test(str):
            if (
                list(
                    map(
                        lambda x: x
                        if x in specialcharacters
                        else "0"
                        if x.isdigit()
                        else "1",
                        str,
                    )
                )
                != time_format
            ):
                return False
            h, m, s, ms = map(int, str.replace(",", ":").split(":"))
            if (m >= 60) or (s >= 60):
                return False
            # valid
            return True

        text = text.strip()
        if len(text) != 29:
            return False
        if not (
            (text[0:12] <= text[-12:])
            and format_test(text[0:12])
            and format_test(text[0:12])
        ):
            return False
        # valid
        return True

    new_lines = []
    print(input_file)
    with open(input_file, "r") as f:
        paragraphs = f.read().lower().split("\n\n")
    for paragraph in paragraphs:
        if paragraph == "":
            continue
        lines = [x.strip() for x in paragraph.split("\n") if x != ""]
        if not lines[0].isdigit():
            continue
        ext_time = lines[1].strip()
        if time_valid(ext_time):
            new_lines.append(" ".join(lines[2:]))
        else:
            new_lines.append(error_code)

    return new_lines


def get_transcript_txt_with_time_extraction(input_file, time_filename):
    def time_valid(text):
        def format_test(str):
            if (
                list(
                    map(
                        lambda x: x
                        if x in specialcharacters
                        else "0"
                        if x.isdigit()
                        else "1",
                        str,
                    )
                )
                != time_format
            ):
                return False
            h, m, s, ms = map(int, str.replace(",", ":").split(":"))
            if (m >= 60) or (s >= 60):
                return False
            # valid
            return True

        text = text.strip()
        if len(text) != 29:
            return False
        if not (
            (text[0:12] <= text[-12:])
            and format_test(text[0:12])
            and format_test(text[0:12])
        ):
            return False
        # valid
        return True

    ext_times = ""
    new_lines = []
    print(input_file)
    with open(input_file, "r") as f:
        paragraphs = f.read().lower().split("\n\n")
    for paragraph in paragraphs:
        if paragraph == "":
            continue
        lines = [x.strip() for x in paragraph.split("\n") if x != ""]
        if not lines[0].isdigit():
            continue
        ext_time = lines[1].strip()
        if time_valid(ext_time):
            ext_times += "\n" + ext_time
            new_lines.append(" ".join(lines[2:]))
        else:
            new_lines.append(error_code)

    open(time_filename, "w").write(ext_times)

    return new_lines


def remove_duplicate_sentences(list):
    result = list.copy()
    i = len(list)
    while i >= 2:
        i = i - 1
        str0 = result[i - 1]
        str1 = result[i]
        if str0 == error_code:
            continue
        l = len(str0)
        if str1[0:l] == str0:
            result[i] = str1[l:].strip()
    return result


def process_list(input_list):
    result = []
    current_sentence = ""

    for item in input_list:
        # Remove leading/trailing whitespace and check if the item is a number
        cleaned_item = item.strip()
        if not cleaned_item.isdigit():
            current_sentence += cleaned_item + " "
        elif current_sentence:
            result.append(current_sentence)
            current_sentence = ""

    # Append the last sentence if it exists
    if current_sentence:
        result.append(current_sentence)

    return result


def del_punct(text):
    return "".join(char for char in text if char not in specialcharacters)


"""
def remove_duplicate_sentences(sentences):
    unique_sentences = []
    for sentence in sentences:
        if sentence not in unique_sentences:
            unique_sentences.append(sentence)
    return unique_sentences
"""

if __name__ == "__main__":
    # 특정 패턴을 지정합니다.
    # pattern = r"(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3}\n)|\n"
    directory = "transcript"
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        # transcripts = get_transcript_txt(f, pattern)
        # transcripts = get_transcript_txt(f)
        transcripts = get_transcript_txt_with_time_extraction(
            f, f"time_info/time_infor_{filename}"
        )
        list_to_txt(
            remove_duplicate_sentences(
                [del_punct(transcript) for transcript in transcripts]
            ),
            f"after_transcript/purified_{filename}",
        )
        # print(transcripts)
        # list_to_txt(transcripts,f'after_transcript/purified_{filename}')
