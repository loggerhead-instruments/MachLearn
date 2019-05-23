import csv
import glob
import os
import re
from pathlib import Path
import librosa as lr
import numpy as np
import matplotlib.pyplot as plt

configs = {}

configs['sampling_rate'] = 44100
configs['duration'] = 1
configs['hop_length'] = 512//3
configs['n_fft'] = 512
configs['samples'] = configs['sampling_rate'] * configs['duration']
configs['dims'] = (257, 260, 1)

for root, dirs, files in os.walk(r'C:\Users\Austin\Documents\Academics\NCF\Semester_2\Loggerhead\practice\tiny_wavs'):
    for file in files:
        # Gets full path of wav
        wav_path = os.path.join(root, file)
        print(wav_path)

        audio, sfreq = lr.load(wav_path, sr = 44100)

        spectrogram = lr.amplitude_to_db(np.abs(lr.stft(audio, n_fft=configs['n_fft'], hop_length=configs['hop_length'])))
        spectrogram = spectrogram.astype(np.float32)

        plt.imsave(r'C:\Users\Austin\Documents\Academics\NCF\Semester_2\Loggerhead\practice\spec\\' + file[:-4]+".png", spectrogram)