from flask import Blueprint, request, jsonify, session
from db import get_db
from datetime import datetime

chat_bp = Blueprint('chat', __name__, url_prefix='/api/chat')

@chat_bp.route('/messages/<int:user_id>', methods=['GET'])
def get_messages(user_id):
    if 'user_id' not in session:
        return jsonify({"error": "Unauthorized"}), 401
    
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute(
        "SELECT * FROM messages WHERE (sender_id = %s AND receiver_id = %s) OR (sender_id = %s AND receiver_id = %s) ORDER BY timestamp ASC",
        (session['user_id'], user_id, user_id, session['user_id'])
    )
    messages = cursor.fetchall()
    cursor.close()
    db.close()
    
    return jsonify(messages)

@chat_bp.route('/send', methods=['POST'])
def send_message():
    if 'user_id' not in session:
        return jsonify({"error": "Unauthorized"}), 401
    
    data = request.json
    receiver_id = data.get('receiver_id')
    message = data.get('message')
    
    if not all([receiver_id, message]):
        return jsonify({"error": "Missing fields"}), 400
    
    db = get_db()
    cursor = db.cursor()
    
    try:
        cursor.execute(
            "INSERT INTO messages (sender_id, receiver_id, message, timestamp) VALUES (%s, %s, %s, NOW())",
            (session['user_id'], receiver_id, message)
        )
        db.commit()
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        db.close()
    
    return jsonify({"message": "Message sent"}), 201
