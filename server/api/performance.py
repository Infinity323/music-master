from flask import request
from random import randint

from app import app, db
from models.performance import Performance

from .record import record

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
    data = request.get_json()
    new_id = randint(1, 1000000)

    # get from request
    new_sheet_music_id = data.get("sheet_music_id")
    new_run_number = data.get("run_number")
    new_date_time = data.get("date_time")

    # start and store recording

    # analyze recording

    # send info to database
    new_tempo_percent_accuracy = 50
    new_average_tempo = 120
    new_tuning_percent_accuracy = 50
    new_dynamics_percent_accuracy = 50
    new_wav_file_path = "test"
    new_data_file_path = "test"
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