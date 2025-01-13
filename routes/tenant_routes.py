from flask import Blueprint, request, jsonify, current_app
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
    
    # Get filter parameters
    max_price = request.args.get('max_price', type=float)
    min_size = request.args.get('min_size', type=float)
    location = request.args.get('location', '')
    amenities = json.loads(request.args.get('amenities', '[]'))
    
    # Get score filter parameters
    min_safety_score = request.args.get('min_safety_score', type=float, default=1)
    max_noise_level = request.args.get('max_noise_level', type=float, default=10)
    min_accessibility_score = request.args.get('min_accessibility_score', type=float, default=1)
    min_cleanliness_score = request.args.get('min_cleanliness_score', type=float, default=1)
    
    current_app.logger.info(f"Filter parameters received: max_price={max_price}, min_size={min_size}, location='{location}', amenities={amenities}")
    current_app.logger.info(f"Score filters: safety>={min_safety_score}, noise<={max_noise_level}, accessibility>={min_accessibility_score}, cleanliness>={min_cleanliness_score}")
    
    # Get tenant preferences for TOPSIS weights
    preference = TenantPreference.query.filter_by(tenant_id=current_user_id).first()
    if not preference:
        return jsonify({'error': 'Please set your preferences first'}), 400
    
    current_app.logger.info(f"Tenant preferences: max_price={preference.max_price}, min_size={preference.min_size}, location='{preference.preferred_location}', amenities={preference.required_amenities}")
    
    # Filter rooms based on basic criteria
    query = Room.query.filter_by(availability=True)
    
    # Apply basic filters if provided
    if max_price:
        query = query.filter(Room.price <= max_price)
        current_app.logger.debug(f"Filtering by max price: {max_price}")
    elif preference.max_price:
        query = query.filter(Room.price <= preference.max_price)
        current_app.logger.debug(f"Filtering by preference max price: {preference.max_price}")
        
    if min_size:
        query = query.filter(Room.size >= min_size)
        current_app.logger.debug(f"Filtering by min size: {min_size}")
    elif preference.min_size:
        query = query.filter(Room.size >= preference.min_size)
        current_app.logger.debug(f"Filtering by preference min size: {preference.min_size}")
        
    if location:
        query = query.filter(Room.location.ilike(f'%{location}%'))
        current_app.logger.debug(f"Filtering by location: '{location}'")
    elif preference.preferred_location:
        query = query.filter(Room.location.ilike(f'%{preference.preferred_location}%'))
        current_app.logger.debug(f"Filtering by preference location: '{preference.preferred_location}'")
    
    # Apply score filters
    query = query.filter(Room.safety_score >= min_safety_score)
    query = query.filter(Room.noise_level <= max_noise_level)
    query = query.filter(Room.accessibility_score >= min_accessibility_score)
    query = query.filter(Room.cleanliness_score >= min_cleanliness_score)
    
    # Get initial results
    rooms = query.all()
    current_app.logger.info(f"After basic filtering: {len(rooms)} rooms found")
    
    if not rooms:
        return jsonify({'message': 'No rooms found matching your basic criteria (price, size, location, scores)'})
    
    # Filter by amenities if provided
    if amenities:
        current_app.logger.debug(f"Filtering by provided amenities: {amenities}")
        filtered_rooms = []
        for room in rooms:
            room_amenities = json.loads(room.amenities)
            current_app.logger.debug(f"Room {room.id} amenities: {room_amenities}")
            if all(amenity in room_amenities for amenity in amenities):
                filtered_rooms.append(room)
        rooms = filtered_rooms
        current_app.logger.info(f"After amenities filtering: {len(rooms)} rooms remaining")
    elif preference.required_amenities:
        required_amenities = json.loads(preference.required_amenities)
        current_app.logger.debug(f"Filtering by preference amenities: {required_amenities}")
        filtered_rooms = []
        for room in rooms:
            room_amenities = json.loads(room.amenities)
            current_app.logger.debug(f"Room {room.id} amenities: {room_amenities}")
            if all(amenity in room_amenities for amenity in required_amenities):
                filtered_rooms.append(room)
        rooms = filtered_rooms
        current_app.logger.info(f"After preference amenities filtering: {len(rooms)} rooms remaining")
    
    if not rooms:
        return jsonify({'message': 'No rooms found matching your criteria'})
    
    # Prepare data for TOPSIS
    current_app.logger.info("Preparing decision matrix...")
    
    # Convert room scores to float arrays, handling None values
    decision_matrix = []
    for room in rooms:
        safety = 5.0 if room.safety_score is None else float(room.safety_score)
        cleanliness = 5.0 if room.cleanliness_score is None else float(room.cleanliness_score)
        accessibility = 5.0 if room.accessibility_score is None else float(room.accessibility_score)
        noise = 5.0 if room.noise_level is None else float(room.noise_level)
        # Invert noise level (10 - noise) so higher is better
        decision_matrix.append([safety, cleanliness, accessibility, 10.0 - noise])
    
    # Convert to numpy array after all values are properly formatted
    decision_matrix = np.array(decision_matrix, dtype=float)
    
    current_app.logger.debug(f"Decision matrix shape: {decision_matrix.shape}")
    current_app.logger.debug(f"Decision matrix:\n{decision_matrix}")
    
    # Normalize the decision matrix using min-max normalization
    min_vals = np.min(decision_matrix, axis=0)
    max_vals = np.max(decision_matrix, axis=0)
    current_app.logger.debug(f"Min values: {min_vals}")
    current_app.logger.debug(f"Max values: {max_vals}")
    
    # Handle normalization with special cases
    ranges = max_vals - min_vals
    normalized_matrix = np.zeros_like(decision_matrix)
    for j in range(decision_matrix.shape[1]):
        if ranges[j] == 0:
            if len(rooms) == 1:
                # For a single room, give full score if it meets minimum criteria
                normalized_matrix[:, j] = 1.0
            else:
                # For multiple rooms with same value, give relative score based on criteria
                criterion_value = decision_matrix[0, j]
                if j == 3:  # Noise level (inverted)
                    normalized_matrix[:, j] = 1.0 if criterion_value >= 5.0 else criterion_value / 10.0
                else:  # Other criteria
                    normalized_matrix[:, j] = 1.0 if criterion_value >= 5.0 else criterion_value / 10.0
        else:
            normalized_matrix[:, j] = (decision_matrix[:, j] - min_vals[j]) / ranges[j]
    
    current_app.logger.debug(f"Normalized matrix:\n{normalized_matrix}")
    
    # Add small epsilon to prevent division by zero in TOPSIS
    normalized_matrix = np.clip(normalized_matrix, 0.001, 1.0)
    
    # Get weights from tenant preferences and ensure they sum to 1
    weights = np.array([
        float(preference.safety_weight),
        float(preference.cleanliness_weight),
        float(preference.accessibility_weight),
        float(preference.noise_level_weight)
    ])
    weights = weights / np.sum(weights)  # Normalize weights to sum to 1
    
    # Ensure weights are not zero to prevent division issues
    weights = np.clip(weights, 0.001, 1.0)
    weights = weights / np.sum(weights)  # Renormalize after clipping
    
    current_app.logger.debug(f"Normalized weights: {weights}")
    
    # All criteria are beneficial (1 for beneficial)
    impacts = np.array([1, 1, 1, 1])
    
    # Calculate TOPSIS scores
    try:
        # Log input data
        current_app.logger.info(f"Number of rooms for TOPSIS: {len(rooms)}")
        current_app.logger.info(f"Decision matrix:\n{decision_matrix}")
        current_app.logger.info(f"Weights: {weights}")
        current_app.logger.info(f"Impacts: {impacts}")
        
        # Validate input data
        if len(rooms) == 0:
            return jsonify({'message': 'No rooms to rank'}), 200
            
        if decision_matrix.size == 0:
            current_app.logger.error("Decision matrix is empty")
            return jsonify({'error': 'Invalid decision matrix'}), 500
            
        # Ensure matrices are the correct shape
        if decision_matrix.shape[1] != len(weights):
            current_app.logger.error(f"Shape mismatch: Decision matrix shape: {decision_matrix.shape}, Weights length: {len(weights)}")
            return jsonify({'error': 'Matrix shape mismatch'}), 500
            
        # Calculate TOPSIS scores
        try:
            topsis_scores = topsis(normalized_matrix.tolist(), weights.tolist(), impacts.tolist())
            current_app.logger.info(f"TOPSIS calculation successful, raw scores: {topsis_scores}")
            
            # Handle mixed types and NaN values
            processed_scores = []
            for score in topsis_scores:
                if isinstance(score, (int, float, np.integer, np.floating)):
                    # Direct numeric value
                    processed_scores.append(float(score))
                elif isinstance(score, np.ndarray):
                    # Handle numpy array - take first non-NaN value or 0
                    score_value = score[0] if not np.isnan(score[0]) else 0.0
                    processed_scores.append(float(score_value))
                else:
                    # Unknown type - default to 0
                    processed_scores.append(0.0)
            
            current_app.logger.info(f"Processed scores: {processed_scores}")
            
            # Convert to numpy array and calculate percentages
            topsis_scores = np.array(processed_scores)
            percentage_scores = np.clip(topsis_scores * 100, 0, 100)
            current_app.logger.info(f"Percentage scores calculated: {percentage_scores}")
            
        except Exception as conversion_error:
            current_app.logger.error(f"Score conversion failed: {str(conversion_error)}")
            current_app.logger.error(f"Score type: {type(topsis_scores)}")
            current_app.logger.error(f"Score content: {topsis_scores}")
            return jsonify({'error': 'Error converting scores to percentages'}), 500
            
    except Exception as e:
        current_app.logger.error(f"Unexpected error in TOPSIS calculation: {str(e)}")
        return jsonify({'error': f'Unexpected error: {str(e)}'}), 500
    
    # For a single room, set score to 100% if it matches all criteria
    if len(rooms) == 1:
        room = rooms[0]
        if (room.safety_score >= min_safety_score and
            room.noise_level <= max_noise_level and
            room.accessibility_score >= min_accessibility_score and
            room.cleanliness_score >= min_cleanliness_score):
            percentage_scores = np.array([100.0])
            current_app.logger.info("Single room matches all criteria - setting score to 100%")
    
    ranked_rooms = sorted(zip(rooms, percentage_scores, range(1, len(rooms) + 1)), 
                         key=lambda x: x[1], reverse=True)
    
    current_app.logger.info(f"Final number of ranked rooms: {len(ranked_rooms)}")
    current_app.logger.info("Top 3 rooms scores and ranks:")
    for room, score, rank in ranked_rooms[:3]:
        current_app.logger.info(f"Room {room.id}: Match={score:.1f}%, Rank #{rank}")
    
    # Calculate percentile ranks and categorize rooms
    total_rooms = len(ranked_rooms)
    
    # Group rooms by match category
    best_matches = []
    good_matches = []
    other_matches = []
    
    for room, score, rank in ranked_rooms:
        percentile = ((total_rooms - rank + 1) / total_rooms) * 100
        match_percentage = round(score, 1)  # Round to 1 decimal place
        
        room_data = {
            'id': room.id,
            'title': room.title,
            'description': room.description,
            'price': float(room.price),
            'size': float(room.size),
            'location': room.location,
            'amenities': json.loads(room.amenities) if room.amenities else [],
            'availability': room.availability,
            'image_url': room.image_url,
            'safety_score': float(room.safety_score) if room.safety_score is not None else None,
            'cleanliness_score': float(room.cleanliness_score) if room.cleanliness_score is not None else None,
            'accessibility_score': float(room.accessibility_score) if room.accessibility_score is not None else None,
            'noise_level': float(room.noise_level) if room.noise_level is not None else None,
            'landlord': {
                'id': room.landlord.id if room.landlord else None,
                'email': room.landlord.email if room.landlord else None,
                'contact_number': room.landlord.contact_number if room.landlord else None
            },
            'topsis_score': score,
            'rank': rank,
            'percentile': int(round(percentile)),
            'match_details': {
                'safety': {
                    'score': float(room.safety_score) if room.safety_score is not None else None,
                    'weight': float(weights[0]),
                    'weighted_score': float(round(room.safety_score * float(weights[0]) * 10, 1)) if room.safety_score is not None else None
                },
                'cleanliness': {
                    'score': float(room.cleanliness_score) if room.cleanliness_score is not None else None,
                    'weight': float(weights[1]),
                    'weighted_score': float(round(room.cleanliness_score * float(weights[1]) * 10, 1)) if room.cleanliness_score is not None else None
                },
                'accessibility': {
                    'score': float(room.accessibility_score) if room.accessibility_score is not None else None,
                    'weight': float(weights[2]),
                    'weighted_score': float(round(room.accessibility_score * float(weights[2]) * 10, 1)) if room.accessibility_score is not None else None
                },
                'noise': {
                    'score': float(room.noise_level) if room.noise_level is not None else None,
                    'weight': float(weights[3]),
                    'weighted_score': float(round((10 - room.noise_level) * float(weights[3]) * 10, 1)) if room.noise_level is not None else None
                }
            }
        }
        
        # Categorize based on match percentage
        if match_percentage >= 80:  # 80% or better
            best_matches.append(room_data)
        elif match_percentage >= 60:  # 60-79%
            good_matches.append(room_data)
        else:  # Below 60%
            other_matches.append(room_data)
    
    return jsonify({
        'summary': {
            'total_rooms': total_rooms,
            'best_matches_count': len(best_matches),
            'good_matches_count': len(good_matches),
            'other_matches_count': len(other_matches),
            'categories': {
                'best_match': '80% or higher',
                'good_match': '60-79%',
                'other_match': 'Below 60%'
            }
        },
        'suggestions': {
            'best_matches': best_matches[:5],  # Limit to top 5 in each category
            'good_matches': good_matches[:5],
            'other_matches': other_matches[:5]
        },
        'all_rooms': best_matches + good_matches + other_matches  # Full list for reference
    }) 