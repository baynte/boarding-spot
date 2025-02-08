from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from extensions import db
from models import User

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    user_type = data.get('user_type')
    contact_number = data.get('contact_number')

    if not all([email, password, user_type]):
        return jsonify({'error': 'Missing required fields'}), 400

    if user_type not in ['tenant', 'landlord']:
        return jsonify({'error': 'Invalid user type'}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'Email already registered'}), 400

    user = User(
        email=email,
        user_type=user_type,
        contact_number=contact_number
    )
    user.set_password(password)

    db.session.add(user)
    db.session.commit()

    return jsonify({
        'message': 'User registered successfully',
        'user': {
            'id': user.id,
            'email': user.email,
            'user_type': user.user_type,
            'contact_number': user.contact_number
        }
    }), 201

@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    
    if not user or not user.check_password(data['password']):
        return jsonify({'error': 'Invalid credentials'}), 401
    
    access_token = create_access_token(identity=str(user.id))
    return jsonify({
        'access_token': access_token,
        'user_type': user.user_type
    })

@bp.route('/user-type', methods=['GET'])
@jwt_required()
def get_user_type():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    return jsonify({'user_type': user.user_type})