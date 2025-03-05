from app import create_app
from models import User
from extensions import db
import sys

def create_admin_user(email, password):
    """Create a new admin user or update an existing user to be an admin."""
    app = create_app()
    
    with app.app_context():
        # Check if user exists
        user = User.query.filter_by(email=email).first()
        
        if user:
            # Update existing user
            user.is_admin = True
            db.session.commit()
            print(f"User {email} has been updated to admin status.")
        else:
            # Create new admin user
            new_user = User(
                email=email,
                user_type='landlord',  # Default type
                is_admin=True
            )
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.commit()
            print(f"New admin user {email} has been created.")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python create_admin.py <email> <password>")
        sys.exit(1)
    
    email = sys.argv[1]
    password = sys.argv[2]
    
    create_admin_user(email, password) 