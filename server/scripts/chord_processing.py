import re
import librosa
import json
import numpy as np
from scripts.objects import Note
from scripts.musicxml_reader import Chord as XMLChord
from scripts.signal_processing import NpEncoder
from music21 import chord, pitch
from chord_extractor.extractors import Chordino
from typing import List

# Note to get velocity use the librosa library at the chords start time (or maybe at the middle of the start and end times)

class ParsedChord:

    def __init__(self, root, chord_type, extensions, accidental = None, accidental_num = 0, end_time = None, start_time = None):
        self.root = root
        self.chord_type = chord_type
        self.extensions = extensions # Interval
        self.accidental = accidental
        self.accidental_num = accidental_num
        self.start_time = start_time
        self.end_time = end_time
        self.velocity = None
        self.notes = None

    def __str__(self):
        return f"Root: {self.root}, Type: {self.chord_type}, Extensions: {self.extensions}, Accidental: {self.accidental}, Accidental Number: {self.accidental_num}, Start Time: {self.start_time}"

    def set_notes(self, notes: List[str]):
        self.notes = notes
    
    def set_start_time(self, start_time):
        self.start_time = start_time
    
    def set_end_time(self, end_time):
        self.end_time = end_time

def find_chords(filename):
    """
    Function to find chords in a given audio file

    Parameters
    ----------
    filename : str
        Path to audio file

    Returns
    -------
    chords : list
        List of chords in the audio file
    """

    # Setup Chordino with one of several parameters that can be passed
    # The boost_n_likelihood parameter deals with the likelihood of something not being a chord (marking it as N)
    chordino = Chordino(roll_on=1)

    # Run extraction
    chords = chordino.extract(filename)
    return chords

def parse_notation(chord):
    """
    Function to parse chord notation into a ParsedChord object

    Parameters
    ----------
    chord : Chord
        Chord object from chordino

    Returns
    -------
    ParsedChord
        Chord object with parsed notation
    
    Raises
    ------
    ValueError
        If chord notation is invalid
    """

    chord_str = chord.chord
    chord_time = chord.timestamp

    chord_type = ""
    extensions = 0
    accidental = None
    accidental_num = 0

    if chord_str == "N":
        return ParsedChord("N", None, extensions, accidental, accidental_num, chord_time)

    # Match root, chord quality, extension, and accidentals
    match = re.match(r'([A-Ga-g][#b]?)(m|min|dim|aug|sus\d?|M)?(\d+)?([#b]\d+)?', chord_str)

    if not match:
        raise ValueError('Invalid chord notation')

    root, quality, extension, accidental_str = match.groups()

    # Determine chord type
    if quality in ("m", "min"):
        chord_type = "minor"
    elif quality == "dim":
        chord_type = "diminished"
    elif quality == "aug":
        chord_type = "augmented"
    elif quality and quality.startswith("sus"):
        chord_type = quality
    else:
        chord_type = "major"

    # Check for extensions (7, 9, 11, 13, or 6)
    if extension:
        extensions = int(extension)

    # Check for accidentals (# or b)
    if accidental_str:
        accidental = "sharp" if accidental_str[0] == "#" else "flat"
        accidental_num = int(accidental_str[1:])

    return ParsedChord(root, chord_type, extensions, accidental, accidental_num, chord_time)

def add_extension_notes(root_note: int, chord_type: str, extension: int, note_reverse: dict):
    """
    Function to add extension notes to a chord

    Parameters
    ----------
    root_note : int
        Root note of the chord
    chord_type : str
        Type of chord (major, minor, diminished, augmented)
    extension : int
        Extension of the chord (7, 9, 11, 13, or 6)
    note_reverse : dict
        Dictionary mapping note values to note names

    Returns
    -------
    extension_notes : list
        List of extension notes
        
    Raises
    ------
    ValueError
        If chord type is invalid
    """

    extension_notes = []

    if chord_type == "major":
        if extension == 6:
            extension_notes.append(interval_to_note(root_note, 9, note_reverse))
        if extension == 7:
            extension_notes.append(interval_to_note(root_note, 11, note_reverse))
        if extension >= 9:
            extension_notes.append(interval_to_note(root_note, 14, note_reverse))
        if extension >= 11:
            extension_notes.append(interval_to_note(root_note, 17, note_reverse))
        if extension >= 13:
            extension_notes.append(interval_to_note(root_note, 21, note_reverse))

    elif chord_type == "minor":
        if extension == 6:
            extension_notes.append(interval_to_note(root_note, 9, note_reverse))
        if extension == 7:
            extension_notes.append(interval_to_note(root_note, 10, note_reverse))
        if extension >= 9:
            extension_notes.append(interval_to_note(root_note, 14, note_reverse))
        if extension >= 11:
            extension_notes.append(interval_to_note(root_note, 17, note_reverse))
        if extension >= 13:
            extension_notes.append(interval_to_note(root_note, 21, note_reverse))

    elif chord_type == "diminished":
        if extension == 7:
            extension_notes.append(interval_to_note(root_note, 9, note_reverse))
        # Diminished chords don't "really" have extensions beyond 7, they are rare in Western music
        
    elif chord_type == "augmented":
        if extension == 7:
            extension_notes.append(interval_to_note(root_note, 10, note_reverse))    
        # Augmented chords don't "really" have extensions beyond 7, they are rare in Western music

    return extension_notes


def interval_to_note(root_note: int, interval: int, note_reverse: dict) -> str:
    """
    Function to convert an interval to a note

    Parameters
    ----------
    root_note : int
        Root note of the chord
    interval : int
        Interval of the note
    note_reverse : dict
        Dictionary mapping note values to note names

    Returns
    -------
    note : str
        Note name
    
    Raises
    ------
    ValueError
        If interval is invalid
    """

    return note_reverse[(root_note + interval) % 12]

def get_basic_chord_notes(root_note: int, chord_type: str, note_reverse: dict) -> List[str]:
    """
    Function to get the basic notes of a chord

    Parameters
    ----------
    root_note : int
        Root note of the chord
    chord_type : str
        Type of chord (major, minor, diminished, augmented)
    note_reverse : dict
        Dictionary mapping note values to note names

    Returns
    -------
    chord_notes : list
        List of basic chord notes

    Raises
    ------
    ValueError
        If chord type is invalid
    """

    if chord_type == "major":
        intervals = [0, 4, 7]
    elif chord_type == "minor":
        intervals = [0, 3, 7]
    elif chord_type == "diminished":
        intervals = [0, 3, 6]
    elif chord_type == "augmented":
        intervals = [0, 4, 8]
    else:
        raise ValueError(f"Invalid chord type: {chord_type}")

    return [interval_to_note(root_note, interval, note_reverse) for interval in intervals]


def chords_to_notes(chord: ParsedChord) -> List[str]:
    """
    Function to convert a ParsedChord object to a list of notes

    Parameters
    ----------
    chord : ParsedChord
        Chord object

    Returns
    -------
    chord_notes : list
        List of notes in the chord

    Raises
    ------
    ValueError
        If chord type is invalid
    
    Notes
    -----
    This function currently doesn't handle slash chords
    """

    if chord.root == "N":
        return None

    notes = {
    'C': 0, 'C#': 1, 'Db': 1,
    'D': 2, 'D#': 3, 'Eb': 3,
    'E': 4,
    'F': 5, 'F#': 6, 'Gb': 6,
    'G': 7, 'G#': 8, 'Ab': 8,
    'A': 9, 'A#': 10, 'Bb': 10,
    'B': 11
    }
    
    note_reverse = {v: k for k, v in notes.items()}  # Reverse of the dictionary

    accidental_value = notes[chord.accidental] if chord.accidental else 0
    root = notes[chord.root] + accidental_value * chord.accidental_num
    chord_type = chord.chord_type
    extension = chord.extensions

    chord_notes = get_basic_chord_notes(root, chord_type, note_reverse)
    extension_notes = add_extension_notes(root, chord_type, extension, note_reverse)
    chord_notes.extend(extension_notes)

    return chord_notes

def set_all_start_times(chords: List[ParsedChord]):
    """
    Function to set the start time of all chords in a list of chords

    Parameters
    ----------
    chords : list
        List of chords

    Returns
    -------
    chords : list
        List of chords with start times set
    """

    chords[0].set_start_time(0)

    for i in range(1, len(chords)):
        chords[i].set_start_time(chords[i-1].end_time)
    return chords

def chord_to_xml(chord: ParsedChord) -> List[dict]:
    """
    Function to convert a ParsedChord object to a string that can be used by the xml reader

    Parameters
    ----------
    notes : list
        List of notes in the chord
    
    Returns
    -------
    xml_chord : list[str]
        An list holding all of the chord objects for a wav file recording that can be used by the xml reader
    """

    velocity = 0

    if chord.notes is None:
        chord_str = 'Chord {N}'
    else:
        chord_str = 'Chord {' + ' | '.join(chord.notes) + '}'

    xml_chord = {
        'Chord': chord_str,
        'Start': chord.start_time,
        'End': chord.end_time,
        'Duration': chord.end_time - chord.start_time,
        'Velocity': velocity,
    }
    
    return xml_chord

def xml_dict_to_chord(xml_dict: dict):
    chord = XMLChord(xml_dict)
    return chord

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

def get_amplitude(file_name: str, audio, sr) -> List[float]:
    """
    Gets the amplitudes of a sound file.

    Parameters:
        file_name (str): The file path of the WAV file

    Returns:
        np.array: A numpy array of amplitudes
    """

    YIN_FRAME_LENGTH = 256
    YIN_HOP_LENGTH = YIN_FRAME_LENGTH // 6 # Frame increment in samples. Default FRAME_LENGTH//4
    YIN_WINDOW_LENGTH = YIN_FRAME_LENGTH//2

    # Getting the amplitudes
    S = librosa.magphase(librosa.stft(audio, n_fft=YIN_FRAME_LENGTH, hop_length=YIN_HOP_LENGTH, win_length=YIN_WINDOW_LENGTH, window=np.ones))[0]
    amplitudes = librosa.feature.rms(S=S, frame_length=YIN_FRAME_LENGTH, hop_length=YIN_HOP_LENGTH)[0]

    # Convert amplitude to MIDI velocity
    midi_velocities = amplitude_to_midi_velocity(amplitudes)

    return midi_velocities

def run_chord_processing(file_name: str, json_notes: dict = None) -> str:
    """
    Function to run chord processing on a wav file
    
    Parameters
    ----------
    file_name : str
        Path to wav file
    
    Returns
    -------
    result_objec : str
        A string holding all of the notes in chords in a WAV file
    """

    YIN_FRAME_LENGTH = 256
    YIN_HOP_LENGTH = YIN_FRAME_LENGTH // 6 # Frame increment in samples. Default FRAME_LENGTH//4

    # TODO (maybe?): Remove silence using librosa.effects.trim
    
    wav_chords = find_chords(file_name)
    chord_objects = []

    # Getting the chords from the WAV file and creating a ParsedChord object
    for chord in wav_chords:
        chord_obj = parse_notation(chord)
        chord_obj.set_notes(chords_to_notes(chord_obj))
        chord_objects.append(chord_obj)
    
    chord_objects = set_all_start_times(chord_objects)

    # Turning the parsed chords into xml dictionaries
    xml_dicts = []

    for chord_obj in chord_objects:
        xml_string = chord_to_xml(chord_obj)
        xml_dicts.append(xml_string)
    
    # Turning the xml dictionaries into the XMLChord object
    xml_chords = []

    for xml_dict in xml_dicts:
        xml_chord = xml_dict_to_chord(xml_dict)
        xml_chords.append(xml_chord)

    # Loads in the audio file
    audio, sr = librosa.load(file_name)
    midi_velocities = get_amplitude(file_name, audio, sr)

    # Turning the xml chord objects into note objects with the encoded pitch
    result_chords = []

    for xml_chord in xml_chords:
        pitch = xml_chord.encrypt_and_encode()
        start = xml_chord.start
        end = xml_chord.end

        # Gets the velocity of the chords at the start of them
        frame_index = int(round(xml_chord.start * sr / YIN_HOP_LENGTH))
        velocity = midi_velocities[frame_index]

        chord_to_note = Note(pitch, velocity, start, end)

        result_chords.append(chord_to_note)    

    json_notes_dict = json.loads(json_notes)

    # Throwing in the results into the json file
    for chord in result_chords:
        json_notes_dict['notes'].append(chord.to_dict())
        json_notes_dict['size'] += 1
    
    result_object = json.dumps(json_notes_dict, indent=4)

    return result_object