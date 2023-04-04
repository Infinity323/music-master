from flask import Flask

from models import db
import config

def create_app():
    app = Flask(__name__)
    app.config.from_object(config.Config)
    
    db.init_app(app)

    with app.app_context():
        db.create_all()

    from api.sheetmusic import sheetmusic_blueprint
    from api.performance import performance_blueprint
    from api.goal import goal_blueprint

    app.register_blueprint(sheetmusic_blueprint)
    app.register_blueprint(performance_blueprint)
    app.register_blueprint(goal_blueprint)

    return app

app = create_app()

if __name__ == "__main__":
    app.run()
