from flask import Blueprint, request, jsonify, session
from db import get_db

order_bp = Blueprint('orders', __name__, url_prefix='/api/orders')

@order_bp.route('/', methods=['GET'])
def get_orders():
    if 'user_id' not in session:
        return jsonify({"error": "Unauthorized"}), 401
    
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM orders WHERE buyer_id = %s", (session['user_id'],))
    orders = cursor.fetchall()
    cursor.close()
    db.close()
    
    return jsonify(orders)

@order_bp.route('/', methods=['POST'])
def create_order():
    if 'user_id' not in session:
        return jsonify({"error": "Unauthorized"}), 401
    
    data = request.json
    product_id = data.get('product_id')
    quantity = data.get('quantity', 1)
    
    if not product_id:
        return jsonify({"error": "Missing product_id"}), 400
    
    db = get_db()
    cursor = db.cursor()
    
    try:
        cursor.execute(
            "INSERT INTO orders (product_id, buyer_id, quantity, status) VALUES (%s, %s, %s, 'pending')",
            (product_id, session['user_id'], quantity)
        )
        db.commit()
        order_id = cursor.lastrowid
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        db.close()
    
    return jsonify({"message": "Order created", "order_id": order_id}), 201

@order_bp.route('/<int:order_id>', methods=['GET'])
def get_order(order_id):
    if 'user_id' not in session:
        return jsonify({"error": "Unauthorized"}), 401
    
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM orders WHERE order_id = %s AND buyer_id = %s", (order_id, session['user_id']))
    order = cursor.fetchone()
    cursor.close()
    db.close()
    
    if not order:
        return jsonify({"error": "Order not found"}), 404
    
    return jsonify(order)
