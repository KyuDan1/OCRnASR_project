import os
import functions
import easyocr


#동영상에서 프레임 추출
if __name__ == "__main__":
    input_file_path = "videos/example_Optimizer-Overview.mp4"  # 입력 동영상 파일 경로
    output_folder_path = "images"  # 추출된 프레임 이미지를 저장할 폴더 경로

    functions.extract_frames_from_mp4(input_file_path, output_folder_path)



#OCR 모델 로딩
reader = easyocr.Reader(['en'],gpu=False) # this needs to run only once to load the model into memory

#OCR 실행 및 text 파일 내보내기
directory = 'images'
for filename in os.listdir(directory):
    f = directory+"/"+filename
    if os.path.isfile(f):
        result = reader.readtext(f, detail=0)
        # 파일에 리스트 데이터 txt 저장
        file_path = f'text/{f.replace("images/","").rstrip(".jpg")}.txt'
        functions.save_list_to_txt_file(result, file_path)
        print(f"{file_path}에 txt생성됨")
    else:
        print("오류")
