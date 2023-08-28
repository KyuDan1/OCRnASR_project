import os
import easyocr

# OCR 실행 시 ANTIALIAS 오류발생하면 pip install --force-reinstall -v "Pillow==9.5.0"
# OCR 모델 로딩
reader = easyocr.Reader(
    ["en"]
)  # this needs to run only once to load the model into memory


upper_directory = "images_timing"
output_directory = "OCR_text"


directories = os.listdir(upper_directory)
# direcory = ['lec1','lec2','lec3','lec4']
for lecture in directories:
    # open the txt file
    with open(output_directory + "/" + lecture + ".txt", "w") as file:
        images = os.listdir(os.path.join(upper_directory, lecture))
        for image in images:
            f = os.path.join(upper_directory, lecture, image)
            if os.path.isfile(f):
                result = reader.readtext(f, detail=0)
                # 파일에 리스트 데이터 txt 저장

                for item in result:
                    file.write(str(item) + " ")
                file.write("\n\n")

                print(f"OCR text is generated {image}")
            else:
                print("ERROR")
        print(f"-----OCR text is generated {lecture}-----")
