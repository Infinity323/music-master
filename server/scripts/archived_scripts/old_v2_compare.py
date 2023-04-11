# this is V2 of mxl_wav_compare.py

# This script compares two arrays of Note objects, representing ideal and actual
# musical performances, and calculates the accuracy and differences between them.

# Define the Note class representing a musical note with its properties.
class Note:
    def __init__(self, note, velocity, start_time, end_time):
        self.note = note
        self.velocity = velocity
        self.start_time = start_time
        self.end_time = end_time

    # Define the equality method for comparing two Note objects.
    def __eq__(self, other):
        if not isinstance(other, Note):
            return False
        return (self.note == other.note and
                self.velocity == other.velocity and
                self.start_time == other.start_time and
                self.end_time == other.end_time)

    # Define the string representation of the Note object.
    def __str__(self):
        return f"Note: {self.note}, Velocity: {self.velocity}, Start Time: {self.start_time}, End Time: {self.end_time}"

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

# Modify the compare_arrays function to detect differences in note, velocity, start_time, and end_time.
def compare_arrays(ideal_array, actual_array):
    # Check for empty arrays and exit early if found.
    if not ideal_array or not actual_array:
        return None, None

    # Get the lengths of the arrays.
    ideal_len = len(ideal_array)
    actual_len = len(actual_array)

    # Check if the ideal array is longer than the actual array and exit early if true.
    if ideal_len > actual_len:
        return None, None

    # Initialize variables to store the maximum matches and best start index.
    max_matches = 0
    best_start = 0

    # Iterate through the actual array to find the best start index for comparison.
    for start in range(actual_len - ideal_len + 1):
        matches = 0
        for i in range(ideal_len):
            if ideal_array[i] == actual_array[start + i]:
                matches += 1

        if matches > max_matches:
            max_matches = matches
            best_start = start

    # Calculate the accuracy as a percentage.
    accuracy = (max_matches / ideal_len) * 100

    # Find the differences between the ideal and actual arrays.
    differences = []
    for i in range(min(ideal_len, actual_len - best_start)):
        ideal_note = ideal_array[i]
        actual_note = actual_array[best_start + i]
        if ideal_note != actual_note:
            if ideal_note.note != actual_note.note:
                differences.append(Difference(i, ideal_note, best_start + i, actual_note, 'note'))
            if ideal_note.velocity != actual_note.velocity:
                differences.append(Difference(i, ideal_note, best_start + i, actual_note, 'velocity'))
            if ideal_note.start_time != actual_note.start_time:
                differences.append(Difference(i, ideal_note, best_start + i, actual_note, 'start_time'))
            if ideal_note.end_time != actual_note.end_time:
                differences.append(Difference(i, ideal_note, best_start + i, actual_note, 'end_time'))

    return accuracy, differences

# Define the function to test the compare_arrays function with various test cases.
def test_case(case_num, description, ideal_array, actual_array, expected_accuracy, expected_differences):
    calculated_accuracy, calculated_differences = compare_arrays(ideal_array, actual_array)
    accuracy_passed = abs(calculated_accuracy - expected_accuracy) < 0.01 if calculated_accuracy is not None else False
    differences_passed = calculated_differences == expected_differences

    # ERROR
    if calculated_accuracy is None or calculated_differences is None:
        print(f"Test Case {case_num}: SKIPPED (Unable to calculate accuracy and differences)")
        print("\n------------------------\n")
        return

    # Print test case results.
    if accuracy_passed and differences_passed:
        print(f"Test Case {case_num} | {description} | PASSED")
    else:
        print(f"Test Case {case_num} | {description} | FAILED")
        if not accuracy_passed:
            print(f"Expected accuracy: {expected_accuracy:.2f}%,\nCalculated accuracy: {calculated_accuracy:.2f}%")
        if not differences_passed:
            print(f"Expected differences: {expected_differences},\nCalculated differences: {calculated_differences}")

    print("\n------------------------\n")


if __name__ == "__main__":

    # BASE CASE
    # Test Case 1: Perfect match

    # WRONG NOTES
    # Test Case 2: One note in the middle (wrong note)
    # Test Case 3: One note in the middle (wrong velocity)
    # Test Case 4: One note in the middle (wrong start time)
    # Test Case 5: One note in the middle (wrong end time)
    # Test Case 6: One note in the middle (wrong start time and end time)
    # Test Case 7: One note in the middle (wrong everything)
    # Test Case 8: One note at the beginning (wrong note)
    # Test Case 9: Two notes at the begginning (wrong note)
    # Test Case 10: One note at the end (wrong note)
    # Test Case 11: Two notes at the end (wrong note )
    # Test Case 12: Two notes swapped in the middle

    # MISSING NOTES
    # Test Case 13: Two missing notes placed randomly in the middle
    # Test Case 14: One missing note and one extra note in the middle
    # Test Case 15: Missing one note at the end
    # Test Case 16: Missing two notes at the end
    # Test Case 17: Missing one note at the beginning *** prio ***
    # Test Case 18: Missing two notes at the beginning *** prio ***

    # EXTRA NOTES
    # Test Case 19: Insert extra note in the middle
    # Test Case 20: Insert two extra notes placed randomly in the middle
    # Test Case 21: Insert two extra notes back-to-back in the middle
    # Test Case 22: Extra note at the beginning
    # Test Case 23: Two extra notes at the beginning
    # Test Case 24: Extra note at the end
    # Test Case 25: Two extra notes at the end

    # TODO:
    # add 3 seperate percent accuracies to the code (note, dynamic, tempo)
    # fix start detection
    # add robustness against extra note and/or missing notes

    print("\n*** Testing Started ***")
    print("------------------------\n")

    # ------------- BASE CASE -------------

    # Test Case 1: Perfect match
    ideal_array1 = [
        Note(60, 80, 0, 1),
        Note(62, 80, 1, 2),
        Note(64, 80, 2, 3),
        Note(65, 80, 3, 4),
        Note(67, 80, 4, 5)
    ]
    actual_array = [
        # Note(60, 80, 0, 1),
        # Note(62, 80, 1, 2),
        # Note(64, 80, 2, 3),
        # Note(65, 80, 3, 4),
        # Note(67, 80, 4, 5)
        Note(60, 80, 0, 1),
        Note(62, 80, 1, 2),
        Note(64, 80, 2, 3),
        Note(65, 80, 3, 4),
        Note(67, 80, 4, 5)
    ]
    test_case(1, "Perfect match", ideal_array1, actual_array, 100.0, []) # no errors

    # ------------- WRONG NOTES -------------

    # Test Case 2: One note in the middle (wrong note)
    actual_array = [
        # Note(60, 80, 0, 1),
        # Note(62, 80, 1, 2),
        # Note(64, 80, 2, 3),
        # Note(65, 80, 3, 4),
        # Note(67, 80, 4, 5)
        Note(60, 80, 0, 1),
        Note(62, 80, 1, 2),
        Note(64, 80, 2, 3),
        Note(64, 80, 3, 4), # diff note
        Note(67, 80, 4, 5)
    ]
    expected_differences = [Difference(3, ideal_array1[3], 3, actual_array[3], 'note')] # should deduct from note accuracy only
    test_case(2, "One note in the middle (wrong note)", ideal_array1, actual_array, 80.0, expected_differences)

    # Test Case 3: One note in the middle (wrong velocity)
    actual_array = [
        # Note(60, 80, 0, 1),
        # Note(62, 80, 1, 2),
        # Note(64, 80, 2, 3),
        # Note(65, 80, 3, 4),
        # Note(67, 80, 4, 5)
        Note(60, 80, 0, 1),
        Note(62, 80, 1, 2),
        Note(64, 81, 2, 3), # diff velocity
        Note(65, 80, 3, 4),
        Note(67, 80, 4, 5)
    ]
    expected_differences = [
        Difference(2, ideal_array1[2], 2, actual_array[2], 'velocity')
    ] # should deduct from velocity and note accuracy only
    test_case(3, "One note in the middle (wrong velocity)", ideal_array1, actual_array, 80.0, expected_differences)

    # Test Case 4: One note in the middle (wrong start time)
    actual_array = [
        # Note(60, 80, 0, 1),
        # Note(62, 80, 1, 2),
        # Note(64, 80, 2, 3),
        # Note(65, 80, 3, 4),
        # Note(67, 80, 4, 5)
        Note(60, 80, 0, 1),
        Note(62, 80, 1, 2),
        Note(64, 80, 2, 3),
        Note(65, 80, 3, 4),
        Note(67, 80, 4, 5)
    ]
    test_case(4, "NOT IMPLEMENTED", ideal_array1, actual_array, 100.0, [])

    # Test Case 5: One note in the middle (wrong end time)
    actual_array = [
        # Note(60, 80, 0, 1),
        # Note(62, 80, 1, 2),
        # Note(64, 80, 2, 3),
        # Note(65, 80, 3, 4),
        # Note(67, 80, 4, 5)
        Note(60, 80, 0, 1),
        Note(62, 80, 1, 2),
        Note(64, 80, 2, 3),
        Note(65, 80, 3, 4),
        Note(67, 80, 4, 5)
    ]
    test_case(5, "NOT IMPLEMENTED", ideal_array1, actual_array, 100.0, [])

    # Test Case 6: One note in the middle (wrong start time and end time)
    actual_array = [
        # Note(60, 80, 0, 1),
        # Note(62, 80, 1, 2),
        # Note(64, 80, 2, 3),
        # Note(65, 80, 3, 4),
        # Note(67, 80, 4, 5)
        Note(60, 80, 0, 1),
        Note(62, 80, 1, 2),
        Note(64, 80, 2, 3),
        Note(65, 80, 3, 4),
        Note(67, 80, 4, 5)
    ]
    test_case(6, "NOT IMPLEMENTED", ideal_array1, actual_array, 100.0, [])

    # Test Case 7: One note in the middle (wrong everything)
    actual_array = [
        # Note(60, 80, 0, 1),
        # Note(62, 80, 1, 2),
        # Note(64, 80, 2, 3),
        # Note(65, 80, 3, 4),
        # Note(67, 80, 4, 5)
        Note(60, 80, 0, 1),
        Note(62, 80, 1, 2),
        Note(64, 80, 2, 3),
        Note(65, 80, 3, 4),
        Note(67, 80, 4, 5)
    ]
    test_case(7, "NOT IMPLEMENTED", ideal_array1, actual_array, 100.0, [])

    # Test Case 8: One note at the beginning (wrong note)
    actual_array = [
        # Note(60, 80, 0, 1),
        # Note(62, 80, 1, 2),
        # Note(64, 80, 2, 3),
        # Note(65, 80, 3, 4),
        # Note(67, 80, 4, 5)
        Note(63, 80, 0, 1), # diff note
        Note(62, 80, 1, 2),
        Note(64, 80, 2, 3),
        Note(65, 80, 3, 4),
        Note(67, 80, 4, 5)
    ]
    expected_differences = [
        Difference(0, ideal_array1[0], 0, actual_array[0], 'note'),
    ]
    test_case(8, "One note at the beginning (wrong note)", ideal_array1, actual_array, 80.0, expected_differences)

    # Test Case 9: Two notes at the begginning (wrong note)
    actual_array = [
        # Note(60, 80, 0, 1),
        # Note(62, 80, 1, 2),
        # Note(64, 80, 2, 3),
        # Note(65, 80, 3, 4),
        # Note(67, 80, 4, 5)
        Note(63, 80, 0, 1), # diff note
        Note(67, 80, 1, 2), # diff note
        Note(64, 80, 2, 3),
        Note(65, 80, 3, 4),
        Note(67, 80, 4, 5)
    ]
    expected_differences = [
        Difference(0, ideal_array1[0], 0, actual_array[0], 'note'),
        Difference(1, ideal_array1[1], 1, actual_array[1], 'note')
    ]
    test_case(9, "Two notes at the begginning (wrong note)",
               ideal_array1, actual_array, 60.0, expected_differences)

    # Test Case 10: One note at the end (wrong note)
    actual_array = [
        # Note(60, 80, 0, 1),
        # Note(62, 80, 1, 2),
        # Note(64, 80, 2, 3),
        # Note(65, 80, 3, 4),
        # Note(67, 80, 4, 5)
        Note(60, 80, 0, 1),
        Note(62, 80, 1, 2),
        Note(64, 80, 2, 3),
        Note(65, 80, 3, 4),
        Note(67, 80, 4, 5)
    ]
    test_case(10, "NOT IMPLEMENTED", ideal_array1, actual_array, 100.0, [])

    # Test Case 11: Two notes at the end (wrong note)
    actual_array = [
        # Note(60, 80, 0, 1),
        # Note(62, 80, 1, 2),
        # Note(64, 80, 2, 3),
        # Note(65, 80, 3, 4),
        # Note(67, 80, 4, 5)
        Note(60, 80, 0, 1),
        Note(62, 80, 1, 2),
        Note(64, 80, 2, 3),
        Note(65, 80, 3, 4),
        Note(67, 80, 4, 5)
    ]
    test_case(11, "NOT IMPLEMENTED", ideal_array1, actual_array, 100.0, [])

    # Test Case 12: Two notes swapped in the middle
    actual_array = [
        # Note(60, 80, 0, 1),
        # Note(62, 80, 1, 2),
        # Note(64, 80, 2, 3),
        # Note(65, 80, 3, 4),
        # Note(67, 80, 4, 5)
        Note(60, 80, 0, 1),
        Note(62, 80, 1, 2),
        Note(67, 80, 2, 3), # swap
        Note(65, 80, 3, 4),
        Note(64, 80, 4, 5) # swap
    ]
    expected_differences = [
        Difference(2, ideal_array1[2], 2, actual_array[2], 'note'),
        Difference(4, ideal_array1[4], 4, actual_array[4], 'note')
    ] # should deduct from note accuracy only and count both wrong
    test_case(12, "Two notes swapped in the middle", ideal_array1, actual_array, 60.0, expected_differences)

    # ------------- MISSING NOTES -------------

    # Test Case 13: Two missing notes placed randomly in the middle
    actual_array = [
        # Note(60, 80, 0, 1),
        # Note(62, 80, 1, 2),
        # Note(64, 80, 2, 3),
        # Note(65, 80, 3, 4),
        # Note(67, 80, 4, 5)
        Note(60, 80, 0, 1),
        Note(62, 80, 1, 2),
        Note(64, 80, 2, 3),
        Note(65, 80, 3, 4),
        Note(67, 80, 4, 5)
    ]
    test_case(13, "NOT IMPLEMENTED", ideal_array1, actual_array, 100.0, [])

    # Test Case 14: One missing note and one extra note in the middle
    actual_array = [
        # Note(60, 80, 0, 1),
        # Note(62, 80, 1, 2),
        # Note(64, 80, 2, 3),
        # Note(65, 80, 3, 4),
        # Note(67, 80, 4, 5)
        Note(60, 80, 0, 1),
        Note(62, 80, 1, 2),
        Note(64, 80, 2, 3),
        Note(65, 80, 3, 4),
        Note(67, 80, 4, 5)
    ]
    test_case(14, "NOT IMPLEMENTED", ideal_array1, actual_array, 100.0, [])

    # Test Case 15: Missing one note at the end
    actual_array = [
        # Note(60, 80, 0, 1),
        # Note(62, 80, 1, 2),
        # Note(64, 80, 2, 3),
        # Note(65, 80, 3, 4),
        # Note(67, 80, 4, 5)
        Note(60, 80, 0, 1),
        Note(62, 80, 1, 2),
        Note(64, 80, 2, 3),
        Note(65, 80, 3, 4)
        # missing note
    ]
    expected_differences = [Difference(4, ideal_array1[4], None, None, 'missing')] # should deduct 5% from note accuracy and indicate a missing note
    test_case(15, "Missing one note at the end", ideal_array1, actual_array, 95.0, expected_differences)

    # Test Case 16: Missing two notes at the end
    actual_array = [
        # Note(60, 80, 0, 1),
        # Note(62, 80, 1, 2),
        # Note(64, 80, 2, 3),
        # Note(65, 80, 3, 4),
        # Note(67, 80, 4, 5)
        Note(60, 80, 0, 1),
        Note(62, 80, 1, 2),
        Note(64, 80, 2, 3),
        Note(65, 80, 3, 4),
        Note(67, 80, 4, 5)
    ]
    test_case(16, "NOT IMPLEMENTED", ideal_array1, actual_array, 100.0, [])

    # Test Case 17: Missing one note at the beginning
    actual_array = [
        # Note(60, 80, 0, 1),
        # Note(62, 80, 1, 2),
        # Note(64, 80, 2, 3),
        # Note(65, 80, 3, 4),
        # Note(67, 80, 4, 5)
        Note(60, 80, 0, 1),
        Note(62, 80, 1, 2),
        Note(64, 80, 2, 3),
        Note(65, 80, 3, 4),
        Note(67, 80, 4, 5)
    ]
    test_case(17, "NOT IMPLEMENTED *** prio ***", ideal_array1, actual_array, 100.0, [])

    # Test Case 18: Missing two notes at the beginning
    actual_array = [
        # Note(60, 80, 0, 1),
        # Note(62, 80, 1, 2),
        # Note(64, 80, 2, 3),
        # Note(65, 80, 3, 4),
        # Note(67, 80, 4, 5)
        Note(60, 80, 0, 1),
        Note(62, 80, 1, 2),
        Note(64, 80, 2, 3),
        Note(65, 80, 3, 4),
        Note(67, 80, 4, 5)
    ]
    test_case(18, "NOT IMPLEMENTED *** prio ***", ideal_array1, actual_array, 100.0, [])

    # ------------- EXTRA NOTES -------------

    # Test Case 19: Insert extra note in the middle
    actual_array = [
        # Note(60, 80, 0, 1),
        # Note(62, 80, 1, 2),
        # Note(64, 80, 2, 3),
        # Note(65, 80, 3, 4),
        # Note(67, 80, 4, 5)
        Note(60, 80, 0, 1),
        Note(62, 80, 1, 2),
        Note(64, 80, 2, 3),
        Note(64, 80, 3, 4), # insert extra
        Note(65, 80, 4, 5),
        Note(67, 80, 5, 6)
    ]
    expected_differences = [
        Difference(3, ideal_array1[3], 3, actual_array[3], 'extra') # should deduct 5% from note accuracy and indicate an extra note
    ]
    test_case(19, "Insert extra note in the middle", ideal_array1, actual_array, 95.0, expected_differences)

    # Test Case 20: Insert two extra notes placed randomly in the middle
    actual_array = [
        # Note(60, 80, 0, 1),
        # Note(62, 80, 1, 2),
        # Note(64, 80, 2, 3),
        # Note(65, 80, 3, 4),
        # Note(67, 80, 4, 5)
        Note(60, 80, 0, 1),
        Note(62, 80, 1, 2),
        Note(64, 80, 2, 3),
        Note(65, 80, 3, 4),
        Note(67, 80, 4, 5)
    ]
    test_case(20, "NOT IMPLEMENTED", ideal_array1, actual_array, 100.0, [])

    # Test Case 21: Insert two extra notes back-to-back in the middle
    actual_array = [
        # Note(60, 80, 0, 1),
        # Note(62, 80, 1, 2),
        # Note(64, 80, 2, 3),
        # Note(65, 80, 3, 4),
        # Note(67, 80, 4, 5)
        Note(60, 80, 0, 1),
        Note(62, 80, 1, 2),
        Note(64, 80, 2, 3),
        Note(65, 80, 3, 4),
        Note(67, 80, 4, 5)
    ]
    test_case(21, "NOT IMPLEMENTED", ideal_array1, actual_array, 100.0, [])

    # Test Case 22: Extra note at the beginning
    actual_array = [
        # Note(60, 80, 0, 1),
        # Note(62, 80, 1, 2),
        # Note(64, 80, 2, 3),
        # Note(65, 80, 3, 4),
        # Note(67, 80, 4, 5)
        Note(30, 80, 0, 1),
        Note(60, 80, 1, 2),
        Note(62, 80, 2, 3),
        Note(64, 80, 3, 4),
        Note(65, 80, 4, 5),
        Note(67, 80, 5, 6)
    ]
    expected_differences = [
        Difference(0, ideal_array1[0], 0, actual_array[0], 'extra')
    ]
    test_case(22, "Extra note at the beginning", ideal_array1, actual_array, 95.0, expected_differences)

    # Test Case 23: Two extra notes at the beginning
    actual_array = [
        # Note(60, 80, 0, 1),
        # Note(62, 80, 1, 2),
        # Note(64, 80, 2, 3),
        # Note(65, 80, 3, 4),
        # Note(67, 80, 4, 5)
        Note(60, 80, 0, 1),
        Note(62, 80, 1, 2),
        Note(64, 80, 2, 3),
        Note(65, 80, 3, 4),
        Note(67, 80, 4, 5)
    ]
    test_case(23, "NOT IMPLEMENTED", ideal_array1, actual_array, 100.0, [])

    # Test Case 24: Extra note at the end
    actual_array = [
        # Note(60, 80, 0, 1),
        # Note(62, 80, 1, 2),
        # Note(64, 80, 2, 3),
        # Note(65, 80, 3, 4),
        # Note(67, 80, 4, 5)
        Note(60, 80, 0, 1),
        Note(62, 80, 1, 2),
        Note(64, 80, 2, 3),
        Note(65, 80, 3, 4),
        Note(67, 80, 4, 5)
    ]
    test_case(24, "NOT IMPLEMENTED", ideal_array1, actual_array, 100.0, [])

    # Test Case 25: Two extra notes at the end
    actual_array = [
        # Note(60, 80, 0, 1),
        # Note(62, 80, 1, 2),
        # Note(64, 80, 2, 3),
        # Note(65, 80, 3, 4),
        # Note(67, 80, 4, 5)
        Note(60, 80, 0, 1),
        Note(62, 80, 1, 2),
        Note(64, 80, 2, 3),
        Note(65, 80, 3, 4),
        Note(67, 80, 4, 5)
    ]
    test_case(25, "NOT IMPLEMENTED", ideal_array1, actual_array, 100.0, [])
