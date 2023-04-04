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
    
    def compare_notes(self, other):
        if not isinstance(other, Note):
            return False

        # Calculate the confidence for each factor
        pitch_confidence = Note.get_pitch_eq_confidence(self.pitch, other.pitch)
        start_confidence = Note.get_end_eq_confidence(self.start, other.start)
        end_confidence = Note.get_end_eq_confidence(self.end, other.end)
        velocity_confidence = Note.get_velocity_eq_confidence(self.velocity, other.velocity)

        # Calculate the total confidence using the weights
        total_confidence = (
            0.7 * pitch_confidence +
            0.2 * start_confidence +
            0.05 * end_confidence +
            0.05 * velocity_confidence
        )

        return total_confidence

    # function to get the difference between two frequencies in unit of cents
    @staticmethod
    def get_pitch_eq_confidence(freq1: float, freq2: float, tolerance=50) -> float:
        return max(0, 1 - (abs(1200 * np.log2(freq1 / freq2)) / tolerance))
    
    @staticmethod
    def get_velocity_eq_confidence(vel1: float, vel2: float, tolerance=30):
        return max(0, 1 - abs(vel1 - vel2) / tolerance)
    
    @staticmethod
    def get_start_eq_confidence(start1: float, start2: float, tolerance=0.25):
        return max(0, 1 - abs(start1 - start2) / tolerance)
    
    @staticmethod
    def get_end_eq_confidence(end1, end2, tolerance=0.5):
        return max(0, 1 - abs(end1 - end2) / tolerance)
    
    @staticmethod
    def get_extra_note_penalty(self, max_duration = 0.125, max_penalty = 0.025):
        note_duration = self.end - self.start
        if note_duration >= max_duration:
            return max_penalty
        else:
            return (note_duration / max_duration) * max_penalty
    
    # --- outout formatting --- #

    # This function is used to ensure that the note object is properly serialized 
    @staticmethod
    def custom_serializer(obj):
        if isinstance(obj, Note):
            return obj.to_dict()
        if isinstance(obj, Difference):
            return obj.to_dict()
        raise TypeError(f'Object of type {obj.__class__.__name__} is not JSON serializable')
    
    # Convert the Note object to a dictionary for JSON serialization.
    def to_dict(self):
        return {
            "pitch": self.pitch,
            "velocity": self.velocity,
            "start": self.start,
            "end": self.end
        }
    
    # Define the string representation of the Note object.
    def __str__(self):
        return f"Note: {self.pitch}, Velocity: {self.velocity}, Start Time: {self.start}, End Time: {self.end}"
    
    def __repr__(self):
        return "Pitch: {pitch}, Start: {start:.2f} sec, End: {end:.2f} sec".format(pitch=self.pitch, start=self.start, end=self.end)