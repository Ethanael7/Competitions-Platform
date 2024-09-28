
from models import Competition, Result, Participant
from App.database import db

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
    competition = Competition.query.filter_by(name=name).first()
    db.session.add(competition)
    db.session.commit()
    return competition

def get_competition():
    return Competition.query.all()

def get_competition_results(competition_id):
    competition = Competition.query.get(competition_id)
    if competition:
        return Result.query.filter_by(competition_id=competition_id).all()
    else:
        return None
    
def import_results(file_path, competition_id):
    competition = Competition.query.get(competition_id)
    if not competition:
        raise Exception("Competition {competition_id} not found")
    
    import csv
    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        
        # Reading each row from the CSV
        for row in reader:
            # Assume the CSV columns are 'name', 'date', 'participants'
            participant_name = row['name']
            participant = create_participant(row['participant_name'])
            result = Result(competition_id=competition_id, participant_id=participant.id, score=row['score'])
            db.session.add(result)
        db.session.commit()
   
        
        
        

    