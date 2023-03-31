import numpy as np

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

        pitch_difference_in_cents = abs(Note.frequency_difference_in_cents(self.pitch, other.pitch))
        pitch_match = pitch_difference_in_cents <= 50 # bound 20 cents

        return (pitch_match and
                Note.is_velocity_equal(self.velocity, other.velocity) and # within 30% accuracy
                (abs(self.start - other.start) <= 0.25) and # bound 0.25 sec
                (abs(self.end - other.end) <= 0.25)) # bound 0.25 sec
        
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
        
    # This function is used to ensure that the note object is properly serialized 
    @staticmethod
    def custom_serializer(obj):
        if isinstance(obj, Note):
            return obj.to_dict()
        raise TypeError(f'Object of type {obj.__class__.__name__} is not JSON serializable')

    # function to get the difference between two frequencies in unit of cents
    @staticmethod
    def frequency_difference_in_cents(freq1: float, freq2: float) -> float:
        return abs(1200 * np.log2(freq1 / freq2))
    
    @staticmethod
    def is_velocity_equal(my_velocity, other, tolerance=30):
        # Calculate the minimum and maximum acceptable range for my_velocity
        min_range = other - tolerance
        max_range = other + tolerance

        # Check if my_velocity is within the acceptable range
        return min_range <= my_velocity <= max_range