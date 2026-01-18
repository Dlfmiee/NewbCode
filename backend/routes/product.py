from flask import Blueprint, request, jsonify
from db import get_db

product_bp = Blueprint('products', __name__, url_prefix='/api/products')

@product_bp.route('/', methods=['GET'])
def get_products():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    cursor.close()
    db.close()
    
    return jsonify(products)

@product_bp.route('/<int:product_id>', methods=['GET'])
def get_product(product_id):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM products WHERE product_id = %s", (product_id,))
    product = cursor.fetchone()
    cursor.close()
    db.close()
    
    if not product:
        return jsonify({"error": "Product not found"}), 404
    
    return jsonify(product)

@product_bp.route('/', methods=['POST'])
def create_product():
    data = request.json
    title = data.get('title')
    description = data.get('description')
    price = data.get('price')
    user_id = data.get('user_id')
    
    if not all([title, description, price, user_id]):
        return jsonify({"error": "Missing fields"}), 400
    
    db = get_db()
    cursor = db.cursor()
    
    try:
        cursor.execute(
            "INSERT INTO products (title, description, price, user_id) VALUES (%s, %s, %s, %s)",
            (title, description, price, user_id)
        )
        db.commit()
        product_id = cursor.lastrowid
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        db.close()
    
    return jsonify({"message": "Product created", "product_id": product_id}), 201

@product_bp.route('/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    db = get_db()
    cursor = db.cursor()
    
    try:
        cursor.execute("DELETE FROM products WHERE product_id = %s", (product_id,))
        db.commit()
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        db.close()
    
    return jsonify({"message": "Product deleted"})
