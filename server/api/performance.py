from flask import request
from random import randint

from deepdiff import DeepDiff
import json

from app import app, db
from models.performance import Performance
from models.sheetmusic import SheetMusic

from signal_processing import signal_processing

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

    # analyze recording
    notes_from_rec = signal_processing(new_wav_file_path)

    # TO-DO: ADD ANALYSIS ALGORITHM HERE

    # set attributes
    
    new_data_file_path = "filepath" # to-do change constant
    new_tempo_percent_accuracy = 0.5 # to-do change constant
    new_average_tempo = 120 # to-do change constant
    new_tuning_percent_accuracy = 0.5 # to-do change constant
    new_dynamics_percent_accuracy = 0.5 # to-do change constant

    # get the json file path for music sheet
    music_sheet_data_file_path = db.session.query(SheetMusic).filter(SheetMusic.id == new_sheet_music_id).first().data_file_path

    # run comparison
    mxl_file = open(new_data_file_path)
    wav_file = open(music_sheet_data_file_path)

    mxl_json = json.load(mxl_file)
    wav_json = json.load(wav_file)

    result = DeepDiff(mxl_json, wav_json)

    mxl_file.close()
    wav_file.close()

    result_object = json.dumps(result, indent=4)
    
    # Writing to sample.json
    with open("../data/dat/feedback.json", "w") as outfile:
        outfile.write(result_object)
    
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