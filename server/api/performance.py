from flask import request, jsonify

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
    new_id = 1
    new_run_number = request.form.get("run_number")
    new_date_time = request.form.get("date_time")
    new_tempo_percent_accuracy = request.form.get("tempo_percent_accuracy")
    new_average_tempo = request.form.get("average_tempo")
    new_tuning_percent_accuracy = request.form.get("tuning_percent_accuracy")
    new_dynamics_percent_accuracy = request.form.get("dynamics_percent_accuracy")
    new_performance = Performance(new_id, new_run_number, new_date_time, new_tempo_percent_accuracy, new_average_tempo, new_tuning_percent_accuracy, new_dynamics_percent_accuracy)
    db.session.add(new_performance)
    db.session.commit()
    return new_performance.serialize

# Delete performance from database
@app.delete("/performance/<int:id>")
def deletePerformance(id):
    performance = db.session.query(Performance).filter(Performance.id == id).first()
    db.session.delete(performance)
    db.session.commit()
    return performance.serialize