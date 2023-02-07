from flask import request, jsonify

from app import app, db
from models.sheetmusic import SheetMusic

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
    newId = 1
    newTitle = request.form.get("title")
    newSheetMusic = SheetMusic(newId, newTitle)
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