# login_handler.py
from flask import Blueprint, request, session, redirect, url_for, jsonify
from werkzeug.security import check_password_hash
from db_insert import fetch_user_profile_by_email
# Import your function to fetch a single user by ID (we'll assume this is needed in user_routes)
# from db_insert import fetch_user_by_id 

login_bp = Blueprint('login_bp', __name__, url_prefix='/user')

@login_bp.route('/login', methods=['POST'])
def handle_login_request():
    # Attempt to parse JSON data from the request body
    try:
        data = request.get_json()
        if not data or 'email' not in data or 'password' not in data:
            return jsonify({"error": "Missing email or password in request."}), 400
        
        email = data['email']
        password = data['password']
    except Exception as e:
        # Handle cases where the request body is not valid JSON
        return jsonify({"error": "Invalid data format."}), 400
    
    # 1. Fetch user data from MySQL
    user = fetch_user_profile_by_email(email) 
    
    # 2. Verify user existence and password
    if user and 'password' in user and check_password_hash(user['password'], password):
        # SUCCESS! Start session
        session['loggedin'] = True
        # 🔑 CRITICAL CHANGE: Store the user's primary key ID
        session['user_id'] = user['id'] 
        session['email'] = user['email']
        
        # Return a simple success response; JavaScript will handle the redirect
        return jsonify({"message": "Login successful"}), 200
    else:
        # FAILURE!
        return jsonify({"error": "Invalid email or password"}), 401