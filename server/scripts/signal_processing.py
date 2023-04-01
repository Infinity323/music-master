"""Signal Processing

This module contains functions needed for the performance API endpoint to
process the data from a WAV sound file, convert the frequency data into a list
of usable notes, store the list of extrapolated notes into a JSON, and then
return that JSON to be stored locally in the file system.
"""
import librosa
import numpy as np
import json
from typing import List, Dict
from .note import Note

# Librosa parameters
FRAME_LENGTH = 256 # Length of frame in samples. Default 2048
SAMPLE_RATE = 22050 # Default 22050
FRAME_PERIOD = FRAME_LENGTH/SAMPLE_RATE # Frame duration in seconds.
WINDOW_LENGTH = FRAME_LENGTH//2 # Window length. Default FRAME_LENGTH//2
HOP_LENGTH = FRAME_LENGTH//4 # Frame increment in samples. Default FRAME_LENGTH//4
FMIN = librosa.note_to_hz('C2') # Min detectable frequency (~65 Hz)
FMAX = librosa.note_to_hz('C7') # Max detectable frequency (~2093 Hz)
# Signal processing function parameters
MAX_CENTS_ERROR = 50 # Max difference between two frequencies in cents before considering them as different notes.
MIN_NOTE_LENGTH = 0.15 # Min note length in seconds.
MIN_NOTE_DISTANCE = 0.05 # Min note distance before merging in seconds.
REST_FREQUENCY = 2205 # Arbitrary frequency value assigned to rests.

def signal_processing(rec_file: str) -> Dict:
    """Analyzes WAV sound file and returns a JSON containing the list
    of extrapolated notes.

    Args:
        rec_file (str): The file path of the WAV file

    Returns:
        Dict: The JSON with the list of notes
    """

    y, sr = librosa.load(rec_file, sr=SAMPLE_RATE)
    y, _ = librosa.effects.trim(y)
    
    f0 = librosa.yin(y, fmin=FMIN, fmax=FMAX, sr=sr, frame_length=FRAME_LENGTH)

    # Get times for frequencies
    times = librosa.times_like(f0, hop_length=HOP_LENGTH)

    # Gets the amplitude of the fundamental frequencies
    amplitude = np.abs(librosa.stft(y, hop_length=HOP_LENGTH))
    amp_maxes = np.max(amplitude, axis=0).tolist()

    # Converts the fundamental frequencies to the notes data structure
    notes = freq_to_notes(f0, times, amp_maxes)

    # Converts the notes data structure to a JSON file structure
    result = notes_to_JSON(notes)

    return result

def freq_to_notes(f0: np.array, times: np.array, amp_maxes: np.array) -> List[Note]:
    """Converts an array of frequencies, timestamps, and amplitudes into
    a list of notes.

    Args:
        f0 (np.array): The array of fundamental frequencies
        times (np.array): The array of timestamps
        amp_maxes (np.array): The array of max amplitudes

    Returns:
        List[Note]: A list of notes
    """
    
    frequencies = f0
    amplitudes = amp_maxes

    # Turns the frequencies into a list of Note objects
    note_objects = []
    i = 1
    while i < len(frequencies):
        previous = frequencies[i-1]
        current = frequencies[i]
        
        # Similar enough frequencies
        if Note.frequency_difference_in_cents(current, previous) <= MAX_CENTS_ERROR:
            # If the note is the same as the previous note, update the duration
            offset = times[i-1]
            new_note = Note(current, amplitudes[i], offset, 0)
            while (i < len(frequencies) and
                   Note.frequency_difference_in_cents(current, previous) <= MAX_CENTS_ERROR):
                end_time = times[i]
                i += 1
                if i >= len(frequencies):
                    break
                previous = frequencies[i-1]
                current = frequencies[i]
            new_note.end = end_time
            note_objects.append(new_note)

        # (Notes that aren't duplicated at all are assumed to be errors and skipped)
        i += 1

    # YIN is kind of noisy. If a note isn't long enough, merge it with the
    # previous note
    last_good_index = 0
    last_good_end = 0
    for i in range(len(note_objects)):
        if note_objects[i].end - note_objects[i].start < MIN_NOTE_LENGTH:
            note_objects[last_good_index].end = note_objects[i].end
            note_objects[i].pitch = REST_FREQUENCY
        else:
            last_good_index = i
            last_good_end = note_objects[i].end

    # Keep notes that don't match the rest frequency
    note_objects = [note for note in note_objects if
                    note.pitch != REST_FREQUENCY]

    # Cut last note's ending short because there might be garbage attached
    note_objects[-1].end = last_good_end
    
    # Time shift notes to start at 0
    offset = note_objects[0].start
    for note in note_objects:
        note.start -= offset
        note.end -= offset
    
    return note_objects

def notes_to_JSON(notes: List[Note]) -> Dict:
    """Converts a list of notes into a JSON.

    Args:
        notes (List[Note]): The list of notes

    Returns:
        Dict: A dict containing the number of notes and the list of notes
    """
    
    notes_JSON_array = []
    for i in range(len(notes)):
        notes_JSON_array.append(notes[i].__dict__)

    result_dict = {
        "size": len(notes),
        "notes": notes_JSON_array
    }

    result_object = json.dumps(result_dict, indent=4)

    return result_object
