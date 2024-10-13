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
        user = User("bob", password)
        hashed = user.password
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
        
        
class CompetitionIntegrationTests(unittest.TestCase):
    
    def test_create_competition(self):
        competition = create_competition("Hackattack","2024-12-12")
        assert competition.name == "Hackattack"
        assert competition.date.date() == datetime.strptime("2024-12-12", "%Y-%m-%d").date()
        assert competition.id is not None
        retrieved_competition = Competition.query.filter_by(name="Hackattack").first()
        assert retrieved_competition is not None
        assert retrieved_competition.id == competition.id
        
    # def test_update_competition(self):
    
    #     competition = create_competition("Hackattack", "2024-12-12")
    #     updated_competition = update_competition(competition.id, new_name="Hackathon", new_date="2024-12-15")
    #     assert updated_competition.name == "Hackathon"
    #     assert updated_competition.date.date() == datetime.strptime("2024-12-15", "%Y-%m-%d").date()
    #     retrieved_competition = Competition.query.get(competition.id)
    #     assert retrieved_competition.name == "Hackathon"
    #     assert retrieved_competition.date == datetime.strptime("2024-12-15", "%Y-%m-%d").date()

    def test_delete_competition(self):
        competition = create_competition("Hackattack", "2024-12-12")
        delete_competition(competition.id)
        deleted_competition = Competition.query.get(competition.id)
        assert deleted_competition is None
        
    # def test_get_results(self):
    #     competition = create_competition("Hackattack", "2024-12-12")
    #     results = get_results(competition.id)

    #     expected_results = [{"participant": "Alice", "score": 100}, {"participant": "Bob", "score": 90}]
    #     assert results == expected_results
        
        
    # def test_import_competitions(self):
    #     # Assume there's a method to import competitions from a file or data source
    #     import_competitions("path/to/competitions_file.json")
        
    #     # Check if the competitions have been added to the database
    #     competitions = Competition.query.all()
    #     assert len(competitions) > 0  # Validate that competitions were imported

    


