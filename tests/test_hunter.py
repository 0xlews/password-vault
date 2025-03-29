"""
Test script for Hunter API integration
Run this script to test the Hunter API integration outside the main application
"""

import os
from pyhunter import PyHunter
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_hunter_api(email):
    """
    Test the Hunter API with a given email address
    Prints detailed information about the email verification and domain lookup
    """
    # Get API key from environment variables
    api_key = os.getenv('HUNTER_API_KEY')
    if not api_key:
        print("Error: Hunter API key not found in environment variables.")
        print("Please add HUNTER_API_KEY to your .env file.")
        return
    
    hunter = PyHunter(api_key)
    
    print(f"Testing Hunter API for email: {email}")
    print("-" * 50)
    
    # Test email verification
    try:
        print("Email verification:")
        verification = hunter.email_verifier(email)
        print(f"Result: {verification.get('result', 'Unknown')}")
        print(f"Score: {verification.get('score', 'Unknown')}")
        print(f"Deliverable: {verification.get('deliverable', 'Unknown')}")
        print("-" * 50)
    except Exception as e:
        print(f"Error verifying email: {str(e)}")
    
    # Test domain search
    try:
        print("Domain search:")
        domain = email.split('@')[1]
        domain_info = hunter.domain_search(domain)
        
        print(f"Domain: {domain}")
        organization = domain_info.get('data', {}).get('organization')
        print(f"Organization: {organization if organization else 'Not found'}")
        
        pattern = domain_info.get('data', {}).get('pattern')
        print(f"Email pattern: {pattern if pattern else 'Not found'}")
        
        print("\nRelated domains:")
        related_domains = domain_info.get('data', {}).get('related_domains', [])
        for domain in related_domains[:5]:  # Show first 5 domains
            print(f"- {domain.get('domain')}")
        
        print("\nEmail distribution by domain:")
        emails_count = domain_info.get('data', {}).get('emails_count')
        print(f"Total emails found: {emails_count}")
    except Exception as e:
        print(f"Error searching domain: {str(e)}")

if __name__ == "__main__":
    # You can test with any email address
    test_email = input("Enter an email address to test (or press Enter for default test@gmail.com): ")
    if not test_email:
        test_email = "test@gmail.com"
    
    test_hunter_api(test_email)