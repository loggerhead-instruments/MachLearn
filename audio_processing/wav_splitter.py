from pydub import AudioSegment
import pandas as pd

# Path to cleaned csv, wav files, and output sliced wav files
df_path = r"D:\cleaned_concat_fix.csv"
wav_path = r"D:\wavs"
wav_out = r"D:\Sliced_Files"

sounds_df = pd.read_csv(df_path)


# Extends length of sounds less than 1 second
def length_extender(length):
    total_extend = 1 - length
    side_extend = total_extend / 2
    # row[2] refers to the relevant start float in the csv
    new_start = row[2] - side_extend

    return new_start


# Centers and shortens length of sound between 1 and 2 seconds
def length_shortener(length):
    total_shorten = length - 1
    side_shorten = total_shorten / 2
    # row[2] refers to the relevant start float in the csv
    new_start = row[2] + side_shorten

    return new_start


# Each Row Contains: Index, Class, Start, End, Length, Date, File, Selection
for row in sounds_df.itertuples():

    # If first row of data, load sound file
    if row[0] == 0:
        sound_file = row[6]
        wavfile = AudioSegment.from_wav(wav_path + "\\" + sound_file)

        # If length is less than one second
        if row[4] < 1:
            start = length_extender(row[4])

            audio_slice = wavfile[start*1000:(start+1)*1000]
            audio_slice.export(wav_out+"\\" + row[1] + "\\"+row[1] + "-" +
                               str(row[7]) + "-" + row[6], format="wav")

        # If length is between one and two seconds
        elif 1 <= row[4] < 2:
            start = length_shortener(row[4])

            audio_slice = wavfile[start * 1000:(start + 1) * 1000]
            audio_slice.export(wav_out + "\\" + row[1] + "\\" + row[1] + "-" +
                               str(row[7]) + "-" + row[6], format="wav")

        # Length is bigger than two seconds
        else:
            audio_slice = wavfile[row[2]*1000:row[3]*1000]
            audio_slice.export(wav_out+"\\" + row[1] + "\\"+row[1] + "-" +
                               str(row[7]) + "-" + row[6], format="wav")

    # Else if this is the same sound file as previous row
    elif row[6] == sound_file:

        # If length is less than one second
        if row[4] < 1:
            start = length_extender(row[4])

            audio_slice = wavfile[start*1000:(start+1)*1000]
            audio_slice.export(wav_out+"\\" + row[1] + "\\"+row[1] + "-" +
                               str(row[7]) + "-" + row[6], format="wav")

        # If length is between one and two seconds
        elif 1 < row[4] < 2:
            start = length_shortener(row[4])

            audio_slice = wavfile[start * 1000:(start + 1) * 1000]
            audio_slice.export(wav_out + "\\" + row[1] + "\\" + row[1] + "-" +
                               str(row[7]) + "-" + row[6], format="wav")

        # Length is bigger than two seconds
        else:
            audio_slice = wavfile[row[2]*1000:row[3]*1000]
            audio_slice.export(wav_out+"\\" + row[1] + "\\"+row[1] + "-" +
                               str(row[7]) + "-" + row[6], format="wav")

    # This is a new file compared to previous row
    else:
        sound_file = row[6]
        wavfile = AudioSegment.from_wav(wav_path + "\\" + sound_file)

        # If length is less than one second
        if row[4] < 1:
            start = length_extender(row[4])

            audio_slice = wavfile[start * 1000:(start + 1) * 1000]
            audio_slice.export(wav_out + "\\" + row[1] + "\\" + row[1] + "-" +
                               str(row[7]) + "-" + row[6], format="wav")

        # If length is between one and two seconds
        elif 1 < row[4] < 2:
            start = length_shortener(row[4])

            audio_slice = wavfile[start * 1000:(start + 1) * 1000]
            audio_slice.export(wav_out + "\\" + row[1] + "\\" + row[1] + "-" +
                               str(row[7]) + "-" + row[6], format="wav")

        # Length is bigger than two seconds
        else:
            audio_slice = wavfile[row[2] * 1000:row[3] * 1000]
            audio_slice.export(wav_out + "\\" + row[1] + "\\" + row[1] + "-" +
                               str(row[7]) + "-" + row[6], format="wav")

# 2018-05-01T051000_0004e9e50005718b_2.0.wav did not exist in wav folder. Removed from csv!

# Tursiops_truncatus_Whistle-3-2018-04-30T022000_0004e9e50005718b_2.0 output seems incorrect
