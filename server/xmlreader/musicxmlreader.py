import json
import pretty_midi
import pygame

from mido import MidiFile
from music21 import *
from music21 import pitch
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
        notes_list = []
        notes = self.instruments[instrument].notes
        for note in notes:
            notes_list.append({"pitch": pitch.Pitch(midi=note.pitch).nameWithOctave, 
                               "velocity": note.velocity, 
                               "start": note.start,
                               "end": note.end
                               })
        return notes_list
    
    def save_notes_json(self, instrument=0):
        notes = self.get_notes(instrument)
        data = {"notes": notes}

        with open('notes.json', 'w') as outfile:
            json.dump(data, outfile)

        return json.dumps(data)
    
    def play(self):
        pygame.mixer.init()
        pygame.mixer.music.load(self.midi_filename)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)


    

def main():
    # note: envronemnt must have MuseScore installed!
    # use for Mac '/Applications/MuseScore 4.app/Contents/MacOS/mscore' 
    # use for linux '/usr/share/applications/mscore.desktop'
    # use for Windows?? i think not certain 'C:\Program Files\MuseScore 4/mscore.exe'
    environment_path = '/Applications/MuseScore 4.app/Contents/MacOS/mscore' 
    environment.set('musescoreDirectPNGPath', environment_path)

    reader = MusicXMLReader('example.musicxml')
    print(reader.save_notes_json())
    


if __name__ == '__main__':
    main() 