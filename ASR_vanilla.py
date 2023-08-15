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

    am_model_conformer = nemo_asr.models.ASRModel.from_pretrained(model_name="stt_en_conformer_ctc_large")
    files = [AUDIO_FILENAME]
    transcript = am_model_conformer.transcribe(paths2audio_files=files, logprobs=True)[0]
    return transcript

directory = 'splitted_audio'

for filename in os.listdir(directory):
    f = os.path.join(directory, filename)
    print(conformer_wav_to_transcript(f))
