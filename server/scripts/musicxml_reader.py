import json
import pygame
import pretty_midi
from music21 import converter, environment, chord, pitch, tempo, note as m21note
from mido import MidiFile

FREQUENCY_OFFSETS = {
    "Piano": 0,
    "Guitar": 0,
    "Violin": 0,
    "Flute": 0,
    "Clarinet": -2,
    "Trumpet": -2,
    "Saxophone": 3,
}

SEMITONE_RATIO = 1.05946

# used for indicating things like "dotted quarter note"
def get_type_with_dots(element):
    type_with_dots = element.duration.type
    for _ in range(element.duration.dots):
        type_with_dots = "dotted " + type_with_dots
    return type_with_dots

class MusicXMLReader:
    def __init__(self, xml_file, midi_file_out, instrument="Piano", custom_tempo=120):
        # Parse the MusicXML file and create a MIDI file
        self.xml_score = converter.parse(xml_file)

        # Set the custom tempo
        self.set_custom_tempo(custom_tempo)
        
        # Set the instrument
        if not FREQUENCY_OFFSETS.get(instrument):
            self.instrument = "Piano"
        else:
            self.instrument = instrument

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

    def get_tempo(self):
        # Return the first detected tempo and assume that for the entire piece
        if self.pretty_midi.get_tempo_changes()[1].size > 0:
            return self.pretty_midi.get_tempo_changes()[1][0]
        else:
            # Default tempo is 120
            return 120

    def get_notes(self, part_index=0):
        # Get a list of notes for the specified instrument
        notes_list = []
        notes = self.pretty_midi.instruments[part_index].notes
        for note in notes:
            notes_list.append({
                "pitch": pitch.Pitch(midi=note.pitch).frequency * # use nameWithOctave for A4
                    (SEMITONE_RATIO**FREQUENCY_OFFSETS.get(self.instrument)), # apply instrument pitch offset
                "velocity": note.velocity,
                "start": note.start,
                "end": note.end
            })
        return notes_list
    
    def get_notes_and_measure_num(self, part_index=0):
        # Get a list of notes and rests for the specified instrument
        elements_list = []
        elements = self.xml_score.parts[part_index].flat.getElementsByClass([m21note.Note, m21note.Rest])

        # Dictionary to store the count of notes and rests in each measure
        measure_position_count = {}

        for element in elements:
            measure_number = element.measureNumber
            if measure_number not in measure_position_count:
                measure_position_count[measure_number] = 1

            if isinstance(element, m21note.Note):
                elements_list.append({
                                    "element": "note",
                                    "name": element.nameWithOctave,
                                    "type": get_type_with_dots(element),
                                    "measure": measure_number,
                                    "position": measure_position_count[measure_number]
                                })
            elif isinstance(element, m21note.Rest):
                elements_list.append({
                                    "element": "rest",
                                    "type": get_type_with_dots(element),
                                    "measure": measure_number,
                                    "position": measure_position_count[measure_number]
                                })

            # Increment the count for the current measure
            measure_position_count[measure_number] += 1

        return elements_list


    def save_notes_json(self, json_file_out, part_index=0):
        # Save note data as a JSON file and return the JSON data as a string
        notes = self.get_notes(part_index)
        tempo = self.get_tempo()
        data = {
            "size": len(notes),
            "tempo": tempo,
            "notes": notes
        }

        with open(json_file_out, 'w') as outfile:
            json.dump(data, outfile, indent=4)  # Indent the JSON output for better readability

        return json.dumps(data, indent=4)  # Indent the returned JSON string for better readability

    def parse_chords(self, part_index=0):
        # Parse chords in the score
        chords = []
        for element in self.xml_score.recurse():
            if isinstance(element, chord.Chord):
                # Get start and end times for the chord
                start_time = element.offset
                end_time = start_time + element.duration.quarterLength

                # Get the average velocity for the chord
                for individual_note in element.notes:
                    velocity = individual_note.volume.velocity 

                chords.append({'Chord': element.fullName, 'Start': start_time, 'End': end_time, 'Duration': element.duration.quarterLength, 'Velocity': velocity})

        return chords

    def play(self):
        # Play the MIDI file using pygame
        with pygame.mixer.init():
            pygame.mixer.music.load(self.midi_filename)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
            pygame.mixer.quit()

# def main():
    # Set the environment variable for the MuseScore path based on the operating system

    # note: envronemnt must have MuseScore installed!
    # use for Mac '/Applications/MuseScore 4.app/Contents/MacOS/mscore' 
    # use for linux '/usr/share/applications/mscore.desktop'
    # use for Windows?? i think not certain 'C:\Program Files\MuseScore 4/mscore.exe'
    # environment_path = '/Applications/MuseScore 4.app/Contents/MacOS/mscore'
    # environment.set('musescoreDirectPNGPath', environment_path)

    # Create a MusicXMLReader instance and print the JSON representation of note data
    # reader = MusicXMLReader('example.musicxml')
    # print(reader.save_notes_json())

# if __name__ == '__main__':
#     main()