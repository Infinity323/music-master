from app import db

class Performance(db.Model):
    __tablename__ = "performance"

    id = db.Column(db.Integer, primary_key=True)
    run_number = db.Column(db.Integer)
    date_time = db.Column(db.DateTime)
    tempo_percent_accuracy = db.Column(db.Float)
    average_tempo = db.Column(db.Integer)
    tuning_percent_accuracy = db.Column(db.Float)
    dynamics_percent_accuracy = db.Column(db.Float)


    def __init__(self, id: int, run_number: int, date_time, tempo_percent_accuracy: float, average_tempo: int, tuning_percent_accuracy: float, dynamics_percent_accuracy: float):
        self.id = id
        self.run_number = run_number
        self.date_time = date_time
        self.tempo_percent_accuracy = tempo_percent_accuracy
        self.average_tempo = average_tempo
        self.tuning_percent_accuracy = tuning_percent_accuracy
        self.dynamics_percent_accuracy = dynamics_percent_accuracy

    @property
    def serialize(self):
        return {
            "id": self.id,
            "run_number": self.run_number,
            "date_time": self.date_time,
            "tempo_percent_accuracy": self.tempo_percent_accuracy,
            "average_tempo": self.average_tempo,
            "tuning_percent_accuracy": self.tuning_percent_accuracy,
            "dynamics_percent_accuracy": self.dynamics_percent_accuracy
        }