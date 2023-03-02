from flask import request
from random import randint

import json

from app import app, db
from models.performance import Performance
from models.sheetmusic import SheetMusic

from signal_processing import signal_processing
from mxl_wav_compare import compare_tuning, compare_dynamics, compare_tempo

from datetime import datetime

import os

# PERFORMANCE

# Get all performance in database
@app.get("/performance")
def getAllPerformances():
    performances = db.session.query(Performance)
    return [ i.serialize for i in performances ]

# Get performance with specific ID from database
@app.get("/performance/<int:id>")
def getSpecificPerformance(id: int):
    performance = db.session.query(Performance).filter(Performance.id == id).first()
    return performance.serialize

# Add performance to database
@app.post("/performance")
def addPerformance():

    new_id = randint(1, 1000000)

    # to-do, get name from music id
    new_sheet_music_id = request.form.get("sheet_music_id")
    selected_sheet_music_name = db.session.query(SheetMusic).filter(SheetMusic.id == new_sheet_music_id).first().title
    new_run_number = len(db.session.query(Performance).all()) + 1
    new_date_time = datetime.now()

    # construct new file path and handle file upload
    new_wav_file_path = "data/wav/" + new_sheet_music_id + "_" + selected_sheet_music_name + "_" + str(new_run_number) + ".wav"
    new_wav_file_data = request.files.get("file")
    new_wav_file_data.save(new_wav_file_path)

    # set new average tempo 
    new_average_tempo = 120 # TO-DO change constant!

    # analyze recording
    notes_from_rec = signal_processing(new_wav_file_path)

    # get json file paths
    wav_json_file_path = "filepath" # to-do change constant
    mxl_json_file_path = db.session.query(SheetMusic).filter(SheetMusic.id == new_sheet_music_id).first().data_file_path

    # open json file and load into obj
    with open(mxl_json_file_path, "r", encoding="utf8") as mxl_json_file:
        mxl_json = json.load(mxl_json_file)
    with open(wav_json_file_path, "r", encoding="utf8") as wav_json_file:
        wav_json = json.load(wav_json_file)

    # run comparison algorithms
    new_tempo_percent_accuracy = compare_tempo(mxl_json, wav_json)
    new_tuning_percent_accuracy = compare_tuning(mxl_json, wav_json)
    new_dynamics_percent_accuracy = compare_dynamics(mxl_json, wav_json)
    
    # send info to database
    new_performance = Performance(new_id, new_sheet_music_id, new_run_number, new_date_time, new_tempo_percent_accuracy, new_average_tempo, new_tuning_percent_accuracy, new_dynamics_percent_accuracy, new_wav_file_path, wav_json_file_path)
    db.session.add(new_performance)
    db.session.commit()
    return new_performance.serialize

# Delete performance from database
@app.delete("/performance/<int:id>")
def deletePerformance(id):
    performance = db.session.query(Performance).filter(Performance.id == id).first()
    if performance:

        # delete recording file
        path = performance.wav_file_path
        os.remove(path)

        # TO-DO delete data file

        # remove entry from database
        db.session.delete(performance)
        db.session.commit()

        return performance.serialize
    else:
        return {}