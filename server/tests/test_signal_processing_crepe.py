"""Test Signal Processing

Test signal processing note extrapolation.
"""
from scripts.archived_scripts.signal_processing_crepe import *
import os
import json

TEST_DIR = os.path.dirname(os.path.abspath(__file__))
WAV_DATA_PATH = TEST_DIR + "/data/wav/"
JSON_DATA_PATH = TEST_DIR + "/data/dat/"

MAX_CENTS_DIFF_PIANO = 10

def initialize_notes(path):
    with open(JSON_DATA_PATH + path) as file:
        json_data = json.load(file)
    notes = [Note(note["pitch"], note["velocity"], note["start"], note["end"])
             for note in json_data["notes"]]
    
    return notes

def test_cmajor_expected():
    # File exported from MuseScore
    file = WAV_DATA_PATH + "cmaj_expected.wav"
    f0, times, velocities, confidences = get_f0_time_amp_crepe(file)
    notes = freq_to_notes_crepe(f0, times, velocities, confidences)
    xml_notes = initialize_notes("CMajor.json")
    
    assert(len(notes) == len(xml_notes))
    for i in range(len(notes)):
        assert(Note.difference_cents(notes[i].pitch, xml_notes[i].pitch) <= MAX_CENTS_DIFF_PIANO)

def test_cmajor_actual():
    # File is an actual piano recording
    file = WAV_DATA_PATH + "cmaj_actual.wav"
    f0, times, velocities, confidences = get_f0_time_amp_crepe(file)
    notes = freq_to_notes_crepe(f0, times, velocities, confidences)
    xml_notes = initialize_notes("CMajor.json")
    
    assert(len(notes) == len(xml_notes))
    for i in range(len(notes)):
        assert(Note.difference_cents(notes[i].pitch, xml_notes[i].pitch) <= MAX_CENTS_DIFF_PIANO)

def test_happy_birthday_expected():
    # File exported from MuseScore
    file = WAV_DATA_PATH + "happybirthday_expected.wav"
    f0, times, velocities, confidences = get_f0_time_amp_crepe(file)
    notes = freq_to_notes_crepe(f0, times, velocities, confidences)
    xml_notes = initialize_notes("Happy Birthday.json")
    
    assert(len(notes) == len(xml_notes))
    for i in range(len(notes)):
        assert(Note.difference_cents(notes[i].pitch, xml_notes[i].pitch) <= MAX_CENTS_DIFF_PIANO)
    
def test_happy_birthday_actual():
    # File is an actual piano recording
    file = WAV_DATA_PATH + "happybirthday_actual.wav"
    f0, times, velocities, confidences = get_f0_time_amp_crepe(file)
    notes = freq_to_notes_crepe(f0, times, velocities, confidences)
    xml_notes = initialize_notes("Happy Birthday.json")
    
    assert(len(notes) == len(xml_notes))
    for i in range(len(notes)):
        assert(Note.difference_cents(notes[i].pitch, xml_notes[i].pitch) <= MAX_CENTS_DIFF_PIANO)

def test_happy_birthday_staccato():
    # File exported from MuseScore (staccato)
    file = WAV_DATA_PATH + "happybirthday_staccato.wav"
    f0, times, velocities, confidences = get_f0_time_amp_crepe(file)
    notes = freq_to_notes_crepe(f0, times, velocities, confidences)
    xml_notes = initialize_notes("Happy Birthday.json")
    
    assert(len(notes) == len(xml_notes))
    for i in range(len(notes)):
        assert(Note.difference_cents(notes[i].pitch, xml_notes[i].pitch) <= MAX_CENTS_DIFF_PIANO)

def test_wet_hands_expected():
    # File exported from MuseScore
    file = WAV_DATA_PATH + "wethands_expected.wav"
    f0, times, velocities, confidences = get_f0_time_amp_crepe(file)
    notes = freq_to_notes_crepe(f0, times, velocities, confidences)
    xml_notes = initialize_notes("Wet Hands.json")
    
    assert(len(notes) == len(xml_notes))
    for i in range(len(notes)):
        assert(Note.difference_cents(notes[i].pitch, xml_notes[i].pitch) <= MAX_CENTS_DIFF_PIANO)

def test_wet_hands_actual():
    # File is an actual piano recording
    file = WAV_DATA_PATH + "wethands_actual.wav"
    f0, times, velocities, confidences = get_f0_time_amp_crepe(file)
    notes = freq_to_notes_crepe(f0, times, velocities, confidences)
    xml_notes = initialize_notes("Wet Hands.json")
    
    assert(len(notes) == len(xml_notes))
    for i in range(len(notes)):
        assert(Note.difference_cents(notes[i].pitch, xml_notes[i].pitch) <= MAX_CENTS_DIFF_PIANO)

def test_gerudo_valley_expected():
    # File exported from MuseScore
    file = WAV_DATA_PATH + "gerudovalley_expected.wav"
    f0, times, velocities, confidences = get_f0_time_amp_crepe(file)
    notes = freq_to_notes_crepe(f0, times, velocities, confidences)
    xml_notes = initialize_notes("Gerudo Valley.json")
    
    assert(len(notes) == len(xml_notes))
    for i in range(len(notes)):
        assert(Note.difference_cents(notes[i].pitch, xml_notes[i].pitch) <= MAX_CENTS_DIFF_PIANO)