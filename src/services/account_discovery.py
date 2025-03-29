import requests
import logging
import hashlib
import os
import time
import json
from datetime import datetime, timedelta
from sqlalchemy.exc import SQLAlchemyError
from src.models.user import Account, db
from src.utils.web_utils import get_common_websites, categorize_email, get_likely_services
from pyhunter import PyHunter

class AccountDiscoveryService:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.common_sites = get_common_websites()
        
        # API keys from environment variables
        self.haveibeenpwned_api_key = os.getenv('HAVEIBEENPWNED_API_KEY')
        self.clearbit_api_key = os.getenv('CLEARBIT_API_KEY')
        self.fullcontact_api_key = os.getenv('FULLCONTACT_API_KEY')
        self.hunter_api_key = os.getenv('HUNTER_API_KEY')
        self.holehe_enabled = os.getenv('HOLEHE_ENABLED', 'false').lower() == 'true'
        
        # Initialize Hunter API client if API key is provided
        self.hunter = PyHunter(self.hunter_api_key) if self.hunter_api_key else None
        
        # Hunter API base URL
        self.hunter_api_base = "https://api.hunter.io/v2"

    def get_user_accounts(self, user_id):
        """Get all accounts associated with a user"""
        try:
            return Account.query.filter_by(user_id=user_id).all()
        except SQLAlchemyError as e:
            self.logger.error(f"Database error retrieving accounts: {str(e)}")
            return []
    
    def scan_for_accounts(self, email):
        """
        Scan for accounts associated with the given email
        Returns a list of new accounts found
        Uses Hunter API for verification
        """
        self.logger.info(f"Starting account scan for {email}")
        new_accounts = []
        
        # Get user from email
        from src.models.user import User
        user = User.query.filter_by(email=email).first()
        
        if not user:
            self.logger.error(f"User with email {email} not found")
            return []
        
        # Get existing accounts to avoid duplicates
        existing_accounts = {acc.service_name.lower(): acc for acc in self.get_user_accounts(user.id)}
        
        # Use Hunter API to discover accounts
        hunter_results = self._check_with_hunter_enhanced(email)
        
        # Filter duplicates
        service_map = {}
        for account in hunter_results:
            service_name = account['service_name']
            # Keep the account with higher confidence if duplicate
            if service_name not in service_map or account['confidence'] > service_map[service_name]['confidence']:
                service_map[service_name] = account
        
        # Create new account records
        for service_name, account_data in service_map.items():
            if service_name.lower() not in existing_accounts:
                # Create new account record
                new_account = Account(
                    user_id=user.id,
                    service_name=service_name,
                    email=email,
                    username=account_data.get('username'),
                    last_breach_check=datetime.utcnow(),
                    date_discovered=datetime.utcnow(),
                    password_compromised=account_data.get('compromised', False),
                    category=account_data.get('category', 'Uncategorized'),
                    confidence_level=account_data.get('confidence_str', 'medium'),
                    discovery_method=account_data.get('method', 'api')
                )
                db.session.add(new_account)
                new_accounts.append(new_account)
        
        if new_accounts:
            try:
                db.session.commit()
                self.logger.info(f"Found {len(new_accounts)} new accounts for {email}")
            except SQLAlchemyError as e:
                self.logger.error(f"Database error saving accounts: {str(e)}")
                db.session.rollback()
                return []
                
        return new_accounts
    
    def _check_with_hunter_enhanced(self, email):
        """Enhanced check using multiple Hunter API endpoints"""
        if not self.hunter_api_key:
            self.logger.warning("Hunter API key not configured")
            return []
        
        accounts = []
        username = email.split('@')[0]
        domain = email.split('@')[1]
        
        try:
            # 1. Email verification
            verification_result = self._hunter_verify_email(email)
            
            # 2. Domain search for the email domain
            domain_info = self._hunter_domain_search(domain)
            
            # 3. Person enrichment for additional details
            person_info = self._hunter_person_enrichment(email)
            
            # 4. Combined enrichment to get comprehensive data
            combined_info = self._hunter_combined_enrichment(email)
            
            # Process domain results
            if domain_info.get('data'):
                # Get company name if available
                company_name = domain_info.get('data', {}).get('organization', '')
                company_industry = domain_info.get('data', {}).get('industry', '')
                
                if company_name:
                    accounts.append({
                        'service_name': company_name,
                        'category': company_industry or 'Work',
                        'confidence': 0.9,
                        'confidence_str': 'high',
                        'method': 'hunter_domain',
                        'username': username,
                        'compromised': False
                    })
                
                # Check for related domains that might indicate other services
                related_domains = domain_info.get('data', {}).get('related_domains', [])
                for related in related_domains:
                    if 'domain' in related:
                        related_domain = related['domain']
                        # Try to match domain to a known service
                        service = self._get_service_from_domain(related_domain)
                        if service:
                            accounts.append({
                                'service_name': service,
                                'category': self._get_category_for_service(service),
                                'confidence': 0.7,
                                'confidence_str': 'medium',
                                'method': 'hunter_related',
                                'username': username,
                                'compromised': False
                            })
            
            # Process person enrichment data
            if person_info.get('data'):
                social_accounts = person_info.get('data', {}).get('social_accounts', [])
                for account in social_accounts:
                    if 'type' in account and 'handle' in account:
                        service_name = account['type'].capitalize()
                        accounts.append({
                            'service_name': service_name,
                            'category': 'Social Media',
                            'confidence': 0.85,
                            'confidence_str': 'high',
                            'method': 'hunter_person',
                            'username': account['handle'],
                            'compromised': False
                        })
            
            # Process combined enrichment data
            if combined_info.get('data'):
                # Additional data points could be extracted here
                pass
                
        except Exception as e:
            self.logger.error(f"Error with Hunter API: {str(e)}")
            
        return accounts
    
    def _hunter_verify_email(self, email):
        """Call Hunter's email verification API directly"""
        try:
            url = f"{self.hunter_api_base}/email-verifier?email={email}&api_key={self.hunter_api_key}"
            response = requests.get(url)
            return response.json() if response.status_code == 200 else {}
        except Exception as e:
            self.logger.error(f"Error verifying email with Hunter API: {str(e)}")
            return {}
    
    def _hunter_domain_search(self, domain):
        """Call Hunter's domain search API directly"""
        try:
            url = f"{self.hunter_api_base}/domain-search?domain={domain}&api_key={self.hunter_api_key}"
            response = requests.get(url)
            return response.json() if response.status_code == 200 else {}
        except Exception as e:
            self.logger.error(f"Error searching domain with Hunter API: {str(e)}")
            return {}
    
    def _hunter_person_enrichment(self, email):
        """Call Hunter's person enrichment API"""
        try:
            url = f"{self.hunter_api_base}/people/find?email={email}&api_key={self.hunter_api_key}"
            response = requests.get(url)
            return response.json() if response.status_code == 200 else {}
        except Exception as e:
            self.logger.error(f"Error with Hunter person enrichment API: {str(e)}")
            return {}
    
    def _hunter_combined_enrichment(self, email):
        """Call Hunter's combined enrichment API"""
        try:
            url = f"{self.hunter_api_base}/combined/find?email={email}&api_key={self.hunter_api_key}"
            response = requests.get(url)
            return response.json() if response.status_code == 200 else {}
        except Exception as e:
            self.logger.error(f"Error with Hunter combined enrichment API: {str(e)}")
            return {}
    
    def _check_with_hunter(self, email):
        """Legacy check using pyhunter library"""
        # For backward compatibility, now redirects to the enhanced version
        return self._check_with_hunter_enhanced(email)
    
    def _get_service_from_domain(self, domain):
        """Map a domain to a service name"""
        # Remove TLD and subdomains for matching
        parts = domain.split('.')
        if len(parts) >= 2:
            main_name = parts[-2].lower()
        else:
            main_name = domain.lower()
        
        # Check common domains
        domain_to_service = {
            'google': 'Google',
            'facebook': 'Facebook',
            'twitter': 'Twitter',
            'linkedin': 'LinkedIn',
            'github': 'GitHub',
            'microsoft': 'Microsoft',
            'apple': 'Apple',
            'amazon': 'Amazon',
            'netflix': 'Netflix',
            'spotify': 'Spotify',
            'dropbox': 'Dropbox',
            'adobe': 'Adobe',
            'slack': 'Slack',
            'zoom': 'Zoom',
            'reddit': 'Reddit'
        }
        
        return domain_to_service.get(main_name, main_name.capitalize())
    
    def _get_category_for_service(self, service_name):
        """Get the category for a service from our database"""
        for site in self.common_sites:
            if site['name'].lower() == service_name.lower():
                return site.get('category', 'Uncategorized')
        return 'Uncategorized'
    
    def get_accounts_by_category(self, user_id):
        """Get user accounts grouped by category"""
        accounts = self.get_user_accounts(user_id)
        categorized = {}
        
        for account in accounts:
            category = account.category or "Uncategorized"
            if category not in categorized:
                categorized[category] = []
            categorized[category].append(account)
        
        return categorized
    
    def get_account_stats(self, user_id):
        """Get statistics about user accounts"""
        accounts = self.get_user_accounts(user_id)
        total = len(accounts)
        compromised = sum(1 for acc in accounts if acc.password_compromised)
        categories = {}
        recent_discoveries = []
        
        # Compile statistics
        for account in accounts:
            category = account.category or "Uncategorized"
            if category in categories:
                categories[category] += 1
            else:
                categories[category] = 1
            
            # Add recent discoveries (accounts found in last 30 days)
            if account.date_discovered and (datetime.utcnow() - account.date_discovered).days <= 30:
                recent_discoveries.append(account)
        
        return {
            'total': total,
            'compromised': compromised,
            'safe': total - compromised,
            'categories': categories,
            'recent_discoveries': sorted(recent_discoveries, 
                                        key=lambda a: a.date_discovered if a.date_discovered else datetime.min, 
                                        reverse=True)
        }