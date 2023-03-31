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
from concurrent.futures import ProcessPoolExecutor, wait, ALL_COMPLETED
from .note import Note

# Librosa parameters
FRAME_LENGTH = 256 # Length of frame in samples. Default 2048
SAMPLE_RATE = 22050 # Default 22050
FRAME_PERIOD = FRAME_LENGTH/SAMPLE_RATE # Frame duration in seconds.
WINDOW_LENGTH = FRAME_LENGTH//2 # Window length. Default FRAME_LENGTH//2
HOP_LENGTH = FRAME_LENGTH//4 # Frame increment in samples. Default FRAME_LENGTH//4
# Signal processing function parameters
NUM_SUBPROCESSES = 8
MAX_CENTS_ERROR = 50 # Max difference between two frequencies in cents before considering them as different notes.
MIN_NOTE_LENGTH = 0.1 # Min note length in seconds.
REST_FREQUENCY = 1 # Arbitrary frequency value assigned to rests.

def signal_processing(rec_file: str) -> Dict:
    """Analyzes WAV sound file and returns a JSON containing the list
    of extrapolated notes.

    Args:
        rec_file (str): The file path of the WAV file

    Returns:
        Dict: The JSON with the list of notes
    """

    y, _ = librosa.load(rec_file, sr=SAMPLE_RATE)
    y, _ = librosa.effects.trim(y)
    
    # Split up time domain data into chunks
    time_domain = [y[int(i/NUM_SUBPROCESSES*len(y)):int((i+1)/NUM_SUBPROCESSES*len(y))-1]
                   for i in range(NUM_SUBPROCESSES)]
    # Start subprocesses
    futures = []
    with ProcessPoolExecutor(max_workers=NUM_SUBPROCESSES) as executor:
        futures = [executor.submit(pyin_wrapper, subarray) for subarray in time_domain]
        wait(futures, return_when=ALL_COMPLETED)
    
    # Merge results and delete any extraneous frequencies
    f0 = np.array([i.result() for i in futures])
    f0 = f0.flatten()
    original_f0_len = len(f0)
    for i in range(NUM_SUBPROCESSES-2, 0, -1):
        f0 = np.delete(f0, int(i/NUM_SUBPROCESSES*original_f0_len))

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

def pyin_wrapper(y: np.array) -> np.array:
    """Wrapper function for librosa.pyin to use with futures library.

    Args:
        y (np.array): An audio time series array

    Returns:
        np.array: An array of fundamental frequencies
    """
    f0, _, _ = librosa.pyin(y,
                            fmin=librosa.note_to_hz('C0'),
                            fmax=librosa.note_to_hz('C7'),
                            frame_length=FRAME_LENGTH)
    return f0

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
    
    frequencies = []
    amplitudes = []
    for i in range(len(f0)):
        # Replace nan frequencies (rests) with arbitrary value and 0 amplitude
        if np.isnan(f0[i]):
            frequencies.append(REST_FREQUENCY)
            amplitudes.append(0)
        else:
            frequencies.append(f0[i])
            amplitudes.append(amp_maxes[i])

    # Turns the frequencies into a list of Note objects
    note_objects = []
    i = 1
    while i < len(frequencies):
        previous = frequencies[i-1]
        current = frequencies[i]
        
        # Similar enough frequencies
        if Note.frequency_difference_in_cents(current, previous) <= MAX_CENTS_ERROR:
            # If the note is the same as the previous note, update the duration
            start_time = times[i-1]
            note_obj = Note(current, amplitudes[i], start_time, 0)
            while (i < len(frequencies) and
                   Note.frequency_difference_in_cents(current, previous) <= MAX_CENTS_ERROR):
                end_time = times[i]
                i += 1
                if i >= len(frequencies):
                    break
                previous = frequencies[i-1]
                # If i is at a point where the subprocesses combined their output, just skip
                while i % int(len(frequencies)/NUM_SUBPROCESSES) <= 2:
                    i += 1
                if i >= len(frequencies):
                    break
                current = frequencies[i]
            note_obj.end = end_time
            note_objects.append(note_obj)

        # (Notes that aren't duplicated at all are assumed to be errors and skipped)
        i += 1

    # Keep notes that meet the minimum length requirement
    note_objects = [note for note in note_objects if
                    note.end - note.start >= MIN_NOTE_LENGTH]

    # Replace note pitches that match rest frequency with "Rest"
    for note in note_objects:
        if note.pitch == REST_FREQUENCY:
            note.pitch = "Rest"
    
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
