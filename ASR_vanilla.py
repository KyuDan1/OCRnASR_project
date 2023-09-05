import os

import numpy as np
import librosa
from IPython.display import Audio, display
from plotly import graph_objects as go

import wave
import whisper
# import ipywidgets

#import nemo
#import nemo.collections.asr as nemo_asr

def softmax(logits):
    e = np.exp(logits - np.max(logits))
    return e / e.sum(axis=-1).reshape([logits.shape[0], 1])

"""am_model_conformer = nemo_asr.models.ASRModel.from_pretrained(
    model_name="stt_en_conformer_ctc_large"
)
am_model_conformer.change_attention_model(
    self_attention_model="rel_pos_local_attn", att_context_size=[128, 128]
)"""

model = whisper.load_model("base")

print("loading complete".upper)

"""# Define number of CPUs to use. Set to the max when processing large batches of log probabilities
num_cpus = max(os.cpu_count(), 1)

# Set the beam size
beam_size = 16

# Get the vocabulary size
vocab = list(am_model_conformer.decoder.vocabulary)

# Beam search
beam_search = nemo_asr.modules.BeamSearchDecoderWithLM(
    beam_width=beam_size,
    lm_path=None,
    alpha=None,
    beta=None,
    vocab=vocab,
    num_cpus=num_cpus,
    input_tensor=False,
)"""

def check_wav_file_has_data(file_path):
        try:
            with wave.open(file_path, "rb") as wav_file:
                frames = wav_file.readframes(-1)
                return len(frames) > 0
        except Exception as e:
            print("Error:", e)
            return False

# AUDIO_FILENAME = 'dli_workspace/data/segment_2.wav' # To be changed
def whisper_wav_to_transcript(AUDIO_FILENAME):
    # load audio signal with librosa
    #signal, sample_rate = librosa.load(AUDIO_FILENAME, sr=16000)
    # duration=librosa.get_duration(y=signal, sr=sample_rate)
    # print("Duration:", duration)
    # print("Native sample rate:", sample_rate)
    #files = [AUDIO_FILENAME]
    transcript = model.transcribe(AUDIO_FILENAME)["text"]
    return transcript


"""def conformer_wav_to_sequence_list(AUDIO_FILENAME):
    files = [AUDIO_FILENAME]
    transcript = am_model_conformer.transcribe(files, logprobs=True)[0]
    return transcript"""


def save_string_to_txt(filename, content):
    try:
        with open(filename, "w") as file:
            file.write(content)
        print(f" '{filename}' saved.")
    except Exception as e:
        print(f"error")

"""def beam_wav_to_sequence_list(AUDIO_FILENAME):
    files = [AUDIO_FILENAME]
    logits = am_model_conformer.transcribe(files, logprobs=True)[0]
    probs = softmax(logits)

    best_sequences = beam_search.forward(
        log_probs=np.expand_dims(probs, axis=0), log_probs_length=None
    )
    #print("Number of best sequences :", len(best_sequences[0]))
    #print("Best sequences :")
    #print(best_sequences)
    return best_sequences[0]"""


if __name__ == "__main__":
    upper_directory = "resampled_splitted_audio"
    output_directory = "pure_ASR_transcript"

    # Create the output directory if it doesn't exist
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    directory = os.listdir(upper_directory)
    count_file = 0
    for file in directory:
        audios = os.listdir(os.path.join(upper_directory, file))

        for audio in audios:
            input_file = os.path.join(upper_directory, file, audio)
            output_dir = os.path.join(output_directory, file)

            # Create the output subdirectory if it doesn't exist
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)

            save_string_to_txt(
                output_dir + "/pureASRtext " + f"{audio}".replace("wav", "txt"),
                whisper_wav_to_transcript(input_file),
            )
