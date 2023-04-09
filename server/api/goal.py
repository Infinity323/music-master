from flask import request, Blueprint
from datetime import date, datetime, timezone
from random import randint

from models import db
from models.goal import Goal

goal_blueprint = Blueprint("goal", __name__)

# PERFORMANCE

# Get all goals in database
@goal_blueprint.route("/goal", methods=["GET"])
def getAllGoals():
    goals = db.session.query(Goal)
    return [ i.serialize for i in goals ]

# Get goal with specific ID from database
@goal_blueprint.route("/goal/<int:id>", methods=["GET"])
def getSpecificGoal(id: int):
    goal = db.session.query(Goal).filter(Goal.id == id).first()
    return goal.serialize

# Add goal to database
@goal_blueprint.route("/goal", methods=["POST"])
def addGoal():
    data = request.get_json()
    new_id = randint(1, 1000000)
    new_sheet_music_id = data.get("sheet_music_id")
    new_name = data.get("name")
    new_start_date = datetime.now(timezone.utc)
    new_end_date = datetime.combine(date.fromisoformat(data.get("end_date")),
                                    datetime.min.time()).astimezone(timezone.utc)
    new_tempo_percent_accuracy = data.get("tempo_percent_accuracy")
    new_average_tempo = data.get("average_tempo")
    new_tuning_percent_accuracy = data.get("tuning_percent_accuracy")
    new_dynamics_percent_accuracy = data.get("dynamics_percent_accuracy")
    new_goal = Goal(new_id, new_sheet_music_id, new_name, new_start_date, new_end_date, new_tempo_percent_accuracy, new_average_tempo, new_tuning_percent_accuracy, new_dynamics_percent_accuracy)
    db.session.add(new_goal)
    db.session.commit()
    return new_goal.serialize

# Delete goal from database
@goal_blueprint.route("/goal/<int:id>", methods=["DELETE"])
def deleteGoal(id):
    goal = db.session.query(Goal).filter(Goal.id == id).first()
    if goal:
        db.session.delete(goal)
        db.session.commit()
        return goal.serialize
    else:
        return {}