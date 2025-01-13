from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from models import User, Room, TenantPreference
import json
import numpy as np
from topsispy import topsis
from sqlalchemy.exc import SQLAlchemyError

bp = Blueprint('tenant', __name__, url_prefix='/tenant')

@bp.route('/preferences', methods=['POST'])
@jwt_required()
def set_preferences():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if user.user_type != 'tenant':
        return jsonify({'error': 'Unauthorized'}), 403
    
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400

        # Validate required fields
        required_fields = ['max_price', 'min_size', 'preferred_location', 'required_amenities',
                         'safety_weight', 'cleanliness_weight', 'accessibility_weight', 'noise_level_weight']
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return jsonify({'error': f'Missing required fields: {", ".join(missing_fields)}'}), 400

        # Validate numeric fields
        try:
            max_price = float(data['max_price'])
            min_size = float(data['min_size'])
            if max_price <= 0 or min_size <= 0:
                return jsonify({'error': 'Price and size must be positive numbers'}), 400
        except (ValueError, TypeError):
            return jsonify({'error': 'Invalid price or size value'}), 400

        # Validate weights
        try:
            weights = [float(data['safety_weight']), float(data['cleanliness_weight']),
                      float(data['accessibility_weight']), float(data['noise_level_weight'])]
            if any(w < 0 or w > 1 for w in weights):
                return jsonify({'error': 'Weights must be between 0 and 1'}), 400
            if abs(sum(weights) - 1.0) > 0.0001:  # Allow small floating point error
                return jsonify({'error': 'Weights must sum to 1.0'}), 400
        except (ValueError, TypeError):
            return jsonify({'error': 'Invalid weight values'}), 400

        # Validate amenities
        if not isinstance(data['required_amenities'], list):
            return jsonify({'error': 'Required amenities must be a list'}), 400
        
        # Delete existing preferences if any
        TenantPreference.query.filter_by(tenant_id=current_user_id).delete()
        
        try:
            # Create new preferences
            preference = TenantPreference(
                tenant_id=current_user_id,
                max_price=max_price,
                min_size=min_size,
                preferred_location=data['preferred_location'],
                required_amenities=json.dumps(data['required_amenities']),
                safety_weight=weights[0],
                cleanliness_weight=weights[1],
                accessibility_weight=weights[2],
                noise_level_weight=weights[3]
            )
            
            db.session.add(preference)
            db.session.commit()
            
            return jsonify({'message': 'Preferences saved successfully'})
            
        except SQLAlchemyError as e:
            db.session.rollback()
            return jsonify({'error': 'Database error occurred'}), 500
            
    except Exception as e:
        return jsonify({'error': 'An unexpected error occurred'}), 500

@bp.route('/preferences', methods=['GET'])
@jwt_required()
def get_preferences():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if user.user_type != 'tenant':
        return jsonify({'error': 'Unauthorized'}), 403
    
    preference = TenantPreference.query.filter_by(tenant_id=current_user_id).first()
    if not preference:
        return jsonify(None)
    
    return jsonify({
        'max_price': preference.max_price,
        'min_size': preference.min_size,
        'preferred_location': preference.preferred_location,
        'required_amenities': json.loads(preference.required_amenities),
        'safety_weight': preference.safety_weight,
        'cleanliness_weight': preference.cleanliness_weight,
        'accessibility_weight': preference.accessibility_weight,
        'noise_level_weight': preference.noise_level_weight
    })

@bp.route('/search', methods=['GET'])
@jwt_required()
def search_rooms():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if user.user_type != 'tenant':
        return jsonify({'error': 'Unauthorized'}), 403
    
    preference = TenantPreference.query.filter_by(tenant_id=current_user_id).first()
    if not preference:
        return jsonify({'error': 'Please set your preferences first'}), 400
    
    # Filter rooms based on basic criteria
    query = Room.query.filter_by(availability=True)
    
    if preference.max_price:
        query = query.filter(Room.price <= preference.max_price)
    if preference.min_size:
        query = query.filter(Room.size >= preference.min_size)
    if preference.preferred_location:
        query = query.filter(Room.location.ilike(f'%{preference.preferred_location}%'))
    
    rooms = query.all()
    if not rooms:
        return jsonify({'message': 'No rooms found matching your criteria'})
    
    # Prepare data for TOPSIS
    decision_matrix = np.array([[
        room.safety_score,
        room.cleanliness_score,
        room.accessibility_score,
        -room.noise_level,  # Negative because lower is better
    ] for room in rooms])
    
    weights = np.array([
        preference.safety_weight,
        preference.cleanliness_weight,
        preference.accessibility_weight,
        preference.noise_level_weight
    ])
    
    # All criteria are beneficial (1 for beneficial, 0 for non-beneficial)
    impacts = np.array([1, 1, 1, 1])
    
    # Calculate TOPSIS scores
    topsis_scores = topsis(decision_matrix, weights, impacts)
    
    # Sort rooms by TOPSIS score
    ranked_rooms = sorted(zip(rooms, topsis_scores), key=lambda x: x[1], reverse=True)
    
    return jsonify([{
        'id': room.id,
        'title': room.title,
        'description': room.description,
        'price': room.price,
        'size': room.size,
        'location': room.location,
        'amenities': json.loads(room.amenities),
        'safety_score': room.safety_score,
        'cleanliness_score': room.cleanliness_score,
        'accessibility_score': room.accessibility_score,
        'noise_level': room.noise_level,
        'topsis_score': float(score)
    } for room, score in ranked_rooms]) 