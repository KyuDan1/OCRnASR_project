import librosa
import os
import soundfile as sf

def down_sample(input_wav, origin_sr, resample_sr):
    y, sr = librosa.load(input_wav, sr=origin_sr)
    resample = librosa.resample(y, orig_sr=sr, target_sr=resample_sr)
    return resample

upper_directory = 'splitted_audio'
output_directory = 'resampled_splitted_audio'

# Create the output directory if it doesn't exist
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

directory = os.listdir(upper_directory)
print(directory)
for file in directory:
    audios = os.listdir(os.path.join(upper_directory, file))
    for audio in audios:
        input_file = os.path.join(upper_directory, file, audio)
        output_dir = os.path.join(output_directory, file)
        
        # Create the output subdirectory if it doesn't exist
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        resample = down_sample(input_file, librosa.get_samplerate(input_file), 16000)
        output_file = os.path.join(output_dir, audio)
        sf.write(output_file, data=resample, samplerate=16000, format='WAV')
