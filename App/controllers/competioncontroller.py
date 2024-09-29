
from App.models import Competition, Result, User, Participant
from App.database import db
from datetime import datetime
import csv
    
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

# controllers/competition_controller.py

def get_results(competition_id):
    competition = Competition.query.get(competition_id)
    if not competition:
        return f"No competition found with ID '{competition_id}'.", None
    
    results = Result.query.filter_by(competition_id=competition.id).all()
    
    if not results:
        return f"No results found for competition ID '{competition_id}'.", None
    
    participants_scores = []
    for result in results:
        participant = User.query.get(result.user_id)
        if participant:
            participants_scores.append((participant.username, result.score))
    
    return None, participants_scores


def import_competitions(competition_file):
    try:
        # Import competitions
        with open(competition_file, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                competition_name = row['name']
                competition_date_str = row['date']  # Date as string from CSV
                try:
                    # Convert the string to a datetime object
                    competition_date = datetime.strptime(competition_date_str, '%Y-%m-%d').date()
                except ValueError:
                    print(f"Error parsing date {competition_date_str} for competition {competition_name}")
                    continue
                
                # Create or fetch the competition
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

def import_results(results_file):
    try:
        # Import results
        with open(results_file, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                participant_name = row['participant_name']
                score = row['score']
                competition_id = row['competition_id']
                
                competition = Competition.query.get(competition_id)
                if not competition:
                    print(f"Competition with ID {competition_id} not found!")
                    continue
                
                participant = User.query.filter_by(username=participant_name).first()  # Assuming User model exists
                if participant:
                    result = Result(user_id=participant.id, competition_id=competition.id, score=score)
                    db.session.add(result)
                    db.session.commit()
                    
        print("Results imported successfully.")

    except FileNotFoundError as e:
        print(f"File not found: {e.filename}")
    except Exception as e:
        print(f"An error occurred: {e}")

  
        

    
   
        
        
        

    