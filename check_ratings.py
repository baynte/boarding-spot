from app import create_app
from models import Room, TenantRating
import json

app = create_app()
with app.app_context():
    # Find a room with ratings
    room = Room.query.join(TenantRating).first()
    
    if room:
        print(f"Room ID: {room.id}")
        print(f"Room has {room.total_ratings} ratings")
        print(f"Room avg_safety_rating: {room.avg_safety_rating}")
        print(f"Room avg_cleanliness_rating: {room.avg_cleanliness_rating}")
        print(f"Room avg_accessibility_rating: {room.avg_accessibility_rating}")
        print(f"Room avg_noise_level_rating: {room.avg_noise_level_rating}")
        print(f"Room avg_amenity_rating: {room.avg_amenity_rating}")
        
        # Mock the JSON response that would be sent to the frontend
        response = {
            'summary': {
                'avg_safety_rating': room.avg_safety_rating,
                'avg_cleanliness_rating': room.avg_cleanliness_rating,
                'avg_accessibility_rating': room.avg_accessibility_rating,
                'avg_noise_level_rating': room.avg_noise_level_rating,
                'avg_amenity_rating': room.avg_amenity_rating,
                'total_ratings': room.total_ratings
            }
        }
        
        print("\nJSON response that would be sent to frontend:")
        print(json.dumps(response, indent=2))
    else:
        print("No rooms with ratings found") 