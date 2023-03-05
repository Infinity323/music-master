import librosa
import librosa.display # for plotting, debugging
import numpy as np
import matplotlib.pyplot as plt
import json

# Receiving the recorded file from the client
# It will be passed in by performance.py

# The data structure should look like the following:

class Note():
    def __init__(self, pitch, velocity, start, end):
        # Pitch, Velocity, Start, End
        self.pitch = pitch
        self.velocity = 0 # not sure how to get this yet, prob just amplitude
        self.start = start
        self.end = end
    
    def set_start(self, start):
        self.start = start
    
    def set_end(self, end):
        self.end = end
        
    def __repr__(self):
        return "Pitch: {pitch}, Start: {start:.2f} sec, End: {end:.2f} sec".format(pitch=self.pitch, start=self.start, end=self.end)

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

# Turns the notes into a JSON file
def notes_to_JSON(note_struct):
    test = []
    for i in range(len(note_struct)):
        test.append(note_struct[i].__dict__)

    result_dict = {"notes": test}

    result_object = json.dumps(result_dict, indent=4)

    # Need to change this path to a different name
    with open("../data/dat/test.json", "w") as outfile:
        outfile.write(result_object)

    return

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

    notes_to_JSON(notes)

    return True