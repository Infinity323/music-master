from flask import request, Blueprint
from random import randint
import json
import os

from models import db
from models.sheetmusic import SheetMusic
from models.goal import Goal
from models.performance import Performance
from scripts.musicxml_reader import MusicXMLReader

sheetmusic_blueprint = Blueprint("sheetmusic", __name__)

# SHEET MUSIC

# Get all sheet music in database
@sheetmusic_blueprint.route("/sheetmusic", methods=["GET"])
def getAllSheetMusic():
    
    sheetMusics = db.session.query(SheetMusic)
    return [ i.serialize for i in sheetMusics ]

# Get sheet music with specific ID from database
@sheetmusic_blueprint.route("/sheetmusic/<int:id>", methods=["GET"])
def getSpecificSheetMusic(id: int):
    sheetMusic = db.session.query(SheetMusic).filter(SheetMusic.id == id).first()
    return sheetMusic.serialize

# Add sheet music to database
@sheetmusic_blueprint.route("/sheetmusic", methods=["POST"])
def addSheetMusic():
    new_id = randint(1, 1000000)
    new_title = request.form.get("title")
    new_composer = request.form.get("composer")
    new_instrument = request.form.get("instrument")

    # Construct new file path and handle file upload
    new_xml_file_path = "data/xml/" + new_title + ".musicxml"
    new_midi_file_path = "data/dat/" + new_title + ".mid"
    new_dat_file_path = "data/dat/" + new_title + ".json"
    new_xml_file_data = request.files.get("file")
    new_xml_file_data.save(new_xml_file_path)

    # Read XML file and convert to MIDI
    xmlReader = MusicXMLReader(new_xml_file_path, new_midi_file_path, new_instrument)
    xmlReader.save_notes_json(new_dat_file_path)

    # save note info locally
    note_info = xmlReader.get_notes_and_measure_num()
    note_info_file_path = "data/dat/" + new_title + "_note_info.json"
    with open(note_info_file_path, 'w') as note_info_file:
        json.dump([info for info in note_info], note_info_file, indent=4)

    # delete temp midi file
    if os.path.isfile(new_midi_file_path):
        os.remove(new_midi_file_path)
        print("temp midi file has been deleted.")
    else:
        print("temp midi file does not exist and cannot be deleted.")

    # Add to database
    # TODO: goal entity should update this tempo, currently it is set to None
    newSheetMusic = SheetMusic(new_id, new_title, new_composer, new_instrument, new_xml_file_path, new_dat_file_path, None, note_info_file_path)
    db.session.add(newSheetMusic)
    db.session.commit()
    return newSheetMusic.serialize

# Delete sheet music from database
@sheetmusic_blueprint.route("/sheetmusic/<int:id>", methods=["DELETE"])
def deleteSheetMusic(id):
    # get current sheet music object
    sheetMusic = db.session.query(SheetMusic).filter(SheetMusic.id == id).first()

    # clear all associated goals
    associated_goals = db.session.query(Goal).filter(Goal.sheet_music_id == id)
    for goal in associated_goals:
        db.session.delete(goal)
    
    # clear all associated performances (for each loop)
    associated_performances = db.session.query(Performance).filter(Performance.sheet_music_id == id)
    for performance in associated_performances:   
        # delete associated .wav files
        wav_file_path = performance.wav_file_path
        if os.path.isfile(wav_file_path):
            os.remove(wav_file_path)
            print("WAV file has been deleted.")
        else:
            print("WAV file does not exist and cannot be deleted.")

        # delete diff json
        diff_file_path = performance.diff_file_path
        if os.path.isfile(diff_file_path):
            os.remove(diff_file_path)
            print("diff file has been deleted.")
        else:
            print("diff file does not exist and cannot be deleted.")

        # delete recording json
        recording_data_file_path = performance.data_file_path
        if os.path.isfile(recording_data_file_path):
            os.remove(recording_data_file_path)
            print("rec dat file has been deleted.")
        else:
            print("rec dat file does not exist and cannot be deleted.")

        # delete performance entries
        db.session.delete(performance)

    # clear sheet music
    if sheetMusic:
        # delete all associated data files

        # delete musicxml file
        musicxml_file_path = sheetMusic.pdf_file_path
        if os.path.isfile(musicxml_file_path):
            os.remove(musicxml_file_path)
            print("musicxml file has been deleted.")
        else:
            print("musicxml file does not exist and cannot be deleted.")

        # delete musicxml dat json
        musicxml_data_file_path = sheetMusic.data_file_path
        if os.path.isfile(musicxml_data_file_path):
            os.remove(musicxml_data_file_path)
            print("musicxml dat file has been deleted.")
        else:
            print("musicxml dat file does not exist and cannot be deleted.")

        # delete note info json
        note_info_file_path = sheetMusic.note_info_file_path
        if os.path.isfile(note_info_file_path):
            os.remove(note_info_file_path)
            print("note info file has been deleted.")
        else:
            print("note info file does not exist and cannot be deleted.")

        # delete entry
        db.session.delete(sheetMusic)
        db.session.commit()
        return sheetMusic.serialize
    else:
        return {}