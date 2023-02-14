from flask import request, jsonify

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
    new_id = 1
    new_title = request.form.get("title")
    new_composer = request.form.get("new_composer")
    new_instrument = request.form.get("instrument")
    new_pdf_file_path = request.form.get("pdf_file_path")
    new_data_file_path = request.form.get("data_file_path")
    new_tempo = request.form.get("tempo")
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