import click, pytest, sys
from datetime import datetime
from flask import Flask
from flask.cli import with_appcontext, AppGroup

from App.database import db, get_migrate
from App.models import User
from App.models import Competition
from App.main import create_app
from App.controllers import ( create_user, get_all_users_json, get_all_users, initialize )
from App.controllers import competitioncontroller 

# This commands file allow you to create convenient CLI commands for testing controllers

app = create_app()
migrate = get_migrate(app)

# This command creates and initializes the database
@app.cli.command("init", help="Creates and initializes the database")
def init():
    initialize()
    print('database intialized')

'''
User Commands
'''

@app.cli.command("create-competition", help = "creates a competition")
@click.argument('name', default ='Javalin')
@click.argument('date',default=str(datetime.now().date()))
def create_competition(name,date):
    existing_competition = Competition.query.filter_by(name=name).first()
    
    if existing_competition:
        print(f'Competition "{name} already exists!')
        return
    
    new_competition = Competition(name=name,date=date)
    
    db.session.add(new_competition)
    db.session.commit()
    
    print(f'Competition "{name}" created successfully!')

@app.cli.command("import_results", help="Import Competition Results")
@click.argument('file_path')
def import_results(file_path):
    try:
        with open(file_path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            
            # Reading each row from the CSV
            for row in reader:
                # Assume the CSV columns are 'name', 'date', 'participants'
                competition_name = row['name']
                competition_date = row['date']
                participants = row['participants'].split(',')  # Participants are comma-separated
                
                # Fetch existing competition or create a new one
                competition = Competition.query.filter_by(name=competition_name).first()
                if not competition:
                    competition = Competition(name=competition_name, date=competition_date)
                    db.session.add(competition)
                    db.session.commit()
                
                # Add participants to competition, assuming 'participants' refer to users
                for participant_name in participants:
                    participant = User.query.filter_by(username=participant_name).first()
                    if participant and participant not in competition.participants:
                        competition.participants.append(participant)

            # Commit all changes after importing
            db.session.commit()
            print(f"Results imported successfully from {file_path}.")

    # Handle file not found error
    except FileNotFoundError:
        print(f"File {file_path} not found.")
    
    # Catch and print any other errors
    except Exception as e:
        print(f"An error occurred: {e}")

    
    
@app.cli.command("view-competitions", help = "lists the competitions")
def view_competitions():
    competitions = competitioncontroller.view_competitions()
    for competition in competitions:
        print(f"Name: {competition['name']}Date: {competition['date']}, Participants: {', '.join(competition['participants'])}")

# Commands can be organized using groups

# create a group, it would be the first argument of the comand
# eg : flask user <command>
user_cli = AppGroup('user', help='User object commands') 

# Then define the command and any parameters and annotate it with the group (@)
@user_cli.command("create", help="Creates a user")
@click.argument("username", default="rob")
@click.argument("password", default="robpass")
def create_user_command(username, password):
    create_user(username, password)
    print(f'{username} created!')

# this command will be : flask user create bob bobpass

@user_cli.command("list", help="Lists users in the database")
@click.argument("format", default="string")
def list_user_command(format):
    if format == 'string':
        print(get_all_users())
    else:
        print(get_all_users_json())

app.cli.add_command(user_cli) # add the group to the cli



'''
Test Commands
'''

test = AppGroup('test', help='Testing commands') 

@test.command("user", help="Run User tests")
@click.argument("type", default="all")
def user_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "UserUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "UserIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "App"]))
    

app.cli.add_command(test)