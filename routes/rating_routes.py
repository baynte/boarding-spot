from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from models import User, Room, TenantRating
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError

bp = Blueprint('rating', __name__, url_prefix='/rating')

@bp.route('/submit/<int:room_id>', methods=['POST'])
@jwt_required()
def submit_rating(room_id):
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if user.user_type != 'tenant':
        return jsonify({'error': 'Only tenants can submit ratings'}), 403
    
    room = Room.query.get_or_404(room_id)
    
    try:
        data = request.get_json()
        
        # Validate rating values
        required_fields = ['safety_rating', 'cleanliness_rating', 'accessibility_rating', 'noise_level_rating']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
            if not isinstance(data[field], (int, float)) or data[field] < 1 or data[field] > 10:
                return jsonify({'error': f'{field} must be a number between 1 and 10'}), 400

        # Create or update rating
        rating = TenantRating.query.filter_by(tenant_id=current_user_id, room_id=room_id).first()
        if rating:
            # Update existing rating
            for field in required_fields:
                setattr(rating, field, data[field])
            if 'comment' in data:
                rating.comment = data['comment']
        else:
            # Create new rating
            rating = TenantRating(
                tenant_id=current_user_id,
                room_id=room_id,
                safety_rating=data['safety_rating'],
                cleanliness_rating=data['cleanliness_rating'],
                accessibility_rating=data['accessibility_rating'],
                noise_level_rating=data['noise_level_rating'],
                comment=data.get('comment')
            )
            db.session.add(rating)

        # Calculate new average ratings
        avg_ratings = db.session.query(
            func.avg(TenantRating.safety_rating).label('avg_safety'),
            func.avg(TenantRating.cleanliness_rating).label('avg_cleanliness'),
            func.avg(TenantRating.accessibility_rating).label('avg_accessibility'),
            func.avg(TenantRating.noise_level_rating).label('avg_noise'),
            func.count(TenantRating.id).label('total')
        ).filter(TenantRating.room_id == room_id).first()

        # Update room's scores with the new averages
        room.safety_score = float(avg_ratings.avg_safety or 0)
        room.cleanliness_score = float(avg_ratings.avg_cleanliness or 0)
        room.accessibility_score = float(avg_ratings.avg_accessibility or 0)
        room.noise_level = float(avg_ratings.avg_noise or 0)
        room.total_ratings = int(avg_ratings.total or 0)

        # Also update the average ratings fields
        room.avg_safety_rating = room.safety_score
        room.avg_cleanliness_rating = room.cleanliness_score
        room.avg_accessibility_rating = room.accessibility_score
        room.avg_noise_level_rating = room.noise_level

        db.session.commit()
        
        return jsonify({
            'message': 'Rating submitted successfully',
            'rating': {
                'safety_rating': rating.safety_rating,
                'cleanliness_rating': rating.cleanliness_rating,
                'accessibility_rating': rating.accessibility_rating,
                'noise_level_rating': rating.noise_level_rating,
                'comment': rating.comment,
                'created_at': rating.created_at.isoformat(),
                'updated_at': rating.updated_at.isoformat()
            },
            'room_scores': {
                'safety_score': room.safety_score,
                'cleanliness_score': room.cleanliness_score,
                'accessibility_score': room.accessibility_score,
                'noise_level': room.noise_level,
                'total_ratings': room.total_ratings
            }
        })
        
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'You have already rated this room'}), 400
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error submitting rating: {str(e)}")
        return jsonify({'error': 'Failed to submit rating'}), 500

@bp.route('/room/<int:room_id>', methods=['GET'])
def get_room_ratings(room_id):
    try:
        ratings = TenantRating.query.filter_by(room_id=room_id).all()
        return jsonify({
            'ratings': [{
                'id': rating.id,
                'safety_rating': rating.safety_rating,
                'cleanliness_rating': rating.cleanliness_rating,
                'accessibility_rating': rating.accessibility_rating,
                'noise_level_rating': rating.noise_level_rating,
                'comment': rating.comment,
                'created_at': rating.created_at.isoformat(),
                'updated_at': rating.updated_at.isoformat()
            } for rating in ratings],
            'summary': {
                'avg_safety_rating': Room.query.get(room_id).avg_safety_rating,
                'avg_cleanliness_rating': Room.query.get(room_id).avg_cleanliness_rating,
                'avg_accessibility_rating': Room.query.get(room_id).avg_accessibility_rating,
                'avg_noise_level_rating': Room.query.get(room_id).avg_noise_level_rating,
                'total_ratings': Room.query.get(room_id).total_ratings
            }
        })
    except Exception as e:
        current_app.logger.error(f"Error getting room ratings: {str(e)}")
        return jsonify({'error': 'Failed to get ratings'}), 500

@bp.route('/user/ratings', methods=['GET'])
@jwt_required()
def get_user_ratings():
    current_user_id = get_jwt_identity()
    try:
        ratings = TenantRating.query.filter_by(tenant_id=current_user_id).all()
        return jsonify([{
            'id': rating.id,
            'room_id': rating.room_id,
            'room_title': rating.room.title,
            'safety_rating': rating.safety_rating,
            'cleanliness_rating': rating.cleanliness_rating,
            'accessibility_rating': rating.accessibility_rating,
            'noise_level_rating': rating.noise_level_rating,
            'comment': rating.comment,
            'created_at': rating.created_at.isoformat(),
            'updated_at': rating.updated_at.isoformat()
        } for rating in ratings])
    except Exception as e:
        current_app.logger.error(f"Error getting user ratings: {str(e)}")
        return jsonify({'error': 'Failed to get user ratings'}), 500 