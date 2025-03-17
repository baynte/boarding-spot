import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import current_app, url_for
import traceback

# Email configuration - these should be set in environment variables
SMTP_SERVER = os.environ.get('SMTP_SERVER', 'smtp.gmail.com')
SMTP_PORT = int(os.environ.get('SMTP_PORT', 587))
SMTP_USERNAME = os.environ.get('SMTP_USERNAME', 'your_email@smccnasipit.edu.ph')
SMTP_PASSWORD = os.environ.get('SMTP_PASSWORD', 'your_password')
SENDER_EMAIL = os.environ.get('SENDER_EMAIL', 'your_email@smccnasipit.edu.ph')

def send_verification_email(user_email, verification_token):
    """
    Send a verification email to the user with a link to verify their email address.
    
    Args:
        user_email (str): The recipient's email address
        verification_token (str): The verification token to include in the URL
    
    Returns:
        bool: True if the email was sent successfully, False otherwise
    """
    try:
        # Create the verification URL
        verification_url = url_for('auth.verify_email', token=verification_token, _external=True)
        current_app.logger.info(f"Generated verification URL: {verification_url}")
        
        # Create the email message
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = user_email
        msg['Subject'] = 'Verify Your Email - Boarding Spot'
        
        # Email body
        body = f"""
        <html>
        <body>
            <h2>Welcome to Boarding Spot!</h2>
            <p>Thank you for registering. Please verify your email address by clicking the link below:</p>
            <p><a href="{verification_url}">Verify Email Address</a></p>
            <p>If you did not create an account, please ignore this email.</p>
            <p>This link will expire in 24 hours.</p>
            <p>Best regards,<br>The Boarding Spot Team</p>
        </body>
        </html>
        """
        
        # Attach the body to the email
        msg.attach(MIMEText(body, 'html'))
        
        current_app.logger.info(f"Attempting to send email to {user_email} using {SMTP_SERVER}:{SMTP_PORT}")
        current_app.logger.info(f"Using SMTP credentials: {SMTP_USERNAME}")
        
        # Connect to the SMTP server and send the email
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.send_message(msg)
            current_app.logger.info(f"Email sent successfully to {user_email}")
        
        return True
    except Exception as e:
        error_traceback = traceback.format_exc()
        current_app.logger.error(f"Error sending verification email: {str(e)}")
        current_app.logger.error(f"Traceback: {error_traceback}")
        current_app.logger.error(f"SMTP settings: Server={SMTP_SERVER}, Port={SMTP_PORT}, Username={SMTP_USERNAME}")
        return False 