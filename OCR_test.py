
import easyocr
import functions

# 프레임 추출-->OCR-->text파일 생성.
# OCR 실행 시 ANTIALIAS 오류발생하면 pip install --force-reinstall -v "Pillow==9.5.0" 
# https://github.com/JaidedAI/EasyOCR
# wjdrbeks1021@gmail.com


#프레임 추출
if __name__ == "__main__":
    input_file_path = "videos\example_Optimizer-Overview.mp4"  # 입력 동영상 파일 경로
    output_folder_path = "images"  # 추출된 프레임 이미지를 저장할 폴더 경로

    functions.extract_frames_from_mp4(input_file_path, output_folder_path)



# OCR 실행
reader = easyocr.Reader(['en'],gpu=False) # this needs to run only once to load the model into memory



result = reader.readtext('images/frame_0.jpg', detail=0)


# 파일에 리스트 데이터 txt 저장
file_path = 'text/output.txt'
functions.save_list_to_txt_file(result, file_path)