# Boarding Spot

A web application for matching tenants with available rooms based on preferences and criteria using the TOPSIS algorithm.

## Features

- Tenant preference management
- Room listing and management for landlords
- Advanced room search with TOPSIS-based matching
- Image upload for room listings
- Score-based filtering (safety, cleanliness, accessibility, noise level)
- Match percentage calculation for room recommendations

## Prerequisites

- Python 3.8 or higher
- Node.js 14 or higher
- npm or yarn
- PostgreSQL database

## Installation

### Backend Setup

1. Clone the repository:
```bash
git clone [repository-url]
cd boarding-spot
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
# On Windows
.\venv\Scripts\activate
# On Unix or MacOS
source venv/bin/activate
```

3. Install Python dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
Create a `.env` file in the root directory with the following variables:
```
FLASK_APP=app.py
FLASK_ENV=development
DATABASE_URL=postgresql://[username]:[password]@localhost/boarding_spot
JWT_SECRET_KEY=[your-secret-key]
```

5. Initialize the database:
```bash
flask db upgrade
```

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
# or
yarn install
```

3. Create a `.env` file in the frontend directory:
```
VITE_API_URL=http://localhost:5000
```

## Running the Application

1. Start the backend server:
```bash
# From the root directory
flask run
```

2. Start the frontend development server:
```bash
# From the frontend directory
npm run dev
# or
yarn dev
```

The application will be available at:
- Frontend: http://localhost:5174
- Backend API: http://localhost:5000

## Project Structure

```
boarding-spot/
├── frontend/               # Vue.js frontend
│   ├── src/
│   │   ├── views/         # Vue components
│   │   ├── stores/        # Pinia stores
│   │   └── router/        # Vue Router
├── static/                 # Static files
│   └── room_images/       # Uploaded room images
├── routes/                 # Flask route handlers
├── models.py              # Database models
├── app.py                 # Flask application
└── requirements.txt       # Python dependencies
```

## API Documentation

The API documentation is available at `/api/docs` when running the backend server.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 