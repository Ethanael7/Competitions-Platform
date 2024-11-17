from flask import Blueprint, render_template, abort, jsonify, request, send_from_directory, flash, redirect, url_for
from App.controllers import(get_competition, update_competition, delete_competition, create_competition, import_competitions, import_results, get_results)
from flask_jwt_extended import get_current_user, jwt_required, current_user as jwt_current_user
from App.controllers.commands import ViewLeaderboardCommand, ViewProfileCommand
from App.models import Competition, Result, CompetitionController
from werkzeug.utils import secure_filename
from App.database import db
from datetime import datetime
from App.controllers.commands import CreateCompetitionsCommand
from App.models.user import User, UserController


from.index import index_views

competition_views = Blueprint('competition_views', __name__, template_folder='../templates')


@competition_views.route('/api/competitions', methods=['GET'])
def get_competitions():
    competitions = Competition.query.all()
    return jsonify([{
        'id': competition.id,
        'name': competition.name,
        'date': competition.date.isoformat()  
    } for competition in competitions])

@competition_views.route('/api/competitions/<int:competition_id>', methods=['GET'])
def get_competition(competition_id):
    print(f"Fetching competition with ID: {competition_id}")  
    competition = Competition.query.get_or_404(competition_id)
    return jsonify({
        'id': competition.id,
        'name': competition.name,
        'date': competition.date.isoformat()
    })

@competition_views.route('/api/upload_results', methods=['POST'])
@jwt_required()
def upload_results_endpoint():
    if 'file' not in request.files:
        return jsonify({'message': 'No file part in the request'}), 400
    
    file = request.files['file']

    if file.filename == '':
        return jsonify({'message': 'No selected file'}), 400

    return jsonify({'message': 'Results uploaded successfully!'}), 200

@competition_views.route('/api/competitions', methods=['POST'])
@jwt_required()
def create_competition_endpoint():
    data = request.json
    
    if 'name' not in data or 'date' not in data:
        return jsonify({'message': 'Name and date are required.'}), 400
    
    competition = create_competition(data['name'], data['date'])
    
    return jsonify({'message': 'Competition created successfully!', 'id': competition.id}), 201

@competition_views.route('/api/competitions/<int:competition_id>', methods=['PUT'])
@jwt_required()
def update_competition(competition_id):
    competition = Competition.query.get_or_404(competition_id)
    data = request.get_json()
    
    if 'name' not in data or 'date' not in data:
        return jsonify({'message': 'Name and date are required.'}), 400

    
    competition.name = data['name']
    
    try:
      
        competition.date = datetime.strptime(data['date'], '%Y-%m-%d')
    except ValueError:
        return jsonify({'message': 'Date format must be YYYY-MM-DD.'}), 400
    
    db.session.commit()
    
    return jsonify({'message': 'Competition updated successfully!'}), 200

@competition_views.route('/api/competitions/<int:competition_id>', methods=['DELETE'])
@jwt_required()
def delete_competition(competition_id):
    competition = Competition.query.get_or_404(competition_id)
    db.session.delete(competition)
    db.session.commit()
    
    return jsonify({'message': 'Competition deleted'})


@competition_views.route('/api/results', methods=['GET'])
def get_all_results():
    
    results = Result.query.all()

    results_data = [{
        'participant_name': result.participant_name,
        'score': result.score,
        'competition_id': result.competition_id
    } for result in results]

    return jsonify(results_data), 200



@competition_views.route('/create_competition', methods=['POST'])
def create_competition():
   
    current_user = jwt_current_user()  
    if not current_user or not current_user.is_moderator:
        abort(403, description="You do not have permission to create a competition")


    data = request.get_json()
    name = data.get('name')
    description = data.get('description')
    date = data.get('date')
    participants_amount = data.get('participants_amount')
    duration = data.get('duration')


    command = CreateCompetitionsCommand(name, description, date, participants_amount, duration)
    
 
    controller = CompetitionController(command)
    competition = controller.execute()

    if isinstance(competition, str):  
        return jsonify({"message": competition}), 400

  
    return jsonify(competition.get_json()), 201


@competition_views.route('/view_profile/<int:id>', methods=['GET'])
def view_profile(id):
    command = ViewProfileCommand(id)
    controller = UserController(command)
    user = controller.execute()

    if user:
        return jsonify(user.get_json())
    return jsonify({"message": "User not found"}), 404


@competition_views.route('/leaderboard', methods=['GET'])
def view_leaderboard():
    command = ViewLeaderboardCommand()
    controller = UserController(command)
    leaderboard = controller.execute()

    return jsonify([user.get_json() for user in leaderboard]), 200

@competition_views.route('/add_results',methods=['POST'])
def add_results():
    user = get_current_user()
    if not user or not user.is_moderator:
        return jsonify({"message": "Permission denied"}), 403

    data = request.get_json()
    competition_id = data.get('competition_id')
    user_id = data.get('user_id')
    score = data.get('score')

    competition = Competition.query.get(competition_id)
    if not competition:
        return jsonify({"message": "Competition not found"}), 404

    result = Result(competition_id=competition_id, user_id=user_id, score=score)
    db.session.add(result)
    db.session.commit()
    return jsonify({"message": "Results added successfully!"}), 201


@competition_views.route('/leaderboard', methods=['GET'])
def leaderboard():

    results = Result.query.order_by(Result.score.desc()).all()
    leaderboard = []
    for result in results:
        user = User.query.get(result.user_id)
        competition = Competition.query.get(result.competition_id)
        leaderboard.append({
            "username": user.username,
            "competition_name": competition.name,
            "score": result.score
        })
    return jsonify({"leaderboard": leaderboard}), 200
        
