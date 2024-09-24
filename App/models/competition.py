from App.database import db  
from datetime import datetime

class Competition(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    date = db.Column(db.DateTime, default=datetime.now)
    participants = db.relationship('Participant', backref='competition', lazy=True)

    def __init__(self, name, date, participants=None):
        self.name = name
        self.date = datetime.fromisoformat(date)
        self.participants = participants or []

    def add_participant(self, participant_name):
        self.participants.append(participant_name)

    def get_competition_info(self):
        return {
            'name': self.name,
            'date': self.date.strftime("%d-%m-%Y"),
            'participants': self.participants
        }
