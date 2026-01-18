-- =========================
-- CREATE DATABASE
-- =========================
CREATE DATABASE IF NOT EXISTS college_marketplace;
USE college_marketplace;

-- =========================
-- USERS
-- =========================
CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    phone_number VARCHAR(20),
    profile_image VARCHAR(255),
    role ENUM('buyer','seller','both') DEFAULT 'both',
    status ENUM('active','suspended') DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =========================
-- CATEGORIES (SELF-REFERENCE)
-- =========================
CREATE TABLE categories (
    category_id INT AUTO_INCREMENT PRIMARY KEY,
    category_name VARCHAR(100) NOT NULL,
    parent_category_id INT,
    FOREIGN KEY (parent_category_id)
        REFERENCES categories(category_id)
        ON DELETE SET NULL
);

-- =========================
-- PRODUCTS
-- =========================
CREATE TABLE products (
    product_id INT AUTO_INCREMENT PRIMARY KEY,
    seller_id INT NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10,2) NOT NULL,
    quantity INT DEFAULT 1,
    product_condition ENUM('new','used') DEFAULT 'used',
    status ENUM('available','sold','hidden') DEFAULT 'available',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (seller_id)
        REFERENCES users(user_id)
        ON DELETE CASCADE
);

-- =========================
-- PRODUCT IMAGES
-- =========================
CREATE TABLE product_images (
    image_id INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT NOT NULL,
    image_url VARCHAR(255) NOT NULL,
    FOREIGN KEY (product_id)
        REFERENCES products(product_id)
        ON DELETE CASCADE
);

-- =========================
-- PRODUCT ↔ CATEGORY (MANY TO MANY)
-- =========================
CREATE TABLE product_categories (
    product_id INT NOT NULL,
    category_id INT NOT NULL,
    PRIMARY KEY (product_id, category_id),
    FOREIGN KEY (product_id)
        REFERENCES products(product_id)
        ON DELETE CASCADE,
    FOREIGN KEY (category_id)
        REFERENCES categories(category_id)
        ON DELETE CASCADE
);

-- =========================
-- ORDERS
-- =========================
CREATE TABLE orders (
    order_id INT AUTO_INCREMENT PRIMARY KEY,
    buyer_id INT NOT NULL,
    order_status ENUM('pending','paid','completed','cancelled') DEFAULT 'pending',
    total_amount DECIMAL(10,2),
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (buyer_id)
        REFERENCES users(user_id)
        ON DELETE CASCADE
);

-- =========================
-- ORDER ITEMS
-- =========================
CREATE TABLE order_items (
    order_item_id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    product_id INT NOT NULL,
    seller_id INT NOT NULL,
    price_at_purchase DECIMAL(10,2) NOT NULL,
    quantity INT DEFAULT 1,
    FOREIGN KEY (order_id)
        REFERENCES orders(order_id)
        ON DELETE CASCADE,
    FOREIGN KEY (product_id)
        REFERENCES products(product_id)
        ON DELETE CASCADE,
    FOREIGN KEY (seller_id)
        REFERENCES users(user_id)
        ON DELETE CASCADE
);

-- =========================
-- PAYMENTS
-- =========================
CREATE TABLE payments (
    payment_id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    payment_method ENUM('cash','bank_transfer','e_wallet') DEFAULT 'cash',
    payment_status ENUM('pending','paid','failed') DEFAULT 'pending',
    paid_at TIMESTAMP NULL,
    FOREIGN KEY (order_id)
        REFERENCES orders(order_id)
        ON DELETE CASCADE
);

-- =========================
-- CHATS
-- =========================
CREATE TABLE chats (
    chat_id INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT NOT NULL,
    buyer_id INT NOT NULL,
    seller_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (product_id)
        REFERENCES products(product_id)
        ON DELETE CASCADE,
    FOREIGN KEY (buyer_id)
        REFERENCES users(user_id)
        ON DELETE CASCADE,
    FOREIGN KEY (seller_id)
        REFERENCES users(user_id)
        ON DELETE CASCADE
);

-- =========================
-- MESSAGES
-- =========================
CREATE TABLE messages (
    message_id INT AUTO_INCREMENT PRIMARY KEY,
    chat_id INT NOT NULL,
    sender_id INT NOT NULL,
    message_text TEXT NOT NULL,
    sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (chat_id)
        REFERENCES chats(chat_id)
        ON DELETE CASCADE,
    FOREIGN KEY (sender_id)
        REFERENCES users(user_id)
        ON DELETE CASCADE
);

-- =========================
-- REVIEWS
-- =========================
CREATE TABLE reviews (
    review_id INT AUTO_INCREMENT PRIMARY KEY,
    order_item_id INT NOT NULL,
    reviewer_id INT NOT NULL,
    rating INT CHECK (rating BETWEEN 1 AND 5),
    comment TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (order_item_id)
        REFERENCES order_items(order_item_id)
        ON DELETE CASCADE,
    FOREIGN KEY (reviewer_id)
        REFERENCES users(user_id)
        ON DELETE CASCADE
);
