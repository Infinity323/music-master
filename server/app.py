from flask import Flask
from flask_cors import CORS
import os

from models import db
import config

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(config.Config)
    
    db.init_app(app)
    from models.goal import model_goal_blueprint
    from models.performance import model_performance_blueprint
    from models.sheetmusic import model_sheetmusic_blueprint
    with app.app_context():
        db.create_all()

    from api.sheetmusic import sheetmusic_blueprint
    from api.performance import performance_blueprint
    from api.goal import goal_blueprint

    app.register_blueprint(model_goal_blueprint)
    app.register_blueprint(model_performance_blueprint)
    app.register_blueprint(model_sheetmusic_blueprint)
    app.register_blueprint(sheetmusic_blueprint)
    app.register_blueprint(performance_blueprint)
    app.register_blueprint(goal_blueprint)

    # Initialize data subdirectories
    os.makedirs("data/xml", exist_ok=True)
    os.makedirs("data/wav", exist_ok=True)
    os.makedirs("data/dat", exist_ok=True)

    return app

app = create_app()

if __name__ == "__main__":
    app.run()
