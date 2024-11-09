from abc import ABC, abstractmethod
from App.models import User, Competition
from database import db
from datetime import datetime
import csv


class Command(ABC):
    @abstractmethod
    def execute(self):
        pass


class CreateCompetitionsCommand(Command):
    def __init__(self,name,description,date,participants_amount,duration):
        self.name = name
        self.description = description
        self.date = date
        self.participants_amount = participants_amount
        self.duration = duration
        
    def execute(self):
        try:
            date = datetime.strptime(self.date, "%Y-%m-%d").date()
        except ValueError:
            return f'Invalid date format: {self.date}. Please use YYYY-MM-DD.', None

        competition = Competition.query.filter_by(name=self.name).first()
        if competition:
            return f'Competition with the name "{self.name}" already exists.', None
        
        competition = Competition(
            name = self.name,
            description= self.description,
            date= date,
            participants_amount= self.participants_amount,
            duration = self.duration
        )
        
        db.session.add(competition)
        db.session.commit()
        
        return competition
    
    
class UpdateCompetitionCommand(Command):
    def __init__(self, competition_id, new_name, new_date):
        self.competition_id = competition_id
        self.new_name = new_name
        self.new_date = new_date

    def execute(self):
        competition = Competition.query.get(self.competition_id)
        if not competition:
            return f'Competition with ID {self.competition_id} not found!', None

        competition.name = self.new_name
        try:
            competition.date = datetime.strptime(self.new_date, "%Y-%m-%d").date()
        except ValueError:
            return f'Invalid date format: {self.new_date}. Please use YYYY-MM-DD.', None

        db.session.commit()
        return None, competition