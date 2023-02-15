from flask import request
from random import randint

from app import app, db
from models.sheetmusic import SheetMusic

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
    data = request.get_json()
    new_id = randint(1, 1000000);
    new_title = data.get("title")
    new_composer = data.get("composer")
    new_instrument = data.get("instrument")
    new_pdf_file_path = data.get("pdf_file_path")
    new_data_file_path = data.get("data_file_path")
    new_tempo = data.get("tempo")
    newSheetMusic = SheetMusic(new_id, new_title, new_composer, new_instrument, new_pdf_file_path, new_data_file_path, new_tempo)
    db.session.add(newSheetMusic)
    db.session.commit()
    return newSheetMusic.serialize

# Delete sheet music from database
@app.delete("/sheetmusic/<int:id>")
def deleteSheetMusic(id):
    sheetMusic = db.session.query(SheetMusic).filter(SheetMusic.id == id).first()
    db.session.delete(sheetMusic)
    db.session.commit()
    return sheetMusic.serialize