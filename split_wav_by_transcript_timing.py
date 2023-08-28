from pydub import AudioSegment
import os
import natsort


# 시간 정보를 밀리초로 변환하는 함수
def time_to_milliseconds(time_str):
    h, m, s, ms = map(int, time_str.split(":"))
    milliseconds = h * 3600000 + m * 60000 + s * 1000 + ms
    return milliseconds


# 시간 정보와 파일명을 기반으로 WAV 파일을 분할하는 함수
def split_wav_file(start_time, end_time, input_file, output_file):
    start_ms = time_to_milliseconds(start_time)
    end_ms = time_to_milliseconds(end_time)

    """if start_ms >= end_ms:
        return"""

    sound = AudioSegment.from_file(input_file)
    segment = sound[start_ms:end_ms]
    segment.export(output_file, format="wav")


# 원본 WAV 파일 이름
# input_wav_file = "audio/audio01.wav"

# 텍스트 파일에서 시간 정보 읽어오기
# time_info_file = "time_info/01.txt"


# with open(time_info_file, "r") as file:
#    time_ranges = [line.strip().split(" --> ") for line in file]

# 반복문으로 WAV 파일을 분할
# for i, (start_time, end_time) in enumerate(time_ranges, start=1):
#    output_file = f"splitted_audio/output{i}.wav"
#    split_wav_file(start_time, end_time, input_wav_file, output_file)
#    print(f"{output_file} 파일 분할이 완료되었습니다.")

input_wav_directory = "audio"
time_info_directory = "time_info"
ordered_listdir_name_wav = natsort.natsorted(os.listdir(input_wav_directory))
ordered_listdir_name_time_info = natsort.natsorted(os.listdir(time_info_directory))


for wav_filename, time_info_file in zip(
    ordered_listdir_name_wav, ordered_listdir_name_time_info
):
    wav_file_path = os.path.join(input_wav_directory, wav_filename)
    timing_file_path = os.path.join(time_info_directory, time_info_file)
    print(f"operating {wav_file_path} and {timing_file_path}")
    # 여기부터 수정
    with open(timing_file_path, "r") as file:
        time_ranges = [line.strip().split(" --> ") for line in file]

    # 반복문으로 WAV 파일을 분할
    for i, (start_time, end_time) in enumerate(time_ranges, start=1):
        folder = f"splitted_audio/{wav_filename}".replace(".wav", "")
        output_file = folder + f"/output{i}.wav"
        if not os.path.exists(folder):
            os.makedirs(folder)
        split_wav_file(start_time, end_time, wav_file_path, output_file)
        print(f"{output_file} complete.")


print("All complete.")
