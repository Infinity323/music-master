import librosa
import librosa.display # for plotting, debugging
import numpy as np
import matplotlib.pyplot as plt

# Receiving the recorded file from the client
# It will be passed in by performance.py

# The data structure should look like the following:

class Note():
    def __init__(self, note, amplitude, duration, cents = 0, beat = 0):
        self.note = note
        self.amplitude = 0 # not sure how to get this yet
        self.duration = duration
        self.cents = cents
        self.beat = beat
    
    def set_duration(self, start, end):
        self.duration = end - start
        
    def __repr__(self):
        return "Note: " + str(self.note) + " " + "Duration: " + str(self.duration) + " seconds"

def freq_to_notes(f0, times):
    # Takes in two lists one for time and one for frequencies, and return a list of Note objects
    # Store the notes into the data folder (in the .dat file), store it as a JSON
    notes = []
    
    for i in f0:
        if np.isnan(i):
            notes.append('NaN')
        else:
            notes.append(librosa.hz_to_note(i))

    note_struct = []

    # Turns the notes into a list of Note objects
    i = 1
    while i < len(notes):
        # Same notes
        if notes[i] == notes[i-1]:
            # If the note is the same as the previous note, update the duration
            start_time = times[i-1]
            note_obj = Note(notes[i], 0, 0, 0, start_time)
            while i < len(notes) and notes[i] == notes[i-1]:
                end_time = times[i]
                if i == len(notes):
                    break
                i += 1
            note_obj.set_duration(start_time, end_time)
            note_struct.append(note_obj)
        
        i += 1

# Analyzes wave file, puts it into a data structure
def signal_processing(rec_file):

    # Loading a test file for now
    rec_file = "../../C4_to_C5.wav"

    y, sr = librosa.load(rec_file)

    # f0 holds the fundamental frequencies we need to use
    f0, voiced_flag, voiced_probs = librosa.pyin(y,
                                                fmin=librosa.note_to_hz('C2'),
                                                fmax=librosa.note_to_hz('C7'))

    times = librosa.times_like(f0)

    # Convert the fundamental frequencies to the notes data structure
    notes = freq_to_notes(f0, times)

    return notes