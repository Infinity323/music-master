import numpy as np

# This script compares two arrays of Note objects, representing ideal and actual
# musical performances, and calculates the accuracy and differences between them.

# This function is used to ensure that the note object is properly serialized 
def custom_serializer(obj):
    if isinstance(obj, Note):
        return obj.to_dict()
    raise TypeError(f'Object of type {obj.__class__.__name__} is not JSON serializable')

class Note:
    def __init__(self, pitch, velocity, start_time, end_time):
        self.pitch = pitch
        self.velocity = velocity
        self.start_time = start_time
        self.end_time = end_time

    # Define the equality method for comparing two Note objects.
    def __eq__(self, other):
        if not isinstance(other, Note):
            return False
        return (self.pitch == other.pitch and
                self.velocity == other.velocity and
                self.start_time == other.start_time and
                self.end_time == other.end_time)

    # Define the string representation of the Note object.
    def __str__(self):
        return f"Note: {self.pitch}, Velocity: {self.velocity}, Start Time: {self.start_time}, End Time: {self.end_time}"
    
    # Convert the Note object to a dictionary for JSON serialization.
    def to_dict(self):
        return {
            "pitch": self.pitch,
            "velocity": self.velocity,
            "start_time": self.start_time,
            "end_time": self.end_time
        }

# Define the Difference class representing the differences between ideal and actual Note objects.
class Difference:
    def __init__(self, ideal_idx, ideal_val, actual_idx, actual_val, diff_type):
        self.ideal_idx = ideal_idx
        self.ideal_val = ideal_val
        self.actual_idx = actual_idx
        self.actual_val = actual_val
        self.diff_type = diff_type

    # Define the string representation of the Difference object.
    def __repr__(self):
        return f"\n* diff_type: {self.diff_type} *\n Ideal: index {self.ideal_idx}, ({self.ideal_val})\n Actual: index {self.actual_idx}, ({self.actual_val})"
    
    # Define the equality method for comparing two Difference objects.
    def __eq__(self, other):
        if not isinstance(other, Difference):
            return False
        return (self.ideal_idx == other.ideal_idx and
                self.ideal_val == other.ideal_val and
                self.actual_idx == other.actual_idx and
                self.actual_val == other.actual_val)
    
    # Convert the Difference object to a dictionary for JSON serialization.
    def to_dict(self):
        return {
            "ideal_idx": self.ideal_idx,
            "ideal_val": self.ideal_val,
            "actual_idx": self.actual_idx,
            "actual_val": self.actual_val,
            "diff_type": self.diff_type
        }

# Implement the Needleman-Wunsch algorithm to find the optimal alignment of two arrays of musical notes.
def needleman_wunsch(seq1, seq2, gap_penalty=-1, mismatch_penalty=-1, match_score=2, extra_note_penalty=-2):
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
            insert = score_matrix[i, j - 1] + gap_penalty
            extra = score_matrix[i - 1, j - 1] + extra_note_penalty
            # Choose the maximum score and store it in the score matrix.
            score_matrix[i, j] = max(match, delete, insert, extra)

    # Return the final score matrix.
    return score_matrix

# Compare two arrays of musical notes and calculate the accuracy and differences between them.
def compare_arrays(ideal_array, actual_array):
    # If either array is empty, return None for all metrics.
    if not ideal_array or not actual_array:
        return None, None, None, None

    # Use the Needleman-Wunsch algorithm to find the optimal alignment of the two arrays
    score_matrix = needleman_wunsch(ideal_array, actual_array, gap_penalty=-1, mismatch_penalty=-1, match_score=2, extra_note_penalty=-0.5)
    ideal_len, actual_len = len(ideal_array), len(actual_array)

    # Traceback through the score matrix to determine the optimal alignment
    i, j = ideal_len, actual_len
    aligned_ideal = []
    aligned_actual = []

    while i > 0 or j > 0:
        match = score_matrix[i - 1, j - 1] + (2 if ideal_array[i - 1] == actual_array[j - 1] else -1) if i > 0 and j > 0 else float('-inf')
        delete = score_matrix[i - 1, j] + (-1) if i > 0 else float('-inf')
        insert = score_matrix[i, j - 1] + (-0.5) if j > 0 else float('-inf')

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

    # Calculate the accuracy values
    matches_notes = matches_dynamics = matches_start_stop = 0
    differences = []
    extra_note_count = 0

    for i, (ideal_note, actual_note) in enumerate(zip(aligned_ideal, aligned_actual)):
        if ideal_note is not None and actual_note is not None:
            if ideal_note.pitch == actual_note.pitch:
                matches_notes += 1
            if ideal_note.velocity == actual_note.velocity:
                matches_dynamics += 1
            if ideal_note.start_time == actual_note.start_time and ideal_note.end_time == actual_note.end_time:
                matches_start_stop += 1
            if ideal_note.pitch != actual_note.pitch:
                differences.append(Difference(i, ideal_note, i, actual_note, 'pitch'))
            if ideal_note.velocity != actual_note.velocity:
                differences.append(Difference(i, ideal_note, i, actual_note, 'velocity'))
            if ideal_note.start_time != actual_note.start_time:
                differences.append(Difference(i, ideal_note, i, actual_note, 'start_time'))
            if ideal_note.end_time != actual_note.end_time:
                differences.append(Difference(i, ideal_note, i, actual_note, 'end_time'))
        elif ideal_note is None and actual_note is not None:
            differences.append(Difference(None, None, i, actual_note, 'extra'))
            extra_note_count = extra_note_count + 1
        elif ideal_note is not None and actual_note is None:
            differences.append(Difference(i - extra_note_count, ideal_note, None, None, 'missing'))

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
# ideal_array = [Note('C', 100, 0, 1), Note('D', 80, 1, 2), Note('E', 60, 2, 3), Note('F', 40, 3, 4)]
# actual_array = [Note('C', 100, 0, 1), Note('D', 80, 1, 2), Note('E', 60, 2, 3), Note('F', 40, 3, 4)]
# expected_accuracies = {'notes': 100.0, 'dynamics': 100.0, 'start_stop': 100.0}
# expected_differences = []
# run_test_case(ideal_array, actual_array, expected_accuracies, expected_differences, "Exact Match")

# # Test Case 2: Different Note
# ideal_array = [Note('C', 100, 0, 1), Note('D', 80, 1, 2), Note('E', 60, 2, 3), Note('F', 40, 3, 4)]
# actual_array = [Note('C', 100, 0, 1), Note('A', 80, 1, 2), Note('E', 60, 2, 3), Note('F', 40, 3, 4)]
# expected_accuracies = {'notes': 75.0, 'dynamics': 100.0, 'start_stop': 100.0}
# expected_differences = [
#     Difference(1, ideal_array[1], 1, actual_array[1], 'pitch')
# ]
# run_test_case(ideal_array, actual_array, expected_accuracies, expected_differences, "Different Note")

# # Test Case 3: Different Dynamics
# ideal_array = [Note('C', 100, 0, 1), Note('D', 80, 1, 2), Note('E', 60, 2, 3), Note('F', 40, 3, 4)]
# actual_array = [Note('C', 100, 0, 1), Note('D', 40, 1, 2), Note('E', 60, 2, 3), Note('F', 40, 3, 4)]
# expected_accuracies = {'notes': 100.0, 'dynamics': 75.0, 'start_stop': 100.0}
# expected_differences = [
#     Difference(1, ideal_array[1], 1, actual_array[1], 'velocity')
# ]
# run_test_case(ideal_array, actual_array, expected_accuracies, expected_differences, "Different Dynamics")

# # Test Case 4: Different Start Time
# ideal_array = [Note('C', 100, 0, 1), Note('D', 80, 1, 2), Note('E', 60, 2, 3), Note('F', 40, 3, 4)]
# actual_array = [Note('C', 100, 0, 1), Note('D', 80, 1.5, 2), Note('E', 60, 2, 3), Note('F', 40, 3, 4)]
# expected_accuracies = {'notes': 100.0, 'dynamics': 100.0, 'start_stop': 75.0}
# expected_differences = [
#     Difference(1, ideal_array[1], 1, actual_array[1], 'start_time')
# ]
# run_test_case(ideal_array, actual_array, expected_accuracies, expected_differences, "Different Start Time")

# # Test Case 5: Different End Time
# ideal_array = [Note('C', 100, 0, 1), Note('D', 80, 1, 2), Note('E', 60, 2, 3), Note('F', 40, 3, 4)]
# actual_array = [Note('C', 100, 0, 1), Note('D', 80, 1, 2.5), Note('E', 60, 2, 3), Note('F', 40, 3, 4)]
# expected_accuracies = {'notes': 100.0, 'dynamics': 100.0, 'start_stop': 75.0}
# expected_differences = [
#     Difference(1, ideal_array[1], 1, actual_array[1], 'end_time')
# ]
# run_test_case(ideal_array, actual_array, expected_accuracies, expected_differences, "Different End Time")

# # Test Case 6: Different Start and End Time
# ideal_array = [Note('C', 100, 0, 1), Note('D', 80, 1, 2), Note('E', 60, 2, 3), Note('F', 40, 3, 4)]
# actual_array = [Note('C', 100, 0, 1), Note('D', 80, 1.5, 2.5), Note('E', 60, 2, 3), Note('F', 40, 3, 4)]
# expected_accuracies = {'notes': 100.0, 'dynamics': 100.0, 'start_stop': 75.0}
# expected_differences = [
#     Difference(1, ideal_array[1], 1, actual_array[1], 'start_time'),
#     Difference(1, ideal_array[1], 1, actual_array[1], 'end_time')
# ]
# run_test_case(ideal_array, actual_array, expected_accuracies, expected_differences, "Different Start and End Time")

# # Test Case 7: Extra Note
# # The actual array has an extra note 'A' that should be detected as an extra note.
# ideal_array = [Note('C', 100, 0, 1), Note('D', 80, 1, 2), Note('E', 60, 2, 3), Note('F', 40, 3, 4)]
# actual_array = [Note('C', 100, 0, 1), Note('D', 80, 1, 1.5), Note('A', 40, 1.5, 2), Note('E', 60, 2, 3), Note('F', 40, 3, 4)]
# expected_accuracies = {'notes': 95.0, 'dynamics': 100.0, 'start_stop': 75.0}
# expected_differences = [
#     Difference(1, ideal_array[1], 1, actual_array[1], 'end_time'),
#     Difference(None, None, 2, actual_array[2], 'extra')
# ]
# run_test_case(ideal_array, actual_array, expected_accuracies, expected_differences, "Extra Note")

# # Test Case 8: Missing Note
# # The actual array is missing the note 'D', which should be detected as a missing note.
# ideal_array = [Note('C', 100, 0, 1), Note('D', 80, 1, 2), Note('E', 60, 2, 3), Note('F', 40, 3, 4)]
# actual_array = [Note('C', 100, 0, 1), Note('E', 60, 2, 3), Note('F', 40, 3, 4)]
# expected_accuracies = {'notes': 75.0, 'dynamics': 75.0, 'start_stop': 75.0}
# expected_differences = [
#     Difference(1, ideal_array[1], None, None, 'missing')
# ]
# run_test_case(ideal_array, actual_array, expected_accuracies, expected_differences, "Missing Note")

# # Test Case 9: Extra Note and Missing Note
# ideal_array = [Note('C', 100, 0, 1), Note('D', 80, 1, 2), Note('E', 60, 2, 3), Note('F', 40, 3, 4)]
# actual_array = [Note('C', 100, 0, 1), Note('D', 80, 1, 1.5), Note('A', 40, 1.5, 2), Note('E', 60, 2, 3)]
# expected_accuracies = {'notes': 70.0, 'dynamics': 75.0, 'start_stop': 50.0}
# expected_differences = [
#     Difference(1, ideal_array[1], 1, actual_array[1], 'end_time'),
#     Difference(None, None, 2, actual_array[2], 'extra'),
#     Difference(3, ideal_array[3], None, None, 'missing')
# ]
# run_test_case(ideal_array, actual_array, expected_accuracies, expected_differences, "Extra Note and Missing Note")

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
