# -*- coding: utf-8 -*-
import os
import easyocr

# OCR 실행 시 ANTIALIAS 오류발생하면 pip install --force-reinstall -v "Pillow==9.5.0"
# OCR 모델 로딩
reader = easyocr.Reader(
    ["en"]
)  # this needs to run only once to load the model into memory


if __name__ == "main":
    # upper_directory = "images_timing"
    input_directory = "files_to_process"
    original_directory = "lecture_images"
    output_directory = "OCR_text"

    upper_directories = os.listdir(input_directory)

    for upper_directory_0 in upper_directories:
        upper_directory = os.path.join(input_directory, upper_directory_0)
        directories = os.listdir(upper_directory)
        # direcory = ['lec1','lec2','lec3','lec4']
        for lecture in directories:
            images = os.listdir(os.path.join(upper_directory, lecture))
            # open the txt file
            with open(
                output_directory + "/" + upper_directory_0 + "/" + lecture + ".txt", "w"
            ) as file:
                for image in images:
                    f = os.path.join(upper_directory, lecture, image)
                    if os.path.isfile(f):
                        result = reader.readtext(f, detail=0)
                        # 파일에 리스트 데이터 txt 저장

                        for item in result:
                            file.write(str(item) + " ")
                        file.write("\n\n")

                        print("OCR text is generated ", image)
                    else:
                        print("ERROR")
                print("-----OCR text is generated ", lecture, "-----")

            # move files
            for image in images:
                os.rename(
                    os.path.join(upper_directory, lecture, image),
                    os.path.join(original_directory, upper_directory_0, lecture, image),
                )
