import pretty_midi
import pygame

from mido import MidiFile
from music21 import *
from pretty_midi import PrettyMIDI


class MusicXMLReader(MidiFile, PrettyMIDI):
    def __init__(self, xml_file, midi_file_out='example.mid'):
        self.xml_score = converter.parse(xml_file)
        self.xml_score.write("midi", midi_file_out)
        self.midi_filename = midi_file_out
        PrettyMIDI.__init__(self, midi_file_out)
        MidiFile.__init__(self, midi_file_out)

    def get_xml_data(self):
        return self.xml_score

    def print_score(self):
        self.xml_score.show()

    def get_notes(self, instrument=0):
        return self.instruments[instrument].notes
    
    def get_notes_and_instruments(self, instrument=0):
        return {(note.pitch, note.start, note.end): instrument for note in self.get_notes(instrument)}
    
    def play(self):
        pygame.mixer.init()
        pygame.mixer.music.load(self.midi_filename)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)


    

def main():
    environment_path = '/Applications/MuseScore 4.app/Contents/MacOS/mscore'
    environment.set('musescoreDirectPNGPath', environment_path)

    reader = MusicXMLReader('example.musicxml')
    reader.play()
    


if __name__ == '__main__':
    main() 