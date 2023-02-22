# https://realpython.com/playing-and-recording-sound-python/#recording-audio

# record audio
import sounddevice as sd
from scipy.io.wavfile import write

def record():
    fs = 44100  # Sample rate
    seconds = 3  # Duration of recording

    myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=1)
    sd.wait()  # Wait until recording is finished
    write('output.wav', fs, myrecording)  # Save as WAV file 