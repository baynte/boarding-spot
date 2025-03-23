from app import create_app, db
from models import Room, TenantRating
from sqlalchemy import func
import sys

app = create_app()
with app.app_context():
    # Update all NULL amenity_rating values to 5.0
    print("Updating NULL amenity_rating values...")
    null_ratings = TenantRating.query.filter(TenantRating.amenity_rating.is_(None)).all()
    
    if null_ratings:
        print(f"Found {len(null_ratings)} ratings with NULL amenity_rating")
        for rating in null_ratings:
            print(f"  Setting default amenity_rating for rating {rating.id}")
            rating.amenity_rating = 5.0
        
        db.session.commit()
        print("All NULL amenity_rating values have been updated to 5.0")
    else:
        print("No NULL amenity_rating values found")
    
    # Update average amenity ratings for all rooms
    print("\nUpdating average amenity ratings for all rooms...")
    rooms = Room.query.all()
    
    for room in rooms:
        # Get all ratings for this room
        ratings = TenantRating.query.filter_by(room_id=room.id).all()
        
        if ratings:
            print(f"Room ID {room.id}:")
            print(f"  Current avg_amenity_rating: {room.avg_amenity_rating}")
            
            # Calculate new average
            valid_ratings = [r for r in ratings if r.amenity_rating is not None]
            if valid_ratings:
                amenity_avg = sum(r.amenity_rating for r in valid_ratings) / len(valid_ratings)
                room.avg_amenity_rating = amenity_avg
                print(f"  New avg_amenity_rating: {room.avg_amenity_rating}")
            else:
                print("  No valid amenity ratings found, skipping")
        
    # Commit all changes
    db.session.commit()
    print("\nAll average amenity ratings have been updated") 