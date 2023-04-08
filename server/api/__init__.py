from api.sheetmusic import sheetmusic_blueprint
from api.goal import goal_blueprint
from api.performance import performance_blueprint

def register_blueprints(app):
    app.register_blueprint(sheetmusic_blueprint)
    app.register_blueprint(goal_blueprint)
    app.register_blueprint(performance_blueprint)
