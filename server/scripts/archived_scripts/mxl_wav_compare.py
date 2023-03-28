from deepdiff import DeepDiff
from deepdiff import DeepSearch

# https://zepworks.com/deepdiff/6.2.3/index.html
def get_diff_raw(mxl_json, wav_json):
    diff_raw = DeepDiff(mxl_json, wav_json) 
    return diff_raw

 # dictionary with all feedback differences (keys and values)
def get_diff_list(mxl_json, wav_json):
    diff_list = get_diff_raw(mxl_json, wav_json).to_dict() 
    return diff_list

# attribute is str "pitch", "velocity", "start", or "end"
def get_diff_indexes(mxl_json, wav_json, attribute: str):
    # OrderedSet of paths that contain a diff
    diff_paths = get_diff_raw(mxl_json, wav_json).affected_paths 
    diff_indexes = DeepSearch(diff_paths, attribute, verbose_level=2) # index locations discrepencies
    return diff_indexes

def get_num_notes(json):
    return len(json["notes"])

def check_same_length(mxl_json, wav_json):
    mxl_note_len = get_num_notes(mxl_json)
    wav_note_len = get_num_notes(wav_json)

    if mxl_note_len == wav_note_len and mxl_note_len != 0:
        return True
    else:
        return False
    
# compares mxl and wav json file against eachother and returns diff
def compare_tuning(mxl_json, wav_json):
    diff_list = get_diff_list(mxl_json,  wav_json) # diff_list

    if check_same_length(mxl_json, wav_json):
        num_notes = get_num_notes(mxl_json)
        print("note length matches!")

        # NOTE: verbose_level = 2 indicates {index of DeepSearch object : original json key name} are stored for each diff
        # use original json key name to access value specifics from diff_list

        # get number of pitch discrepencies
        pitch_diffs = get_diff_indexes(mxl_json, wav_json, "pitch") # index locations of pitch discrepencies
        if "matched_values" in pitch_diffs:
            num_pitch_diffs = len(pitch_diffs['matched_values']) # number of pitch discrepencies
            for index in pitch_diffs['matched_values']: # iterate through discrepencies and print each
                diff_list_index = pitch_diffs['matched_values'][index]
                print("Pitch Diff: ", diff_list['values_changed'][diff_list_index], " at note: ", diff_list_index) # get specific diff and print it
                # 'new value' indicates wav value
                # 'old value' indicates mxl value
        new_tuning_percent_accuracy = (num_notes - num_pitch_diffs) / num_notes # percent correct <--- DB ENTRY
    
    print("tuning: ", new_tuning_percent_accuracy)
    return new_tuning_percent_accuracy

def compare_dynamics(mxl_json, wav_json):
    diff_list = get_diff_list(mxl_json,  wav_json) # diff_list

    if check_same_length(mxl_json, wav_json):
        num_notes = get_num_notes(mxl_json)
        print("note length matches!")

        # get number of dynamics discrepencies
        dynamics_diffs = get_diff_indexes(mxl_json, wav_json, "velocity") # index locations of dynamics discrepencies
        if "matched_values" in dynamics_diffs: # check if any discrepencies were found
            num_dynamics_diffs = len(dynamics_diffs['matched_values']) # number of dynamics discrepencies
            for index in dynamics_diffs['matched_values']: # iterate through discrepencies and print each
                diff_list_index = dynamics_diffs['matched_values'][index]
                print("Dynamics Diff: ", diff_list['values_changed'][diff_list_index], " at note: ", diff_list_index) # get specific diff and print it
        new_dynamics_percent_accuracy = (num_notes - num_dynamics_diffs) / num_notes # percent correct <--- DB ENTRY

    print("dynamics: ", new_dynamics_percent_accuracy)
    return new_dynamics_percent_accuracy

def compare_tempo(mxl_json, wav_json):
    diff_list = get_diff_list(mxl_json,  wav_json) # diff_list

    if check_same_length(mxl_json, wav_json):
        num_notes = get_num_notes(mxl_json)
        print("note length matches!")

        # get number of tempo discrepencies
        tempo_start_diffs = get_diff_indexes(mxl_json, wav_json, "start")
        tempo_end_diffs = get_diff_indexes(mxl_json, wav_json, "end")
        num_tempo_diffs = 0
        if "matched_values" in tempo_start_diffs:
            num_tempo_diffs += len(tempo_start_diffs['matched_values'])
            for index in tempo_start_diffs['matched_values']: # iterate through discrepency and print each
                diff_list_index = tempo_start_diffs['matched_values'][index]
                print("Tempo Start Diff: ", diff_list['values_changed'][diff_list_index], " at note: ", diff_list_index) # get specific diff and print it
        if "matched_values" in tempo_start_diffs:
            num_tempo_diffs += len(tempo_end_diffs['matched_values'])
            for index in tempo_end_diffs['matched_values']: # iterate through discrepency and print each
                diff_list_index = tempo_end_diffs['matched_values'][index]
                print("Tempo End Diff: ", diff_list['values_changed'][diff_list_index], " at note: ", diff_list_index) # get specific diff and print it
        new_tempo_percent_accuracy = ((num_notes * 2) - num_tempo_diffs) / (num_notes * 2) # (*2 becuase there are 2 per note) percent correct <--- DB ENTRY

    print("tempo: ", new_tempo_percent_accuracy)
    return new_tempo_percent_accuracy
    

