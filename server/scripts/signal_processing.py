import librosa
import librosa.display # for plotting, debugging
import numpy as np
import matplotlib.pyplot as plt
import json
from threading import Thread
from .note import Note

# Receiving the recorded file from the client
# It will be passed in by performance.py

# Librosa parameters
FRAME_LENGTH = 256 # Length of frame in samples. Default 2048
SAMPLE_RATE = 22050 # Default 22050
FRAME_PERIOD = FRAME_LENGTH/SAMPLE_RATE # Frame duration in seconds.
WINDOW_LENGTH = FRAME_LENGTH//2 # Window length. Default FRAME_LENGTH//2
HOP_LENGTH = FRAME_LENGTH//4 # Frame increment in samples. Default FRAME_LENGTH//4
# Signal processing function parameters
NUM_THREADS = 4
MAX_CENTS_ERROR = 50 # Max difference between two frequencies in cents before considering them as different notes.
MIN_NOTE_LENGTH = 0.1 # Min note length in seconds.

def freq_to_notes(f0, times, amp_maxes):
    # Takes in two lists one for time and one for frequencies, and return a list of Note objects
    # Store the frequencies in the data/dat/ folder as a JSON
    frequencies = []
    amplitudes = []

    for i in range(len(f0)):
        # This deals with rests
        if np.isnan(f0[i]):
            frequencies.append('Rest')
            amplitudes.append(0)
        else:
            frequencies.append(f0[i])
            amplitudes.append(amp_maxes[i])

    note_struct = []

    # Turns the frequencies into a list of Note objects
    i = 1
    while i < len(frequencies):
        previous_freq = 1 if frequencies[i-1] == "Rest" else frequencies[i-1]
        current_freq = 1 if frequencies[i] == "Rest" else frequencies[i]
        
        # Similar enough frequencies
        if Note.frequency_difference_in_cents(current_freq, previous_freq) <= MAX_CENTS_ERROR:
            # If the note is the same as the previous note, update the duration
            start_time = times[i-1]
            note_obj = Note(current_freq, amplitudes[i], start_time, 0)
            while (i < len(frequencies) and
                   Note.frequency_difference_in_cents(current_freq, previous_freq) <= MAX_CENTS_ERROR):
                end_time = times[i]
                i += 1
                if i == len(frequencies):
                    break
                previous_freq = 1 if frequencies[i-1] == "Rest" else frequencies[i-1]
                current_freq = 1 if frequencies[i] == "Rest" else frequencies[i]
            note_obj.end = end_time
            note_struct.append(note_obj)

        # (Notes that aren't duplicated are skipped)    
        i += 1
    
    # Replace notes with frequencies of 1 with "Rest"
    for note in note_struct:
        if note.pitch == 1:
            note.pitch = "Rest"
    # Remove notes that are too short
    note_struct = [note for note in note_struct if
                   note.end - note.start >= MIN_NOTE_LENGTH]
    
    return note_struct

# Turns the notes into a JSON file structure
def notes_to_JSON(note_struct):
    test = []
    for i in range(len(note_struct)):
        test.append(note_struct[i].__dict__)

    result_dict = {
        "size": len(note_struct),
        "notes": test
    }

    result_object = json.dumps(result_dict, indent=4)

    return result_object

class PYINThread(Thread):
    def __init__(self, y):
        Thread.__init__(self)
        self.y = y
    def run(self):
        self.f0, self._, self._ = librosa.pyin(self.y,
                                               fmin=librosa.note_to_hz('C0'),
                                               fmax=librosa.note_to_hz('C7'),
                                               frame_length=FRAME_LENGTH)

# Analyzes wave file, puts it into a data structure
def signal_processing(rec_file):

    y, sr = librosa.load(rec_file, sr=SAMPLE_RATE)
    y, _ = librosa.effects.trim(y)

    threads = []
    for i in range(NUM_THREADS):
        start = int(i/NUM_THREADS*len(y))
        end = int((i+1)/NUM_THREADS*len(y))-1
        threads.append(PYINThread(y[start:end]))
    
    for thread in threads:
        thread.start()
        
    for thread in threads:
        thread.join()
    
    f0 = np.array([i.f0 for i in threads])
    f0 = f0.flatten()

    # f0 holds the fundamental frequencies we need to use
    # f0, voiced_flag, voiced_probs = librosa.pyin(y,
    #                                              fmin=librosa.note_to_hz('C0'),
    #                                              fmax=librosa.note_to_hz('C7'),
    #                                              frame_length=FRAME_LENGTH)

    times = librosa.times_like(f0, hop_length=HOP_LENGTH)

    # Gets the amplitude of the fundamental frequencies
    amplitude = np.abs(librosa.stft(y, hop_length=HOP_LENGTH))
    amp_maxes = np.max(amplitude, axis=0).tolist()

    # Converts the fundamental frequencies to the notes data structure
    notes = freq_to_notes(f0, times, amp_maxes)

    # Converts the notes data structure to a JSON file structure
    result = notes_to_JSON(notes)

    return result