from flask import request, jsonify

from app import app, db
from models.goal import Goal

# PERFORMANCE

# Get all goals in database
@app.get("/goal")
def getAllGoals():
    goals = db.session.query(Goal)
    return [ i.serialize for i in goals ]

# Get goal with specific ID from database
@app.get("/goal/<int:id>")
def getSpecificGoal(id: int):
    goal = db.session.query(Goal).filter(Goal.id == id).first()
    return goal.serialize

# Add goal to database
@app.post("/goal")
def addGoal():
    new_id = 1
    new_name = request.form.get("name")
    new_start_date = request.form.get("start_date")
    new_end_date = request.form.get("end_date")
    new_tempo_percent_accuracy = request.form.get("tempo_percent_acuracy")
    new_average_tempo = request.form.get("average_tempo")
    new_tuning_percent_accuracy = request.form.get("tuning_percent_accuracy")
    new_dynamics_percent_accuracy = request.form.get("dynamics_percent_accuracy")
    new_goal = Goal(new_id, new_name, new_start_date, new_end_date, new_tempo_percent_accuracy, new_average_tempo, new_tuning_percent_accuracy, new_dynamics_percent_accuracy)
    db.session.add(new_goal)
    db.session.commit()
    return new_goal.serialize

# Delete goal from database
@app.delete("/goal/<int:id>")
def deleteGoal(id):
    goal = db.session.query(Goal).filter(Goal.id == id).first()
    db.session.delete(goal)
    db.session.commit()
    return goal.serialize