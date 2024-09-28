
from App.models import Competition, Result, Participant
from App.database import db
from datetime import datetime

def create_participant(name):
    participant = Participant.query.filter_by(name=name).first()
    if participant:
        return participant
    else:
        new_participant = Participant(name=name)
        db.session.add(new_participant)
        db.session.commit()
        return new_participant
    
def create_competition(name, date):
    
    date = datetime.strptime(date, "%Y-%m-%d").date()
    comp = Competition.query.filter_by(name=name).first()
    if not comp:  
        comp = Competition(name=name, date=date)
        db.session.add(comp)
        db.session.commit()
    return comp

def get_competition():
    return Competition.query.all()

def get_competition_results(competition_id):
    comp = Competition.query.get(competition_id)
    if comp:
        return Result.query.filter_by(competition_id=competition_id).all()
    else:
        return None
    
def import_results(file_path, competition_id):
    comp = Competition.query.get(competition_id)
    if not comp:
        raise Exception(f"Competition {competition_id} not found")  # Corrected to use an f-string
    
    import csv
    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        
        # Reading each row from the CSV
        for row in reader:
            # Assume the CSV columns are 'name', 'score'
            participant_name = row['name']
            participant = create_participant(participant_name)
            result = Result(competition_id=competition_id, participant_id=participant.id, score=row['score'])
            db.session.add(result)
        db.session.commit()
   
        
        
        

    