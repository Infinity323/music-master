"""Goal API

API endpoints to access interact with the goal schema in the database.
"""
from flask import request, Blueprint
from datetime import date, datetime, timezone
from random import randint

from models import db
from models.goal import Goal

goal_blueprint = Blueprint("goal", __name__)

@goal_blueprint.route("/goal", methods=["GET"])
def get_all_goals():
    """Get all goals from the database.

    Returns:
        list: A list of all the goals
    """
    goals = db.session.query(Goal)
    if goals:
        return [ i.serialize for i in goals ]
    else:
        return []

@goal_blueprint.route("/goal/<int:id>", methods=["GET"])
def get_specific_goal(id: int):
    """Get the goal with the matching ID from the database.

    Args:
        id (int): The ID of the goal

    Returns:
        dict: A dict of the goal
    """
    goal = db.session.query(Goal).filter(Goal.id == id).first()
    if goal:
        return goal.serialize
    else:
        return {}

@goal_blueprint.route("/goal", methods=["POST"])
def add_goal():
    """Add a goal to the database.

    Returns:
        dict: A dict of the new goal
    """
    data = request.get_json()
    
    new_id = randint(1, 1000000)
    new_sheet_music_id = data.get("sheet_music_id")
    new_name = data.get("name")
    
    # Have to do some datetime conversions to UTC
    new_start_date = datetime.now(timezone.utc)
    new_end_date = datetime.combine(date.fromisoformat(data.get("end_date")),
                                    datetime.min.time()).astimezone(timezone.utc)
    
    new_tempo_percent_accuracy = data.get("tempo_percent_accuracy")
    new_average_tempo = data.get("average_tempo")
    new_tuning_percent_accuracy = data.get("tuning_percent_accuracy")
    new_dynamics_percent_accuracy = data.get("dynamics_percent_accuracy")
    
    new_goal = Goal(new_id, new_sheet_music_id, new_name, new_start_date,
                    new_end_date, new_tempo_percent_accuracy, new_average_tempo,
                    new_tuning_percent_accuracy, new_dynamics_percent_accuracy)
    db.session.add(new_goal)
    db.session.commit()
    
    return new_goal.serialize

@goal_blueprint.route("/goal/<int:id>", methods=["DELETE"])
def delete_goal(id: int):
    """Delete the goal with the matching ID from the database.

    Args:
        id (int): The ID of the goal

    Returns:
        dict: A dict of the deleted goal
    """
    goal = db.session.query(Goal).filter(Goal.id == id).first()
    if goal:
        db.session.delete(goal)
        db.session.commit()
        return goal.serialize
    else:
        return {}