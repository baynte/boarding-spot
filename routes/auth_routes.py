from flask import Blueprint, request, jsonify, url_for, redirect, current_app
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from extensions import db
from models import User
from datetime import datetime
import re
from utils.email_utils import send_verification_email
import traceback

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        current_app.logger.info(f"Registration request received: {data}")
        
        email = data.get('email')
        password = data.get('password')
        user_type = data.get('user_type')
        contact_number = data.get('contact_number')

        if not all([email, password, user_type]):
            current_app.logger.warning(f"Missing required fields: email={bool(email)}, password={bool(password)}, user_type={bool(user_type)}")
            return jsonify({'error': 'Missing required fields'}), 400

        if user_type not in ['tenant', 'landlord']:
            current_app.logger.warning(f"Invalid user type: {user_type}")
            return jsonify({'error': 'Invalid user type'}), 400

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            current_app.logger.warning(f"Email already registered: {email}")
            return jsonify({'error': 'Email already registered'}), 400
            
        # Check if tenant email is from smccnasipit.edu.ph domain
        if user_type == 'tenant' and not email.endswith('@smccnasipit.edu.ph'):
            current_app.logger.warning(f"Tenant email not from smccnasipit.edu.ph domain: {email}")
            return jsonify({'error': 'Tenant accounts must use an @smccnasipit.edu.ph email address'}), 400

        user = User(
            email=email,
            user_type=user_type,
            contact_number=contact_number
        )
        user.set_password(password)
        
        # Always auto-verify the account
        user.is_email_verified = True
        email_verification_required = False
        
        # Still attempt to send verification email for tenants with smccnasipit.edu.ph email
        if user_type == 'tenant' and email.endswith('@smccnasipit.edu.ph'):
            current_app.logger.info(f"Generating verification token for tenant: {email}")
            verification_token = user.generate_verification_token()
            
            # Try to send verification email, but don't block registration if it fails
            try:
                email_sent = send_verification_email(email, verification_token)
                if email_sent:
                    current_app.logger.info(f"Verification email sent successfully to {email}")
                else:
                    current_app.logger.warning(f"Failed to send verification email to {email}, but account is auto-verified")
            except Exception as email_error:
                current_app.logger.error(f"Error sending verification email to {email}: {str(email_error)}")
                current_app.logger.error(f"Account is still auto-verified despite email error")
        
        current_app.logger.info(f"Auto-verifying account for: {email}")

        db.session.add(user)
        db.session.commit()
        
        current_app.logger.info(f"User registered successfully: {email}, user_type={user_type}, auto-verified=True")

        return jsonify({
            'message': 'User registered successfully',
            'email_verification_required': email_verification_required,
            'user': {
                'id': user.id,
                'email': user.email,
                'user_type': user.user_type,
                'contact_number': user.contact_number
            }
        }), 201
    except Exception as e:
        error_traceback = traceback.format_exc()
        current_app.logger.error(f"Error in registration: {str(e)}")
        current_app.logger.error(f"Traceback: {error_traceback}")
        return jsonify({'error': 'An unexpected error occurred during registration'}), 500

@bp.route('/verify-email/<token>', methods=['GET'])
def verify_email(token):
    try:
        current_app.logger.info(f"Email verification request received for token: {token}")
        
        user = User.query.filter_by(verification_token=token).first()
        
        if not user:
            current_app.logger.warning(f"Invalid verification token: {token}")
            return jsonify({'error': 'Invalid verification token'}), 400
        
        # Check if token has expired
        if user.token_expiry and user.token_expiry < datetime.utcnow():
            current_app.logger.warning(f"Verification token expired for user: {user.email}")
            return jsonify({'error': 'Verification token has expired'}), 400
        
        # Mark email as verified
        user.is_email_verified = True
        user.verification_token = None
        user.token_expiry = None
        db.session.commit()
        
        current_app.logger.info(f"Email verified successfully for user: {user.email}")
        
        # Redirect to frontend verification success page
        return redirect(url_for('static', filename='email-verified.html'))
    except Exception as e:
        error_traceback = traceback.format_exc()
        current_app.logger.error(f"Error in email verification: {str(e)}")
        current_app.logger.error(f"Traceback: {error_traceback}")
        return jsonify({'error': 'An unexpected error occurred during email verification'}), 500

@bp.route('/resend-verification', methods=['POST'])
def resend_verification():
    try:
        data = request.get_json()
        current_app.logger.info(f"Resend verification request received: {data}")
        
        email = data.get('email')
        
        if not email:
            current_app.logger.warning("Email is required for resend verification")
            return jsonify({'error': 'Email is required'}), 400
        
        user = User.query.filter_by(email=email).first()
        
        if not user:
            current_app.logger.warning(f"User not found for resend verification: {email}")
            return jsonify({'error': 'User not found'}), 404
        
        if user.is_email_verified:
            current_app.logger.info(f"Email is already verified for user: {email}")
            return jsonify({'message': 'Email is already verified'}), 200
        
        # Generate new verification token
        current_app.logger.info(f"Generating new verification token for user: {email}")
        verification_token = user.generate_verification_token()
        
        # Try to send verification email
        try:
            email_sent = send_verification_email(email, verification_token)
            if email_sent:
                current_app.logger.info(f"Verification email sent successfully to {email}")
                db.session.commit()
                return jsonify({'message': 'Verification email sent successfully'}), 200
            else:
                current_app.logger.warning(f"Failed to send verification email to {email}, auto-verifying account")
        except Exception as email_error:
            current_app.logger.error(f"Error sending verification email to {email}: {str(email_error)}")
            current_app.logger.error(f"Will auto-verify account instead")
        
        # If email sending failed, auto-verify the account
        user.is_email_verified = True
        user.verification_token = None
        user.token_expiry = None
        db.session.commit()
        
        current_app.logger.info(f"Auto-verified account for: {email} due to email sending failure")
        return jsonify({'message': 'Account has been automatically verified'}), 200
    except Exception as e:
        error_traceback = traceback.format_exc()
        current_app.logger.error(f"Error in resend verification: {str(e)}")
        current_app.logger.error(f"Traceback: {error_traceback}")
        return jsonify({'error': 'An unexpected error occurred while resending verification email'}), 500

@bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        current_app.logger.info(f"Login request received for email: {data.get('email')}")
        
        user = User.query.filter_by(email=data['email']).first()
        
        if not user:
            current_app.logger.warning(f"User not found for login: {data.get('email')}")
            return jsonify({'error': 'Invalid credentials'}), 401
            
        if not user.check_password(data['password']):
            current_app.logger.warning(f"Invalid password for user: {data.get('email')}")
            return jsonify({'error': 'Invalid credentials'}), 401
        
        # If user is not verified, auto-verify them now
        if not user.is_email_verified:
            current_app.logger.info(f"Auto-verifying unverified user during login: {user.email}")
            user.is_email_verified = True
            user.verification_token = None
            user.token_expiry = None
            db.session.commit()
        
        access_token = create_access_token(identity=str(user.id))
        current_app.logger.info(f"Login successful for user: {user.email}, user_type: {user.user_type}")
        
        return jsonify({
            'access_token': access_token,
            'user_type': user.user_type,
            'is_admin': user.is_admin
        })
    except Exception as e:
        error_traceback = traceback.format_exc()
        current_app.logger.error(f"Error in login: {str(e)}")
        current_app.logger.error(f"Traceback: {error_traceback}")
        return jsonify({'error': 'An unexpected error occurred during login'}), 500

@bp.route('/user-type', methods=['GET'])
@jwt_required()
def get_user_type():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    return jsonify({'user_type': user.user_type})