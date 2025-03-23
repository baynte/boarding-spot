from app import create_app, db
from models import Room, User, TenantRating
from flask import jsonify
import json

app = create_app()
with app.app_context():
    # Get a room with ratings to examine
    room = Room.query.filter(Room.id == 26).first()
    
    if room:
        print(f"Room ID: {room.id}")
        print(f"Room title: {room.title}")
        print(f"Current avg_amenity_rating in database: {room.avg_amenity_rating}")
        
        # Create a room_data dict similar to what's in tenant_routes.py
        room_data = {
            'id': room.id,
            'title': room.title,
            'description': room.description,
            'price': float(room.price),
            'capacity': room.capacity,
            'location': room.location,
            'latitude': float(room.latitude) if room.latitude is not None else None,
            'longitude': float(room.longitude) if room.longitude is not None else None,
            'amenities': json.loads(room.amenities) if room.amenities else [],
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
            'total_ratings': room.total_ratings
            # Note: avg_amenity_rating is missing here!
        }
        
        print("\nRoom data sent to frontend WITHOUT avg_amenity_rating:")
        print(json.dumps(room_data, indent=2))
        
        # Now add the avg_amenity_rating
        room_data['avg_amenity_rating'] = float(room.avg_amenity_rating) if room.avg_amenity_rating is not None else None
        
        print("\nRoom data sent to frontend WITH avg_amenity_rating:")
        print(json.dumps(room_data, indent=2))
    else:
        print("Room not found") 