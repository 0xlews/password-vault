from flask import Blueprint, jsonify, request

api_bp = Blueprint('api', __name__)

@api_bp.route('/check-password', methods=['POST'])
def check_password():
    """
    API endpoint that previously checked for password breaches
    Now returns a simplified response since breach detection is no longer supported
    """
    return jsonify({
        'found': False,
        'message': 'Breach detection service is no longer available',
        'status': 'success'
    })