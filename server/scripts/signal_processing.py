"""Signal Processing

This module contains functions needed for the performance API endpoint to
process the data from a WAV sound file, convert the frequency data into a list
of usable notes, store the list of extrapolated notes into a JSON, and then
return that JSON to be stored locally in the file system.
"""
import librosa
import torchcrepe
import torch
import numpy as np
import json
from typing import List, Dict, Tuple
from .objects import Note

FMIN = librosa.note_to_hz('C2') # Min detectable frequency (~65 Hz)
FMAX = librosa.note_to_hz('C7') # Max detectable frequency (~2093 Hz)
# YIN signal processing parameters
YIN_SAMPLE_RATE = 22050
YIN_FRAME_LENGTH = 256
YIN_HOP_LENGTH = YIN_FRAME_LENGTH//6 # Frame increment in samples. Default FRAME_LENGTH//4
YIN_WINDOW_LENGTH = YIN_FRAME_LENGTH//2
# CREPE signal processing parameters
CREPE_FRAME_LENGTH = 512 # Length of frame in samples. Default 2048
CREPE_SAMPLE_RATE = 16000 # Default 22050
CREPE_HOP_LENGTH = 40
CREPE_WINDOW_LENGTH = CREPE_HOP_LENGTH*2 # Window length. Default FRAME_LENGTH//2
# Note extrapolation parameters
MIN_CREPE_CONFIDENCE = 0.93
MAX_CENTS_DIFFERENCE = 31.5 # Max cents difference between notes.
MIN_NOTE_LENGTH = 0.09 # Min note length in seconds.
MIN_NOTE_DISTANCE = YIN_HOP_LENGTH/YIN_SAMPLE_RATE # Min note distance before merging in seconds.
REST_FREQUENCY = 2205 # Arbitrary frequency value assigned to rests.

class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        else:
            return super(NpEncoder, self).default(obj)

def signal_processing(rec_file: str) -> Dict:
    """Analyzes WAV sound file and returns a JSON containing the list
    of extrapolated notes.

    Args:
        rec_file (str): The file path of the WAV file

    Returns:
        Dict: The JSON with the list of notes
    """

    # Converts sound file to frequency data, etc.
    f0, times, amplitudes = get_f0_time_amp_crepe(rec_file)

    # Converts the fundamental frequencies, etc. to notes
    notes = freq_to_notes_yin(f0, times, amplitudes)

    # Converts the notes to a JSON file structure
    result = notes_to_JSON(notes)

    return result

def amplitude_to_midi_velocity(amplitude: np.array) -> np.array:
    """Converts raw amplitude values to velocity values.

    Args:
        amplitude (np.array): The raw amplitude values

    Returns:
        np.array: Normalized velocity values
    """

    # Amplitude value assigned to mezzo forte (velocity 80)
    MF_RMS = np.log10(0.0282389)
    amplitude = np.log10(amplitude)
    lower = np.min(amplitude)
    upper = MF_RMS
    # Normalize notes to this mf value
    normalized_amplitude = (amplitude - lower) / (upper - lower)
    midi_velocity = np.round(normalized_amplitude * 80 + 1).astype(int)

    # Convert the NumPy array to a list of native integers
    return midi_velocity.tolist()

def get_f0_time_amp_yin(rec_file: str) -> Tuple[np.array, np.array, np.array]:
    """Gets fundamental frequencies, timestamps, and amplitudes from a WAV
    sound file. YIN implementation.

    Args:
        rec_file (str): The file path of the WAV file

    Returns:
        Tuple[np.array, np.array, np.array, np.array]: The arrays for fundamental
            frequency, their times, and amplitudes
    """
    
    audio, sr = librosa.load(rec_file)
    audio, _ = librosa.effects.trim(audio)
    
    f0 = librosa.yin(audio, sr=sr, fmin=FMIN, fmax=FMAX, frame_length=YIN_FRAME_LENGTH, win_length=YIN_WINDOW_LENGTH, hop_length=YIN_HOP_LENGTH)

    # Get times for frequencies
    times = np.array([YIN_HOP_LENGTH/sr*i for i in range(f0.size)])

    # Gets the amplitude of the fundamental frequencies
    S = librosa.magphase(librosa.stft(audio, n_fft=YIN_FRAME_LENGTH, hop_length=YIN_HOP_LENGTH, win_length=YIN_WINDOW_LENGTH, window=np.ones))[0]
    amplitudes = librosa.feature.rms(S=S, frame_length=YIN_FRAME_LENGTH, hop_length=YIN_HOP_LENGTH)[0]

    # Convert amplitude to MIDI velocity
    midi_velocities = amplitude_to_midi_velocity(amplitudes)
    
    return f0, times, midi_velocities

def get_f0_time_amp_crepe(rec_file: str) -> Tuple[np.array, np.array, np.array, np.array]:
    """Gets fundamental frequencies, timestamps, amplitudes, and confidences from a WAV
    sound file. CREPE implementation.

    Args:
        rec_file (str): The file path of the WAV file

    Returns:
        Tuple[np.array, np.array, np.array, np.array]: The arrays for fundamental
            frequency, their times, amplitudes, and confidences
    """
    
    audio, sr = librosa.load(rec_file, sr=CREPE_SAMPLE_RATE)
    audio, _ = librosa.effects.trim(audio)
    audio_tensor = torch.from_numpy(np.array([audio]))
    
    f0, periodicities = torchcrepe.predict(audio_tensor, sr, CREPE_HOP_LENGTH, FMIN, FMAX, 'tiny', return_periodicity=True)

    # Get times for frequencies
    times = np.array([CREPE_HOP_LENGTH/CREPE_SAMPLE_RATE*i for i in range(f0.size(1))])

    # Gets the amplitude of the fundamental frequencies
    S = librosa.magphase(librosa.stft(audio, n_fft=CREPE_FRAME_LENGTH, hop_length=int(CREPE_HOP_LENGTH/2), win_length=int(CREPE_WINDOW_LENGTH/2), window=np.ones))[0]
    amplitudes = librosa.feature.rms(S=S, frame_length=CREPE_FRAME_LENGTH, hop_length=int(CREPE_HOP_LENGTH/2))[0]

    # Convert amplitude to MIDI velocity
    midi_velocities = amplitude_to_midi_velocity(amplitudes)
    
    return f0.numpy().flatten(), times, midi_velocities, periodicities.numpy().flatten()

def freq_to_notes_yin(f0: np.array, times: np.array, amplitudes: np.array) -> List[Note]:
    """Converts an array of frequencies, timestamps, and amplitudes into
    a list of notes.

    Args:
        f0 (np.array): The array of fundamental frequencies
        times (np.array): The array of timestamps
        amplitudes (np.array): The array of max amplitudes

    Returns:
        List[Note]: A list of notes
    """

    # Turns the frequencies into a list of Note objects
    note_objects = []
    i = 1
    while i < len(f0):
        previous_freq = f0[i-1]
        current_freq = f0[i]
        previous_amp = amplitudes[i-1]
        current_amp = amplitudes[i]
        
        # Similar enough frequencies
        if Note.difference_cents(current_freq, previous_freq) <= MAX_CENTS_DIFFERENCE:
            # If the note is the same as the previous note, update the duration
            offset = times[i-1]
            new_note = Note(current_freq, current_amp, offset, 0)
            note_frequencies = [previous_freq]
            note_amplitudes = [previous_amp]
            while (i < len(f0) and
                   Note.difference_cents(current_freq, note_frequencies[0]) <= MAX_CENTS_DIFFERENCE):
                end_time = times[i]
                note_frequencies.append(current_freq)
                note_amplitudes.append(current_amp)
                i += 1
                if i >= len(f0):
                    break
                previous_freq = f0[i-1]
                current_freq = f0[i]
                previous_amp = amplitudes[i-1]
                current_amp = amplitudes[i]
            # Average note's frequencies and reset end time
            new_note.pitch = np.average(note_frequencies)
            new_note.end = end_time
            new_note.velocity = np.max(note_amplitudes)
            note_objects.append(new_note)

        # (Notes that aren't duplicated at all are assumed to be errors and skipped)
        i += 1

    # # Merge identical notes that are too close to each other
    # for i in range(1, len(note_objects)):
    #     if (note_objects[i].start - note_objects[i-1].end <= YIN_HOP_LENGTH/YIN_SAMPLE_RATE and
    #         Note.difference_cents(note_objects[i].pitch, note_objects[i-1].pitch) <= MAX_CENTS_DIFFERENCE):
    #         note_objects[i-1].end = note_objects[i].end
    #         note_objects[i-1].pitch = (note_objects[i-1].pitch + note_objects[i].pitch)/2
    #         note_objects[i].pitch = REST_FREQUENCY
            
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

def freq_to_notes_crepe(f0, times, amplitudes, confidences):

    # Turns the frequencies into a list of Note objects
    note_objects = []
    i = 1
    while i < len(f0):
        previous_freq = f0[i-1]
        current_freq = f0[i]
        previous_amp = amplitudes[i-1]
        current_amp = amplitudes[i]
        
        # Similar enough frequencies
        if (confidences[i] >= MIN_CREPE_CONFIDENCE or
            (Note.difference_cents(current_freq, previous_freq) <= MAX_CENTS_DIFFERENCE and
             confidences[i] >= MIN_CREPE_CONFIDENCE - 0.1)):
            # If the note is the same as the previous note, update the duration
            offset = times[i-1]
            new_note = Note(current_freq, current_amp, offset, 0)
            note_frequencies = [previous_freq]
            note_amplitudes = [previous_amp]
            while (i < len(f0) and
                   (confidences[i] >= MIN_CREPE_CONFIDENCE or
                    (Note.difference_cents(current_freq, previous_freq) <= MAX_CENTS_DIFFERENCE and
                     confidences[i] >= MIN_CREPE_CONFIDENCE - 0.15))):
                end_time = times[i]
                note_frequencies.append(current_freq)
                note_amplitudes.append(current_amp)
                i += 1
                if i >= len(f0):
                    break
                previous_freq = f0[i-1]
                current_freq = f0[i]
                previous_amp = amplitudes[i-1]
                current_amp = amplitudes[i]
            # Average note's frequencies and reset end time
            new_note.pitch = np.average(note_frequencies)
            new_note.end = end_time
            new_note.velocity = np.max(note_amplitudes)
            note_objects.append(new_note)

        # (Notes that aren't duplicated at all are assumed to be errors and skipped)
        i += 1

    # Keep notes that are long enough
    note_objects = [note for note in note_objects if
                    note.end - note.start >= MIN_NOTE_LENGTH]
    
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
        "size": int(len(notes)),
        "notes": notes_JSON_array
    }

    result_object = json.dumps(result_dict, indent=4, cls=NpEncoder)

    return result_object
