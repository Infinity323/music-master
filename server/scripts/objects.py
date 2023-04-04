import numpy as np

# Define the Difference class representing the differences between ideal and actual Note objects.
class Difference_with_info:
    def __init__(self, diff, note_info, description="note_info contains the note that was supposed to be played and its location"):
        self.diff = diff
        self.note_info = note_info
        self.description = description
    
    # Convert the Difference object to a dictionary for JSON serialization.
    def to_dict(self):
        return {
            "diff": self.diff,
            "description": self.description,
            "note_info": self.note_info
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

class Note:
    def __init__(self, pitch, velocity, start, end):
        self.pitch = pitch
        self.velocity = velocity
        self.start = start
        self.end = end

    # Define the equality method for comparing two Note objects.
    def __eq__(self, other):
        if not isinstance(other, Note):
            return False
        confidence = self.compare_notes(other)
        return confidence >= 0.7
        
    # Define the string representation of the Note object.
    def __str__(self):
        return f"Note: {self.pitch}, Velocity: {self.velocity}, Start Time: {self.start}, End Time: {self.end}"
    
    def __repr__(self):
        return "Pitch: {pitch}, Start: {start:.2f} sec, End: {end:.2f} sec".format(pitch=self.pitch, start=self.start, end=self.end)
    
    # Convert the Note object to a dictionary for JSON serialization.
    def to_dict(self):
        return {
            "pitch": self.pitch,
            "velocity": self.velocity,
            "start": self.start,
            "end": self.end
        }
    
    def compare_notes(self, other):
        if not isinstance(other, Note):
            return False

        # Calculate the confidence for each factor
        pitch_confidence = max(0, 1 - abs(Note.frequency_difference_in_cents(self.pitch, other.pitch)) / 50)
        start_confidence = max(0, 1 - abs(self.start - other.start) / 0.25)
        end_confidence = max(0, 1 - abs(self.end - other.end) / 0.25)
        dynamics_confidence = max(0, 1 - abs(self.velocity - other.velocity) / 30)

        # Calculate the total confidence using the weights
        total_confidence = (
            0.7 * pitch_confidence +
            0.2 * start_confidence +
            0.05 * end_confidence +
            0.05 * dynamics_confidence
        )

        return total_confidence
        
    # This function is used to ensure that the note object is properly serialized 
    @staticmethod
    def custom_serializer(obj):
        if isinstance(obj, Note):
            return obj.to_dict()
        if isinstance(obj, Difference):
            return obj.to_dict()
        raise TypeError(f'Object of type {obj.__class__.__name__} is not JSON serializable')

    # function to get the difference between two frequencies in unit of cents
    @staticmethod
    def frequency_difference_in_cents(freq1: float, freq2: float) -> float:
        return abs(1200 * np.log2(freq1 / freq2))
    
    @staticmethod
    def is_velocity_equal(my_velocity, other, tolerance=30): # this tolerance needs to be changed
        # Calculate the minimum and maximum acceptable range for my_velocity
        min_range = other - tolerance
        max_range = other + tolerance

        # Check if my_velocity is within the acceptable range
        return min_range <= my_velocity <= max_range