import click, pytest, sys, csv
from datetime import datetime
from flask import Flask
from flask.cli import with_appcontext, AppGroup

from App.database import db, get_migrate
from App.models import User, competition, Result, Participant
from App.main import create_app
from App.controllers import (
    create_user, 
    get_all_users_json, 
    get_all_users, 
    initialize, 
    create_competition,   
    get_competition,
    get_results,
    import_competitions,
    import_results,
    update_competition,
    delete_competition,
   
)

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

#Competition Commands
competition_cli = AppGroup('competition', help='Competition commands')

@app.cli.command("create-competition", help = 'Creates a Competition')
@click.argument('name')
@click.argument('date')
def create_competition_cli(name, date):
    competition = create_competition(name, date)
    click.echo(f'Competition created: {competition}')
     
@app.cli.command("update-competition")
@click.argument('competition_id')
@click.argument('new_name')
@click.argument('new_date')
def update_competition_cli(competition_id, new_name, new_date):
    competition = update_competition(competition_id, new_name, new_date)
    if competition is None:
        click.echo(f'Failed to Update')
    else:
        print(f'Competition updated successfully: {competition}')

@app.cli.command("delete-competition")
@click.argument('competition_id')
def delete_competition_cli(competition_id):
    success = delete_competition(competition_id)
    if not success:
        click.echo(f'Failed to delete competition with ID {competition_id}. Please ensure the competition exists.')
    else:
        print(f'Competition with ID {competition_id} deleted successfully.')


@app.cli.command("view-competitions", help = "View competitions")
def view_competitions_cli():
    competitions = get_competition()
    if competitions:
        for competition in competitions:
            click.echo(f"ID: {competition.id}, Name: {competition.name}, Date: {competition.date}")
    else:
        click.echo("No competitions found")
  
    
@app.cli.command("import-competitions", help="Import competitions CSV file")
@click.argument('competition_file', default='competitions.csv')
def import_competitions_cli(competition_file):
    import_competitions(competition_file)
        
@app.cli.command("import-results", help="Import results CSV file")
@click.argument('results_file', default='results.csv')
def import_results_cli(results_file):
    import_results(results_file)
    
    
    
#Print results function in wsgi cause of errors
@app.cli.command("view-results", help="Print results from the results CSV file with competition names")
@click.argument('results-file', default='results.csv')
@click.argument('competitions-file', default='competitions.csv')
def print_results(results_file, competitions_file):
    try:
        competition_mapping = {}
        with open(competitions_file, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                competition_id = row['id']
                competition_name = row['name']
                competition_mapping[competition_id] = competition_name
                
        with open(results_file, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            click.echo("Participant Name, Score, Competition Name")
            click.echo("-" * 40)
            for row in reader:
                participant_name = row['participant_name']
                score = row['score']
                competition_id = row['competition_id']
                
                competition_name = competition_mapping.get(competition_id, "Unknown Competition")
                click.echo(f'{participant_name}, {score}, {competition_name}')
   
    except FileNotFoundError as e:
        click.echo(f"File not found: {e.filename}")
    except Exception as e:
        click.echo(f"An error occurred: {e}")


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