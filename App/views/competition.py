from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
from App.controllers import(get_competition, update_competition, delete_competition, create_competition, import_competitions, import_results, get_results)
from flask_jwt_extended import jwt_required, current_user as jwt_current_user
from App.models import Competition
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
        'date': competition.date
    } for competition in competitions])


@competition_views.route('/api/competitions/<int:competition_id>', methods=['GET'])
def get_competition(competition_id):
    competition = Competition.query.get_or_404(competition_id)
    return jsonify({
        'id': competition.id,
        'name': competition.name,
        'date': competition.date
    })
    
@competition_views.route('/api/upload_results', methods=['POST'])
@jwt_required()
def upload_results_endpoint():
    if 'file' not in request.files:
        return jsonify({'message': 'No file part'}), 400
    file = request.files['file']
    # Add logic to save the file
    return jsonify({'message': 'Results uploaded successfully!'}), 200
    
    
@competition_views.route('/api/competitions', methods=['POST'])
@jwt_required()
def create_competition_endpoint():
    data = request.json
    competition = create_competition(data['name'], data['date'])
    return jsonify({'message': 'Competition created successfully!', 'id': competition.id}), 201
   

# PUT update a competition
@competition_views.route('/competitions/<int:competition_id>', methods=['PUT'])
def update_competition(competition_id):
    competition = Competition.query.get_or_404(competition_id)
    data = request.get_json()
    competition.name = data['name']
    competition.date = data.get('date', competition.date)
    db.session.commit()
    return jsonify({'message': 'Competition updated'})

# DELETE a competition
@competition_views.route('/api/competitions/<int:competition_id>', methods=['DELETE'])
def delete_competition(competition_id):
    competition = Competition.query.get_or_404(competition_id)
    db.session.delete(competition)
    db.session.commit()
    return jsonify({'message': 'Competition deleted'})
