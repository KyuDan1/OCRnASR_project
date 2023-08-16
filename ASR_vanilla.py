import os

import numpy as np
import librosa
from IPython.display import Audio, display
from plotly import graph_objects as go
import ipywidgets

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


directory = 'resampled_splitted_audio'
am_model_conformer = nemo_asr.models.ASRModel.from_pretrained(model_name="stt_en_conformer_ctc_large")

output_filename = 'pure_ASR_transcript/'

for filename in os.listdir(directory):
    f = os.path.join(directory, filename)
    save_string_to_txt(output_filename+f'{filename}'.replace("wav","txt"),conformer_wav_to_transcript(f))
    #with open(output_filename+f'{filename}.', 'w')
    #print(conformer_wav_to_transcript(f))
