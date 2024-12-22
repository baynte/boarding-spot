from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from extensions import db
from models import User

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already registered'}), 400
    
    user = User(
        email=data['email'],
        user_type=data['user_type']
    )
    user.set_password(data['password'])
    
    db.session.add(user)
    db.session.commit()
    
    return jsonify({'message': 'User registered successfully'}), 201

@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    
    if not user or not user.check_password(data['password']):
        return jsonify({'error': 'Invalid credentials'}), 401
    
    access_token = create_access_token(identity=user.id)
    return jsonify({
        'access_token': access_token,
        'user_type': user.user_type
    }) 