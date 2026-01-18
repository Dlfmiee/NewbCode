from flask import Blueprint, request, jsonify, session
from db import get_db

review_bp = Blueprint('reviews', __name__, url_prefix='/api/reviews')

@review_bp.route('/product/<int:product_id>', methods=['GET'])
def get_reviews(product_id):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM reviews WHERE product_id = %s", (product_id,))
    reviews = cursor.fetchall()
    cursor.close()
    db.close()
    
    return jsonify(reviews)

@review_bp.route('/', methods=['POST'])
def create_review():
    if 'user_id' not in session:
        return jsonify({"error": "Unauthorized"}), 401
    
    data = request.json
    product_id = data.get('product_id')
    rating = data.get('rating')
    comment = data.get('comment')
    
    if not all([product_id, rating, comment]):
        return jsonify({"error": "Missing fields"}), 400
    
    if not (1 <= rating <= 5):
        return jsonify({"error": "Rating must be between 1 and 5"}), 400
    
    db = get_db()
    cursor = db.cursor()
    
    try:
        cursor.execute(
            "INSERT INTO reviews (product_id, user_id, rating, comment) VALUES (%s, %s, %s, %s)",
            (product_id, session['user_id'], rating, comment)
        )
        db.commit()
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        db.close()
    
    return jsonify({"message": "Review created"}), 201
