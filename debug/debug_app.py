"""
Debug version of app.py with additional routes for API testing
"""

import os
import json
from flask import Flask, render_template, redirect, url_for, flash, request, jsonify
from flask_login import LoginManager, login_required, current_user, logout_user, login_user
from dotenv import load_dotenv
from src.models.user import User, db
from src.api.routes import api_bp
from src.services.account_discovery import AccountDiscoveryService
from src.utils.web_utils import get_common_websites, categorize_email

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev_key_change_in_production')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI', 'sqlite:///passwordservice.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db.init_app(app)

# Initialize login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Register blueprints
app.register_blueprint(api_bp, url_prefix='/api')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Import all routes from main app.py
from app import index, dashboard, login, register, logout, reset_password, scan_accounts, discover_accounts

# Debug routes only available in this file
@app.route('/debug/hunter_test')
@login_required
def hunter_test():
    """Debug route to test Hunter API integration directly in browser"""
    email = current_user.email
    
    # Create AccountDiscoveryService
    discovery_service = AccountDiscoveryService()
    
    # Test all Hunter API endpoints
    results = {
        'email': email,
        'verification': {},
        'domain_search': {},
        'person_enrichment': {},
        'combined_enrichment': {},
        'discovered_accounts': []
    }
    
    try:
        # Get domain from email
        domain = email.split('@')[1]
        
        # Test email verification
        verification_result = discovery_service._hunter_verify_email(email)
        results['verification'] = verification_result
        
        # Test domain search
        domain_result = discovery_service._hunter_domain_search(domain)
        results['domain_search'] = domain_result
        
        # Test person enrichment
        person_result = discovery_service._hunter_person_enrichment(email)
        results['person_enrichment'] = person_result
        
        # Test combined enrichment
        combined_result = discovery_service._hunter_combined_enrichment(email)
        results['combined_enrichment'] = combined_result
        
        # Get discovered accounts
        accounts = discovery_service._check_with_hunter_enhanced(email)
        
        # Format accounts for display
        for account in accounts:
            results['discovered_accounts'].append({
                'service_name': account.get('service_name', ''),
                'category': account.get('category', 'Uncategorized'),
                'confidence': account.get('confidence_str', 'medium'),
                'method': account.get('method', 'api'),
                'username': account.get('username', '')
            })
        
    except Exception as e:
        return jsonify({
            'error': str(e),
            'partial_results': results
        }), 500
    
    return jsonify(results)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5001)