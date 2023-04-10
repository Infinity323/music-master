class Config(object):
    SQLALCHEMY_DATABASE_URI = "sqlite:///music_master.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

JSON_DIR = "data/json/"
WAV_DIR = "data/wav/"
XML_DIR = "data/xml/"
TMP_DIR = "data/tmp/"

DATA_DIRS = [
    JSON_DIR,
    WAV_DIR,
    XML_DIR,
    TMP_DIR,
]