import os
import platform

# Set instance path for Flask app
if platform.system() == "Linux":
    user_home = os.path.expanduser("~")
    instance_path = os.path.join(user_home, "music-master")
else:
    instance_path = os.path.join(os.getcwd(), "instance")

# Config class for Flask app
class Config(object):
    database_path = os.path.join(instance_path, "music_master.db")

    SQLALCHEMY_DATABASE_URI = f"sqlite:///{database_path}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

# Data directories
JSON_DIR = os.path.join(instance_path, "data/json")
WAV_DIR = os.path.join(instance_path, "data/wav")
XML_DIR = os.path.join(instance_path, "data/xml")
TMP_DIR = os.path.join(instance_path, "data/tmp")

DATA_DIRS = [
    JSON_DIR,
    WAV_DIR,
    XML_DIR,
    TMP_DIR,
]

# the following constants are used for the comparison algorithm (xml vs wav)

# pass confidence values are percentages
# these values are only used for determining if a diff should be filed
# if equality confidence is under these percentages then it is considered a mismatch
# pitch: 70% confidence happens: tolerance of 130 cents and pitch difference of no more than 39 cents
# velocity: 60% confidence happens: tolerance of 30 and velocity difference of no more than 18 MIDI velocity units
# start: 70% confidence happens: tolerance of 0.25 seconds and start difference of no more than 0.075 seconds
# end: 60% confidence happens: tolerance of 0.5 seconds and end difference of no more than 0.2 seconds

# using %1 as passing to negate these values since they are redundant calcuations
PITCH_PASS_CONF = 0.01
VELOCITY_PASS_CONF = 0.01
START_PASS_CONF = 0.01
END_PASS_CONF = 0.01

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
START_TOLERANCE = 0.1 # seconds
END_TOLERANCE = 0.2 # seconds

# duration at which an extra note will recieve the maximum pitch accuracy penalty
EXTRA_NOTE_MAX_PENALTY_DURATION = 0.125

# maximum percentage that will be deducted from pitch accuracy when extra note is detected
EXTRA_NOTE_MAX_PENALTY = 0.5
