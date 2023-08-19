# OCRnASR_project
### 이후에 아래 .py 코드 functions에 옮길 수 있음.
## introai1 계정, nemo 가상환경, python 3.10, Pytorch 1.13.1, cuda11.7
## 현재 6번 까지 폴더에 있는 여러개의 강의 영상들에 대해서 반복하여 실행하는 것으로 수정함.

1. 원본 transcript 에서 시간 정보 추출 ---> <b>extracting_time_info.py</b>
2. transcript 텍스트 추출 ---> <b>extract_purified_transcript.py</b>
   <br>(오로지 transcript만 한 줄 마다 txt파일로 나오게 함.)
3. 음성추출---> <b>audio_extract.py</b>
   <br>(.wav 파일로 추출됨)
4. 음성 파일을 시간 정보에 따라 분할하기 ---> <b>split_wav_by_transcript_timing.py</b>
5. sampling rate 16000으로 조절 ---> <b>resampling.py</b>
6. 각 음성에 대해서 ASR 실행 (OCR 적용 안함, WER을 구하기 위한 데이터) ---> <b>ASR_vanilla.py</b>
#### 위 과정에서 쓰이는 package 중 일부와 NeMo가 호환이 안 되는 문제를 해결하기 위해서 nemoreal 가상환경을 새로만들었고, NeMo를 돌릴땐 가상환경을 nemoreal로 바꿔서 진행해야함.

#### --OCR 관련 과정--
7. 동영상에서 시간 정보에 따라 첫 시간의 frame 추출하기 ---> <b>extract_image_by_transcript_timing.py</b>
#### 7번 작업 오래걸림
8. 7번에서 추출한 각 이미지에 대해서 OCR 진행 및 text 파일 생성 ---><b>OCR.py</b>
#### OCR을 실행할 때에는 가상환경 (ocr) 에서 실행해야 됨.
9. OCR을 적용시킨 ASR 실행 ---><b></b>
10. 2번의 결과물과 9번의 결과물을 비교하여 WER을 산출 ---><b></b>
