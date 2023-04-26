import json
# import pygame
import pretty_midi
import music21
from music21 import converter, pitch, tempo, note as m21note, repeat
# from music21 import environment
# from mido import MidiFile

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

        # Handle al coda instructions
        self.handle_al_coda()

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

    def handle_al_coda(self):
        for part in self.xml_score.parts:
            # Initialize variables to store positions of the instructions
            coda_position = None
            segno_position = None
            to_coda_position = None

            # Search for the instructions in the part
            for measure in part.getElementsByClass(music21.stream.Measure):
                for element in measure.elements:
                    if isinstance(element, music21.repeat.Coda):
                        coda_position = measure.number

                    if isinstance(element, music21.repeat.Segno):
                        segno_position = measure.number

                    if isinstance(element, music21.expressions.TextExpression):
                        if 'To Coda' in element.content:
                            to_coda_position = measure.number

            # If all positions are found, handle the Al Coda instructions
            if coda_position is not None and segno_position is not None and to_coda_position is not None:
                # Reorder the measures based on the Al Coda instructions
                reordered_measures = music21.stream.Stream()
                reordered_measures.append(part.measures(0, segno_position - 1).flat.elements)
                reordered_measures.append(part.measures(segno_position, to_coda_position).flat.elements)
                
                # Append the remaining measures after the coda_position
                reordered_measures.append(part.measures(coda_position + 1, None).flat.elements)

                # Replace the original measures with the reordered measures
                part.elements = reordered_measures.elements
    
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
        elements_list = self.get_notes_and_measure_num(part_index)
        return self.get_notes_from_elements(elements_list)
    
    def get_notes_from_elements(self, elements_list):
        notes_list = []
        instrument_notes = self.pretty_midi.instruments[0].notes
        for element in elements_list:
            if element["element"] == "note":
                note_pitch = pitch.Pitch(element["name"]).midi

                # Find the corresponding note in the PrettyMIDI notes list
                matched_note = None
                for note in instrument_notes:
                    if note.pitch == note_pitch:
                        matched_note = note
                        break

                if matched_note is not None:
                    notes_list.append({
                        "pitch": pitch.Pitch(midi=note_pitch).frequency *
                                (SEMITONE_RATIO ** FREQUENCY_OFFSETS.get(self.instrument)),
                        "velocity": matched_note.velocity,
                        "start": matched_note.start,
                        "end": matched_note.end
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
                                    "name": "Rest",
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
        downbeat_locations = self.pretty_midi.get_downbeats().tolist()
        data = {
            "size": len(notes),
            "tempo": tempo,
            "downbeat_locations": downbeat_locations,
            "notes": notes,
        }

        with open(json_file_out, 'w') as outfile:
            json.dump(data, outfile, indent=4)  # Indent the JSON output for better readability

        return json.dumps(data, indent=4)  # Indent the returned JSON string for better readability

    # def play(self):
    #     # Play the MIDI file using pygame
    #     with pygame.mixer.init():
    #         pygame.mixer.music.load(self.midi_filename)
    #         pygame.mixer.music.play()
    #         while pygame.mixer.music.get_busy():
    #             pygame.time.Clock().tick(10)
    #         pygame.mixer.quit()

def main():
    # Set the environment variable for the MuseScore path based on the operating system

    # note: envronemnt must have MuseScore installed!
    # use for Mac '/Applications/MuseScore 4.app/Contents/MacOS/mscore' 
    # use for linux '/usr/share/applications/mscore.desktop'
    # use for Windows?? i think not certain 'C:\Program Files\MuseScore 4/mscore.exe'
    # environment_path = '/Applications/MuseScore 4.app/Contents/MacOS/mscore'
    # environment.set('musescoreDirectPNGPath', environment_path)

    # Create a MusicXMLReader instance and print the JSON representation of note data
    # reader = MusicXMLReader('Scotland_the_Brave-_Clarinet.musicxml', instrument="Clarinet", midi_file_out="out.wav")
    # print(reader.save_notes_json("out.json"))
    pass

if __name__ == '__main__':
    main()