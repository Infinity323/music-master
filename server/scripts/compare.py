import numpy as np
import json
from .objects import Difference, Note

import pandas as pd # Debugging

MATCH_SCORE = 2
MISMATCH_PENALTY = -4
GAP_PENALTY = -3
INSERT_PENALTY = -4

# This script compares two arrays of Note objects, representing ideal and actual
# musical performances, and calculates the accuracy and differences between them.

# DEBUGGING FUNCTION

def save_score_matrix_to_csv(score_matrix, ideal_notes, actual_notes, output_file):
    score_matrix_list = []

    for i in range(score_matrix.shape[0]):
        row = []
        for j in range(score_matrix.shape[1]):
            row.append(int(score_matrix[i, j]))
        score_matrix_list.append(row)

    columns = [''] + [str(note) for note in actual_notes]
    index = [''] + [str(note) for note in ideal_notes]
    df = pd.DataFrame(score_matrix_list, columns=columns, index=index)

    df.to_csv(output_file, sep=',')

# DEBUGGING FUNCTION
def save_aligned_arrays_to_json(aligned_ideal, aligned_actual, output_file):
    aligned_data = []

    for ideal_note, actual_note in zip(aligned_ideal, aligned_actual):
        aligned_data.append({
            "ideal": ideal_note.to_dict() if ideal_note else None,
            "actual": actual_note.to_dict() if actual_note else None
        })

    with open(output_file, 'w') as f:
        json.dump(aligned_data, f, default=Note.custom_serializer, indent=4)
    
# this will ensure that the start time for the actual array happens at 0.0
def shift_start_time_to_zero(notes_array):
    if not notes_array:
        return

    first_note_start_time = notes_array[0].start

    for note in notes_array:
        note.start -= first_note_start_time
        note.end -= first_note_start_time

# Implement the Needleman-Wunsch algorithm to find the optimal alignment of two arrays of musical notes.
def needleman_wunsch(seq1, seq2, insert_penalty=INSERT_PENALTY, gap_penalty=GAP_PENALTY, mismatch_penalty=MISMATCH_PENALTY, match_score=MATCH_SCORE):
    len1, len2 = len(seq1), len(seq2)
    # Create a score matrix of size (len1 + 1) x (len2 + 1) initialized with zeros.
    score_matrix = np.zeros((len1 + 1, len2 + 1), dtype=int)

    # Fill the first row and column of the score matrix with gap penalty values.
    for i in range(len1 + 1):
        score_matrix[i, 0] = gap_penalty * i
    for j in range(len2 + 1):
        score_matrix[0, j] = gap_penalty * j

    # Fill in the rest of the score matrix using the Needleman-Wunsch algorithm.
    for i in range(1, len1 + 1):
        for j in range(1, len2 + 1):
            # Calculate the score for a match or a mismatch.
            match = score_matrix[i - 1, j - 1] + (match_score if seq1[i - 1] == seq2[j - 1] else mismatch_penalty)
            # Calculate the score for a gap in seq2.
            delete = score_matrix[i - 1, j] + gap_penalty
            # Calculate the score for a gap in seq1.
            insert = score_matrix[i, j - 1] + insert_penalty
            # Choose the maximum score and store it in the score matrix.
            score_matrix[i, j] = max(match, delete, insert)

    # Return the final score matrix.
    return score_matrix

# Compare two arrays of musical notes and calculate the accuracy and differences between them.
def compare_arrays(ideal_array, actual_array):
    
    # If either array is empty, return None for all metrics.
    if not ideal_array or not actual_array:
        return None, None, None, [Difference(None, None, None, None, "error")]

    # Use the Needleman-Wunsch algorithm to find the optimal alignment of the two arrays
    score_matrix = needleman_wunsch(ideal_array, actual_array)
    save_score_matrix_to_csv(score_matrix, ideal_array, actual_array, 'scripts/temp_dat/score_matrix.csv') # DEBUGGING
    ideal_len, actual_len = len(ideal_array), len(actual_array)

    # Traceback through the score matrix to determine the optimal alignment
    i, j = ideal_len, actual_len
    aligned_ideal = []
    aligned_actual = []

    while i > 0 or j > 0:
        match = score_matrix[i - 1, j - 1] + (MATCH_SCORE if ideal_array[i - 1] == actual_array[j - 1] else MISMATCH_PENALTY) if i > 0 and j > 0 else float('-inf')
        delete = score_matrix[i - 1, j] + (GAP_PENALTY) if i > 0 else float('-inf')
        insert = score_matrix[i, j - 1] + (INSERT_PENALTY) if j > 0 else float('-inf')

        if match >= delete and match >= insert:
            aligned_ideal.append(ideal_array[i - 1])
            aligned_actual.append(actual_array[j - 1])
            i -= 1
            j -= 1
        elif delete >= insert:
            aligned_ideal.append(ideal_array[i - 1])
            aligned_actual.append(None)
            i -= 1
        else:
            aligned_ideal.append(None)
            aligned_actual.append(actual_array[j - 1])
            j -= 1

    # Reverse the aligned arrays to get the correct order.
    aligned_ideal.reverse()
    aligned_actual.reverse()

    # export aligned arrays (used for DEBUGGING)
    save_aligned_arrays_to_json(aligned_ideal, aligned_actual, 'scripts/temp_dat/aligned_arrays.json')

    # Calculate the accuracy values
    matches_notes = matches_dynamics = matches_start_stop = 0
    differences = []
    extra_note_count = 0
    
    ideal_index = 0
    actual_index = 0

    for i, (ideal_note, actual_note) in enumerate(zip(aligned_ideal, aligned_actual)):
        if ideal_note is not None and actual_note is not None:
            if abs(Note.frequency_difference_in_cents(ideal_note.pitch, actual_note.pitch)) <= 50: # bound 50 cents
                matches_notes += 1
            if Note.is_velocity_equal(actual_note.velocity, ideal_note.velocity): # within 30%
                matches_dynamics += 1
            if (abs(ideal_note.start - actual_note.start) <= 0.25 and abs(ideal_note.end - actual_note.end) <= 0.25): # bound 0.25 sec
                matches_start_stop += 1
            if abs(Note.frequency_difference_in_cents(ideal_note.pitch, actual_note.pitch)) > 50: # bound 50 cents
                differences.append(Difference(ideal_index, ideal_note, actual_index, actual_note, 'pitch'))
            if not Note.is_velocity_equal(actual_note.velocity, ideal_note.velocity): # within 30%
                differences.append(Difference(ideal_index, ideal_note, actual_index, actual_note, 'velocity'))
            if (abs(ideal_note.start - actual_note.start) > 0.25): # bound 0.25 sec
                differences.append(Difference(ideal_index, ideal_note, actual_index, actual_note, 'start'))
            if (abs(ideal_note.end - actual_note.end) > 0.25): # bound 0.25 sec
                differences.append(Difference(ideal_index, ideal_note, actual_index, actual_note, 'end'))
            ideal_index = ideal_index + 1
            actual_index = actual_index + 1
        elif ideal_note is None and actual_note is not None: # extra note
            differences.append(Difference(None, None, actual_index, actual_note, 'extra'))
            extra_note_count = extra_note_count + 1
            actual_index = actual_index + 1
        elif ideal_note is not None and actual_note is None: # missing note
            differences.append(Difference(ideal_index, ideal_note, None, None, 'missing'))
            actual_index = actual_index + 1

    ideal_len_aligned = sum(note is not None for note in aligned_ideal)
    accuracy_notes = round((matches_notes / ideal_len_aligned) * 100, 2)
    accuracy_dynamics = round((matches_dynamics / ideal_len_aligned) * 100, 2)
    accuracy_start_stop = round((matches_start_stop / ideal_len_aligned) * 100, 2)

    # Deduct 5% for every extra note that is detected
    accuracy_notes = round(((matches_notes / ideal_len_aligned) * 100) - (extra_note_count * 5), 2)

    return accuracy_notes, accuracy_dynamics, accuracy_start_stop, differences

# def run_test_case(ideal_array, actual_array, expected_accuracies, expected_differences, test_case_name):
#     print(f"Test case: {test_case_name}")
#     accuracy_notes, accuracy_dynamics, accuracy_start_stop, differences = compare_arrays(ideal_array, actual_array)
    
#     accuracies = {
#         'notes': accuracy_notes,
#         'dynamics': accuracy_dynamics,
#         'start_stop': accuracy_start_stop,
#     }
    
#     failed = False
    
#     for key in accuracies:
#         if accuracies[key] != expected_accuracies[key]:
#             print(f"  - {key.capitalize()} accuracy: Expected {expected_accuracies[key]:.1f}%, got {accuracies[key]:.1f}%")
#             failed = True
    
#     if len(differences) != len(expected_differences):
#         print(f"  - Differences: Expected {len(expected_differences)}, got {len(differences)}")
#         failed = True
#     else:
#         for i, (actual_diff, expected_diff) in enumerate(zip(differences, expected_differences)):
#             if actual_diff != expected_diff:
#                 print(f"  - Difference {i}: Expected {expected_diff}, got {actual_diff}")
#                 failed = True
    
#     if not failed:
#         print("Passed")
#     else:
#         print("Failed")

# # Test Case 1: Exact Match
# ideal_array = [Note(261.63, 100, 0, 1), Note(293.66, 80, 1, 2), Note(329.63, 60, 2, 3), Note(349.23, 40, 3, 4)]
# actual_array = [Note(261.63, 100, 0, 1), Note(293.66, 80, 1, 2), Note(329.63, 60, 2, 3), Note(349.23, 40, 3, 4)]
# expected_accuracies = {'notes': 100.0, 'dynamics': 100.0, 'start_stop': 100.0}
# expected_differences = []
# run_test_case(ideal_array, actual_array, expected_accuracies, expected_differences, "Exact Match")

# # Test Case 2: Different Note
# ideal_array = [Note(261.63, 100, 0, 1), Note(293.66, 80, 1, 2), Note(329.63, 60, 2, 3), Note(349.23, 40, 3, 4)]
# actual_array = [Note(261.63, 100, 0, 1), Note(440.00, 80, 1, 2), Note(329.63, 60, 2, 3), Note(349.23, 40, 3, 4)]
# expected_accuracies = {'notes': 75.0, 'dynamics': 100.0, 'start_stop': 100.0}
# expected_differences = [
#     Difference(1, ideal_array[1], 1, actual_array[1], 'pitch')
# ]
# run_test_case(ideal_array, actual_array, expected_accuracies, expected_differences, "Different Note")

# # Test Case 3: Different Dynamics
# ideal_array = [Note(261.63, 100, 0, 1), Note(293.66, 80, 1, 2), Note(329.63, 60, 2, 3), Note(349.23, 40, 3, 4)]
# actual_array = [Note(261.63, 100, 0, 1), Note(293.66, 49, 1, 2), Note(329.63, 60, 2, 3), Note(349.23, 40, 3, 4)]
# expected_accuracies = {'notes': 100.0, 'dynamics': 75.0, 'start_stop': 100.0}
# expected_differences = [
#     Difference(1, ideal_array[1], 1, actual_array[1], 'velocity')
# ]
# run_test_case(ideal_array, actual_array, expected_accuracies, expected_differences, "Different Dynamics")

# # Test Case 4: Different Start Time
# ideal_array = [Note(261.63, 100, 0, 1), Note(293.66, 80, 1, 2), Note(329.63, 60, 2, 3), Note(349.23, 40, 3, 4)]
# actual_array = [Note(261.63, 100, 0, 1), Note(293.66, 80, 1.5, 2), Note(329.63, 60, 2, 3), Note(349.23, 40, 3, 4)]
# expected_accuracies = {'notes': 100.0, 'dynamics': 100.0, 'start_stop': 75.0}
# expected_differences = [
#     Difference(1, ideal_array[1], 1, actual_array[1], 'start')
# ]
# run_test_case(ideal_array, actual_array, expected_accuracies, expected_differences, "Different Start Time")

# # Test Case 5: Different End Time
# ideal_array = [Note(261.63, 100, 0, 1), Note(293.66, 80, 1, 2), Note(329.63, 60, 2, 3), Note(349.23, 40, 3, 4)]
# actual_array = [Note(261.63, 100, 0, 1), Note(293.66, 80, 1, 2.5), Note(329.63, 60, 2, 3), Note(349.23, 40, 3, 4)]
# expected_accuracies = {'notes': 100.0, 'dynamics': 100.0, 'start_stop': 75.0}
# expected_differences = [
#     Difference(1, ideal_array[1], 1, actual_array[1], 'end')
# ]
# run_test_case(ideal_array, actual_array, expected_accuracies, expected_differences, "Different End Time")

# # Test Case 6: Different Start and End Time
# ideal_array = [Note(261.63, 100, 0, 1), Note(293.66, 80, 1, 2), Note(329.63, 60, 2, 3), Note(349.23, 40, 3, 4)]
# actual_array = [Note(261.63, 100, 0, 1), Note(293.66, 80, 1.5, 2.5), Note(329.63, 60, 2, 3), Note(349.23, 40, 3, 4)]
# expected_accuracies = {'notes': 100.0, 'dynamics': 100.0, 'start_stop': 75.0}
# expected_differences = [
#     Difference(1, ideal_array[1], 1, actual_array[1], 'start'),
#     Difference(1, ideal_array[1], 1, actual_array[1], 'end')
# ]
# run_test_case(ideal_array, actual_array, expected_accuracies, expected_differences, "Different Start and End Time")

# # Test Case 7: Extra Note
# # The actual array has an extra note 440.00 that should be detected as an extra note.
# ideal_array = [Note(261.63, 100, 0, 1), Note(293.66, 80, 1, 2), Note(329.63, 60, 2, 3), Note(349.23, 40, 3, 4)]
# actual_array = [Note(261.63, 100, 0, 1), Note(293.66, 80, 1, 1.5), Note(440.00, 40, 1.5, 2), Note(329.63, 60, 2, 3), Note(349.23, 40, 3, 4)]
# expected_accuracies = {'notes': 95.0, 'dynamics': 100.0, 'start_stop': 75.0}
# expected_differences = [
#     Difference(1, ideal_array[1], 1, actual_array[1], 'end'),
#     Difference(None, None, 2, actual_array[2], 'extra')
# ]
# run_test_case(ideal_array, actual_array, expected_accuracies, expected_differences, "Extra Note")

# # Test Case 8: Missing Note
# # The actual array is missing the note 293.66, which should be detected as a missing note.
# ideal_array = [Note(261.63, 100, 0, 1), Note(293.66, 80, 1, 2), Note(329.63, 60, 2, 3), Note(349.23, 40, 3, 4)]
# actual_array = [Note(261.63, 100, 0, 1), Note(329.63, 60, 2, 3), Note(349.23, 40, 3, 4)]
# expected_accuracies = {'notes': 75.0, 'dynamics': 75.0, 'start_stop': 75.0}
# expected_differences = [
#     Difference(1, ideal_array[1], None, None, 'missing')
# ]
# run_test_case(ideal_array, actual_array, expected_accuracies, expected_differences, "Missing Note")

# # Test Case 9: Extra Note and Missing Note
# ideal_array = [Note(261.63, 100, 0, 1), Note(293.66, 80, 1, 2), Note(329.63, 60, 2, 3), Note(349.23, 40, 3, 4)]
# actual_array = [Note(261.63, 100, 0, 1), Note(293.66, 80, 1, 1.5), Note(440.00, 40, 1.5, 2), Note(329.63, 60, 2, 3)]
# expected_accuracies = {'notes': 70.0, 'dynamics': 75.0, 'start_stop': 50.0}
# expected_differences = [
#     Difference(1, ideal_array[1], 1, actual_array[1], 'end'),
#     Difference(None, None, 2, actual_array[2], 'extra'),
#     Difference(3, ideal_array[3], None, None, 'missing')
# ]
# run_test_case(ideal_array, actual_array, expected_accuracies, expected_differences, "Extra Note and Missing Note")

# # Test Case 10: One of the notes is 20 cents sharp
# ideal_array = [Note(261.63, 100, 0, 1), Note(293.66, 80, 1, 2), Note(329.63, 60, 2, 3), Note(349.23, 40, 3, 4)]
# actual_array = [Note(265.02, 100, 0, 1), Note(293.66, 80, 1, 2), Note(329.63, 60, 2, 3), Note(349.23, 40, 3, 4)]
# expected_accuracies = {'notes': 75.0, 'dynamics': 100.0, 'start_stop':100.0}
# expected_differences = [
#     Difference(0, ideal_array[0], 0, actual_array[0], 'pitch'),
# ]
# run_test_case(ideal_array, actual_array, expected_accuracies, expected_differences, "One of the notes is too sharp")

    # Some extra test cases to take into consideration?
    # Test Case: missing note and then a extra note after
    # Test Case: One note in the middle (wrong everything)
    # Test Case: One note at the beginning (wrong note)
    # Test Case: Two notes at the begginning (wrong note)
    # Test Case: One note at the end (wrong note)
    # Test Case: Two notes at the end (wrong note )
    # Test Case: Two notes swapped in the middle
    # Test Case: Two missing notes placed randomly in the middle
    # Test Case: Missing two notes at the end
    # Test Case: Missing one note at the beginning *** prio ***
    # Test Case: Missing two notes at the beginning *** prio ***
    # Test Case: Insert two extra notes placed randomly in the middle
    # Test Case: Insert two extra notes back-to-back in the middle
    # Test Case: Extra note at the beginning
    # Test Case: Two extra notes at the beginning
    # Test Case: Extra note at the end
    # Test Case: Two extra notes at the end
