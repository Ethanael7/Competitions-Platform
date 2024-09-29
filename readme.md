[![Open in Gitpod](https://gitpod.io/button/open-in-gitpod.svg)](https://gitpod.io/#https://github.com/uwidcit/flaskmvc)
<a href="https://render.com/deploy?repo=https://github.com/uwidcit/flaskmvc">
  <img src="https://render.com/images/deploy-to-render-button.svg" alt="Deploy to Render">
</a>

![Tests](https://github.com/uwidcit/flaskmvc/actions/workflows/dev.yml/badge.svg)

# Flask MVC Template
A template for flask applications structured in the Model View Controller pattern [Demo](https://dcit-flaskmvc.herokuapp.com/). [Postman Collection](https://documenter.getpostman.com/view/583570/2s83zcTnEJ)


# Dependencies
* Python3/pip3
* Packages listed in requirements.txt

# Installing Dependencies
```bash
$ pip install -r requirements.txt
```

# Configuration Management


Configuration information such as the database url/port, credentials, API keys etc are to be supplied to the application. However, it is bad practice to stage production information in publicly visible repositories.
Instead, all config is provided by a config file or via [environment variables](https://linuxize.com/post/how-to-set-and-list-environment-variables-in-linux/).

## In Development

When running the project in a development environment (such as gitpod) the app is configured via default_config.py file in the App folder. By default, the config for development uses a sqlite database.

default_config.py
```python
SQLALCHEMY_DATABASE_URI = "sqlite:///temp-database.db"
SECRET_KEY = "secret key"
JWT_ACCESS_TOKEN_EXPIRES = 7
ENV = "DEVELOPMENT"
```

These values would be imported and added to the app in load_config() function in config.py

config.py
```python
# must be updated to inlude addtional secrets/ api keys & use a gitignored custom-config file instad
def load_config():
    config = {'ENV': os.environ.get('ENV', 'DEVELOPMENT')}
    delta = 7
    if config['ENV'] == "DEVELOPMENT":
        from .default_config import JWT_ACCESS_TOKEN_EXPIRES, SQLALCHEMY_DATABASE_URI, SECRET_KEY
        config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
        config['SECRET_KEY'] = SECRET_KEY
        delta = JWT_ACCESS_TOKEN_EXPIRES
...
```

## In Production

When deploying your application to production/staging you must pass
in configuration information via environment tab of your render project's dashboard.

![perms](./images/fig1.png)

# Flask Commands

wsgi.py is a utility script for performing various tasks related to the project. You can use it to import and test any code in the project. 
You just need create a manager command function, for example:

```python
# inside wsgi.py
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


user_cli = AppGroup('user', help='User object commands')

@user_cli.cli.command("create-user")
@click.argument("username")
@click.argument("password")
def create_user_command(username, password):
    create_user(username, password)
    print(f'{username} created!')

app.cli.add_command(user_cli) # add the group to the cli

```

Then execute the command invoking with flask cli with command name and the relevant parameters

```bash
$ flask user create bob bobpass
$ flask create-competition "Competition name"
$ flask view-competitions
$ flask import-competitions competition.csv
$ flask import-results results.csv
$ flask view-results 
$ flask update-competition id name date 
$ flask delete-competition id
```


# Running the Project

_For development run the serve command (what you execute):_
```bash
$ flask run
```

_For production using gunicorn (what heroku executes):_
```bash
$ gunicorn wsgi:app
```

# Deploying
You can deploy your version of this app to heroku by clicking on the "Deploy to heroku" link above.

# Initializing the Database
When connecting the project to a fresh empty database ensure the appropriate configuration is set then file then run the following command. This must also be executed once when running the app on heroku by opening the heroku console, executing bash and running the command in the dyno.

```bash
$ flask init
```

# Database Migrations
If changes to the models are made, the database must be'migrated' so that it can be synced with the new models.
Then execute following commands using manage.py. More info [here](https://flask-migrate.readthedocs.io/en/latest/)

```bash
$ flask db init
$ flask db migrate
$ flask db upgrade
$ flask db --help
```

# Testing

## Unit & Integration
Unit and Integration tests are created in the App/test. You can then create commands to run them. Look at the unit test command in wsgi.py for example

```python
@test.command("user", help="Run User tests")
@click.argument("type", default="all")
def user_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "UserUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "UserIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "User"]))
```

You can then execute all user tests as follows

```bash
$ flask test user
```

You can also supply "unit" or "int" at the end of the comand to execute only unit or integration tests.

You can run all application tests with the following command

```bash
$ pytest
```

## Test Coverage

You can generate a report on your test coverage via the following command

```bash
$ coverage report
```

You can also generate a detailed html report in a directory named htmlcov with the following comand

```bash
$ coverage html
```

# Troubleshooting

## Views 404ing

If your newly created views are returning 404 ensure that they are added to the list in main.py.

```python
from App.views import (
    user_views,
    index_views
)

# New views must be imported and added to this list
views = [
    user_views,
    index_views
]
```

## Cannot Update Workflow file

If you are running into errors in gitpod when updateding your github actions file, ensure your [github permissions](https://gitpod.io/integrations) in gitpod has workflow enabled ![perms](./images/gitperms.png)

## Database Issues

If you are adding models you may need to migrate the database with the commands given in the previous database migration section. Alternateively you can delete you database file.
