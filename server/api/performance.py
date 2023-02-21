from flask import request
from random import randint

from app import app, db
from models.performance import Performance

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
    new_run_number = data.get("run_number")
    new_date_time = data.get("date_time")
    new_tempo_percent_accuracy = data.get("tempo_percent_accuracy")
    new_average_tempo = data.get("average_tempo")
    new_tuning_percent_accuracy = data.get("tuning_percent_accuracy")
    new_dynamics_percent_accuracy = data.get("dynamics_percent_accuracy")
    new_performance = Performance(new_id, new_run_number, new_date_time, new_tempo_percent_accuracy, new_average_tempo, new_tuning_percent_accuracy, new_dynamics_percent_accuracy)
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