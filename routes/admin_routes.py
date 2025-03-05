from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import db
from models import User, Room
from functools import wraps

bp = Blueprint('admin', __name__, url_prefix='/admin')

# Admin authentication decorator
def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user or not user.is_admin:
            return jsonify({'error': 'Admin access required'}), 403
        
        return fn(*args, **kwargs)
    return wrapper

@bp.route('/dashboard', methods=['GET'])
@jwt_required()
@admin_required
def dashboard():
    # Count total tenants
    tenant_count = User.query.filter_by(user_type='tenant').count()
    
    # Count total landlords
    landlord_count = User.query.filter_by(user_type='landlord').count()
    
    # Count total rooms
    room_count = Room.query.count()
    
    # Get recent users (last 5)
    recent_users = User.query.order_by(User.created_at.desc()).limit(5)
    recent_users_data = [
        {
            'id': user.id,
            'email': user.email,
            'user_type': user.user_type,
            'created_at': user.created_at.isoformat()
        } for user in recent_users
    ]
    
    return jsonify({
        'tenant_count': tenant_count,
        'landlord_count': landlord_count,
        'room_count': room_count,
        'recent_users': recent_users_data
    })

@bp.route('/users', methods=['GET'])
@jwt_required()
@admin_required
def get_users():
    users = User.query.all()
    users_data = [
        {
            'id': user.id,
            'email': user.email,
            'user_type': user.user_type,
            'is_admin': user.is_admin,
            'created_at': user.created_at.isoformat()
        } for user in users
    ]
    
    return jsonify(users_data)

@bp.route('/users/<int:user_id>', methods=['PUT'])
@jwt_required()
@admin_required
def update_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    data = request.get_json()
    
    # Update user fields
    if 'is_admin' in data:
        user.is_admin = data['is_admin']
    
    if 'user_type' in data:
        if data['user_type'] in ['tenant', 'landlord']:
            user.user_type = data['user_type']
        else:
            return jsonify({'error': 'Invalid user type'}), 400
    
    db.session.commit()
    
    return jsonify({
        'id': user.id,
        'email': user.email,
        'user_type': user.user_type,
        'is_admin': user.is_admin
    }) 