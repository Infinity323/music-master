from flask import request
from random import randint
import json

from app import app, db
from models.sheetmusic import SheetMusic
from xmlreader.musicxmlreader import MusicXMLReader

# SHEET MUSIC

# Get all sheet music in database
@app.get("/sheetmusic")
def getAllSheetMusic():
    sheetMusics = db.session.query(SheetMusic)
    return [ i.serialize for i in sheetMusics ]

# Get sheet music with specific ID from database
@app.get("/sheetmusic/<int:id>")
def getSpecificSheetMusic(id: int):
    sheetMusic = db.session.query(SheetMusic).filter(SheetMusic.id == id).first()
    return sheetMusic.serialize

# Add sheet music to database
@app.post("/sheetmusic")
def addSheetMusic():
    new_id = randint(1, 1000000)
    new_title = request.form.get("title")
    new_composer = request.form.get("composer")
    new_instrument = request.form.get("instrument")
    # Construct new file path and handle file upload
    new_pdf_file_path = "data/xml/" + new_title + ".xml"
    new_pdf_file_data = request.files.get("file")
    new_pdf_file_data.save(new_pdf_file_path)
    # Read XML file and convert to MIDI
    xmlReader = MusicXMLReader(new_pdf_file_path)
    xmlReader.save_notes_json()
    # Add to database
    newSheetMusic = SheetMusic(new_id, new_title, new_composer, new_instrument, new_pdf_file_path, None, None)
    db.session.add(newSheetMusic)
    db.session.commit()
    return newSheetMusic.serialize

# Delete sheet music from database
@app.delete("/sheetmusic/<int:id>")
def deleteSheetMusic(id):
    sheetMusic = db.session.query(SheetMusic).filter(SheetMusic.id == id).first()
    if sheetMusic:
        db.session.delete(sheetMusic)
        db.session.commit()
        return sheetMusic.serialize
    else:
        return {}