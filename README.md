# OCRnASR_project
### 이후에 아래 .py 코드 functions에 옮길 수 있음.
## introai1 계정, nemo 가상환경, python 3.10, Pytorch 1.13.1, cuda11.7
## 현재 6번 까지 폴더에 있는 여러개의 강의 영상들에 대해서 반복하여 실행하는 것으로 수정함.
#### ASR 과정에서 쓰이는 package 중 일부와 NeMo가 호환이 안 되는 문제를 해결하기 위해서 nemoreal 가상환경을 새로만들었고, NeMo를 돌릴땐 가상환경을 nemoreal로 바꿔서 진행해야함.
#### OCR을 실행할 때에는 가상환경 (ocr) 에서 실행해야 됨.

1. 원본 transcript 에서 시간 정보 추출 ---> <b>extracting_time_info.py</b>
2. transcript 텍스트 추출 ---> <b>extract_purified_transcript.py</b>
   <br>(오로지 transcript만 한 줄 마다 txt파일로 나오게 함.)
3. 음성추출---> <b>audio_extract.py</b>
   <br>(.wav 파일로 추출됨)
4. 음성 파일을 시간 정보에 따라 분할하기 ---> <b>split_wav_by_transcript_timing.py</b>
5. sampling rate 16000으로 조절 ---> <b>resampling.py</b>
6. 각 음성에 대해서 ASR 실행 (OCR 적용 안함, WER을 구하기 위한 데이터) ---> <b>ASR_vanilla.py</b>
7. 동영상에서 시간 정보에 따라 첫 시간의 frame 추출하기 ---> <b>extract_image_by_transcript_timing.py</b>
8. 7번에서 추출한 각 이미지에 대해서 OCR 진행 및 text 파일 생성 ---><b>OCR.py</b>
9. OCR을 적용시킨 ASR 실행 ---><b>Fuse.py</b>
11. 2번의 결과물과 9번의 결과물을 비교하여 WER을 산출 ---><b>WER_test.py</b>


### 강의 여러 개를 실험 데이터로 활용하게 되면서, 실험 과정에서는 일부 강의만 처리하게 되었습니다.
### 코드를 실행하기 전에, 작업을 원하는 파일을 작업용 폴더 files_to_process에 넣어야 합니다.
### 이 때 '강의명' 폴더를 통째로 이동하시기 바랍니다. 작업 완료 후 폴더는 원위치로 돌아갑니다.
### 4. split_wav_by_transcript_timing.py 실행 시 작업용 폴더에는 영상에서 추출된 "음성 파일만을" 옮깁니다. 시간 정보는 폴더의 이름을 읽어서 얻은 강의명을 통해 참조합니다. (따라서 동일한 강의에 대해서는 폴더의 이름을 통일해 주어야 합니다)
### 9. Fuse.py 실행 시 작업용 폴더에는 "분할된 음성 파일만" 옮깁니다. OCR 텍스트 파일은 폴더의 이름을 읽어서 얻은 강의명을 통해 참조합니다. (따라서 동일한 강의에 대해서는 폴더의 이름을 통일해 주어야 합니다)
### 11. WER_test.py 실행 시 작업용 폴더에는 "vanilla ASR 결과만을" 옮깁니다. OCR이 적용된 transcript와 원본 자막 파일은 폴더의 이름을 읽어서 얻은 강의명을 통해 참조합니다. (따라서 동일한 강의에 대해서는 폴더의 이름을 통일해 주어야 합니다)

### 2. extract_purified_transcript.py 실행 시 1.까지 실행됩니다. (기능 통합)
### 5. resampling.py를 4.보다 먼저 실행합니다.
### 7. extract_image_by_transcript_timing.py의 프레임 이미지는 정해진 시간 간격으로 추출됩니다.