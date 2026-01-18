from flask import Blueprint, request, jsonify, session
from backend.db import supabase
import bcrypt

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    # Hash password for security
    hashed_pw = bcrypt.hashpw(data['password'].encode(), bcrypt.gensalt()).decode()

    try:
        response = supabase.table("users").insert({
            "full_name": data.get('full_name'),
            "email": data.get('email'),
            "password_hash": hashed_pw,
            "role": data.get('role', 'both')
        }).execute()
        return jsonify({"success": True, "user": response.data[0]}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@auth_bp.route('/me', methods=['GET'])
def get_current_user():
    if 'user_id' not in session:
        return jsonify({"error": "No session"}), 401
    
    user = supabase.table("users").select("full_name, email, avatar_url, role").eq("user_id", session['user_id']).single().execute()
    return jsonify(user.data), 200

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user_query = supabase.table("users").select("*").eq("email", data['email']).execute()
    user = user_query.data[0] if user_query.data else None

    if user and bcrypt.checkpw(data['password'].encode(), user['password_hash'].encode()):
        session['user_id'] = user['user_id']
        return jsonify({
            "success": True, 
            "message": "Logged in!",
            "user": {
                "name": user['full_name'],
                "email": user['email'],
                "role": user['role']
            }
        }), 200
    
    return jsonify({"error": "Invalid email or password"}), 401