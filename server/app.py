from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:password@localhost:5432/musicmaster"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize tables in database
db = SQLAlchemy(app)
import models.sheetmusic
with app.app_context():
    db.create_all()

@app.get("/")
def home():
    return "Hello World!"

# Import endpoints in api subdirectory
import api.sheetmusic