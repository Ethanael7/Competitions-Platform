from abc import ABC, abstractmethod
from App.models import User, Competition,Result
from App.database import db
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
    
    
class DeleteCompetitionCommand(Command):
    def __init__(self, competition_id):
        self.competition_id = competition_id

    def execute(self):
        competition = Competition.query.get(self.competition_id)
        if not competition:
            return f'Competition with ID {self.competition_id} not found!', None

        db.session.delete(competition)
        db.session.commit()
        return None, f'Competition with ID {self.competition_id} deleted.'


class GetCompetitionDetailsCommand(Command):
    def __init__(self, competition_id):
        self.competition_id = competition_id

    def execute(self):
        competition = Competition.query.get(self.competition_id)
        if not competition:
            return f"No competition found with ID '{self.competition_id}'.", None
        return None, competition


class ImportCompetitionsCommand(Command):
    def __init__(self, competition_file):
        self.competition_file = competition_file

    def execute(self):
        try:
            with open(self.competition_file, newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    competition_name = row['name']
                    competition_date_str = row['date']
                    try:
                        competition_date = datetime.strptime(competition_date_str, '%Y-%m-%d').date()
                    except ValueError:
                        print(f"Error parsing date {competition_date_str} for competition {competition_name}")
                        continue
                    
                    competition = Competition.query.filter_by(name=competition_name).first()
                    if not competition:
                        competition = Competition(name=competition_name, date=competition_date)
                        db.session.add(competition)
                        db.session.commit()
                        
            print("Competitions imported successfully.")
        except FileNotFoundError as e:
            print(f"File not found: {e.filename}")
        except Exception as e:
            print(f"An error occurred: {e}")


class ImportResultsCommand(Command):
    def __init__(self, results_file):
        self.results_file = results_file

    def execute(self):
        try:
            with open(self.results_file, newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    participant_name = row['participant_name']
                    score = row['score']
                    competition_id = row['competition_id']
                    
                    competition = Competition.query.get(competition_id)
                    if not competition:
                        print(f"Competition with ID {competition_id} not found!")
                        continue
                    
                    participant = User.query.filter_by(username=participant_name).first()
                    if participant:
                        result = Result(user_id=participant.id, competition_id=competition.id, score=score)
                        db.session.add(result)
                        db.session.commit()
                        
            print("Results imported successfully.")
        except FileNotFoundError as e:
            print(f"File not found: {e.filename}")
        except Exception as e:
            print(f"An error occurred: {e}")