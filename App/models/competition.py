from App.database import db  
from datetime import datetime

class Competition(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    date = db.Column(db.DateTime, default=datetime.now)
    participants = db.relationship('Participant', backref='competition', lazy=True)
    results = db.relationship('Result', backref='competition', lazy=True)
    
    def __repr__(self):
        return f'<Competition {self.name} on {self.date}>'
    

class Participant(db.Model):
    id = db.Column(db.Integer, primary_key=True)   
    name = db.Column(db.String, nullable=False)
    competition_id = db.Column(db.Integer, db.ForeignKey('competition.id'), nullable=False)
    
    results = db.relationship('Result', backref='participant', lazy=True)
    
    def __repr__(self):
        return f"Participant('{self.name}')"
    
class Result(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    score = db.Column(db.Integer, nullable=False)
    participant_id = db.Column(db.Integer, db.ForeignKey('participant.id'), nullable=False)
    competition_id = db.Column(db.Integer, db.ForeignKey('competition.id'), nullable=False)
                               
    participant = db.relationship('Participant', backref='results')  
    competition = db.relationship('Competition', backref='results', lazy=True)
    
    def __repr__(self):
        return f'<Result {self.participant_name} - {self.score}>'