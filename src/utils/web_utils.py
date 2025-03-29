"""
Utilities for working with web services and websites
"""

def get_common_websites():
    """
    Returns a list of common websites for account discovery
    """
    return [
        {
            'name': 'Google',
            'domain': 'google.com',
            'check_endpoint': 'https://accounts.google.com/signin/v2/identifier',
            'category': 'Email/Productivity',
            'popular_domains': ['gmail.com', 'googlemail.com'],
            'logo': 'https://www.google.com/favicon.ico'
        },
        {
            'name': 'Facebook',
            'domain': 'facebook.com',
            'check_endpoint': 'https://www.facebook.com/login/identify',
            'category': 'Social Media',
            'logo': 'https://www.facebook.com/favicon.ico'
        },
        {
            'name': 'Twitter',
            'domain': 'twitter.com',
            'check_endpoint': 'https://twitter.com/account/begin_password_reset',
            'category': 'Social Media',
            'logo': 'https://twitter.com/favicon.ico'
        },
        {
            'name': 'LinkedIn',
            'domain': 'linkedin.com',
            'check_endpoint': 'https://www.linkedin.com/uas/request-password-reset',
            'category': 'Professional',
            'logo': 'https://www.linkedin.com/favicon.ico'
        },
        {
            'name': 'GitHub',
            'domain': 'github.com',
            'check_endpoint': 'https://github.com/password_reset',
            'category': 'Development',
            'logo': 'https://github.com/favicon.ico'
        },
        {
            'name': 'Microsoft',
            'domain': 'microsoft.com',
            'check_endpoint': 'https://account.live.com/ResetPassword.aspx',
            'category': 'Email/Productivity',
            'popular_domains': ['outlook.com', 'hotmail.com', 'live.com', 'msn.com'],
            'logo': 'https://www.microsoft.com/favicon.ico'
        },
        {
            'name': 'Apple',
            'domain': 'apple.com',
            'check_endpoint': 'https://iforgot.apple.com/',
            'category': 'Technology',
            'popular_domains': ['icloud.com', 'me.com', 'mac.com'],
            'logo': 'https://www.apple.com/favicon.ico'
        },
        {
            'name': 'Yahoo',
            'domain': 'yahoo.com',
            'check_endpoint': 'https://login.yahoo.com/forgot',
            'category': 'Email/Productivity',
            'popular_domains': ['yahoo.com', 'ymail.com', 'rocketmail.com'],
            'logo': 'https://www.yahoo.com/favicon.ico'
        },
        {
            'name': 'Amazon',
            'domain': 'amazon.com',
            'check_endpoint': 'https://www.amazon.com/ap/forgotpassword',
            'category': 'Shopping',
            'logo': 'https://www.amazon.com/favicon.ico'
        },
        {
            'name': 'Netflix',
            'domain': 'netflix.com',
            'check_endpoint': 'https://www.netflix.com/LoginHelp',
            'category': 'Entertainment',
            'logo': 'https://www.netflix.com/favicon.ico'
        },
        {
            'name': 'Instagram',
            'domain': 'instagram.com',
            'check_endpoint': 'https://www.instagram.com/accounts/password/reset/',
            'category': 'Social Media',
            'logo': 'https://www.instagram.com/favicon.ico'
        },
        {
            'name': 'Spotify',
            'domain': 'spotify.com',
            'check_endpoint': 'https://www.spotify.com/password-reset/',
            'category': 'Entertainment',
            'logo': 'https://www.spotify.com/favicon.ico'
        },
        {
            'name': 'PayPal',
            'domain': 'paypal.com',
            'check_endpoint': 'https://www.paypal.com/authflow/password-recovery/',
            'category': 'Finance',
            'logo': 'https://www.paypal.com/favicon.ico'
        },
        {
            'name': 'Adobe',
            'domain': 'adobe.com',
            'check_endpoint': 'https://account.adobe.com/security/password-reset',
            'category': 'Creative',
            'logo': 'https://www.adobe.com/favicon.ico'
        },
        {
            'name': 'Dropbox',
            'domain': 'dropbox.com',
            'check_endpoint': 'https://www.dropbox.com/forgot',
            'category': 'Storage',
            'logo': 'https://www.dropbox.com/favicon.ico'
        },
        {
            'name': 'Reddit',
            'domain': 'reddit.com',
            'check_endpoint': 'https://www.reddit.com/password',
            'category': 'Social Media',
            'logo': 'https://www.reddit.com/favicon.ico'
        },
        {
            'name': 'Pinterest',
            'domain': 'pinterest.com',
            'check_endpoint': 'https://www.pinterest.com/password/reset/',
            'category': 'Social Media',
            'logo': 'https://www.pinterest.com/favicon.ico'
        },
        {
            'name': 'Twitch',
            'domain': 'twitch.tv',
            'check_endpoint': 'https://www.twitch.tv/user/password-reset',
            'category': 'Entertainment',
            'logo': 'https://www.twitch.tv/favicon.ico'
        },
        {
            'name': 'Discord',
            'domain': 'discord.com',
            'check_endpoint': 'https://discord.com/reset',
            'category': 'Communication',
            'logo': 'https://discord.com/assets/favicon.ico'
        },
        {
            'name': 'Slack',
            'domain': 'slack.com',
            'check_endpoint': 'https://slack.com/forgot',
            'category': 'Communication',
            'logo': 'https://slack.com/favicon.ico'
        }
    ]

def get_reset_endpoints():
    """
    Returns password reset endpoints for common websites
    """
    # In a production application, this would be a more comprehensive
    # database of reset endpoints with more detailed information
    return [
        {
            'name': 'Google',
            'reset_url': 'https://accounts.google.com/signin/recovery',
            'email_field': 'identifier'
        },
        {
            'name': 'Facebook',
            'reset_url': 'https://www.facebook.com/login/identify',
            'email_field': 'email'
        },
        {
            'name': 'Twitter',
            'reset_url': 'https://twitter.com/account/begin_password_reset',
            'email_field': 'account_identifier'
        },
        {
            'name': 'LinkedIn',
            'reset_url': 'https://www.linkedin.com/uas/request-password-reset',
            'email_field': 'session_key'
        },
        {
            'name': 'GitHub',
            'reset_url': 'https://github.com/password_reset',
            'email_field': 'email'
        },
        {
            'name': 'Microsoft',
            'reset_url': 'https://account.live.com/ResetPassword.aspx',
            'email_field': 'login'
        },
        {
            'name': 'Apple',
            'reset_url': 'https://iforgot.apple.com/',
            'email_field': 'email'
        },
        {
            'name': 'Amazon',
            'reset_url': 'https://www.amazon.com/ap/forgotpassword',
            'email_field': 'email'
        },
        {
            'name': 'Netflix',
            'reset_url': 'https://www.netflix.com/LoginHelp',
            'email_field': 'email'
        },
        {
            'name': 'Instagram',
            'reset_url': 'https://www.instagram.com/accounts/password/reset/',
            'email_field': 'email'
        }
        # In a production system, this would include many more websites
    ]

def get_email_providers():
    """
    Returns a list of common email providers with their domains
    """
    return {
        'Gmail': ['gmail.com', 'googlemail.com'],
        'Yahoo': ['yahoo.com', 'ymail.com', 'rocketmail.com'],
        'Microsoft': ['outlook.com', 'hotmail.com', 'live.com', 'msn.com'],
        'Apple': ['icloud.com', 'me.com', 'mac.com'],
        'ProtonMail': ['protonmail.com', 'pm.me'],
        'AOL': ['aol.com'],
        'Zoho': ['zoho.com'],
        'GMX': ['gmx.com', 'gmx.net'],
        'Mail.com': ['mail.com'],
        'Tutanota': ['tutanota.com', 'tutanota.de']
    }

def categorize_email(email):
    """
    Identifies the provider of an email address
    """
    if not email or '@' not in email:
        return None
        
    domain = email.split('@')[1].lower()
    
    for provider, domains in get_email_providers().items():
        if domain in domains:
            return provider
    
    return None

def get_likely_services(email):
    """
    Based on the email domain and common patterns,
    returns a list of services the user is likely to have
    """
    if not email or '@' not in email:
        return []
    
    domain = email.split('@')[1].lower()
    username = email.split('@')[0].lower()
    
    likely_services = []
    
    # Check if using a provider's email implies having their service
    email_provider = categorize_email(email)
    if email_provider:
        for site in get_common_websites():
            if site['name'] == email_provider or (
                'popular_domains' in site and domain in site.get('popular_domains', [])
            ):
                likely_services.append({
                    'name': site['name'],
                    'confidence': 'high',
                    'reason': f"You use a {site['name']} email address"
                })
                break
    
    # Check for common usernames across services
    for site in get_common_websites():
        if site['name'] not in [s['name'] for s in likely_services]:
            likely_services.append({
                'name': site['name'],
                'confidence': 'medium',
                'category': site.get('category', 'Other'),
                'reason': f"Popular service, commonly used with your email provider"
            })
    
    return likely_services