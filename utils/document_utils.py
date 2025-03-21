import os
from werkzeug.utils import secure_filename
from datetime import datetime

ALLOWED_EXTENSIONS = {'pdf'}
UPLOAD_FOLDER = 'static/documents'

def allowed_file(filename):
    """Check if the file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_document(file):
    """Save a document file and return its URL and name"""
    if not file or not allowed_file(file.filename):
        return None, None

    # Create a secure filename with timestamp
    filename = secure_filename(file.filename)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"{timestamp}_{filename}"

    # Ensure upload directory exists
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    # Save the file
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(file_path)

    # Return the URL and original filename
    document_url = f"/{UPLOAD_FOLDER}/{filename}"
    document_name = secure_filename(file.filename)

    return document_url, document_name

def delete_document(document_url):
    """Delete a document file"""
    if not document_url:
        return

    # Extract filename from URL
    filename = document_url.split('/')[-1]
    file_path = os.path.join(UPLOAD_FOLDER, filename)

    # Delete file if it exists
    if os.path.exists(file_path):
        os.remove(file_path) 