import cv2
import numpy as np
from scipy.spatial import distance

def mse(image_a, image_b):
    err = np.sum((image_a.astype("float") - image_b.astype("float")) ** 2)
    err /= float(image_a.shape[0] * image_a.shape[1])
    return err

def is_duplicate_frame(frame, previous_frames, threshold=0.1):
    if not previous_frames:
        return False

    for prev_frame in previous_frames:
        similarity = mse(frame, prev_frame)
        if similarity > threshold:
            return True

    return False

def extract_frames(video_path, output_folder, interval=10):
    cap = cv2.VideoCapture(video_path)
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    previous_frames = []

    for t in range(0, frame_count, interval * fps):
        cap.set(cv2.CAP_PROP_POS_FRAMES, t)
        ret, frame = cap.read()

        if not ret:
            break

        if not is_duplicate_frame(frame, previous_frames):
            frame_filename = f"{output_folder}/frame_{t // fps}.png"
            cv2.imwrite(frame_filename, frame)
            previous_frames.append(frame)

    cap.release()

if __name__ == "__main__":
    video_path = "videos/example_Optimizer-Overview.mp4"
    output_folder = "images_diff"
    interval_seconds = 10

    extract_frames(video_path, output_folder, interval_seconds)
