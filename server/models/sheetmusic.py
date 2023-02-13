from app import db

class SheetMusic(db.Model):
    __tablename__ = "sheet_music"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    composer = db.Column(db.String)
    instrument = db.Column(db.String)
    pdf_file_path = db.Column(db.String)
    data_file_path = db.Column(db.String)
    tempo = db.Column(db.Integer)

    def __init__(self, id: int, title: str, composer: str, instrument: str, pdf_file_path: str, data_file_path: str, tempo: int):
        self.id = id
        self.title = title
        self.composer = composer
        self.instrument = instrument
        self.pdf_file_path = pdf_file_path
        self.data_file_path = data_file_path
        self.tempo = tempo

    @property
    def serialize(self):
        return {
            "id": self.id,
            "title": self.title,
            "composer": self.composer,
            "instrument": self.instrument,
            "pdf_file_path": self.pdf_file_path,
            "data_file_path": self.data_file_path,
            "tempo": self.tempo
        }