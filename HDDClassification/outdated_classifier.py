import os
import random
import numpy as np
import pandas as pd
import librosa as lr
from pydub import AudioSegment
from matplotlib import pyplot as plt
from keras.models import load_model

filename = []
slicename = []
time = []
confidence = []

with os.scandir(my_path) as directory:
    for file in directory:
        if file.is_file() and file.name.endswith('.wav'):
            print("Loading Audio File: " + file.name)
            
            try:
                sound = AudioSegment.from_file(file.path, format="wav")

                for i, chunk in enumerate(sound[::1000]):

                    if len(chunk) == 1000:
                        samples = chunk.get_array_of_samples()
                        new_samples = lr.util.buf_to_float(samples, n_bytes=2,
                                                  dtype=np.float32)

                        new_samples = np.pad(new_samples, (3, 2), 'constant')
                        spectrogram = lr.amplitude_to_db(np.abs(lr.stft(new_samples, n_fft=597, hop_length=148)))
                        spectrogram = spectrogram.astype(np.float32)


                        model_spectrogram = np.stack([spectrogram, spectrogram, spectrogram], axis=-1)
                        model_spectrogram = np.expand_dims(model_spectrogram, axis=0)

                        prediction = model.predict(model_spectrogram)

                        if prediction >= .3:

                            if prediction < .5:
                                folder = "30-50"

                            elif .5 <= prediction < .7:
                                folder = "50-70"
                                
                            elif  .7 <= prediction < .9:
                                folder = "70-90"

                            elif .9 <= prediction < .98:
                                folder = "90-98"

                            else:
                                folder = "98-100"

                            rounded_prediction = round(float(prediction),4)
                            new_filename = file.name[:len(file.name)-4] + "~" + str(i) + "~" + str(rounded_prediction)

                            with open(my_out_path + folder + "\\" + new_filename + ".wav", "wb") as f:
                                chunk.export(f, format="wav")

                            filename.append(file.name)
                            slicename.append(new_filename)
                            time.append(i)
                            confidence.append(rounded_prediction)

                            plt.imsave(my_out_path+ folder + "image\\"  + new_filename +".png", spectrogram)
                            
                        else:
                            
                            folder = "0-30"
                            
                            dice_roll = random.choice(range(1, 1000))
                            
                            if prediction < .05 and dice_roll == 1:
                                
                                rounded_prediction = round(float(prediction),4)
                                new_filename = file.name[:len(file.name)-4] + "~" + str(i) + "~" + str(rounded_prediction)

                                with open(my_out_path + folder + "\\" + new_filename + ".wav", "wb") as f:
                                    chunk.export(f, format="wav")

                                plt.imsave(my_out_path+ folder + "image\\"  + new_filename +".png", spectrogram)
                                
                            elif  .05 <= prediction < .20 and dice_roll <= 2:
                                
                                rounded_prediction = round(float(prediction),4)
                                new_filename = file.name[:len(file.name)-4] + "~" + str(i) + "~" + str(rounded_prediction)

                                with open(my_out_path + folder + "\\" + new_filename + ".wav", "wb") as f:
                                    chunk.export(f, format="wav")

                                plt.imsave(my_out_path+ folder + "image\\"  + new_filename +".png", spectrogram)
                                
                            elif prediction >= .20 and dice_roll <= 10: 
                                
                                rounded_prediction = round(float(prediction),4)
                                new_filename = file.name[:len(file.name)-4] + "~" + str(i) + "~" + str(rounded_prediction)

                                with open(my_out_path + folder + "\\" + new_filename + ".wav", "wb") as f:
                                    chunk.export(f, format="wav")

                                plt.imsave(my_out_path+ folder + "image\\"  + new_filename +".png", spectrogram)
                                
                                
                            
            except:
                print("ERROR OPENING FILE")
