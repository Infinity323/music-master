import os
import platform

user_home = os.path.expanduser("~")

class Config(object):
    if platform.system() == "Linux":
        database_path = os.path.join(user_home, "music-master/music_master.db")
    else:
        database_path = "music_master.db"

    SQLALCHEMY_DATABASE_URI = f"sqlite:///{database_path}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

if platform.system() == "Linux":
    # linux requires that files be stored in writable file system
    JSON_DIR = os.path.join(user_home, "music-master/data/json")
    WAV_DIR = os.path.join(user_home, "music-master/data/wav")
    XML_DIR = os.path.join(user_home, "music-master/data/xml")
    TMP_DIR = os.path.join(user_home, "music-master/data/tmp")
else: 
    JSON_DIR = "data/json"
    WAV_DIR = "data/wav"
    XML_DIR = "data/xml"
    TMP_DIR = "data/tmp"

# the following constants are used for the comparison algorithm (xml vs wav)

# pass confidence values are percentages
# these values are only used for determining if a diff should be filed
# if equality confidence is under these percentages then it is considered a mismatch
# pitch: 70% confidence happens: tolerance of 50 cents and pitch difference of no more than 15 cents
# velocity: 60% confidence happens: tolerance of 30 and velocity difference of no more than 18 MIDI velocity units
# start: 70% confidence happens: tolerance of 0.25 seconds and start difference of no more than 0.075 seconds
# end: 60% confidence happens: tolerance of 0.5 seconds and end difference of no more than 0.2 seconds
PITCH_PASS_CONF = 0.7
VELOCITY_PASS_CONF = 0.6
START_PASS_CONF = 0.7
END_PASS_CONF = 0.6

# percent confidence for a note object to be considered equal
NOTE_MATCH_PASS_CONF = 0.7

# weight values are the amount of weight each attribute has at determining if note objects are equal
PITCH_WEIGHT = 0.7
VELOCITY_WEIGHT = 0.05
END_WEIGHT = 0.05
START_WEIGHT = 0.2

# tolerance values upper/lower bounds where 0% confidence occurs
PITCH_TOLERANCE = 50 # cents
VELOCITY_TOLERANCE = 30 # MIDI velocity units
START_TOLERANCE = 0.25 # seconds
END_TOLERANCE = 0.5 # seconds

# duration at which an extra note will recieve the maximum pitch accuracy penalty
EXTRA_NOTE_MAX_PENALTY_DURATION = 0.125

# maximum percentage that will be deducted from pitch accuracy when extra note is detected
EXTRA_NOTE_MAX_PENALTY = 0.025

DATA_DIRS = [
    JSON_DIR,
    WAV_DIR,
    XML_DIR,
    TMP_DIR,
]