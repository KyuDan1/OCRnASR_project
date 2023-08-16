import librosa
import os
import soundfile as sf

def down_sample(input_wav, origin_sr, resample_sr):
    y, sr = librosa.load(input_wav, sr=origin_sr)
    resample = librosa.resample(y, orig_sr = sr, target_sr = resample_sr)
    return resample

directory = 'splitted_audio'

for filename in os.listdir(directory):
    f = os.path.join(directory, filename)
    resample = down_sample(f,librosa.get_samplerate(f),16000)
    #print(librosa.get_samplerate(f))
    sf.write(f'resampled_splitted_audio/{filename}',data=resample,samplerate=16000, format='WAV')
    #librosa.output.write_wav('resampled_splitted_audio/{filename}', resample, 16000) # save half-cut file
