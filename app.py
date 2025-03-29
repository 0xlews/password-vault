import os
from flask import Flask, render_template, redirect, url_for, flash, request
from flask_login import LoginManager, login_required, current_user, logout_user, login_user
from dotenv import load_dotenv
from src.models.user import User, db
from src.api.routes import api_bp
from src.services.account_discovery import AccountDiscoveryService
from src.services.password_reset import PasswordResetService
from datetime import datetime

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

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
@login_required
def dashboard():
    # Get user accounts and their security status
    account_service = AccountDiscoveryService()
    
    accounts = account_service.get_user_accounts(current_user.id)
    
    return render_template(
        'dashboard.html', 
        accounts=accounts,
        compromised_accounts=[]
    )

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
        
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password', 'danger')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
        
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Check if email already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email already registered', 'danger')
            return render_template('register.html')
        
        # Create new user
        new_user = User(email=email)
        new_user.set_password(password)
        
        db.session.add(new_user)
        db.session.commit()
        
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

@app.route('/reset_password/<account_id>')
@login_required
def reset_password(account_id):
    reset_service = PasswordResetService()
    success = reset_service.initiate_password_reset(account_id)
    
    if success:
        flash('Password reset initiated! Check your email for reset instructions.', 'success')
    else:
        flash('Unable to initiate password reset. Please try again later.', 'danger')
    
    return redirect(url_for('dashboard'))

@app.route('/scan')
@login_required
def scan_accounts():
    account_service = AccountDiscoveryService()
    
    # Scan for new accounts
    new_accounts = account_service.scan_for_accounts(current_user.email)
    
    if new_accounts:
        flash(f'Found {len(new_accounts)} new accounts associated with your email.', 'success')
    else:
        flash('No new accounts were discovered during the scan.', 'info')
    
    return redirect(url_for('dashboard'))

@app.route('/discover', methods=['GET', 'POST'])
@login_required
def discover_accounts():
    account_service = AccountDiscoveryService()
    
    if request.method == 'POST':
        # If it's a POST request, perform the scan
        new_accounts = account_service.scan_for_accounts(current_user.email)
        if new_accounts:
            flash(f'Found {len(new_accounts)} new accounts associated with your email.', 'success')
        else:
            flash('No new accounts were discovered during the scan.', 'info')
    
    # Get accounts categorized for display
    accounts_by_category = account_service.get_accounts_by_category(current_user.id)
    
    # Get account statistics
    stats = account_service.get_account_stats(current_user.id)
    
    return render_template(
        'discover.html',
        accounts_by_category=accounts_by_category,
        stats=stats,
        total_accounts=stats['total'],
        now=datetime.utcnow()
    )

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)