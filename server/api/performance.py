from flask import request, Blueprint
from random import randint
import json
import os
from datetime import datetime

from models import db
from models.performance import Performance
from models.sheetmusic import SheetMusic

from scripts.signal_processing import signal_processing
from scripts.compare import compare_arrays, shift_start_time_to_zero
from scripts.objects import Difference, Difference_with_info, Note

performance_blueprint = Blueprint("performance", __name__)

# PERFORMANCE

# Get all performance in database
@performance_blueprint.route("/performance", methods=["GET"])
def getAllPerformances():
    performances = db.session.query(Performance)
    return [ i.serialize for i in performances ]

# Get performance with specific ID from database
@performance_blueprint.route("/performance/<int:id>", methods=["GET"])
def getSpecificPerformance(id: int):
    performance = db.session.query(Performance).filter(Performance.id == id).first()
    return performance.serialize

# Add performance to database
@performance_blueprint.route("/performance", methods=["POST"])
def addPerformance():

    new_id = randint(1, 1000000)

    new_sheet_music_id = request.form.get("sheet_music_id")
    selected_sheet_music_name = db.session.query(SheetMusic).filter(SheetMusic.id == new_sheet_music_id).first().title
    new_run_number = len(db.session.query(Performance).all()) + 1
    new_date_time = datetime.now()

    # construct new file path and handle file upload
    new_wav_file_path = "data/wav/" + new_sheet_music_id + "_" + selected_sheet_music_name + "_" + str(new_run_number) + ".wav"
    new_wav_file_data = request.files.get("file")
    new_wav_file_data.save(new_wav_file_path)
    # new_wav_file_path = "data/wav/Happy_Birthday_Piano_Perfect.wav" # test perfect wav

    # set new average tempo 
    new_average_tempo = int(request.form.get("average_tempo"))

    # analyze recording
    notes_from_rec = signal_processing(new_wav_file_path, new_average_tempo)
    rec_json_path = "data/dat/" + new_sheet_music_id + "_" + selected_sheet_music_name + "_" + str(new_run_number) + "_rec.json"
    
    # save notes info into a json file
    with open(rec_json_path, 'w') as rec_json_file:
        rec_json_file.write(notes_from_rec)

    # get json file paths
    wav_json_file_path = rec_json_path # use "scripts/test_dat/wav.json" for testing
    xml_json_file_path = db.session.query(SheetMusic).filter(SheetMusic.id == new_sheet_music_id).first().data_file_path # use "scripts/test_dat/xml.json" for testing

    # open json file and load into obj
    with open(xml_json_file_path) as xml_json_file:
        xml_data = json.load(xml_json_file)
    with open(wav_json_file_path) as wav_json_file:
        wav_data = json.load(wav_json_file)

    ideal_notes = [Note(note["pitch"], note["velocity"], note["start"], note["end"]) for note in xml_data["notes"]]
    raw_actual_notes = [Note(note["pitch"], note["velocity"], note["start"], note["end"]) for note in wav_data["notes"]]

    # strip out "Rest" notes in the actual array
    filtered_actual_notes = [note for note in raw_actual_notes if note.pitch != "Rest"]

    # shift back the start time of the actual array
    shift_start_time_to_zero(filtered_actual_notes)

    # run comparison algorithms
    new_tuning_percent_accuracy, new_dynamics_percent_accuracy, new_tempo_percent_accuracy, differences = compare_arrays(ideal_notes, filtered_actual_notes)

    # append info to differences
    note_info_file_path = db.session.query(SheetMusic).filter(SheetMusic.id == new_sheet_music_id).first().note_info_file_path
    with open(note_info_file_path) as file:
        note_info_data = json.load(file)

    differences_with_info  = []
    prev_ideal_index = 0
    for diff in differences:
        # (pitch, velocity, start, or end)
        if diff.diff_type in ["pitch", "velocity", "start", "end"]:
            differences_with_info.append(Difference_with_info(diff, note_info_data[diff.ideal_idx]))
            prev_ideal_index = diff.ideal_idx

        # (extra or missing)
        if diff.diff_type == "missing":
            differences_with_info.append(Difference_with_info(diff, note_info_data[diff.ideal_idx], "note_info contains the missing note"))
            prev_ideal_index = diff.ideal_idx

        if diff.diff_type == "extra":
            differences_with_info.append(Difference_with_info(diff, [note_info_data[prev_ideal_index]], "note_info contains the last known ideal note that was played correctly"))

    # save the diff file locally
    diff_json_path = "data/dat/" + new_sheet_music_id + "_" + selected_sheet_music_name + "_" + str(new_run_number) + "_diff.json"
    with open(diff_json_path, 'w') as diff_json_file:
        json.dump([info.to_dict() for info in differences_with_info], diff_json_file, indent=4, default=Note.custom_serializer)
    
    # send info to database
    new_performance = Performance(new_id, new_sheet_music_id, new_run_number, new_date_time, new_tempo_percent_accuracy, new_average_tempo, new_tuning_percent_accuracy, new_dynamics_percent_accuracy, new_wav_file_path, wav_json_file_path, diff_json_path)
    db.session.add(new_performance)
    db.session.commit()
    return new_performance.serialize

# Delete performance from database
@performance_blueprint.route("/performance/<int:id>", methods=["DELETE"])
def deletePerformance(id):
    performance = db.session.query(Performance).filter(Performance.id == id).first()
    if performance:

        # delete recording file
        path = performance.wav_file_path
        os.remove(path)

        # TO-DO delete data file

        # remove entry from database
        db.session.delete(performance)
        db.session.commit()

        return performance.serialize
    else:
        return {}