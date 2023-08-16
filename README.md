# OCRnASR_project
### 이후에 아래 .py 코드 functions에 옮길 수 있음.
##
## 현재 6번 까지 폴더에 있는 여러개의 강의 영상들에 대해서 반복하여 실행하는 것으로 수정함.

1. 원본 transcript 에서 시간 정보 추출 ---> <b>extracting_time_info.py</b>
2. transcipt 텍스트 추출 ---> <b>extract_purified_transcript.py</b>
   <br>(오로지 transcript만 한 줄 마다 txt파일로 나오게 함.)
3. 음성추출---> <b>audio_extract.py</b>
   <br>(.wav 파일로 추출됨)
4. 음성 파일을 시간 정보에 따라 분할하기 ---> <b>split_wav_by_transcript_timing.py</b>
#### 4번 작업 오래걸림
5. 동영상에서 시간 정보에 따라 첫 시간의 frame 추출하기 ---> <b>extract_image_by_transcript_timing.py</b>
6. sampling rate 16000으로 조절 ---> <b>resampling.py</b>
7. 각 음성에 대해서 ASR 실행 (OCR 적용 안함, WER을 구하기 위한 데이터) ---> <b>ASR_vanilla.py</b>

8. 5번에서 추출한 각 이미지에 대해서 OCR 진행 및 text 파일 생성 ---><b></b>
9. OCR을 적용시킨 ASR 실행 ---><b></b>
10. 6번의 결과물과 8번의 결과물을 비교하여 WER을 산출 ---><b></b>
