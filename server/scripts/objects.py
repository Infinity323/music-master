import numpy as np
import os
import base64
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet
from config import NOTE_MATCH_PASS_CONF, PITCH_WEIGHT, VELOCITY_WEIGHT, END_WEIGHT, START_WEIGHT, PITCH_TOLERANCE, VELOCITY_TOLERANCE, START_TOLERANCE, END_TOLERANCE, EXTRA_NOTE_MAX_PENALTY_DURATION, EXTRA_NOTE_MAX_PENALTY

class Chord:
    def __init__(self, chord):
        self.notes_str = chord[0]
        self.start = chord[1]
        self.end = chord[2]
        self.duration = chord[3]
        self.velocity = chord[4]

        # Generate a key for encryption and decryption
        self.key = self.generate_key()

        # Encrypt and encode the notes string
        self.encoded_notes_str = self.encrypt_and_encode()

    def generate_key(self):
        password = b'password'
        salt = os.urandom(16)
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000
        )
        key = base64.urlsafe_b64encode(kdf.derive(password))
        return key

    def encrypt_and_encode(self):
        f = Fernet(self.key)
        encrypted_data = f.encrypt(self.notes_str.encode("utf-8"))
        encoded_value = int.from_bytes(encrypted_data, byteorder='big') + 90001
        return encoded_value

    @staticmethod
    def decode_and_decrypt(encoded_value, key):
        encrypted_data = (encoded_value - 90001).to_bytes((encoded_value.bit_length() + 7) // 8, byteorder='big')
        f = Fernet(key)
        decrypted_data = f.decrypt(encrypted_data)
        return decrypted_data.decode("utf-8")


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


A4 = 440.0
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
        return confidence >= NOTE_MATCH_PASS_CONF
    
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
            PITCH_WEIGHT * pitch_confidence +
            START_WEIGHT * start_confidence +
            END_WEIGHT * end_confidence +
            VELOCITY_WEIGHT * velocity_confidence
        )

        return total_confidence

    # function to get the difference between two frequencies in unit of cents
    @staticmethod
    def difference_cents(freq1: float, freq2: float) -> float:
        return abs(1200 * np.log2(freq1 / freq2))

    @staticmethod
    def round_frequency(freq: float) -> float:
        exponent = np.round(12*np.log2(freq/A4))
        return A4*2**(exponent/12.0)
    
    @staticmethod
    def get_pitch_eq_confidence(freq1: float, freq2: float, tolerance=PITCH_TOLERANCE) -> float:
        return max(0, 1 - (abs(1200 * np.log2(freq1 / freq2)) / tolerance))
    
    @staticmethod
    def get_velocity_eq_confidence(vel1: float, vel2: float, tolerance=VELOCITY_TOLERANCE):
        return max(0, 1 - abs(vel1 - vel2) / tolerance)
    
    @staticmethod
    def get_start_eq_confidence(start1: float, start2: float, tolerance=START_TOLERANCE):
        return max(0, 1 - abs(start1 - start2) / tolerance)
    
    @staticmethod
    def get_end_eq_confidence(end1, end2, tolerance=END_TOLERANCE):
        return max(0, 1 - abs(end1 - end2) / tolerance)
    
    @staticmethod
    def get_extra_note_penalty(self, max_duration = EXTRA_NOTE_MAX_PENALTY_DURATION, max_penalty = EXTRA_NOTE_MAX_PENALTY):
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
        return "{pitch:.2f} Hz, {velocity} m/s, {start:.2f}-{end:.2f} s".format(
            pitch=self.pitch, velocity=self.velocity, start=self.start, end=self.end)