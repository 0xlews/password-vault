"""
Test script for the account discovery feature with Hunter API integration
This script simulates the account discovery process for an email address
without needing to run the full Flask application
"""

import os
import sys
from dotenv import load_dotenv
from src.services.account_discovery import AccountDiscoveryService
from flask import Flask
from src.models.user import db, User, Account

# Load environment variables
load_dotenv()

# Create a Flask app for testing
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test_discovery.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

def create_test_user(email):
    """Create a test user with the given email"""
    user = User(email=email)
    user.set_password('testpassword')
    db.session.add(user)
    db.session.commit()
    print(f"Created test user with email: {email} and ID: {user.id}")
    return user

def print_account_details(account):
    """Print details of an account in a readable format"""
    print(f"- {account.service_name} ({account.category or 'Uncategorized'})")
    print(f"  Email: {account.email}")
    if account.username:
        print(f"  Username: {account.username}")
    print(f"  Compromised: {'Yes' if account.password_compromised else 'No'}")
    print(f"  Discovery Method: {account.discovery_method or 'Unknown'}")
    print(f"  Confidence Level: {account.confidence_level or 'Unknown'}")
    print(f"  Date Discovered: {account.date_discovered}")
    print()

def test_account_discovery(email):
    """Test the account discovery service with the given email"""
    print(f"Testing account discovery for email: {email}")
    print("-" * 50)
    
    # Create an instance of the account discovery service
    service = AccountDiscoveryService()
    
    # Get user ID
    user = User.query.filter_by(email=email).first()
    if not user:
        print("User not found. Creating test user...")
        user = create_test_user(email)
    
    # Get existing accounts for this user
    existing_accounts = service.get_user_accounts(user.id)
    print(f"User has {len(existing_accounts)} existing accounts")
    
    # Scan for new accounts
    print("\nStarting account discovery scan...")
    new_accounts = service.scan_for_accounts(email)
    
    # Print results
    print(f"\nDiscovery complete. Found {len(new_accounts)} new accounts.")
    
    if new_accounts:
        print("\nNew accounts discovered:")
        for account in new_accounts:
            print_account_details(account)
    
    # Get accounts by category
    print("\nAccounts by category:")
    accounts_by_category = service.get_accounts_by_category(user.id)
    for category, accounts in accounts_by_category.items():
        print(f"\n{category} ({len(accounts)} accounts):")
        for account in accounts:
            print(f"- {account.service_name}")
    
    return new_accounts

if __name__ == '__main__':
    # Set up the database with app context
    with app.app_context():
        db.create_all()
        
        # Use command line argument or default email
        if len(sys.argv) > 1:
            test_email = sys.argv[1]
        else:
            test_email = "test@gmail.com"
            
        print(f"Using email: {test_email}")
        
        # Run the test
        discovered_accounts = test_account_discovery(test_email)
        
        # Print statistics
        print("\nTest completed.")
        print(f"Total accounts discovered: {len(discovered_accounts)}")