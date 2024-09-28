import click, pytest, sys
from datetime import datetime
from flask import Flask
from flask.cli import with_appcontext, AppGroup

from App.database import db, get_migrate
from App.models import User, competition
from App.main import create_app
from App.controllers import (
    create_user, 
    get_all_users_json, 
    get_all_users, 
    initialize, 
    create_competition,   
    get_competition,
    get_competition_results,
    import_competitions_and_results
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

competition_cli = AppGroup('competition', help='Competition commands')

@app.cli.command("create-competition", help = 'Creates a Competition')
@click.argument('name')
@click.argument('date')
def create_competition_cli(name, date):
    competition = create_competition(name, date)
    click.echo(f'Competition created: {competition}')

@app.cli.command("view-competitions")
def view_competitions_cli():
    competitions = get_competition()
    if competitions:
        for competition in competitions:
            click.echo(f"ID: {competition.id}, Name: {competition.name}, Date: {competition.date}")
    else:
        click.echo("No competitions found")

@app.cli.command("view-results")
@click.argument("competition_id")
@with_appcontext
def view_results_cli(competition_id):
    results = get_competition_results(competition_id)
    if results:
        for result in results:
            click.echo(f"Participant:{result.participant.name},Score: {result.score}")
    else:
        click.echo(f"No results found for competition with ID {competition_id}")

@app.cli.command("import-competitions", help="Import competitions and results from CSV files")
@click.argument('competition-file', default='competitions.csv')
@click.argument('results_file', default='results.csv')
def import_competitions(competition_file, results_file):
    """CLI command to import competitions and results from specified CSV files."""
    try:
        import_competitions_and_results(competition_file, results_file)
        print("Data import completed successfully.")
    except Exception as e:
        print(f"An error occurred during import: {e}")
        



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