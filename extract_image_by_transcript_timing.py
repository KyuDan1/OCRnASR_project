import cv2
import os
import natsort

# timing 정보에서 시작 시작만 뽑아오기.
def start_time(input_text):
    with open(input_text, "r") as file:
        time_ranges = [line.strip().split(" --> ") for line in file]
    start_time=[]
    for i in time_ranges:
        start_time.append(i[0])
    return start_time


# 시간 문자열을 밀리초(ms)로 변환하는 함수
def time_to_milliseconds(time_str):
    h, m, s, ms = map(int, time_str.split(":"))
    milliseconds = h * 3600000 + m * 60000 + s * 1000 + ms
    return milliseconds


input_video_directory = 'MoonSoomook_Advanced_compiler'
time_info_directory = 'time_info'
ordered_listdir_name_wav = natsort.natsorted(os.listdir(input_video_directory))
ordered_listdir_name_time_info = natsort.natsorted(os.listdir(time_info_directory))

for wav_filename, time_info_file in zip(ordered_listdir_name_wav, ordered_listdir_name_time_info):
    wav_file_path = os.path.join(input_video_directory, wav_filename)
    timing_file_path = os.path.join(time_info_directory, time_info_file)

    print(f"extracting images from {wav_file_path} with {timing_file_path}")
    #여기부터 수정
    target_times = start_time(timing_file_path)
    # 동영상 열기
    cap = cv2.VideoCapture(wav_file_path)

    if not cap.isOpened():
        print("can't open the video.")
    else:
        for target_time in target_times:
            target_milliseconds = time_to_milliseconds(target_time)

            # 가장 가까운 프레임을 찾기 위해 동영상을 읽어서 시간을 비교
            closest_frame = None
            min_time_diff = float('inf')

            while True:
                ret, frame = cap.read()
                if not ret:
                    break

                frame_time = cap.get(cv2.CAP_PROP_POS_MSEC)

                time_diff = abs(frame_time - target_milliseconds)
                if time_diff < min_time_diff:
                    min_time_diff = time_diff
                    closest_frame = frame

                if frame_time > target_milliseconds:
                    break

            # 추출된 프레임 저장 또는 처리
            if closest_frame is not None:
                # 여기에서 closest_frame를 사용하여 필요한 처리를 수행하거나 저장합니다.
                folder = f'images_timing/{wav_filename.replace(".mp4","")}/'
                os.makedirs(folder, exist_ok=True)  # 폴더가 이미 존재하면 무시하도록 수정
                frame_filename = f'{folder}frame_{target_time.replace(":", "_")}.jpg'
                cv2.imwrite(frame_filename, closest_frame)

                print(f"{frame_filename} extracted.")

        cap.release()
print("All complete.")
