from flask import request, Blueprint
from random import randint
import json

from models import db
from models.sheetmusic import SheetMusic
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

    # Add to database
    # TODO: goal entity should update this tempo, currently it is set to None
    newSheetMusic = SheetMusic(new_id, new_title, new_composer, new_instrument, new_xml_file_path, new_dat_file_path, None, note_info_file_path)
    db.session.add(newSheetMusic)
    db.session.commit()
    return newSheetMusic.serialize

# Delete sheet music from database
@sheetmusic_blueprint.route("/sheetmusic/<int:id>", methods=["DELETE"])
def deleteSheetMusic(id):
    sheetMusic = db.session.query(SheetMusic).filter(SheetMusic.id == id).first()
    if sheetMusic:
        db.session.delete(sheetMusic)
        db.session.commit()
        return sheetMusic.serialize
    else:
        return {}