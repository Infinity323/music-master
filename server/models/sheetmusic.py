from app import db

class SheetMusic(db.Model):
    __tablename__ = "sheet_music"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)

    def __init__(self, id: int, title: str):
        self.id = id
        self.title = title

    @property
    def serialize(self):
        return {
            "id": self.id,
            "title": self.title
        }