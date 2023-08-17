import os

import numpy as np
import librosa
from IPython.display import Audio, display
from plotly import graph_objects as go
#import ipywidgets

import nemo
import nemo.collections.asr as nemo_asr

#AUDIO_FILENAME = 'dli_workspace/data/segment_2.wav' # To be changed

def conformer_wav_to_transcript(AUDIO_FILENAME):
    # load audio signal with librosa
    signal, sample_rate = librosa.load(AUDIO_FILENAME, sr=16000)
    #duration=librosa.get_duration(y=signal, sr=sample_rate)
    #print("Duration:", duration)
    #print("Native sample rate:", sample_rate)
    files = [AUDIO_FILENAME]
    transcript = am_model_conformer.transcribe(paths2audio_files=files)[0]
    return transcript

def save_string_to_txt(filename, content):
    try:
        with open(filename, 'w') as file:
            file.write(content)
        print(f" '{filename}' saved.")
    except Exception as e:
        print(f"error")



am_model_conformer = nemo_asr.models.ASRModel.from_pretrained(model_name="stt_en_conformer_ctc_large")
print("loading complete".upper)

upper_directory = 'resampled_splitted_audio'
output_directory = 'pure_ASR_transcript'

# Create the output directory if it doesn't exist
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

directory = os.listdir(upper_directory)
for file in directory:
    audios = os.listdir(os.path.join(upper_directory, file))
    for audio in audios:
        input_file = os.path.join(upper_directory, file, audio)
        output_dir = os.path.join(output_directory, file)
        
        # Create the output subdirectory if it doesn't exist
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        save_string_to_txt(output_dir+'/pureASRtext '+f'{audio}'.replace("wav","txt"),conformer_wav_to_transcript(input_file))

#오디오에 데이터가 없을 때는 빈 txt 파일을 만드도록 하는 코드가 필요함.
