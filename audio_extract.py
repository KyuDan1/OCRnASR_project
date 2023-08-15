from moviepy.editor import *
import scipy.io.wavfile as wav
import librosa

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

def resample_wav(input_path, output_path, target_sr):
    # Load the original WAV file
    data, original_sr = librosa.load(input_path, sr=None)
    
    # Resample the data
    resampled_data = librosa.resample(data, original_sr, target_sr)
    
    # Save the resampled data as a new WAV file
    librosa.output.write_wav(output_path, resampled_data, target_sr)


mp4_file_path = "MoonSoomook_Advanced_compiler/1-Orientation.mp4"
wav_file_path = "audio/audio01.wav"
#output_file = "audio_sr16000.wav"
    

mp4_to_wav(mp4_file_path, wav_file_path)
#resample_wav(wav_file_path, output_file, 16000)
