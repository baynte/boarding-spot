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
    
    try:
        # Convert room scores to float arrays, handling None values
        decision_matrix = []
        required_amenities = json.loads(preference.required_amenities) if preference.required_amenities else []
        
        # Define criteria ranges for normalization
        max_price = max(room.price for room in rooms)
        min_price = min(room.price for room in rooms)
        max_size = max(room.size for room in rooms)
        min_size = min(room.size for room in rooms)
        
        for room in rooms:
            # Normalize scores to 0-1 range and handle None values
            safety = (float(room.safety_score) if room.safety_score is not None else 5.0) / 10.0
            cleanliness = (float(room.cleanliness_score) if room.cleanliness_score is not None else 5.0) / 10.0
            accessibility = (float(room.accessibility_score) if room.accessibility_score is not None else 5.0) / 10.0
            noise = 1 - ((float(room.noise_level) if room.noise_level is not None else 5.0) / 10.0)  # Invert noise so higher is better
            
            # Normalize price and size (lower price and higher size are better)
            price_norm = 1 - ((float(room.price) - min_price) / (max_price - min_price) if max_price != min_price else 0)
            size_norm = (float(room.size) - min_size) / (max_size - min_size) if max_size != min_size else 1
            
            # Calculate amenity match score
            room_amenities = json.loads(room.amenities) if room.amenities else []
            if required_amenities:
                matched_amenities = sum(1 for amenity in required_amenities if amenity in room_amenities)
                amenity_score = matched_amenities / len(required_amenities)
            else:
                amenity_score = 1.0
            
            # Create row with normalized values
            row = [
                safety,
                cleanliness,
                accessibility,
                noise,
                amenity_score,
                price_norm,
                size_norm
            ]
            decision_matrix.append(row)
        
        # Convert to numpy array
        decision_matrix = np.array(decision_matrix, dtype=np.float64)
        
        if len(decision_matrix) == 0:
            return jsonify({'message': 'No rooms available for ranking'})
        
        # Get weights from tenant preferences and normalize
        weights = np.array([
            float(preference.safety_weight),
            float(preference.cleanliness_weight),
            float(preference.accessibility_weight),
            float(preference.noise_level_weight),
            0.25,  # amenity weight
            0.25,  # price weight
            0.25   # size weight
        ], dtype=np.float64)
        
        # Normalize weights to sum to 1
        weights = weights / np.sum(weights)
        
        # All criteria are beneficial (1 for beneficial)
        impacts = np.array([1, 1, 1, 1, 1, 1, 1], dtype=np.float64)
        
        # Calculate TOPSIS scores
        raw_scores = []
        for i in range(len(decision_matrix)):
            room_scores = topsis([decision_matrix[i].tolist()], weights.tolist(), impacts.tolist())
            # Extract the first value from the TOPSIS result tuple
            raw_scores.append(float(room_scores[0]))
        
        # Convert to numpy array and scale to percentages
        raw_scores = np.array(raw_scores, dtype=np.float64)
        percentage_scores = raw_scores * 100
        
        # Apply preference-based adjustments
        for i, (room, score) in enumerate(zip(rooms, percentage_scores)):
            # Preference match bonuses
            if room.price <= preference.max_price:
                percentage_scores[i] += 5  # 5% bonus for meeting price preference
            if room.size >= preference.min_size:
                percentage_scores[i] += 5  # 5% bonus for meeting size preference
            if preference.preferred_location.lower() in room.location.lower():
                percentage_scores[i] += 5  # 5% bonus for location match
            
            # Required amenities penalty
            if required_amenities:
                room_amenities = json.loads(room.amenities) if room.amenities else []
                missing_amenities = sum(1 for amenity in required_amenities if amenity not in room_amenities)
                if missing_amenities > 0:
                    percentage_scores[i] -= missing_amenities * 10  # 10% penalty per missing amenity
            
            # Clip scores to 0-100 range
            percentage_scores = np.clip(percentage_scores, 0, 100)
        
        # Rank rooms
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
            
            # Calculate amenity match percentage for this room
            room_amenities = json.loads(room.amenities) if room.amenities else []
            if required_amenities:
                matched_amenities = sum(1 for amenity in required_amenities if amenity in room_amenities)
                amenity_match_percentage = (matched_amenities / len(required_amenities)) * 100
            else:
                amenity_match_percentage = 100.0
            
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
                    },
                    'amenities': {
                        'score': float(amenity_match_percentage),
                        'weight': float(weights[4]),
                        'weighted_score': float(round(amenity_match_percentage * float(weights[4]) / 10, 1)),
                        'matched': [amenity for amenity in required_amenities if amenity in room_amenities],
                        'missing': [amenity for amenity in required_amenities if amenity not in room_amenities]
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
                'best_matches': sorted(best_matches, key=lambda x: x['topsis_score'], reverse=True)[:5],  # Sort and limit to top 5
                'good_matches': sorted(good_matches, key=lambda x: x['topsis_score'], reverse=True)[:5],  # Sort and limit to top 5
                'other_matches': sorted(other_matches, key=lambda x: x['topsis_score'], reverse=True)[:5]  # Sort and limit to top 5
            },
            'all_rooms': sorted(best_matches + good_matches + other_matches, key=lambda x: x['topsis_score'], reverse=True)  # Full sorted list
        })
        
    except Exception as e:
        current_app.logger.error(f"Error in TOPSIS calculation or room processing: {str(e)}")
        return jsonify({'error': 'Error in ranking calculation'}), 500 