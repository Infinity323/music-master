import os

class Config(object):
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:password@localhost:5432/music_master"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DATA_DIRS = {
        "xml": "data/xml",
        "wav": "data/wav",
        "dat": "data/dat",
    }
