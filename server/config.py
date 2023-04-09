class Config(object):
    SQLALCHEMY_DATABASE_URI = "sqlite:///music_master.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

DATA_DIRS = [
    "data/xml",
    "data/wav",
    "data/dat",
]