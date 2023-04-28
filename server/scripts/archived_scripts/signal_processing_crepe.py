"""Signal Processing (CREPE)

Scrapped CREPE implementation of the Signal Processing module.
"""
import librosa
import numpy as np
import torchcrepe
import torch
from typing import List, Dict, Tuple
from ..objects import Note

FMIN = librosa.note_to_hz('C2') # Min detectable frequency (~65 Hz)
FMAX = librosa.note_to_hz('C7') # Max detectable frequency (~2093 Hz)
# CREPE signal processing parameters
CREPE_FRAME_LENGTH = 512 # Length of frame in samples. Default 2048
CREPE_SAMPLE_RATE = 16000 # Default 22050
CREPE_HOP_LENGTH = 40
CREPE_WINDOW_LENGTH = CREPE_HOP_LENGTH*2 # Window length. Default FRAME_LENGTH//2
# Note extrapolation parameters
MIN_CREPE_CONFIDENCE = 0.93
MIN_NOTE_LENGTH = 0.1
MAX_CENTS_DIFFERENCE = 31.5 # Max cents difference between notes.

def amplitude_to_midi_velocity(amplitude: np.array) -> np.array:
    """Converts raw amplitude values to velocity values.

    Args:
        amplitude (np.array): The raw amplitude values

    Returns:
        np.array: Normalized velocity values
    """

    # Amplitude value assigned to mezzo forte (velocity 80)
    MF_RMS = np.log10(0.058209)
    amplitude = np.log10(amplitude)
    lower = np.min(amplitude)
    upper = MF_RMS
    # Normalize notes to this mf value
    normalized_amplitude = (amplitude - lower) / (upper - lower)
    midi_velocity = np.round(normalized_amplitude * 80 + 1).astype(int)

    # Convert the NumPy array to a list of native integers
    return midi_velocity.tolist()

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
