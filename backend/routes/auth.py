from flask import Blueprint, request, jsonify, session
from db import get_db
import bcrypt

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    full_name = data.get('full_name')
    email = data.get('email')
    password = data.get('password')

    if not all([full_name, email, password]):
        return jsonify({"error": "Missing fields"}), 400

    hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    db = get_db()
    cursor = db.cursor()

    try:
        cursor.execute(
            "INSERT INTO users (full_name, email, password_hash) VALUES (%s, %s, %s)",
            (full_name, email, hashed_pw)
        )
        db.commit()
    except:
        return jsonify({"error": "Email already exists"}), 400
    finally:
        cursor.close()
        db.close()

    return jsonify({"message": "User registered successfully"}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
    user = cursor.fetchone()
    cursor.close()
    db.close()

    if not user:
        return jsonify({"error": "Invalid credentials"}), 401

    if not bcrypt.checkpw(password.encode(), user['password_hash'].encode()):
        return jsonify({"error": "Invalid credentials"}), 401

    # Save session
    session['user_id'] = user['user_id']
    session['role'] = user['role']

    return jsonify({
        "message": "Login successful",
        "user": {
            "id": user['user_id'],
            "name": user['full_name'],
            "role": user['role']
        }
    })

@auth_bp.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({"message": "Logged out"})

@auth_bp.route('/me', methods=['GET'])
def me():
    if 'user_id' not in session:
        return jsonify({"user": None}), 401

    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute(
        "SELECT user_id, full_name, email, role FROM users WHERE user_id = %s",
        (session['user_id'],)
    )
    user = cursor.fetchone()
    cursor.close()
    db.close()

    return jsonify(user)
