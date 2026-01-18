from flask import Flask
from flask_cors import CORS
from backend.auth.routes import auth_bp
from backend.products.routes import products_bp
from backend.chats.routes import chats_bp
from backend.reviews.routes import reviews_bp
from backend.orders.routes import orders_bp

app = Flask(__name__, static_folder='../frontend', static_url_path='')

# Enable CORS (though now less critical since we serve frontend here)
CORS(app, supports_credentials=True)

app.secret_key = "college_marketplace_secret_2026"

# Register ALL folders (Blueprints)
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(products_bp, url_prefix='/api/products')
app.register_blueprint(chats_bp, url_prefix='/api/chats')
app.register_blueprint(reviews_bp, url_prefix='/api/reviews')
app.register_blueprint(orders_bp, url_prefix='/api/orders')

@app.route('/')
def home():
    return app.send_static_file('index.html')

@app.route('/<path:path>')
def serve_static(path):
    return app.send_static_file(path)

if __name__ == '__main__':
    app.run(debug=True, port=5000)