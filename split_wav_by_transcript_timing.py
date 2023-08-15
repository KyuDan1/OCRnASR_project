from pydub import AudioSegment

# 원본 WAV 파일 이름
input_wav_file = "audio/audio01.wav"

# 시간 정보를 밀리초로 변환하는 함수
def time_to_milliseconds(time_str):
    h, m, s, ms = map(int, time_str.split(":"))
    milliseconds = h * 3600000 + m * 60000 + s * 1000 + ms
    return milliseconds

# 시간 정보와 파일명을 기반으로 WAV 파일을 분할하는 함수
def split_wav_file(start_time, end_time, input_file, output_file):
    start_ms = time_to_milliseconds(start_time)
    end_ms = time_to_milliseconds(end_time)
    
    sound = AudioSegment.from_file(input_file)
    segment = sound[start_ms:end_ms]
    segment.export(output_file, format="wav")

# 텍스트 파일에서 시간 정보 읽어오기
time_info_file = "time_info/01.txt"

with open(time_info_file, "r") as file:
    time_ranges = [line.strip().split(" --> ") for line in file]

# 반복문으로 WAV 파일을 분할
for i, (start_time, end_time) in enumerate(time_ranges, start=1):
    output_file = f"splitted_audio/output{i}.wav"
    split_wav_file(start_time, end_time, input_wav_file, output_file)
    print(f"{output_file} 파일 분할이 완료되었습니다.")

print("모든 WAV 파일 분할이 완료되었습니다.")
