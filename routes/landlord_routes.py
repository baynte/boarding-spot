from flask import Blueprint, request, jsonify, current_app, url_for
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename
from app import db
from models import User, Room, TenantRating
from utils.document_utils import save_document, delete_document
import json
import os
from datetime import datetime
from werkzeug.security import check_password_hash

bp = Blueprint('landlord', __name__, url_prefix='/landlord')

# Configure upload folder
UPLOAD_FOLDER = 'static/room_images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def ensure_upload_folder():
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

def get_image_url(filename):
    if not filename:
        return None
    # Return the URL with /static prefix
    return f'http://localhost:5000/static/room_images/{filename}'

@bp.route('/rooms', methods=['POST'])
@jwt_required()
def create_room():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if user.user_type != 'landlord':
        return jsonify({'error': 'Unauthorized'}), 403
    
    ensure_upload_folder()
    
    # Handle multiple image uploads
    image_urls = []
    if 'images' in request.files:
        files = request.files.getlist('images')
        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(f"{current_user_id}_{int(datetime.utcnow().timestamp())}_{file.filename}")
                file.save(os.path.join(UPLOAD_FOLDER, filename))
                image_urls.append(get_image_url(filename))
    
    # Handle document upload
    document_url = None
    document_name = None
    if 'document' in request.files:
        document_file = request.files['document']
        document_url, document_name = save_document(document_file)
    
    data = request.form.to_dict()
    # Convert amenities from string to list if present
    if 'amenities' in data:
        data['amenities'] = json.loads(data['amenities'])
    
    room = Room(
        landlord_id=current_user_id,
        title=data['title'],
        description=data['description'],
        price=float(data['price']),
        capacity=int(data.get('capacity', 1)),
        location=data['location'],
        latitude=float(data.get('latitude')) if data.get('latitude') else None,
        longitude=float(data.get('longitude')) if data.get('longitude') else None,
        living_space_type=data.get('living_space_type', 'Boarding House'),
        amenities=json.dumps(data.get('amenities', [])),
        safety_score=5.0,
        cleanliness_score=5.0,
        accessibility_score=5.0,
        noise_level=5.0,
        image_urls=json.dumps(image_urls),
        document_url=document_url,
        document_name=document_name,
        approval_status='pending'
    )
    
    db.session.add(room)
    db.session.commit()
    
    return jsonify({
        'message': 'Room created successfully and is pending approval by admin',
        'room_id': room.id
    }), 201

@bp.route('/rooms', methods=['GET'])
@jwt_required()
def get_rooms():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if user.user_type != 'landlord':
        return jsonify({'error': 'Unauthorized'}), 403
    
    rooms = Room.query.filter_by(landlord_id=current_user_id).all()
    rooms_data = [{
        'id': room.id,
        'title': room.title,
        'description': room.description,
        'price': room.price,
        'capacity': room.capacity,
        'location': room.location,
        'latitude': room.latitude,
        'longitude': room.longitude,
        'living_space_type': room.living_space_type,
        'amenities': json.loads(room.amenities),
        'availability': room.availability,
        'safety_score': room.safety_score,
        'cleanliness_score': room.cleanliness_score,
        'accessibility_score': room.accessibility_score,
        'noise_level': room.noise_level,
        'image_urls': json.loads(room.image_urls),
        'document_url': room.document_url,
        'document_name': room.document_name,
        'approval_status': room.approval_status,
        'admin_notes': room.admin_notes
    } for room in rooms]
    return jsonify(rooms_data)

@bp.route('/rooms/<int:room_id>', methods=['PUT'])
@jwt_required()
def update_room(room_id):
    current_user_id = get_jwt_identity()
    print(f"Received request to update room {room_id} from user {current_user_id}")
    
    user = User.query.get(current_user_id)
    print(f"User type: {user.user_type}")
    
    if user.user_type != 'landlord':
        print(f"User {current_user_id} is not a landlord")
        return jsonify({'error': 'Unauthorized - User is not a landlord'}), 403
    
    room = Room.query.get_or_404(room_id)
    print(f"Room landlord_id: {room.landlord_id}, Current user_id: {current_user_id}")
    print(f"Types - Room landlord_id: {type(room.landlord_id)}, Current user_id: {type(current_user_id)}")
    
    # Convert both IDs to integers for comparison
    landlord_id = int(room.landlord_id)
    user_id = int(current_user_id)
    
    if landlord_id != user_id:
        print(f"User {current_user_id} does not own room {room_id}")
        return jsonify({'error': 'Unauthorized - User does not own this room'}), 403
    
    # Handle multiple image uploads
    if 'images' in request.files:
        files = request.files.getlist('images')
        if any(file and allowed_file(file.filename) for file in files):
            # Delete old images if they exist
            if room.image_urls:
                old_urls = json.loads(room.image_urls)
                for old_url in old_urls:
                    old_filename = os.path.basename(old_url)
                    old_path = os.path.join(UPLOAD_FOLDER, old_filename)
                    if os.path.exists(old_path):
                        os.remove(old_path)
            
            # Save new images
            new_image_urls = []
            for file in files:
                if file and allowed_file(file.filename):
                    filename = secure_filename(f"{current_user_id}_{int(datetime.utcnow().timestamp())}_{file.filename}")
                    ensure_upload_folder()
                    file.save(os.path.join(UPLOAD_FOLDER, filename))
                    new_image_urls.append(get_image_url(filename))
            room.image_urls = json.dumps(new_image_urls)
    
    # Handle document upload
    if 'document' in request.files:
        document_file = request.files['document']
        if document_file:
            # Delete old document if it exists
            if room.document_url:
                delete_document(room.document_url)
            
            # Save new document
            document_url, document_name = save_document(document_file)
            if document_url and document_name:
                room.document_url = document_url
                room.document_name = document_name
    
    # Process form data
    data = request.form.to_dict()
    
    # Convert numeric fields
    float_fields = ['price']
    for field in float_fields:
        if field in data:
            data[field] = float(data[field])
    
    # Convert capacity to integer
    if 'capacity' in data:
        data['capacity'] = int(data['capacity'])
        
    # Convert lat/lng to float if present
    if 'latitude' in data:
        data['latitude'] = float(data['latitude'])
    if 'longitude' in data:
        data['longitude'] = float(data['longitude'])
        
    # Convert availability to boolean
    if 'availability' in data:
        data['availability'] = data['availability'].lower() == 'true'

    # Update room attributes
    for key, value in data.items():
        if hasattr(room, key):
            setattr(room, key, value)
        
    try:
        db.session.commit()
        print(f"Successfully updated room {room_id}")
        return jsonify({'message': 'Room updated successfully'})
    except Exception as e:
        print(f"Error updating room: {str(e)}")
        db.session.rollback()
        return jsonify({'error': 'Failed to update room'}), 500 

@bp.route('/rooms/<int:room_id>', methods=['DELETE'])
@jwt_required()
def delete_room(room_id):
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if user.user_type != 'landlord':
        return jsonify({'error': 'Unauthorized - User is not a landlord'}), 403
    
    room = Room.query.get_or_404(room_id)
    
    # Convert both IDs to integers for comparison
    landlord_id = int(room.landlord_id)
    user_id = int(current_user_id)
    
    if landlord_id != user_id:
        return jsonify({'error': 'Unauthorized - User does not own this room'}), 403
    
    try:
        # Delete the room images if they exist
        if room.image_urls:
            old_urls = json.loads(room.image_urls)
            for old_url in old_urls:
                old_filename = os.path.basename(old_url)
                old_path = os.path.join(UPLOAD_FOLDER, old_filename)
                if os.path.exists(old_path):
                    os.remove(old_path)
        
        # Delete the room document if it exists
        if room.document_url:
            delete_document(room.document_url)
        
        # Delete related tenant ratings first
        TenantRating.query.filter_by(room_id=room_id).delete()
        
        # Delete the room from database
        db.session.delete(room)
        db.session.commit()
        
        return jsonify({'message': 'Room deleted successfully'})
    except Exception as e:
        print(f"Error deleting room: {str(e)}")
        db.session.rollback()
        return jsonify({'error': 'Failed to delete room: ' + str(e)}), 500

@bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if user.user_type != 'landlord':
        return jsonify({'error': 'Unauthorized'}), 403
    
    return jsonify({
        'email': user.email,
        'contact_number': user.contact_number
    })

@bp.route('/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if user.user_type != 'landlord':
        return jsonify({'error': 'Unauthorized'}), 403
    
    try:
        data = request.get_json()
        
        # Verify current password
        if not data.get('current_password'):
            return jsonify({'error': 'Current password is required'}), 400
            
        if not user.check_password(data['current_password']):
            return jsonify({'error': 'Current password is incorrect'}), 400
        
        # Update contact number
        if 'contact_number' in data:
            user.contact_number = data['contact_number']
        
        # Update password if provided
        if data.get('new_password'):
            user.set_password(data['new_password'])
        
        db.session.commit()
        return jsonify({'message': 'Profile updated successfully'})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to update profile'}), 500 