import cv2

# 동영상 파일 경로
video_path = '1 (edited).mp4'

# timing 정보에서 시작 시작만 뽑아오기.
def start_time(input_text):
    with open(input_text, "r") as file:
        time_ranges = [line.strip().split(" --> ") for line in file]
    start_time=[]
    for i in time_ranges:
        start_time.append(i[0])
    return start_time

# 추출할 시간 목록
input_text = '시간정보.txt'
target_times = start_time(input_text)

# 시간 문자열을 밀리초(ms)로 변환하는 함수
def time_to_milliseconds(time_str):
    h, m, s, ms = map(int, time_str.split(":"))
    milliseconds = h * 3600000 + m * 60000 + s * 1000 + ms
    return milliseconds

# 동영상 열기
cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    print("동영상 파일을 열 수 없습니다.")
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
            frame_filename = f'images_timing/frame_{target_time.replace(":", "_")}.jpg' # Can be modified
            cv2.imwrite(frame_filename, closest_frame)

    cap.release()

print("프레임 추출이 완료되었습니다.")
