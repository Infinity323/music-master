import cherrypy
from flask import Flask
from flask_cors import CORS
import os

from models import db
import config
import logging

def create_app():
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger(__name__)
    logger.info("Starting app initialization...")

    os.makedirs(config.instance_path, exist_ok=True)

    app = Flask(__name__, instance_path=config.instance_path)
    CORS(app)
    app.config.from_object(config.Config)
    
    # Initialize database connection and autogenerate tables
    logger.info(f"Initializing db in {config.instance_path}")
    db.init_app(app)
    from models.goal import model_goal_blueprint
    from models.performance import model_performance_blueprint
    from models.sheetmusic import model_sheetmusic_blueprint
    with app.app_context():
        db.create_all()

    # Import endpoints
    from api.status import status_blueprint
    from api.sheetmusic import sheetmusic_blueprint    
    from api.performance import performance_blueprint
    from api.goal import goal_blueprint

    app.register_blueprint(model_goal_blueprint)
    app.register_blueprint(model_performance_blueprint)
    app.register_blueprint(model_sheetmusic_blueprint)
    app.register_blueprint(status_blueprint)
    app.register_blueprint(sheetmusic_blueprint)
    app.register_blueprint(performance_blueprint)
    app.register_blueprint(goal_blueprint)

    # Initialize data subdirectories
    for dir in config.DATA_DIRS:
        os.makedirs(dir, exist_ok=True)

    logger.info('App initialization complete.')

    return app

app = create_app()

if __name__ == "__main__":
    # app.run() # (flask debugging mode)

    # Reason for choosing cherrypy
    # https://blog.appdynamics.com/engineering/a-performance-analysis-of-python-wsgi-servers-part-2/
    #
    # Flask application based on Quickstart
    # http://flask.pocoo.org/docs/0.12/quickstart/
    #
    # CherryPy documentation for this
    # http://docs.cherrypy.org/en/latest/deploy.html#wsgi-servers
    # http://docs.cherrypy.org/en/latest/advanced.html#host-a-foreign-wsgi-application-in-cherrypy
    # Install: pip install cherrypy

    # WSGI Settings
    cherrypy.tree.graft(app.wsgi_app, '/')
    cherrypy.config.update({'server.socket_host': '127.0.0.1',
                            'server.socket_port': 5000,
                            'engine.autoreload.on': False,
                            })
    
    try:
        cherrypy.engine.start()
        cherrypy.engine.block()  # Add this line to block the main thread
    except (KeyboardInterrupt, SystemExit, BaseException):
        cherrypy.engine.stop()  # Stop the server before exiting
        cherrypy.engine.exit()
        print("Shutting down server...")