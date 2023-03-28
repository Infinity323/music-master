import json
import pygame
import pretty_midi
from mido import MidiFile
from music21 import converter, environment, pitch




class MusicXMLReader(MidiFile, pretty_midi.PrettyMIDI):
    def __init__(self, xml_file, midi_file_out='example.mid'):
        # Parse the MusicXML file and create a MIDI file
        self.xml_score = converter.parse(xml_file)
        self.xml_score.write("midi", midi_file_out)
        self.midi_filename = midi_file_out

        # Initialize parent classes
        pretty_midi.PrettyMIDI.__init__(self, midi_file_out)
        MidiFile.__init__(self, midi_file_out)

    def get_xml_data(self):
        # Return the parsed MusicXML score
        return self.xml_score

    def print_score(self):
        # Display the parsed MusicXML score
        self.xml_score.show()

    def get_notes(self, instrument=0):
        # Get a list of notes for the specified instrument
        notes_list = []
        notes = self.instruments[instrument].notes
        for note in notes:
            notes_list.append({"pitch": pitch.Pitch(midi=note.pitch).nameWithOctave, 
                               "velocity": note.velocity, 
                               "start": note.start,
                               "end": note.end
                               })
        return notes_list
    
    def save_notes_json(self, instrument=0, json_file_out='notes.json'):
        # Save note data as a JSON file and return the JSON data as a string
        notes = self.get_notes(instrument)
        data = {"notes": notes}

        with open(json_file_out, 'w') as outfile:
            json.dump(data, outfile)

        return json.dumps(data)
    
    def play(self):
        # Play the MIDI file using pygame
        with pygame.mixer.init():
            pygame.mixer.music.load(self.midi_filename)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)


def main():
    # note: envronemnt must have MuseScore installed!
    # use for Mac '/Applications/MuseScore 4.app/Contents/MacOS/mscore' 
    # use for linux '/usr/share/applications/mscore.desktop'
    # use for Windows?? i think not certain 'C:\Program Files\MuseScore 4/mscore.exe'
    environment_path = '/usr/share/applications/mscore.desktop'
    environment.set('musescoreDirectPNGPath', environment_path)

    # Create a MusicXMLReader instance and print the JSON representation of note data
    reader = MusicXMLReader('example.musicxml')
    print(reader.save_notes_json())
    


if __name__ == '__main__':
    main() 