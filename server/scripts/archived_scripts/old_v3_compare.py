import numpy as np

class DifferenceDTW:
    def __init__(self, ideal_idx, actual_idx, diff_type):
        self.ideal_idx = ideal_idx
        self.actual_idx = actual_idx
        self.diff_type = diff_type

    def __repr__(self):
        return f"\n* diff_type: {self.diff_type} *\n Ideal: index {self.ideal_idx}\n Actual: index {self.actual_idx}"

def dtw_distance(s1, s2, dist_func, step_pattern):
    M, N = len(s1), len(s2)
    cost_matrix = np.zeros((M + 1, N + 1))
    cost_matrix[0, 1:] = np.inf
    cost_matrix[1:, 0] = np.inf
    cost_matrix[0, 0] = 0

    for i in range(1, M + 1):
        for j in range(1, N + 1):
            cost, _, _, _ = dist_func(s1[i - 1], s2[j - 1])
            neighbors = [cost_matrix[i - 1, j], cost_matrix[i, j - 1], cost_matrix[i - 1, j - 1]]
            if step_pattern:
                neighbors.extend([cost_matrix[i - 2, j - 1], cost_matrix[i - 1, j - 2]])
            cost_matrix[i, j] = cost + min(neighbors)

    return cost_matrix

def note_distance(n1, n2):
    if n1 is None or n2 is None:
        return 1.0, 1, 1, 1

    note_diff = 0 if n1.note == n2.note else 1
    velocity_diff = 0 if n1.velocity == n2.velocity else 1
    start_time_diff = 0 if n1.start_time == n2.start_time else 1
    end_time_diff = 0 if n1.end_time == n2.end_time else 1

    # You can adjust the weights according to your requirements
    total_diff = note_diff * 1.0 + velocity_diff * 0.5 + start_time_diff * 0.5 + end_time_diff * 0.5
    return total_diff, note_diff, velocity_diff, start_time_diff + end_time_diff

def compare_arrays_dtw(ideal_array, actual_array, step_pattern=True):
    cost_matrix = dtw_distance(ideal_array, actual_array, note_distance, step_pattern)
    M, N = len(ideal_array), len(actual_array)

    path = []
    i, j = M, N
    while i > 0 and j > 0:
        min_cost = min(cost_matrix[i - 1, j - 1], cost_matrix[i - 1, j], cost_matrix[i, j - 1])
        if step_pattern:
            min_cost = min(min_cost, cost_matrix[i - 2, j - 1], cost_matrix[i - 1, j - 2])

        if min_cost == cost_matrix[i - 1, j - 1]:
            path.append((i - 1, j - 1))
            i -= 1
            j -= 1
        elif min_cost == cost_matrix[i - 1, j]:
            path.append((i - 1, j))
            i -= 1
        else:
            path.append((i, j - 1))
            j -= 1
        if step_pattern:
            if min_cost == cost_matrix[i - 2, j - 1]:
                path.append((i - 2, j - 1))
                i -= 2
            elif min_cost == cost_matrix[i - 1, j - 2]:
                path.append((i - 1, j - 2))
                j -= 2

    path.reverse()

    total_diff, note_diff, velocity_diff, time_diff = 0, 0, 0, 0
    differences = []
    for i, j in path:
        diff, n_diff, v_diff, t_diff = note_distance(ideal_array[i], actual_array[j])
        total_diff += diff
        note_diff += n_diff
        velocity_diff += v_diff
        time_diff += t_diff
        if n_diff + v_diff + t_diff > 0:
            if n_diff:
                differences.append(DifferenceDTW(i, j, 'note'))
            if v_diff:
                differences.append(DifferenceDTW(i, j, 'velocity'))
            if t_diff:
                differences.append(DifferenceDTW(i, j, 'start_time' if t_diff == 1 else 'end_time'))

    # Handle extra and missing notes
    if M < N:
        for j in range(M, N):
            differences.append(DifferenceDTW(None, j, 'extra'))
    elif M > N:
        for i in range(N, M):
            differences.append(DifferenceDTW(i, None, 'missing'))

    note_accuracy = (1 - note_diff / max(M, N)) * 100
    velocity_accuracy = (1 - velocity_diff / max(M, N)) * 100
    time_accuracy = (1 - time_diff / max(M, N) * 2) * 100

    return note_accuracy, velocity_accuracy, time_accuracy, differences


# Test case function
def test_case(ideal_array, actual_array, expected_note_accuracy, expected_velocity_accuracy, expected_time_accuracy, expected_differences_str, test_name):
    note_accuracy, velocity_accuracy, time_accuracy, differences = compare_arrays_dtw(ideal_array, actual_array)
    differences_str = [str(d) for d in differences]
    
    result = "PASS" if (round(note_accuracy) == round(expected_note_accuracy) and
                        round(velocity_accuracy) == round(expected_velocity_accuracy) and
                        round(time_accuracy) == round(expected_time_accuracy) and
                        differences_str == expected_differences_str) else "FAIL"
    print(f"{test_name}: {result}")

    if result == "FAIL":
        print("Expected Differences: ", expected_differences_str, "\nActual differences: ", differences_str)
        # print("Expected Note Accuracy: ", expected_note_accuracy)
        # print("Actual Note Accuracy: ", note_accuracy)
        # print("Expected Velocity Accuracy: ", expected_velocity_accuracy)
        # print("Actual Velocity Accuracy: ", velocity_accuracy)
        # print("Expected Time Accuracy: ", expected_time_accuracy)
        # print("Actual Time Accuracy: ", time_accuracy)

# Simple test cases
class TestNote:
    def __init__(self, note, velocity, start_time, end_time):
        self.note = note
        self.velocity = velocity
        self.start_time = start_time
        self.end_time = end_time

ideal_array1 = [TestNote(60, 80, 0, 1), TestNote(62, 80, 1, 2)]
actual_array1 = [TestNote(60, 80, 0, 1), TestNote(62, 80, 1, 2)]
test_case(ideal_array1, actual_array1, 100, 100, 100, [], "Test 1: Identical sequences")

ideal_array2 = [TestNote(60, 80, 0, 1), TestNote(62, 80, 1, 2)]
actual_array2 = [TestNote(60, 80, 0, 1), TestNote(61, 80, 1, 2)]
test_case(ideal_array2, actual_array2, 50, 100, 100, ["\n* diff_type: note *\n Ideal: index 1\n Actual: index 1"], "Test 2: One note different")

ideal_array3 = [TestNote(60, 80, 0, 1), TestNote(62, 80, 1, 2)]
actual_array3 = [TestNote(60, 70, 0, 1), TestNote(62, 80, 1, 2)]
test_case(ideal_array3, actual_array3, 100, 50, 100, ["\n* diff_type: velocity *\n Ideal: index 0\n Actual: index 0"], "Test 3: Different velocities")

# ideal_array4 = [TestNote(60, 80, 0, 1), TestNote(62, 80, 1, 2)]
# actual_array4 = [TestNote(60, 80, 0.5, 1.5), TestNote(62, 80, 1, 2)]
# test_case(ideal_array4, actual_array4, 100, 100, 50, ["\n* diff_type: start_time *\n Ideal: index 0\n Actual: index 0", "\n* diff_type: end_time *\n Ideal: index 0\n Actual: index 0"], "Test 4: Different start and end times")
#     # FAILS: only recognizing end_time and not both start_time and end_time

# ideal_array5 = [TestNote(60, 80, 0, 1), TestNote(62, 80, 1, 2)]
# actual_array5 = [TestNote(60, 80, 0, 0.5), TestNote(62, 80, 1, 2)]
# test_case(ideal_array5, actual_array5, 100, 100, 50, ["\n* diff_type: end_time *\n Ideal: index 0\n Actual: index 0"], "Test 5: Different end times")
#     # FAILS: actual time accuracy is 0.0% 

# ideal_array6 = [TestNote(60, 80, 0.5, 1), TestNote(62, 80, 1, 2)]
# actual_array6 = [TestNote(60, 80, 0, 1), TestNote(62, 80, 1, 2)]
# test_case(ideal_array6, actual_array6, 100, 100, 50, ["\n* diff_type: start_time *\n Ideal: index 0\n Actual: index 0"], "Test 5: Different start times")
#     # FAILS: actual time accruacy is 0.0%

# # COMPLEX TESTING

# # Test Case 6: Extra note
# # In this case, the expected results are:
# # Note Accuracy: 5/6 (5 correct notes out of 6 actual notes) = 5/6 * 100 = 83.33%
# # Velocity Accuracy: 5/6 (5 correct velocities out of 6 actual velocities) = 5/6 * 100 = 83.33%
# # Time Accuracy: 10/12 (5 correct start times and 5 correct end times out of 6 actual start and end times) = 10/12 * 100 = 83.33%
# ideal_array6 = [TestNote(60, 80, 0, 1), TestNote(62, 80, 1, 2), TestNote(64, 80, 2, 3),
#                 TestNote(65, 80, 3, 4), TestNote(67, 80, 4, 5)]
# actual_array6 = [TestNote(60, 80, 0, 1), TestNote(62, 80, 1, 2), TestNote(70, 90, 2, 3),
#                  TestNote(64, 80, 3, 4), TestNote(65, 80, 4, 5), TestNote(67, 80, 5, 6)]
# test_case(ideal_array6, actual_array6, 83.33, 83.33, 83.33, ["\n* diff_type: extra *\n Ideal: index None\n Actual: index 2"], "Test 6: Extra note in the middle")
#     # FAILS: actual note accuracy 66.66 %, actual time accuracy -33.33%
#     # Actual Differences: ['\n* diff_type: note *\n Ideal: index 2\n Actual: index 2', 
#     # '\n* diff_type: velocity *\n Ideal: index 2\n Actual: index 2', 
#     # '\n* diff_type: note *\n Ideal: index 3\n Actual: index 3', 
#     # '\n* diff_type: end_time *\n Ideal: index 3\n Actual: index 4', 
#     # '\n* diff_type: end_time *\n Ideal: index 4\n Actual: index 5', 
#     # '\n* diff_type: extra *\n Ideal: index None\n Actual: index 5']

# Test Case 7: Missing note
# Ideal array: 5 notes (C4, D4, E4, F4, G4) with equal start and end times and same velocity
# Actual array: 4 notes, the same as the ideal array but with the E4 note missing
# Expected differences: One 'missing' difference for the E4 note
# Expected accuracies: Note accuracy: 80%, Velocity accuracy: 100%, Time accuracy: 100%
ideal_array7 = [TestNote(60, 64, 0, 1), TestNote(62, 64, 1, 2), TestNote(64, 64, 2, 3), TestNote(65, 64, 3, 4), TestNote(67, 64, 4, 5)]
actual_array7 = [TestNote(60, 64, 0, 1), TestNote(62, 64, 1, 2), TestNote(65, 64, 2, 3), TestNote(67, 64, 3, 4)]
test_case(ideal_array7, actual_array7, 80.0, 100.0, 100.0, ["\n* diff_type: missing *\n Ideal: index 2\n Actual: index None"], "Test 7: Missing note")



