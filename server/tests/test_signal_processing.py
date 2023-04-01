"""Test Signal Processing

Test signal processing note extrapolation.
"""
from scripts.signal_processing import *
import json

WAV_DATA_PATH = "server/tests/data/wav/"
JSON_DATA_PATH = "server/tests/data/dat/"

MAX_CENTS_ERROR = 10

def initialize_notes(path):
    with open(JSON_DATA_PATH + path) as file:
        json_data = json.load(file)
    notes = [Note(note["pitch"], note["velocity"], note["start"], note["end"])
             for note in json_data["notes"]]
    
    return notes

def test_cmajor_expected():
    # File exported from MuseScore
    file = WAV_DATA_PATH + "cmaj_expected.wav"
    f0, times, amp_maxes = get_f0_time_amp(file)
    notes = freq_to_notes(f0, times, amp_maxes)
    xml_notes = initialize_notes("CMajor.json")
    
    assert(len(notes) == len(xml_notes))
    for i in range(len(notes)):
        assert(Note.frequency_difference_in_cents(notes[i].pitch, xml_notes[i].pitch) <= MAX_CENTS_ERROR)

def test_cmajor_actual():
    # File is an actual piano recording
    file = WAV_DATA_PATH + "cmaj_actual.wav"
    f0, times, amp_maxes = get_f0_time_amp(file)
    notes = freq_to_notes(f0, times, amp_maxes)
    xml_notes = initialize_notes("CMajor.json")
    
    assert(len(notes) == len(xml_notes))
    for i in range(len(notes)):
        assert(Note.frequency_difference_in_cents(notes[i].pitch, xml_notes[i].pitch) <= MAX_CENTS_ERROR)

def test_happy_birthday_expected():
    # File exported from MuseScore
    file = WAV_DATA_PATH + "happybirthday_expected.wav"
    f0, times, amp_maxes = get_f0_time_amp(file)
    notes = freq_to_notes(f0, times, amp_maxes)
    xml_notes = initialize_notes("Happy Birthday.json")
    
    assert(len(notes) == len(xml_notes))
    for i in range(len(notes)):
        assert(Note.frequency_difference_in_cents(notes[i].pitch, xml_notes[i].pitch) <= MAX_CENTS_ERROR)
    
def test_happy_birthday_actual():
    # File is an actual piano recording
    file = WAV_DATA_PATH + "happybirthday_actual.wav"
    f0, times, amp_maxes = get_f0_time_amp(file)
    notes = freq_to_notes(f0, times, amp_maxes)
    xml_notes = initialize_notes("Happy Birthday.json")
    
    assert(len(notes) == len(xml_notes))
    for i in range(len(notes)):
        assert(Note.frequency_difference_in_cents(notes[i].pitch, xml_notes[i].pitch) <= MAX_CENTS_ERROR)