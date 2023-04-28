"""Performance API

API endpoints to access interact with the performance schema in the database.
"""
from flask import request, Blueprint
from random import randint
import json
import os
from datetime import datetime, timezone

from models import db
from models.performance import Performance
from models.sheetmusic import SheetMusic

from scripts.signal_processing import signal_processing
from scripts.compare import compare_arrays
from scripts.objects import Difference_with_info, Note
from config import JSON_DIR, WAV_DIR

performance_blueprint = Blueprint("performance", __name__)

@performance_blueprint.route("/performance", methods=["GET"])
def get_all_performances():
    """Get all performances from the database.

    Returns:
        list: A list with all the performances
    """
    performances = db.session.query(Performance)
    if performances:
        return [ i.serialize for i in performances ]
    else:
        return []

@performance_blueprint.route("/performance/<int:id>", methods=["GET"])
def get_specific_performance(id: int):
    """Get the performance with the matching ID from the database.

    Args:
        id (int): The ID of the performance

    Returns:
        dict: A dict of the performance
    """
    performance = db.session.query(Performance).filter(Performance.id == id).first()
    if performance:
        return performance.serialize
    else:
        return {}

@performance_blueprint.route("/performance/<int:performance_id>/notes", methods=["GET"])
def get_notes_jsons(performance_id: int):
    """Get notes played during a performance, as well as the ideal notes for
    the corresponding sheet music.

    Args:
        performance_id (int): The ID of the performance

    Returns:
        dict: A dict of the actual notes played and the expected notes
    """
    performance = (db.session.query(Performance)
                   .filter(Performance.id == performance_id)
                   .first())
    sheet_music_id = performance.sheet_music_id
    run_number = performance.run_number

    sheet_music_name = (db.session.query(SheetMusic)
                        .filter(SheetMusic.id == sheet_music_id)
                        .first().title)
    runs_subdir = f"{JSON_DIR}/{sheet_music_id}_{sheet_music_name}/runs"
    rec_json_path = f"{runs_subdir}/{run_number}_rec.json"
    master_json_path = f"{JSON_DIR}/{sheet_music_id}_{sheet_music_name}/master.json"
    try:
        with open(rec_json_path, 'r') as rec_json_file:
            rec_data = json.load(rec_json_file)
        with open(master_json_path, 'r') as master_json_file:
            master_data = json.load(master_json_file)
        return {
            "actual": rec_data,
            "expected": master_data
        }
    except FileNotFoundError:
        return {"error": "File not found"}, 404

@performance_blueprint.route("/performance/diff/<int:sheet_music_id>/<int:run_number>", methods=["GET"])
def get_diff_json(sheet_music_id: int, run_number: int):
    """Get the diff file for a performance.

    Args:
        sheet_music_id (int): The ID of the sheet music
        run_number (int): The run number of the performance

    Returns:
        dict: A dict of the diff file's data
    """
    sheet_music_name = (db.session.query(SheetMusic)
                        .filter(SheetMusic.id == sheet_music_id)
                        .first().title)
    subdir = f"{JSON_DIR}/{sheet_music_id}_{sheet_music_name}/runs"
    diff_json_path = f"{subdir}/{run_number}_diff.json"
    try:
        with open(diff_json_path, 'r') as diff_json_file:
            data = json.load(diff_json_file)
        return data
    except FileNotFoundError:
        return {"error": "File not found"}, 404

@performance_blueprint.route("/performance", methods=["POST"])
def add_performance():
    """Add a performance to the database.

    Returns:
        dict: A dict of the new performance
    """

    new_id = randint(1, 1000000)

    sheet_music_id = request.form.get("sheet_music_id")
    sheet_music_name = (db.session.query(SheetMusic)
                                 .filter(SheetMusic.id == sheet_music_id)
                                 .first().title)
    new_run_number = len(db.session.query(Performance)
                         .filter(Performance.sheet_music_id == sheet_music_id).all()) + 1
    new_average_tempo = int(request.form.get("average_tempo"))
    new_date_time = datetime.now(timezone.utc)

    # construct new file path and handle file upload
    new_wav_file_path = f"{WAV_DIR}/{sheet_music_id}_{sheet_music_name}/{new_run_number}.wav"
    new_wav_file_data = request.files.get("file")
    new_wav_file_data.save(new_wav_file_path)

    # Make new subdirectory
    new_subdir = f"{JSON_DIR}/{sheet_music_id}_{sheet_music_name}/runs"
    os.makedirs(new_subdir, exist_ok=True)
    
    # analyze recording
    notes_from_rec = signal_processing(new_wav_file_path, new_average_tempo)
    rec_json_path = f"{new_subdir}/{new_run_number}_rec.json"
    
    # save notes info into a json file
    with open(rec_json_path, 'w') as rec_json_file:
        rec_json_file.write(notes_from_rec)

    # get json file paths
    wav_json_file_path = rec_json_path
    xml_json_file_path = (db.session.query(SheetMusic)
                          .filter(SheetMusic.id == sheet_music_id)
                          .first().data_file_path)

    # open json file and load into obj
    with open(xml_json_file_path) as xml_json_file:
        xml_data = json.load(xml_json_file)
    with open(wav_json_file_path) as wav_json_file:
        wav_data = json.load(wav_json_file)

    ideal_notes = [Note(note["pitch"], note["velocity"], note["start"], note["end"])
                   for note in xml_data["notes"]]
    actual_notes = [Note(note["pitch"], note["velocity"], note["start"], note["end"])
                        for note in wav_data["notes"]]

    # run comparison algorithms
    (new_tuning_percent_accuracy, new_dynamics_percent_accuracy,
     new_tempo_percent_accuracy, differences) = compare_arrays(ideal_notes, actual_notes)

    # append info to differences
    note_info_file_path = (db.session.query(SheetMusic)
                           .filter(SheetMusic.id == sheet_music_id)
                           .first().note_info_file_path)
    with open(note_info_file_path) as file:
        note_info_data = json.load(file)

    differences_with_info  = []
    prev_ideal_index = None
    next_ideal_index = None
    for i, diff in enumerate(differences):
        # (pitch, velocity, start, or end)
        if diff.diff_type in ["pitch", "velocity", "start", "end"]:
            differences_with_info.append(Difference_with_info(diff,
                                                              note_info_data[diff.ideal_idx]))
            prev_ideal_index = diff.ideal_idx

        # (missing)
        if diff.diff_type == "missing":
            differences_with_info.append(Difference_with_info(diff,
                                                              note_info_data[diff.ideal_idx],
                                                              "note_info contains the missing note"))
            prev_ideal_index = diff.ideal_idx

        # (extra)
        if diff.diff_type == "extra":
            # Find the next ideal index
            next_ideal_index = None
            for next_diff in differences[i+1:]:
                if next_diff.diff_type in ["pitch", "velocity", "start", "end", "missing"]:
                    next_ideal_index = next_diff.ideal_idx
                    break
            
            if prev_ideal_index is None and next_ideal_index is not None:
                differences_with_info.append(Difference_with_info(diff,
                                                                [note_info_data[next_ideal_index]],
                                                                "Before"))
            elif prev_ideal_index is not None and next_ideal_index is None:
                differences_with_info.append(Difference_with_info(diff,
                                                                [note_info_data[prev_ideal_index]],
                                                                "After"))
            elif prev_ideal_index is not None and next_ideal_index is not None:
                differences_with_info.append(Difference_with_info(diff,
                                                                [note_info_data[prev_ideal_index], note_info_data[next_ideal_index]],
                                                                "Between"))

    # save the diff file locally
    diff_json_path = f"{new_subdir}/{new_run_number}_diff.json"
    with open(diff_json_path, 'w') as diff_json_file:
        json.dump([info.to_dict() for info in differences_with_info],
                  diff_json_file, indent=4, default=Note.custom_serializer)
    
    # send info to database
    new_performance = Performance(new_id, sheet_music_id, new_run_number,
                                  new_date_time, new_tempo_percent_accuracy,
                                  new_average_tempo, new_tuning_percent_accuracy,
                                  new_dynamics_percent_accuracy, new_wav_file_path,
                                  wav_json_file_path, diff_json_path)
    db.session.add(new_performance)
    db.session.commit()
    
    return new_performance.serialize

@performance_blueprint.route("/performance/<int:id>", methods=["DELETE"])
def delete_performance(id: int):
    """Delete a performance with the matching ID from the database.

    Args:
        id (int): The ID of the performance

    Returns:
        dict: A dict of the deleted performance
    """
    
    performance = db.session.query(Performance).filter(Performance.id == id).first()
    if performance:
        # delete recording file
        path = performance.wav_file_path
        os.remove(path)      

        # remove entry from database
        db.session.delete(performance)
        db.session.commit()

        return performance.serialize
    else:
        return {}