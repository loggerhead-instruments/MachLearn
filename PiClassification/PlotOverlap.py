import argparse
import queue
import sys
import matplotlib.pyplot as plt
import numpy as np
import sounddevice as sd
import librosa

#Framework used from sounddevice documentation at https://python-sounddevice.readthedocs.io/en/0.3.13/examples.html
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
                data = data[args.samplerate//2:]

                S1 = librosa.feature.melspectrogram(np.squeeze(X), sr=args.samplerate)
                S1 = 10 * np.log(S1 + 1e-15)
                plt.imshow(S1)
                plt.pause(0.05)
                plt.close("all")


except KeyboardInterrupt:
    print('\nRecording finished')
    parser.exit(0)
except Exception as e:
    parser.exit(type(e).__name__ + ': ' + str(e))
