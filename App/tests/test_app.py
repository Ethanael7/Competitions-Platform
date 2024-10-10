import os, tempfile, pytest, logging, unittest
from werkzeug.security import check_password_hash, generate_password_hash

from App.main import create_app
from App.database import db, create_db
from datetime import datetime
from App.models import User, Competition, Result
from App.controllers import (
    create_user,
    get_all_users_json,
    login,
    get_user,
    get_user_by_username,
    update_user,
    create_competition,   
    get_competition,
    get_results,
    import_competitions,
    import_results,
    update_competition,
    delete_competition,
)


LOGGER = logging.getLogger(__name__)

'''
   Unit Tests
'''
class UserUnitTests(unittest.TestCase):

    def test_new_user(self):
        user = User("bob", "bobpass")
        assert user.username == "bob"

    # pure function no side effects or integrations called
    def test_get_json(self):
        user = User("bob", "bobpass")
        user_json = user.get_json()
        self.assertDictEqual(user_json, {"id":None, "username":"bob"})
    
    def test_hashed_password(self):
        password = "mypass"
        hashed = generate_password_hash(password, method='pbkdf2:sha256')
        user = User("bob", hashed)
        assert user.password != password
        assert check_password_hash(user.password, password)

    def test_check_password(self):
        password = "mypass"
        user = User("bob", password)
        assert user.check_password(password)

'''
    Integration Tests
'''

# This fixture creates an empty database for the test and deletes it after the test
# scope="class" would execute the fixture once and resued for all methods in the class
@pytest.fixture(autouse=True, scope="module")
def empty_db():
    app = create_app({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///test.db'})
    create_db()
    yield app.test_client()
    db.drop_all()


def test_authenticate():
    user = create_user("bob", "bobpass")
    assert login("bob", "bobpass") != None

class UsersIntegrationTests(unittest.TestCase):

    def test_create_user(self):
        user = create_user("rick", "bobpass")
        assert user.username == "rick"

    def test_get_all_users_json(self):
        users_json = get_all_users_json()
        self.assertListEqual([{"id":1, "username":"bob"}, {"id":2, "username":"rick"}], users_json)

    # Tests data changes in the database
    def test_update_user(self):
        update_user(1, "ronnie")
        user = get_user(1)
        assert user.username == "ronnie"
        



@pytest.fixture
def add_sample_competition(test_client):
    competition = Competition(name='Sample Competition', date=datetime.strptime('2024-10-10', '%Y-%m-%d').date())
    db.session.add(competition)
    db.session.commit()
    return competition

def test_create_competition(test_client):
    name = 'New Competition'
    date = '2024-12-15'
    competition = create_competition(name, date)
    assert competition.name == name
    assert competition.date == datetime.strptime(date, '%Y-%m-%d').date()

def test_get_competition(test_client, add_sample_competition):
    competitions = Competition.query.all()
    assert len(competitions) == 1
    assert competitions[0].name == add_sample_competition.name

def test_update_competition(test_client, add_sample_competition):
    new_name = 'Updated Competition Name'
    new_date = '2024-12-15'
    error_message, updated_comp = update_competition(add_sample_competition.id, new_name, new_date)
    
    assert error_message is None
    assert updated_comp.name == new_name
    assert updated_comp.date == datetime.strptime(new_date, '%Y-%m-%d').date()

def test_delete_competition(test_client, add_sample_competition):
    error_message, response = delete_competition(add_sample_competition.id)
    
    assert error_message is None
    assert response == f'Competition with ID {add_sample_competition.id} deleted.'
    
    # Check that the competition is indeed deleted
    deleted_comp = Competition.query.get(add_sample_competition.id)
    assert deleted_comp is None

def test_import_competitions(test_client, tmp_path):
    competition_data = """name,date
    Sample Competition 1,2024-10-01
    Sample Competition 2,2024-10-02
    """
    import_file = tmp_path / "competitions.csv"
    import_file.write_text(competition_data)

    import_competitions(str(import_file))

    competitions = Competition.query.all()
    assert len(competitions) == 2  # Two competitions should have been imported
    assert competitions[0].name == 'Sample Competition 1'
    assert competitions[1].name == 'Sample Competition 2'

def test_import_results(test_client, tmp_path, add_sample_competition):
    # Create a user for results
    user = User(username='Alice')
    db.session.add(user)
    db.session.commit()

    results_data = f"""participant_name,score,competition_id
    Alice,85,{add_sample_competition.id}
    """
    import_file = tmp_path / "results.csv"
    import_file.write_text(results_data)

    import_results(str(import_file))

    # Check if the result was imported correctly
    results = Result.query.filter_by(competition_id=add_sample_competition.id).all()
    assert len(results) == 1
    assert results[0].score == 85
    assert results[0].user_id == user.id

def test_get_results(test_client, add_sample_competition):
    # Create a user and a result for that competition
    user = User(username='Alice')
    db.session.add(user)
    db.session.commit()
    
    result = Result(user_id=user.id, competition_id=add_sample_competition.id, score=90)
    db.session.add(result)
    db.session.commit()
    
    error_message, participant_scores = get_results(add_sample_competition.id)

    assert error_message is None
    assert len(participant_scores) == 1
    assert participant_scores[0] == (user.username, result.score)
        

