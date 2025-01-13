from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename
from app import db
from models import User, Room
import json
import os
from datetime import datetime

bp = Blueprint('landlord', __name__, url_prefix='/landlord')

# Configure upload folder
UPLOAD_FOLDER = 'static/room_images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def ensure_upload_folder():
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

@bp.route('/rooms', methods=['POST'])
@jwt_required()
def create_room():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if user.user_type != 'landlord':
        return jsonify({'error': 'Unauthorized'}), 403
    
    ensure_upload_folder()
    
    # Handle image upload
    image_url = None
    if 'image' in request.files:
        file = request.files['image']
        if file and allowed_file(file.filename):
            filename = secure_filename(f"{current_user_id}_{int(datetime.utcnow().timestamp())}_{file.filename}")
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            image_url = f"/{UPLOAD_FOLDER}/{filename}"
    
    data = request.form.to_dict()
    # Convert amenities from string to list if present
    if 'amenities' in data:
        data['amenities'] = json.loads(data['amenities'])
    
    room = Room(
        landlord_id=current_user_id,
        title=data['title'],
        description=data['description'],
        price=float(data['price']),
        size=float(data.get('size', 0)),
        location=data['location'],
        amenities=json.dumps(data.get('amenities', [])),
        safety_score=float(data.get('safety_score', 5.0)),
        cleanliness_score=float(data.get('cleanliness_score', 5.0)),
        accessibility_score=float(data.get('accessibility_score', 5.0)),
        noise_level=float(data.get('noise_level', 5.0)),
        image_url=image_url
    )
    
    db.session.add(room)
    db.session.commit()
    
    return jsonify({'message': 'Room created successfully', 'room_id': room.id}), 201

@bp.route('/rooms', methods=['GET'])
@jwt_required()
def get_rooms():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if user.user_type != 'landlord':
        return jsonify({'error': 'Unauthorized'}), 403
    
    rooms = Room.query.filter_by(landlord_id=current_user_id).all()
    return jsonify([{
        'id': room.id,
        'title': room.title,
        'description': room.description,
        'price': room.price,
        'size': room.size,
        'location': room.location,
        'amenities': json.loads(room.amenities),
        'availability': room.availability,
        'safety_score': room.safety_score,
        'cleanliness_score': room.cleanliness_score,
        'accessibility_score': room.accessibility_score,
        'noise_level': room.noise_level,
        'image_url': room.image_url
    } for room in rooms])

@bp.route('/rooms/<int:room_id>', methods=['PUT'])
@jwt_required()
def update_room(room_id):
    current_user_id = get_jwt_identity()
    print(f"Received request to update room {room_id} from user {current_user_id}")  # Debug print
    
    user = User.query.get(current_user_id)
    print(f"User type: {user.user_type}")  # Debug print
    
    if user.user_type != 'landlord':
        print(f"User {current_user_id} is not a landlord")  # Debug print
        return jsonify({'error': 'Unauthorized - User is not a landlord'}), 403
    
    room = Room.query.get_or_404(room_id)
    print(f"Room landlord_id: {room.landlord_id}, Current user_id: {current_user_id}")  # Debug print
    print(f"Types - Room landlord_id: {type(room.landlord_id)}, Current user_id: {type(current_user_id)}")  # Debug print
    
    # Convert both IDs to integers for comparison
    landlord_id = int(room.landlord_id)
    user_id = int(current_user_id)
    
    if landlord_id != user_id:
        print(f"User {current_user_id} does not own room {room_id}")  # Debug print
        return jsonify({'error': 'Unauthorized - User does not own this room'}), 403
    
    # Handle image upload
    if 'image' in request.files:
        file = request.files['image']
        if file and allowed_file(file.filename):
            # Delete old image if it exists
            if room.image_url and os.path.exists(room.image_url.lstrip('/')):
                os.remove(room.image_url.lstrip('/'))
            
            filename = secure_filename(f"{current_user_id}_{int(datetime.utcnow().timestamp())}_{file.filename}")
            ensure_upload_folder()
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            room.image_url = f"/{UPLOAD_FOLDER}/{filename}"
    
    # Handle other form data
    data = request.form.to_dict()
    print(f"Received form data: {data}")  # Debug print
    
    if 'amenities' in data:
        data['amenities'] = json.dumps(json.loads(data['amenities']))
    
    # Handle boolean values
    if 'availability' in data:
        data['availability'] = str(data['availability']).lower() == 'true'
        print(f"Setting availability to: {data['availability']}")  # Debug print
    
    try:
        for key, value in data.items():
            if hasattr(room, key):
                if key in ['price', 'size', 'safety_score', 'cleanliness_score', 'accessibility_score', 'noise_level']:
                    value = float(value)
                print(f"Setting {key} to {value}")  # Debug print
                setattr(room, key, value)
        
        db.session.commit()
        print(f"Successfully updated room {room_id}")  # Debug print
        return jsonify({'message': 'Room updated successfully'})
    except Exception as e:
        print(f"Error updating room: {str(e)}")  # Debug print
        db.session.rollback()
        return jsonify({'error': 'Failed to update room'}), 500 