import moviepy.editor as mp

def extract_audio_from_mp4(input_file, output_file):
    try:
        clip = mp.VideoFileClip(input_file)
        clip.audio.write_audiofile(output_file)

        print("음성 추출이 완료되었습니다.")
    except Exception as e:
        print(f"음성 추출 중 오류가 발생했습니다: {str(e)}")



import cv2

def extract_frames_from_mp4(input_file, output_folder, interval_seconds=10):
    try:
        video = cv2.VideoCapture(input_file)
        fps = video.get(cv2.CAP_PROP_FPS)
        frame_count = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
        interval_frames = int(interval_seconds * fps)

        frame_number = 0
        success = True

        while success:
            success, frame = video.read()
            if frame_number % interval_frames == 0:
                output_file = f"{output_folder}/frame_{frame_number}.jpg"
                cv2.imwrite(output_file, frame)
                print(f"Frame {frame_number} 이미지를 저장했습니다.")
            frame_number += 1

        video.release()
        cv2.destroyAllWindows()
        print("프레임 이미지 추출이 완료되었습니다.")
    except Exception as e:
        print(f"프레임 이미지 추출 중 오류가 발생했습니다: {str(e)}")


def save_list_to_txt_file(data_list, file_path):
    with open(file_path, 'w') as file:
        for item in data_list:
            file.write(str(item) + '\n')

