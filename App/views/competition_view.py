from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
from App.controllers import get_competition, update_competition, delete_competition, create_competition, import_competitions, import_results, get_results
from App.models import Competition
from App.database import db

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
    
    
@competition_views.route('/api/competitions', methods=['POST'])
def create_competition():
    data = request.get_json()
    new_competition = Competition(name=data['name'], date=data.get('date'))
    db.session.add(new_competition)
    db.session.commit()
    return jsonify({'message': 'Competition created'}), 201

# PUT update a competition
@competition_views.route('/api/competitions/<int:competition_id>', methods=['PUT'])
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
