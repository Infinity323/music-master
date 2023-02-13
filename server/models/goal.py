from app import db

class Goal(db.Model):
    __tablename__ = "goal"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    tempo_percent_acuracy = db.Column(db.Float)
    average_tempo = db.Column(db.Integer)
    tuning_percent_accuracy = db.Column(db.Float)
    dynamics_percent_accuracy = db.Column(db.Float)


    def __init__(self, id: int, name: int, start_date, end_date, tempo_percent_accuracy: float, average_tempo: int, tuning_percent_accuracy: float, dynamics_percent_accuracy: float):
        self.id = id
        self.name = name
        self.start_date = start_date
        self.end_date = end_date
        self.tempo_percent_accuracy = tempo_percent_accuracy
        self.average_tempo = average_tempo
        self.tuning_percent_accuracy = tuning_percent_accuracy
        self.dynamics_percent_accuracy = dynamics_percent_accuracy

    @property
    def serialize(self):
        return {
            "id": self.id,
            "run_number": self.name,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "tempo_percent_accuracy": self.tempo_percent_accuracy,
            "average_tempo": self.average_tempo,
            "tuning_percent_accuracy": self.tuning_percent_accuracy,
            "dynamics_percent_accuracy": self.dynamics_percent_accuracy
        }