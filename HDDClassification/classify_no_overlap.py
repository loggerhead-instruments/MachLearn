import tensorflow as tf
import numpy as np
import librosa as lr
import os
from pydub import AudioSegment
from matplotlib import pyplot as plt

np.set_printoptions(suppress=True)

with os.scandir(path) as directory:
    for file in directory:
        if file.is_file() and file.name.endswith('.wav'):
            print("Loading Audio File: " + file.name)
            
            # Check if file has content
            if os.path.getsize(file.path):
            
                sound = AudioSegment.from_file(file.path, format="wav")

                spectrogram_array = []

                # Break sound into 1 second chunks
                for i, chunk in enumerate(sound[::1000]):

                    if len(chunk) == 1000:
                        samples = chunk.get_array_of_samples()
                        new_samples = lr.util.buf_to_float(samples, n_bytes=2,dtype=np.float32)

                        spectrogram = lr.amplitude_to_db(np.abs(lr.stft(new_samples, n_fft=256, hop_length=145)))
                        cutoff_spectrogram = spectrogram[3:, :]

                        model_spectrogram = np.expand_dims(cutoff_spectrogram, axis=-1)
                        spectrogram_array.append(model_spectrogram)

                spectrogram_array = np.asarray(spectrogram_array)

                predictions = model.predict(spectrogram_array)

                #Provide indices above whistle threshold (default to .5)
                whistle_hits = np.where(predictions[:,0]>=.7)

                # Check if there are any whistles before executing
                if whistle_hits[0].size:
                    for index in np.nditer(whistle_hits):
                        print(index)
                        print(predictions[index,:])
                        plt.imshow(np.squeeze(spectrogram_array[index]))
                        plt.show()
                        
            else:
                print("ERROR: FILE SIZE 0 BYTES. SKIPPING...")
print("PREDICTIONS COMPLETE")
