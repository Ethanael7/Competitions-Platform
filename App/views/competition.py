from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
from App.controllers import(get_competition, update_competition, delete_competition, create_competition, import_competitions, import_results, get_results)
from flask_jwt_extended import jwt_required, current_user as jwt_current_user
from App.models import Competition, Result
from werkzeug.utils import secure_filename
from App.database import db
from datetime import datetime


from.index import index_views

competition_views = Blueprint('competition_views', __name__, template_folder='../templates')


@competition_views.route('/api/competitions', methods=['GET'])
def get_competitions():
    competitions = Competition.query.all()
    return jsonify([{
        'id': competition.id,
        'name': competition.name,
        'date': competition.date.isoformat()  # Ensure dates are in ISO format
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
    
    # Validate required fields
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
