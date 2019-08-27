import argparse
import queue
import sys
import matplotlib.pyplot as plt
import numpy as np
import sounddevice as sd
import librosa as lr
import tensorflow as tf


# Framework used from sounddevice documentation at https://python-sounddevice.readthedocs.io/en/0.3.13/examples.html
def int_or_str(text):
    """Helper function for argument parsing."""
    try:
        return int(text)
    except ValueError:
        return text


parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument(
    '-l', '--list-devices', action='store_true',
    help='show list of audio devices and exit')
parser.add_argument(
    '-d', '--device', type=int_or_str,
    help='input device (numeric ID or substring)')
parser.add_argument(
    '-r', '--samplerate', type=int, help='sampling rate')
parser.add_argument(
    '-c', '--channels', type=int, default=1, help='number of input channels')
parser.add_argument(
    '-t', '--subtype', type=str, help='sound file subtype (e.g. "PCM_24")')
args = parser.parse_args()

# Load TFLite model and allocate tensors.
interpreter = tf.lite.Interpreter(model_path="converted_model.tflite")
interpreter.allocate_tensors()

# Get input and output tensors.
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

try:

    if args.list_devices:
        print(sd.query_devices())
        parser.exit(0)
    if args.samplerate is None:
        device_info = sd.query_devices(args.device, 'input')
        # soundfile expects an int, sounddevice provides a float:
        args.samplerate = int(device_info['default_samplerate'])

    q = queue.Queue()


    def callback(indata, frames, time, status):
        """This is called (from a separate thread) for each audio block."""
        if status:
            print(status, file=sys.stderr)

        q.put(indata.copy())


    data = []

    with sd.InputStream(samplerate=args.samplerate, device=args.device, channels=args.channels, callback=callback):
        print('#' * 80)
        print('press Ctrl+C to stop the recording')
        print('#' * 80)
        while True:
            # Extends data from queue if total is < 1 second
            if len(data) < args.samplerate:
                data.extend(q.get())
            else:
                # Grabs one second and turns list into single np array
                X = np.array(data[:args.samplerate])

                # Resets data to only contain last 0.5 seconds + overhang from queue
                data = data[args.samplerate // 2:]

                spectrogram = lr.amplitude_to_db(np.abs(lr.stft(np.squeeze(X), n_fft=256, hop_length=145)))
                cutoff_spectrogram = spectrogram[3:, :]

                model_spectrogram = np.expand_dims(cutoff_spectrogram, axis=-1)

                # WxHxC --> 1xWxHxC
                model_spectrogram = np.expand_dims(model_spectrogram, axis=0)

                # Make prediction
                interpreter.set_tensor(input_details[0]['index'], model_spectrogram)
                interpreter.invoke()

                tflite_results = interpreter.get_tensor(output_details[0]['index'])
                print(tflite_results)

                if np.any(tflite_results > .5):
                    print(tflite_results)
                    plt.imshow(cutoff_spectrogram)
                    plt.show()
                    plt.pause(0.1)
                    plt.close("all")

            # S1 = librosa.feature.melspectrogram(np.squeeze(X), sr=args.samplerate)
            # S1 = 10 * np.log(S1 + 1e-15)
            # plt.imshow(S1)
            # plt.pause(0.05)
            # plt.close("all")


except KeyboardInterrupt:
    print('\nRecording finished')
    parser.exit(0)
except Exception as e:
    parser.exit(type(e).__name__ + ': ' + str(e))
