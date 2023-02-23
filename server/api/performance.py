from flask import request
from random import randint

from app import app, db
from models.performance import Performance
from models.sheetmusic import SheetMusic

from datetime import datetime

# PERFORMANCE

# Get all performance in database
@app.get("/performance")
def getAllPerformances():
    performances = db.session.query(Performance)
    return [ i.serialize for i in performances ]

# Get performance with specific ID from database
@app.get("/performance/<int:id>")
def getSpecificPerformance(id: int):
    performance = db.session.query(Performance).filter(Performance.id == id)
    return performance.serialize

# Add performance to database
@app.post("/performance")
def addPerformance():

    new_id = randint(1, 1000000)

    # to-do, get name from music id
    new_sheet_music_id = request.form.get("sheet_music_id")
    selected_sheet_music_name = db.session.query(SheetMusic).filter(SheetMusic.id == new_sheet_music_id).first().title
    new_run_number = len(db.session.query(Performance).all()) + 1

    # construct new file path and handle file upload
    new_wav_file_path = "data/wav/" + new_sheet_music_id + "_" + selected_sheet_music_name + "_" + str(new_run_number) + ".wav"
    new_wav_file_data = request.files.get("file")
    new_wav_file_data.save(new_wav_file_path)

    # analyze recording

    # set attributes
    new_date_time = datetime.now()
    new_tempo_percent_accuracy = 50 # todo change constant
    new_average_tempo = 120 # todo change constant
    new_tuning_percent_accuracy = 50 # todo change constant
    new_dynamics_percent_accuracy = 50 # todo change constant
    new_data_file_path = "filepath" # todo change constant

    # send info to database
    new_performance = Performance(new_id, new_sheet_music_id, new_run_number, new_date_time, new_tempo_percent_accuracy, new_average_tempo, new_tuning_percent_accuracy, new_dynamics_percent_accuracy, new_wav_file_path, new_data_file_path)
    db.session.add(new_performance)
    db.session.commit()
    return new_performance.serialize

# Delete performance from database
@app.delete("/performance/<int:id>")
def deletePerformance(id):
    performance = db.session.query(Performance).filter(Performance.id == id).first()
    if performance:
        db.session.delete(performance)
        db.session.commit()
        return performance.serialize
    else:
        return {}