import json
import pygame
import pretty_midi
from music21 import converter, environment, pitch, tempo, note as m21note
from mido import MidiFile

class MusicXMLReader:
    def __init__(self, xml_file, midi_file_out, custom_tempo=120):
        # Parse the MusicXML file and create a MIDI file
        self.xml_score = converter.parse(xml_file)

        # Set the custom tempo
        self.set_custom_tempo(custom_tempo)

        # Create a MIDI file
        self.xml_score.write("midi", midi_file_out)
        self.midi_filename = midi_file_out

        # Initialize the PrettyMIDI object
        self.pretty_midi = pretty_midi.PrettyMIDI(midi_file_out)
    
    def set_custom_tempo(self, custom_tempo):
        # Set the custom tempo for all parts in the score
        for part in self.xml_score.parts:
            # Create a tempo indication (metronome mark) for the custom tempo
            metronome = tempo.MetronomeMark(number=custom_tempo)

            # Insert the tempo indication at the beginning of the part
            part.insert(0, metronome)

    def get_xml_data(self):
        # Return the parsed MusicXML score
        return self.xml_score

    def print_score(self):
        # Display the parsed MusicXML score
        self.xml_score.show()

    def get_notes(self, part_index=0):
        # Get a list of notes for the specified instrument
        notes_list = []
        notes = self.pretty_midi.instruments[part_index].notes
        for note in notes:
            notes_list.append({"pitch": pitch.Pitch(midi=note.pitch).nameWithOctave,
                               "velocity": note.velocity,
                               "start": note.start,
                               "end": note.end
                               })
        return notes_list
    
    def get_notes_and_measure_num(self, part_index=0):
        # Get a list of notes and rests for the specified instrument
        elements_list = []
        elements = self.xml_score.parts[part_index].flat.getElementsByClass([m21note.Note, m21note.Rest])
        
        for element in elements:
            if isinstance(element, m21note.Note):
                elements_list.append({
                                    "element": "note",
                                    "name": element.nameWithOctave,
                                    "type": element.duration.type,
                                    "measure": element.measureNumber
                                })
            elif isinstance(element, m21note.Rest):
                elements_list.append({
                                    "element": "rest",
                                    "type": element.duration.type,
                                    "measure": element.measureNumber
                                })
        
        return elements_list

    def save_notes_json(self, json_file_out, part_index=0):
        # Save note data as a JSON file and return the JSON data as a string
        notes = self.get_notes(part_index)
        data = {"notes": notes}

        with open(json_file_out, 'w') as outfile:
            json.dump(data, outfile, indent=4)  # Indent the JSON output for better readability

        return json.dumps(data, indent=4)  # Indent the returned JSON string for better readability

    def play(self):
        # Play the MIDI file using pygame
        with pygame.mixer.init():
            pygame.mixer.music.load(self.midi_filename)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
            pygame.mixer.quit()

def main():
    # Set the environment variable for the MuseScore path based on the operating system

    # note: envronemnt must have MuseScore installed!
    # use for Mac '/Applications/MuseScore 4.app/Contents/MacOS/mscore' 
    # use for linux '/usr/share/applications/mscore.desktop'
    # use for Windows?? i think not certain 'C:\Program Files\MuseScore 4/mscore.exe'
    environment_path = '/Applications/MuseScore 4.app/Contents/MacOS/mscore'
    environment.set('musescoreDirectPNGPath', environment_path)

    # Create a MusicXMLReader instance and print the JSON representation of note data
    # reader = MusicXMLReader('example.musicxml')
    # print(reader.save_notes_json())

if __name__ == '__main__':
    main()