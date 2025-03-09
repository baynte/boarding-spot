from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from models import User, Room, TenantPreference
import json
import numpy as np
from topsispy import topsis
from sqlalchemy.exc import SQLAlchemyError
import math
import os
from werkzeug.utils import secure_filename

# List of high-value amenities that tenants might want even if not explicitly requested
HIGH_VALUE_AMENITIES = [
    'WiFi', 
    'Private Bathroom', 
    'Air Conditioning', 
    'Kitchen', 
    'Laundry', 
    'Water included', 
    'Electricity Included',
    'CCTV',
    'Security Guard'
]

bp = Blueprint('tenant', __name__, url_prefix='/tenant')

# Function to calculate distance between two points using Haversine formula
def calculate_distance(lat1, lon1, lat2, lon2):
    # Convert decimal degrees to radians
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    
    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    r = 6371  # Radius of earth in kilometers
    return c * r

# Helper function to check if file extension is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}

# Helper function to ensure upload folder exists
def ensure_upload_folder():
    upload_folder = os.path.join(current_app.static_folder, 'uploads', 'avatars')
    os.makedirs(upload_folder, exist_ok=True)
    return upload_folder

# Helper function to get image URL
def get_image_url(filename):
    return f"/static/uploads/avatars/{filename}"

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
        required_fields = ['max_price', 'min_capacity', 'preferred_location', 'required_amenities',
                         'safety_weight', 'cleanliness_weight', 'accessibility_weight', 'noise_level_weight']
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return jsonify({'error': f'Missing required fields: {", ".join(missing_fields)}'}), 400

        # Validate numeric fields
        try:
            max_price = float(data['max_price'])
            min_capacity = int(data['min_capacity'])
            if max_price <= 0 or min_capacity <= 0:
                return jsonify({'error': 'Price and capacity must be positive numbers'}), 400
            
            # Validate preferred_distance if provided
            preferred_distance = None
            if 'preferred_distance' in data and data['preferred_distance']:
                preferred_distance = float(data['preferred_distance'])
                if preferred_distance <= 0:
                    return jsonify({'error': 'Preferred distance must be a positive number'}), 400
        except (ValueError, TypeError):
            return jsonify({'error': 'Invalid price, capacity, or distance value'}), 400

        # Validate weights
        try:
            weights = [
                float(data['safety_weight']),
                float(data['cleanliness_weight']),
                float(data['accessibility_weight']),
                float(data['noise_level_weight'])
            ]
            if any(not isinstance(w, (int, float)) or w < 0 or w > 1 for w in weights):
                return jsonify({'error': 'Weights must be between 0 and 1'}), 400
            
            # Allow for small floating point errors in weight sum
            weight_sum = sum(weights)
            if abs(weight_sum - 1.0) > 0.0001:
                return jsonify({'error': f'Weights must sum to 1.0 (current sum: {weight_sum:.4f})'}), 400
        except (ValueError, TypeError) as e:
            return jsonify({'error': f'Invalid weight values: {str(e)}'}), 400

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
                min_capacity=min_capacity,
                preferred_location=data['preferred_location'],
                required_amenities=json.dumps(data['required_amenities']),
                living_space_type=data.get('living_space_type'),
                preferred_distance=preferred_distance if preferred_distance is not None else 5.0,
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
            current_app.logger.error(f"Database error while saving preferences: {str(e)}")
            return jsonify({'error': 'Database error occurred while saving preferences'}), 500
            
    except Exception as e:
        current_app.logger.error(f"Unexpected error in set_preferences: {str(e)}")
        return jsonify({'error': f'An unexpected error occurred: {str(e)}'}), 500

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
        'min_capacity': preference.min_capacity,
        'preferred_location': preference.preferred_location,
        'required_amenities': json.loads(preference.required_amenities),
        'living_space_type': preference.living_space_type,
        'preferred_distance': preference.preferred_distance,
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
    
    # Get request parameters directly without preference fallbacks
    max_price = request.args.get('max_price', type=float)
    min_capacity = request.args.get('min_capacity', type=int)
    location = request.args.get('location', '')
    living_space_type = request.args.get('living_space_type')
    max_distance = request.args.get('max_distance', type=float)
    
    # SMCC base point coordinates
    SMCC_LAT = 8.9882671
    SMCC_LONG = 125.3404024
    
    # Handle amenities from request
    amenities_str = request.args.get('amenities', '')
    amenities = []
    if amenities_str:
        try:
            amenities = json.loads(amenities_str)
        except json.JSONDecodeError:
            amenities = []
    
    # Get score filter parameters with sensible defaults
    min_safety_score = request.args.get('min_safety_score', type=float, default=1)
    max_noise_level = request.args.get('max_noise_level', type=float, default=10)
    min_accessibility_score = request.args.get('min_accessibility_score', type=float, default=1)
    min_cleanliness_score = request.args.get('min_cleanliness_score', type=float, default=1)

    # Log the parameters for debugging
    current_app.logger.info(f"Search parameters: max_price={max_price}, min_capacity={min_capacity}, location='{location}', amenities={amenities}, living_space_type={living_space_type}")
    current_app.logger.info(f"Score filters: safety>={min_safety_score}, noise<={max_noise_level}, accessibility>={min_accessibility_score}, cleanliness>={min_cleanliness_score}")
    
    # Start with a base query that only includes approved rooms
    query = Room.query.filter(Room.approval_status == 'approved').filter_by(availability=True)
    
    # Apply basic filters only if provided
    if max_price is not None:
        query = query.filter(Room.price <= max_price)
        current_app.logger.debug(f"Filtering by max price: {max_price}")
        
    if min_capacity is not None:
        query = query.filter(Room.capacity >= min_capacity)
        current_app.logger.debug(f"Filtering by min capacity: {min_capacity}")
        
    if location:
        query = query.filter(Room.location.ilike(f'%{location}%'))
        current_app.logger.debug(f"Filtering by location: '{location}'")

    # Apply Rental type filter if provided
    if living_space_type:
        query = query.filter(Room.living_space_type == living_space_type)
        current_app.logger.debug(f"Filtering by Rental type: {living_space_type}")

    # Apply score filters - handle NULL values in the database
    if min_safety_score > 1:  # Only apply filter if it's stricter than the minimum
        query = query.filter((Room.safety_score >= min_safety_score) | (Room.safety_score.is_(None)))
    
    if max_noise_level < 10:  # Only apply filter if it's stricter than the maximum
        query = query.filter((Room.noise_level <= max_noise_level) | (Room.noise_level.is_(None)))
    
    if min_accessibility_score > 1:  # Only apply filter if it's stricter than the minimum
        query = query.filter((Room.accessibility_score >= min_accessibility_score) | (Room.accessibility_score.is_(None)))
    
    if min_cleanliness_score > 1:  # Only apply filter if it's stricter than the minimum
        query = query.filter((Room.cleanliness_score >= min_cleanliness_score) | (Room.cleanliness_score.is_(None)))
    
    # Apply distance filter if provided
    if max_distance is not None:
        # We need to filter in Python since we need to calculate distances
        rooms = query.all()
        filtered_rooms = []
        for room in rooms:
            if room.latitude is not None and room.longitude is not None:
                distance = calculate_distance(SMCC_LAT, SMCC_LONG, room.latitude, room.longitude)
                if distance <= max_distance:
                    # Add distance as an attribute for later use
                    room.distance_from_smcc = distance
                    filtered_rooms.append(room)
            else:
                # If coordinates are not available, include the room but set distance to None
                room.distance_from_smcc = None
                filtered_rooms.append(room)
        rooms = filtered_rooms
    else:
        # Get all rooms and calculate distances
        rooms = query.all()
        for room in rooms:
            if room.latitude is not None and room.longitude is not None:
                room.distance_from_smcc = calculate_distance(SMCC_LAT, SMCC_LONG, room.latitude, room.longitude)
            else:
                room.distance_from_smcc = None
    
    # Get initial results
    current_app.logger.info(f"After basic filtering: {len(rooms)} rooms found")
    
    if not rooms:
        return jsonify({'message': 'No rooms found matching your basic criteria (price, capacity, location, scores)'})
    
    # Filter by amenities if provided
    if amenities:
        current_app.logger.debug(f"Filtering by amenities: {amenities}")
        filtered_rooms = []
        for room in rooms:
            room_amenities = json.loads(room.amenities) if room.amenities else []
            current_app.logger.debug(f"Room {room.id} amenities: {room_amenities}")
            if all(amenity in room_amenities for amenity in amenities):
                filtered_rooms.append(room)
        rooms = filtered_rooms
        current_app.logger.info(f"After amenities filtering: {len(rooms)} rooms remaining")
    
    if not rooms:
        return jsonify({'message': 'No rooms found matching your criteria'})
    
    # Prepare data for TOPSIS
    current_app.logger.info("Preparing decision matrix...")

# Start of Logic
    try:
        # Convert room scores to float arrays, handling None values
        decision_matrix = []
        
        # Define criteria ranges for normalization
        max_price_value = max(room.price for room in rooms) if rooms else 0
        min_capacity_value = min(room.capacity for room in rooms) if rooms else 0
        
        # Process each room for the decision matrix
        for room in rooms:
            # Normalize scores to 0-1 range and handle None values
            safety = (float(room.safety_score) if room.safety_score is not None else 5.0) / 10.0
            cleanliness = (float(room.cleanliness_score) if room.cleanliness_score is not None else 5.0) / 10.0
            accessibility = (float(room.accessibility_score) if room.accessibility_score is not None else 5.0) / 10.0
            noise = 1 - ((float(room.noise_level) if room.noise_level is not None else 5.0) / 10.0)  # Invert noise so higher is better
            
            # Calculate price match score based on proximity to max_price
            if max_price is not None:
                # Perfect match if price is exactly at or below max_price
                # Otherwise, score decreases as price increases above max_price
                price_score = 1.0 if room.price <= max_price else max(0, 1 - ((room.price - max_price) / max_price))
            else:
                # If no max price specified, use a relative score based on the range of prices
                price_score = 1.0 - (room.price / max_price_value) if max_price_value > 0 else 0.5
            
            # Calculate distance score (closer to SMCC is better)
            if room.distance_from_smcc is not None:
                # Convert distance to a score where closer is better
                # 0km = 1.0, 10km or more = 0.0
                max_reasonable_distance = 10.0  # km
                distance_score = max(0, 1.0 - (room.distance_from_smcc / max_reasonable_distance))
            else:
                # If distance is unknown, use a neutral score
                distance_score = 0.5
            
            # Calculate capacity match score based only on request parameters
            if min_capacity is not None:
                capacity_score = 1.0 if room.capacity >= min_capacity else 0.0
            else:
                # If no min capacity specified, use a relative score based on the range of capacities
                capacity_score = room.capacity / 10.0  # Assuming max reasonable capacity is 10
            
            # Calculate amenity match score
            room_amenities = json.loads(room.amenities) if room.amenities else []
            
            if amenities:
                matched_amenities = sum(1 for amenity in amenities if amenity in room_amenities)
                amenity_score = matched_amenities / len(amenities)
            else:
                # If no amenities specified, score based on total amenities
                amenity_score = min(1.0, len(room_amenities) / 10.0)  # Assuming 10 amenities is "complete"
            
            # Calculate location match score
            if location:
                location_score = 1.0 if location.lower() in room.location.lower() else 0.0
            else:
                location_score = 0.5  # Neutral score if no location preference
            
            # Calculate Rental type match score
            if living_space_type:
                living_space_match = 1.0 if room.living_space_type == living_space_type else 0.0
            else:
                living_space_match = 0.5  # Neutral score if no type preference
            
            # Create row with normalized values
            row = [
                distance_score,      # Distance score (0-1) - NEW
                price_score,         # Price match (0-1)
                safety,              # Safety score (0-1)
                amenity_score,       # Amenity match (0-1)
                cleanliness,         # Cleanliness score (0-1)
                accessibility,       # Accessibility score (0-1)
                noise,               # Noise score (0-1)
                capacity_score,      # Capacity match (0-1)
                living_space_match   # Rental type match (0-1)
            ]
            decision_matrix.append(row)
        
        # Convert to numpy array
        decision_matrix = np.array(decision_matrix, dtype=np.float64)
        
        if len(decision_matrix) == 0:
            return jsonify({'message': 'No rooms available for ranking'})
        
        # Define equal weights for all criteria since we don't have user preferences
        weights = np.array([
            0.20,  # Distance weight (NEW)
            0.20,  # Price weight
            0.15,  # Safety weight
            0.15,  # Amenity weight
            0.10,  # Cleanliness weight
            0.10,  # Accessibility weight
            0.05,  # Noise weight
            0.03,  # Capacity weight
            0.02   # Rental type weight
        ], dtype=np.float64)
        
        # Normalize weights to sum to 1
        weights = weights / np.sum(weights)
        
        # All criteria are beneficial (1 for beneficial)
        impacts = np.array([1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=np.float64)
        
        # Calculate TOPSIS scores
        raw_scores = []
        for i in range(len(decision_matrix)):
            room_scores = topsis([decision_matrix[i].tolist()], weights.tolist(), impacts.tolist())
            raw_scores.append(float(room_scores[0]))
        
        # Convert to numpy array and scale to percentages
        raw_scores = np.array(raw_scores, dtype=np.float64)
        percentage_scores = raw_scores * 100

# End of Logic
        
        # Apply perfect match bonuses
        for i, (room, score) in enumerate(zip(rooms, percentage_scores)):
            room_amenities = json.loads(room.amenities) if room.amenities else []
            
            # Check for perfect matches - only consider criteria if they were specified
            perfect_price = max_price is None or room.price <= max_price
            perfect_capacity = min_capacity is None or room.capacity >= min_capacity
            perfect_amenities = not amenities or all(amenity in room_amenities for amenity in amenities)
            perfect_location = not location or location.lower() in room.location.lower()
            perfect_type = not living_space_type or room.living_space_type == living_space_type
            
            # Apply bonuses for perfect matches
            if perfect_price and perfect_capacity and perfect_amenities and perfect_location and perfect_type:
                percentage_scores[i] = 100.0  # Perfect match gets 100%
            elif perfect_price and perfect_capacity and perfect_amenities:
                percentage_scores[i] = min(100, percentage_scores[i] + 15)  # Major criteria bonus
            elif perfect_price and perfect_capacity:
                percentage_scores[i] = min(100, percentage_scores[i] + 10)  # Essential criteria bonus
            
            # Ensure score doesn't exceed 100
            percentage_scores[i] = min(100, percentage_scores[i])
        
        # Rank rooms with updated scores
        ranked_rooms = sorted(zip(rooms, percentage_scores, range(1, len(rooms) + 1)), 
                            key=lambda x: (x[1], -x[0].price), reverse=True)  # Secondary sort by price if scores are equal
        
        current_app.logger.info(f"Final number of ranked rooms: {len(ranked_rooms)}")
        current_app.logger.info("Top 3 rooms scores and ranks:")
        for room, score, rank in ranked_rooms[:3]:
            current_app.logger.info(f"Room {room.id}: Match={score:.1f}%, Rank #{rank}")
        
        # Calculate percentile ranks and categorize rooms
        total_rooms = len(ranked_rooms)
        
        # Group rooms by match category
        perfect_matches = []
        excellent_matches = []
        good_matches = []
        fair_matches = []
        other_matches = []
        
        # For rooms with additional valuable amenities
        rooms_with_additional_amenities = []
        
        for room, score, rank in ranked_rooms:
            percentile = ((total_rooms - rank + 1) / total_rooms) * 100
            match_percentage = round(score, 1)  # Round to 1 decimal place
            
            # Calculate amenity match percentage for this room
            room_amenities = json.loads(room.amenities) if room.amenities else []
            if amenities:
                matched_amenities = sum(1 for amenity in amenities if amenity in room_amenities)
                amenity_match_percentage = (matched_amenities / len(amenities)) * 100
                
                # Check for valuable additional amenities the tenant didn't request
                additional_valuable_amenities = []
                for amenity in room_amenities:
                    if amenity in HIGH_VALUE_AMENITIES and amenity not in amenities:
                        additional_valuable_amenities.append(amenity)
            else:
                amenity_match_percentage = 100.0
                additional_valuable_amenities = [a for a in room_amenities if a in HIGH_VALUE_AMENITIES]
            
            # Calculate location match score
            location_match_score = 0
            if location.lower() in room.location.lower():
                # Exact neighborhood match
                location_match_score = 100
            elif any(loc in room.location.lower() for loc in location.lower().split()):
                # Partial area match
                location_match_score = 70

            # Calculate price value score
            price_value_score = 100
            if room.price > max_price:
                price_diff_percentage = ((room.price - max_price) / max_price) * 100
                price_value_score = max(0, 100 - price_diff_percentage)

            # Calculate comprehensive match score
            comprehensive_score = (
                match_percentage * 0.4 +  # TOPSIS score weight
                amenity_match_percentage * 0.2 +  # Amenities weight
                location_match_score * (0.2 if location else 0.0) +  # Location weight (only if location specified)
                price_value_score * (0.2 if max_price is not None else 0.0)  # Price value weight (only if max_price specified)
            )
            
            # Normalize the comprehensive score if some criteria weren't specified
            total_weight = 0.4  # TOPSIS score always counts
            total_weight += 0.2  # Amenities always count (even if empty)
            if location:
                total_weight += 0.2
            if max_price is not None:
                total_weight += 0.2
                
            # Normalize to ensure the score is out of 100
            if total_weight > 0:
                comprehensive_score = comprehensive_score * (1.0 / total_weight)
            
            room_data = {
                'id': room.id,
                'title': room.title,
                'description': room.description,
                'price': float(room.price),
                'capacity': float(room.capacity),
                'location': room.location,
                'latitude': float(room.latitude) if room.latitude is not None else None,
                'longitude': float(room.longitude) if room.longitude is not None else None,
                'distance_from_smcc': float(room.distance_from_smcc) if hasattr(room, 'distance_from_smcc') and room.distance_from_smcc is not None else None,
                'amenities': json.loads(room.amenities) if room.amenities else [],
                'additional_valuable_amenities': additional_valuable_amenities if 'additional_valuable_amenities' in locals() else [],
                'availability': room.availability,
                'image_urls': json.loads(room.image_urls) if room.image_urls else [],
                'safety_score': float(room.safety_score) if room.safety_score is not None else None,
                'cleanliness_score': float(room.cleanliness_score) if room.cleanliness_score is not None else None,
                'accessibility_score': float(room.accessibility_score) if room.accessibility_score is not None else None,
                'noise_level': float(room.noise_level) if room.noise_level is not None else None,
                'avg_safety_rating': float(room.avg_safety_rating) if room.avg_safety_rating is not None else None,
                'avg_cleanliness_rating': float(room.avg_cleanliness_rating) if room.avg_cleanliness_rating is not None else None,
                'avg_accessibility_rating': float(room.avg_accessibility_rating) if room.avg_accessibility_rating is not None else None,
                'avg_noise_level_rating': float(room.avg_noise_level_rating) if room.avg_noise_level_rating is not None else None,
                'total_ratings': int(room.total_ratings) if room.total_ratings is not None else 0,
                'landlord': {
                    'id': room.landlord.id if room.landlord else None,
                    'email': room.landlord.email if room.landlord else None,
                    'contact_number': room.landlord.contact_number if room.landlord else None
                },
                'topsis_score': score,
                'rank': rank,
                'percentile': int(round(percentile)),
                'comprehensive_score': round(comprehensive_score, 1),
                'match_details': {
                    'distance': {
                        'value': float(room.distance_from_smcc) if hasattr(room, 'distance_from_smcc') and room.distance_from_smcc is not None else None,
                        'unit': 'km',
                        'weight': float(weights[0]),
                        'score': float(round(distance_score * 100, 1)) if 'distance_score' in locals() else None
                    },
                    'price': {
                        'value': float(room.price),
                        'max_price': float(max_price) if max_price is not None else None,
                        'weight': float(weights[1]),
                        'score': float(round(price_value_score, 1))
                    },
                    'safety': {
                        'score': float(room.safety_score) if room.safety_score is not None else 5.0,
                        'weight': float(weights[2]),
                        'weighted_score': float(round((room.safety_score if room.safety_score is not None else 5.0) * float(weights[2]) * 10, 1))
                    },
                    'cleanliness': {
                        'score': float(room.cleanliness_score) if room.cleanliness_score is not None else 5.0,
                        'weight': float(weights[3]),
                        'weighted_score': float(round((room.cleanliness_score if room.cleanliness_score is not None else 5.0) * float(weights[3]) * 10, 1))
                    },
                    'accessibility': {
                        'score': float(room.accessibility_score) if room.accessibility_score is not None else 5.0,
                        'weight': float(weights[4]),
                        'weighted_score': float(round((room.accessibility_score if room.accessibility_score is not None else 5.0) * float(weights[4]) * 10, 1))
                    },
                    'noise': {
                        'score': float(room.noise_level) if room.noise_level is not None else 5.0,
                        'weight': float(weights[5]),
                        'weighted_score': float(round((10 - (room.noise_level if room.noise_level is not None else 5.0)) * float(weights[5]) * 10, 1))
                    },
                    'amenities': {
                        'score': float(amenity_match_percentage),
                        'weight': float(weights[6]),
                        'weighted_score': float(round(amenity_match_percentage * float(weights[6]) / 10, 1)),
                        'matched': [amenity for amenity in amenities if amenity in room_amenities],
                        'missing': [amenity for amenity in amenities if amenity not in room_amenities],
                        'additional_valuable': additional_valuable_amenities if 'additional_valuable_amenities' in locals() else []
                    },
                    'location': {
                        'score': float(location_match_score),
                        'preferred_location': location,
                        'actual_location': room.location
                    },
                    'price_value': {
                        'score': float(price_value_score),
                        'preferred_max': float(max_price),
                        'actual_price': float(room.price)
                    }
                }
            }
            
            # Categorize based on comprehensive match percentage
            if comprehensive_score >= 90 and (not amenities or amenity_match_percentage == 100) and (not max_price or price_value_score >= 90):
                perfect_matches.append(room_data)
            elif comprehensive_score >= 85:
                excellent_matches.append(room_data)
            elif comprehensive_score >= 75:
                good_matches.append(room_data)
            elif comprehensive_score >= 60:
                fair_matches.append(room_data)
            else:
                other_matches.append(room_data)
                
            # Add to rooms with additional amenities if it has valuable amenities not requested
            if additional_valuable_amenities and comprehensive_score >= 60:
                # Create a copy with a highlight on the additional amenities
                room_data_copy = room_data.copy()
                room_data_copy['highlighted_amenities'] = additional_valuable_amenities
                rooms_with_additional_amenities.append(room_data_copy)
        
        # Sort rooms with additional amenities by comprehensive score
        rooms_with_additional_amenities = sorted(
            rooms_with_additional_amenities, 
            key=lambda x: (x['comprehensive_score'], len(x['highlighted_amenities'])), 
            reverse=True
        )[:5]  # Limit to top 5
        
        return jsonify({
            'summary': {
                'total_rooms': total_rooms,
                'perfect_matches_count': len(perfect_matches),
                'excellent_matches_count': len(excellent_matches),
                'good_matches_count': len(good_matches),
                'fair_matches_count': len(fair_matches),
                'other_matches_count': len(other_matches),
                'rooms_with_additional_amenities_count': len(rooms_with_additional_amenities),
                'categories': {
                    'perfect_match': '90% or higher with all amenities and within budget',
                    'excellent_match': '85-89%',
                    'good_match': '75-84%',
                    'fair_match': '60-74%',
                    'other_match': 'Below 60%',
                    'additional_amenities': 'Rooms with valuable amenities you didn\'t request'
                }
            },
            'suggestions': {
                'perfect_matches': sorted(perfect_matches, key=lambda x: x['comprehensive_score'], reverse=True)[:5],
                'excellent_matches': sorted(excellent_matches, key=lambda x: x['comprehensive_score'], reverse=True)[:5],
                'good_matches': sorted(good_matches, key=lambda x: x['comprehensive_score'], reverse=True)[:5],
                'fair_matches': sorted(fair_matches, key=lambda x: x['comprehensive_score'], reverse=True)[:5],
                'other_matches': sorted(other_matches, key=lambda x: x['comprehensive_score'], reverse=True)[:5],
                'rooms_with_additional_amenities': rooms_with_additional_amenities
            },
            'all_rooms': sorted(
                perfect_matches + excellent_matches + good_matches + fair_matches + other_matches,
                key=lambda x: x['comprehensive_score'],
                reverse=True
            )
        })
        
    except Exception as e:
        current_app.logger.error(f"Error in TOPSIS calculation or room processing: {str(e)}")
        return jsonify({'error': 'Error in ranking calculation'}), 500

@bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if user.user_type != 'tenant':
        return jsonify({'error': 'Unauthorized'}), 403
    
    return jsonify({
        'email': user.email,
        'full_name': user.full_name,
        'contact_number': user.contact_number,
        'bio': user.bio,
        'avatar_url': user.avatar_url
    })

@bp.route('/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if user.user_type != 'tenant':
        return jsonify({'error': 'Unauthorized'}), 403
    
    try:
        data = request.get_json()
        
        # Verify current password
        if not data.get('current_password'):
            return jsonify({'error': 'Current password is required'}), 400
            
        if not user.check_password(data['current_password']):
            return jsonify({'error': 'Current password is incorrect'}), 400
        
        # Update profile fields
        if 'full_name' in data:
            user.full_name = data['full_name']
            
        if 'contact_number' in data:
            user.contact_number = data['contact_number']
            
        if 'bio' in data:
            user.bio = data['bio']
        
        # Update password if provided
        if data.get('new_password'):
            user.set_password(data['new_password'])
        
        db.session.commit()
        return jsonify({'message': 'Profile updated successfully'})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to update profile'}), 500

@bp.route('/profile/avatar', methods=['POST'])
@jwt_required()
def update_avatar():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if user.user_type != 'tenant':
        return jsonify({'error': 'Unauthorized'}), 403
    
    if 'avatar' not in request.files:
        return jsonify({'error': 'No file part'}), 400
        
    file = request.files['avatar']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
        
    if file and allowed_file(file.filename):
        try:
            filename = secure_filename(f"user_{current_user_id}_{file.filename}")
            upload_folder = ensure_upload_folder()
            file_path = os.path.join(upload_folder, filename)
            
            # Save the file
            file.save(file_path)
            
            # Update user's avatar URL
            user.avatar_url = get_image_url(filename)
            db.session.commit()
            
            return jsonify({
                'message': 'Avatar updated successfully',
                'avatar_url': user.avatar_url
            })
            
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500
    else:
        return jsonify({'error': 'File type not allowed'}), 400