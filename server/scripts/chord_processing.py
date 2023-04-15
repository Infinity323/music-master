from music21 import chord, pitch
from chord_extractor.extractors import Chordino
from typing import List

class Chord:

    def __init__(self, root, chord_type, extensions, accidental = None, accidental_num = 0, start_time = None):
        self.root = root
        self.chord_type = chord_type
        self.extensions = extensions # Interval
        self.accidental = accidental
        self.accidental_num = accidental_num
        self.start_time = start_time

    def __str__(self):
        return f"Root: {self.root}, Type: {self.chord_type}, Extensions: {self.extensions}, Accidental: {self.accidental}, Accidental Number: {self.accidental_num}, Start Time: {self.start_time}"

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
    import re

    chord_str = chord.chord
    chord_time = chord.timestamp

    chord_type = ""
    extensions = None
    accidental = None
    accidental_num = None

    if chord_str == "N":
        return Chord("N", None, extensions, accidental, accidental_num, chord_time)

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

    return Chord(root, chord_type, extensions, accidental, accidental_num, chord_time)

def add_extension_notes(root_note: int, chord_type: str, extension: int, note_reverse: dict) -> List[str]:
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
    return note_reverse[(root_note + interval) % 12]

def get_basic_chord_notes(root_note: int, chord_type: str, note_reverse: dict) -> List[str]:
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


def chords_to_notes(chord: Chord) -> List[str]:
    notes = {'C': 0, 'C#': 1, 'D': 2, 'D#': 3, 'E': 4, 'F': 5, 'F#': 6, 'G': 7, 'G#': 8, 'A': 9, 'A#': 10, 'B': 11}
    note_reverse = {v: k for k, v in notes.items()}  # Reverse of the dictionary

    accidental_value = notes[chord.accidental] if chord.accidental is not None else 0
    root = notes[chord.root] + accidental_value * chord.accidental_num
    chord_type = chord.chord_type
    extension = chord.extensions

    chord_notes = get_basic_chord_notes(root, chord_type, note_reverse)
    extension_notes = add_extension_notes(root, chord_type, extension, note_reverse)
    chord_notes.extend(extension_notes)

    return chord_notes

def run_chord_processing(file_name):
    chords = find_chords(file_name)
    chord_objects = []
    for chord in chords:
        chord_obj = parse_notation(chord)
        print(chord_obj)
        chord_objects.append(chord_obj)
