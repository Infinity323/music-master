import librosa
import librosa.display # for plotting, debugging
import numpy as np
import matplotlib.pyplot as plt
import csv

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
            note_obj = Note(notes[i], 0, 0, 0)
            while i < len(notes) and notes[i] == notes[i-1]:
                end_time = times[i]
                if i == len(notes):
                    break
                i += 1
            note_obj.set_start(start_time)
            note_obj.set_end(end_time)
            note_struct.append(note_obj)
        
        i += 1
    
    return note_struct

# Turns the notes into a CSV file
def notes_to_CSV(notes):
    csv_header = ['Note', 'Amplitude', 'Duration', 'Cents', 'Beat']
    csv_body = []

    for i in range(len(notes)):
        csv_body.append([notes[i].note, notes[i].amplitude, notes[i].duration, notes[i].cents, notes[i].beat])
    
    filename = 'test.csv'
    
    with open(filename, 'w', newline="") as file:
        csvwriter = csv.writer(file)
        csvwriter.writerow(csv_header)
        csvwriter.writerows(csv_body)
    
    return True

# Analyzes wave file, puts it into a data structure
def signal_processing(rec_file):

    y, sr = librosa.load(rec_file)

    # f0 holds the fundamental frequencies we need to use
    f0, voiced_flag, voiced_probs = librosa.pyin(y,
                                                fmin=librosa.note_to_hz('C2'),
                                                fmax=librosa.note_to_hz('C7'))

    times = librosa.times_like(f0)

    # Convert the fundamental frequencies to the notes data structure
    notes = freq_to_notes(f0, times)

    notes_to_CSV(notes)

    return True