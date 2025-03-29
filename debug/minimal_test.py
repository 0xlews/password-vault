"""
Minimal test script for Hunter API web integration
This script tests the Hunter API integration and outputs results to console
"""

import os
import json
import requests
from dotenv import load_dotenv
from pyhunter import PyHunter
from flask import Flask
from src.models.user import db, User, Account
from src.services.account_discovery import AccountDiscoveryService

# Load environment variables
load_dotenv()

# Create a Flask app with test database
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test_hunter_integration.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

def test_hunter_web_integration(email):
    """Test Hunter API integration for web app"""
    print(f"Testing Hunter API web integration for {email}")
    print("-" * 50)
    
    # Initialize discovery service
    service = AccountDiscoveryService()
    
    # Test all APIs
    print("1. Testing Hunter Email Verification API")
    verification = service._hunter_verify_email(email)
    if verification:
        print(f"  Result: {verification.get('data', {}).get('result', 'Unknown')}")
        print(f"  Score: {verification.get('data', {}).get('score', 'Unknown')}")
        print(f"  Status: {verification.get('data', {}).get('status', 'Unknown')}")
    else:
        print("  No verification results")
    print()
    
    # Domain search
    domain = email.split('@')[1]
    print(f"2. Testing Hunter Domain Search API for {domain}")
    domain_info = service._hunter_domain_search(domain)
    if domain_info and 'data' in domain_info:
        print(f"  Organization: {domain_info.get('data', {}).get('organization', 'Unknown')}")
        print(f"  Pattern: {domain_info.get('data', {}).get('pattern', 'Unknown')}")
        related_domains = domain_info.get('data', {}).get('related_domains', [])
        print(f"  Related domains: {len(related_domains)} found")
        for i, domain in enumerate(related_domains[:3]):  # Show first 3
            if 'domain' in domain:
                print(f"    - {domain['domain']}")
        if len(related_domains) > 3:
            print(f"    ... ({len(related_domains) - 3} more)")
    else:
        print("  No domain search results")
    print()
    
    # Person enrichment
    print("3. Testing Hunter Person Enrichment API")
    person_info = service._hunter_person_enrichment(email)
    if person_info and 'data' in person_info:
        print(f"  Full name: {person_info.get('data', {}).get('full_name', 'Unknown')}")
        print(f"  Position: {person_info.get('data', {}).get('position', 'Unknown')}")
        print(f"  LinkedIn: {person_info.get('data', {}).get('linkedin', 'Unknown')}")
    else:
        print("  No person enrichment results")
    print()
    
    # Combined enrichment
    print("4. Testing Hunter Combined Enrichment API")
    combined_info = service._hunter_combined_enrichment(email)
    if combined_info and 'data' in combined_info:
        print("  Combined data received")
    else:
        print("  No combined enrichment results")
    print()
    
    # Account discovery
    print("5. Testing Account Discovery with Hunter API")
    accounts = service._check_with_hunter_enhanced(email)
    print(f"  Found {len(accounts)} potential accounts:")
    for i, account in enumerate(accounts, 1):
        print(f"  {i}. {account.get('service_name')} ({account.get('category', 'Unknown')})")
        print(f"     Method: {account.get('method', 'Unknown')}")
        print(f"     Confidence: {account.get('confidence_str', 'Unknown')}")
        print(f"     Username: {account.get('username', 'Unknown')}")
        print()
    
    return accounts

def save_accounts_to_db(email, accounts):
    """Save discovered accounts to database for testing"""
    with app.app_context():
        # Create a test user if not exists
        user = User.query.filter_by(email=email).first()
        if not user:
            user = User(email=email)
            user.set_password('testpassword')
            db.session.add(user)
            db.session.commit()
            print(f"Created test user with email {email}")
        
        # Add accounts
        for account_data in accounts:
            account = Account(
                user_id=user.id,
                service_name=account_data.get('service_name', 'Unknown Service'),
                email=email,
                username=account_data.get('username'),
                category=account_data.get('category', 'Uncategorized'),
                confidence_level=account_data.get('confidence_str', 'medium'),
                discovery_method=account_data.get('method', 'api'),
                password_compromised=account_data.get('compromised', False),
                date_discovered=None  # Will be set to current date automatically
            )
            db.session.add(account)
        
        db.session.commit()
        print(f"Saved {len(accounts)} accounts to test database")

if __name__ == "__main__":
    # Create database if not exists
    with app.app_context():
        db.create_all()
    
    # Ask for test email
    test_email = input("Enter an email to test (or press Enter for test@gmail.com): ")
    if not test_email:
        test_email = "test@gmail.com"
    
    # Run test
    discovered_accounts = test_hunter_web_integration(test_email)
    
    # Ask if we should save to database
    save_to_db = input("Save discovered accounts to test database? (y/n): ")
    if save_to_db.lower() == 'y':
        save_accounts_to_db(test_email, discovered_accounts)
        print("Accounts saved to test database")