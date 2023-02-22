from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:password@localhost:5432/music_master"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize tables in database
db = SQLAlchemy(app)
import models.sheetmusic as _
import models.performance as _
import models.goal as _
with app.app_context():
    db.create_all()

# Initialize data subdirectories
os.makedirs("data/xml", exist_ok=True)
os.makedirs("data/wav", exist_ok=True)
os.makedirs("data/dat", exist_ok=True)

# Import endpoints from api subdirectory
import api.sheetmusic as _
import api.performance as _
import api.goal as _