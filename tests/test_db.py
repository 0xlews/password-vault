from flask import Flask
from src.models.user import db

# Create a minimal Flask application
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///passwordservice.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db.init_app(app)

# Test database connection
with app.app_context():
    try:
        # Try a simple query to validate connection
        result = db.session.execute(db.select(db.text("1"))).scalar()
        print(f"Database connection test: {result}")
        print("Database connection successful!")
        
    except Exception as e:
        print(f"Database connection error: {str(e)}")