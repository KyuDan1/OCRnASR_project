from moviepy.editor import *
import os


def mp4_to_wav(mp4_file_path, wav_file_path):
    try:
        # Load the video clip
        video_clip = VideoFileClip(mp4_file_path)

        # Extract audio from the video
        audio_clip = video_clip.audio

        # Save the audio as WAV file
        audio_clip.write_audiofile(wav_file_path)

        # Close the audio clip to free up resources
        audio_clip.close()
    except Exception as e:
        print(f"Error occurred during conversion: {e}")


if __name__ == "__main__":
    # directory = 'MoonSoomook_Advanced_compiler'
    input_directory = "files_to_process"
    output_directory = "audio"
    original_directory = "lecture_videos"

    for subdirectory in os.listdir(input_directory):
        d = os.path.join(input_directory, subdirectory)
        os.makedirs(os.path.join(output_directory, subdirectory), exist_ok=True)

        for filename in os.listdir(d):
            f = os.path.join(d, filename)
            mp4_to_wav(
                f,
                f"{output_directory}/{subdirectory}/audio_{filename}".replace(
                    "mp4", "wav"
                ),
            )

            # move files
            os.renames(f, os.path.join(original_directory, subdirectory, filename))

    os.makedirs(input_directory, exist_ok=True)
