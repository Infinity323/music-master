from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:password@localhost:5432/music_master"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize tables in database
db = SQLAlchemy(app)
import models.sheetmusic as _
import models.goal as _
import models.performance as _
with app.app_context():
    db.create_all()

# Import endpoints from api subdirectory
import api.sheetmusic as _