from music21 import chord, pitch
from chord_extractor.extractors import Chordino

class Chord:

    def __init__(self, root, chord_type, extensions, accidental, accidental_num, start_time = None):
        self.root = root
        self.chord_type = chord_type
        self.extensions = extensions
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
    # Does not handle dimished chords, augmented chords, or sus chords
    import re

    chord_str = chord.chord
    chord_time = chord.timestamp

    chord_type = ""
    extensions = None
    accidental = None
    accidental_num = None

    if chord_str == "N":
        return Chord("N", None, extensions, accidental, accidental_num, chord_time)

    # Finds the root and quality of a chord (where quality is the rest of the chord string)
    match = re.match(r'([A-Ga-g][#b]?)([^/]*)', chord_str)

    if not match:
        raise ValueError('Invalid chord notation')
    
    root, quality = match.groups()

    # Checking if a chord is major or minor

    minor = r'(?:m|M|min)'
    if re.search(minor, quality):
        quality = re.sub(minor, '', quality) # Removing it from the string
        chord_type = "minor"
    else:
        chord_type = "major"

    # Checking if a chord is a 7, 9, 11, or 13, chord
    if not quality:
        # Empty check
        return Chord(root, chord_type, extensions, accidental, accidental_num, chord_time)

    if quality[0] == "1":
        extensions = int(quality[0:2]) # 11th or 13th chords
        quality = quality[2:] # Removing the number from the string
    elif quality[0] == "6" or quality[0] == "7" or quality[0] == "9":
        extensions = int(quality[0]) # 7th or 9th chords
        quality = quality[1:] # Removing the number from the string

    # Checking if a chord has an accidental
    if not quality:
        # Empty check
        return Chord(root, chord_type, extensions, accidental, accidental_num, chord_time)

    if quality[0] == "#":
        accidental = "sharp"
        quality = quality[1:]
        accidental_num = int(quality)
        quality = ""
    elif quality[0] == "b":
        accidental = "flat"
        quality = quality[1:]
        accidental_num = int(quality)
        quality = ""

    if len(quality) != 0:
        return ValueError('Invalid or unsupported chord notation')

    return Chord(root, chord_type, extensions, accidental, accidental_num, chord_time)

def chords_to_notes(chord):
    notes = {'C': 0, 'C#': 1, 'D': 2, 'D#': 3, 'E': 4, 'F': 5, 'F#': 6, 'G': 7, 'G#': 8, 'A': 9, 'A#': 10, 'B': 11}
    note_reverse = {v: k for k, v in notes.items()} # Reverse of the dictionary

    root = chord.root
    chord_type = chord.chord_type
    extensions = chord.extensions
    accidental = chord.accidental
    accidental_num = chord.accidental_num

    chord_notes = []

    # Adding in the root note to the notes list
    chord_notes.append(root)

    # Assigning notes based on the chord type
    if extensions == None:
        if chord_type == "major":
            chord_notes.append(note_reverse[(notes[root] + 4) % 12])
            chord_notes.append(note_reverse[(notes[root] + 7) % 12])
        elif chord_type == "minor":
            chord_notes.append(note_reverse[(notes[root] + 3) % 12])
            chord_notes.append(note_reverse[(notes[root] + 7) % 12])
    elif extensions == 6:
        if chord_type == "major":
            chord_notes.append(note_reverse[(notes[root] + 4) % 12])
            chord_notes.append(note_reverse[(notes[root] + 7) % 12])
            chord_notes.append(note_reverse[(notes[root] + 9) % 12])
        elif chord_type == "minor":
            chord_notes.append(note_reverse[(notes[root] + 3) % 12])
            chord_notes.append(note_reverse[(notes[root] + 7) % 12])
            chord_notes.append(note_reverse[(notes[root] + 9) % 12])
    elif extensions == 7:
        if chord_type == "major":
            chord_notes.append(note_reverse[(notes[root] + 4) % 12])
            chord_notes.append(note_reverse[(notes[root] + 7) % 12])
            chord_notes.append(note_reverse[(notes[root] + 10) % 12])
        elif chord_type == "minor":
            chord_notes.append(note_reverse[(notes[root] + 3) % 12])
            chord_notes.append(note_reverse[(notes[root] + 7) % 12])
            chord_notes.append(note_reverse[(notes[root] + 10) % 12])
    elif extensions == 9:
        if chord_type == "major":
            chord_notes.append(note_reverse[(notes[root] + 4) % 12])
            chord_notes.append(note_reverse[(notes[root] + 7) % 12])
            chord_notes.append(note_reverse[(notes[root] + 10) % 12])
            chord_notes.append(note_reverse[(notes[root] + 14) % 12])
        elif chord_type == "minor":
            chord_notes.append(note_reverse[(notes[root] + 3) % 12])
            chord_notes.append(note_reverse[(notes[root] + 7) % 12])
            chord_notes.append(note_reverse[(notes[root] + 10) % 12])
            chord_notes.append(note_reverse[(notes[root] + 14) % 12])
    elif extensions == 11:
        if chord_type == "major":
            chord_notes.append(note_reverse[(notes[root] + 4) % 12])
            chord_notes.append(note_reverse[(notes[root] + 7) % 12])
            chord_notes.append(note_reverse[(notes[root] + 10) % 12])
            chord_notes.append(note_reverse[(notes[root] + 14) % 12])
            chord_notes.append(note_reverse[(notes[root] + 17) % 12])
        elif chord_type == "minor":
            chord_notes.append(note_reverse[(notes[root] + 3) % 12])
            chord_notes.append(note_reverse[(notes[root] + 7) % 12])
            chord_notes.append(note_reverse[(notes[root] + 10) % 12])
            chord_notes.append(note_reverse[(notes[root] + 14) % 12])
            chord_notes.append(note_reverse[(notes[root] + 17) % 12])
    elif extensions == 13:
        if chord_type == "major":
            chord_notes.append(note_reverse[(notes[root] + 4) % 12])
            chord_notes.append(note_reverse[(notes[root] + 7) % 12])
            chord_notes.append(note_reverse[(notes[root] + 10) % 12])
            chord_notes.append(note_reverse[(notes[root] + 14) % 12])
            chord_notes.append(note_reverse[(notes[root] + 17) % 12])
            chord_notes.append(note_reverse[(notes[root] + 21) % 12])
        elif chord_type == "minor":
            chord_notes.append(note_reverse[(notes[root] + 3) % 12])
            chord_notes.append(note_reverse[(notes[root] + 7) % 12])
            chord_notes.append(note_reverse[(notes[root] + 10) % 12])
            chord_notes.append(note_reverse[(notes[root] + 14) % 12])
            chord_notes.append(note_reverse[(notes[root] + 17) % 12])
            chord_notes.append(note_reverse[(notes[root] + 21) % 12])

    # Adding in the accidental
    # Goes here
    
    return chord_notes

def notes_to_chords():
    pass

def run_chord_processing(file_name):
    chords = find_chords(file_name)
    chord_objects = []
    for chord in chords:
        chord_obj = parse_notation(chord)
        print(chord_obj)
        chord_objects.append(chord_obj)
