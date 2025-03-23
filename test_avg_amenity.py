from app import create_app, db
from models import Room, TenantRating
from sqlalchemy import func
import sys

app = create_app()
with app.app_context():
    room = Room.query.first()
    if room:
        print(f"Room ID: {room.id}")
        print(f"Room has avg_amenity_rating: {hasattr(room, 'avg_amenity_rating')}")
        print(f"Room avg_amenity_rating value: {room.avg_amenity_rating}")
        
        # Check if there are any ratings for this room
        ratings = TenantRating.query.filter_by(room_id=room.id).all()
        print(f"Number of ratings: {len(ratings)}")
        
        # Inspect each rating
        for i, rating in enumerate(ratings):
            print(f"Rating {i+1}:")
            print(f"  ID: {rating.id}")
            print(f"  Tenant ID: {rating.tenant_id}")
            print(f"  Safety: {rating.safety_rating}")
            print(f"  Cleanliness: {rating.cleanliness_rating}")
            print(f"  Accessibility: {rating.accessibility_rating}")
            print(f"  Noise Level: {rating.noise_level_rating}")
            print(f"  Amenity: {rating.amenity_rating}")
            
            # Set default value for amenity_rating if it's None
            if rating.amenity_rating is None:
                print(f"  Setting default amenity_rating for rating {rating.id}")
                rating.amenity_rating = 5.0
                
        # Commit changes if any ratings were updated
        db.session.commit()
        
        # Calculate amenity rating average manually
        valid_ratings = [r for r in ratings if r.amenity_rating is not None]
        if valid_ratings:
            amenity_avg = sum(r.amenity_rating for r in valid_ratings) / len(valid_ratings)
            print(f"Manually calculated avg_amenity_rating: {amenity_avg}")
            
            # Update the room's avg_amenity_rating
            room.avg_amenity_rating = amenity_avg
            db.session.commit()
            print(f"After update, room avg_amenity_rating: {room.avg_amenity_rating}")
        else:
            print("No valid amenity ratings found")
    else:
        print("No rooms found in database") 