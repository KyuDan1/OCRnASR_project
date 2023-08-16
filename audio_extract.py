from moviepy.editor import *

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


    


directory = 'MoonSoomook_Advanced_compiler'
for filename in os.listdir(directory):
    f = os.path.join(directory,filename)
    mp4_to_wav(f, f'audio/audio_{filename}'.replace("mp4","wav"))

