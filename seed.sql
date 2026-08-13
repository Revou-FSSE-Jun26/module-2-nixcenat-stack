-- 1. Bersihkan semua data lama & reset auto-increment ID ke angka 1
TRUNCATE TABLE order_items, orders, products, categories, users RESTART IDENTITY CASCADE;

-- 2. Insert Data Users
INSERT INTO users (username, email, password_hash) VALUES
('alice_dev', 'alice@example.com', '$2b$12$eImiTXuWVxfM37uY4JANjO.gLzYj8P2/Vp7iT4hX7.3g1q2'),
('bob_builder', 'bob@example.com', '$2b$12$K89fA1.7uY4JANjO.gLzYj8P2/Vp7iT4hX7.3g1q2v9Z0'),
('charlie_tech', 'charlie@example.com', '$2b$12$L99gB2.8vZ5KBOkP.hMzZj9Q3/Wq8jU5iY8.4h2r3w0A1');

-- 3. Insert Data Categories
INSERT INTO categories (category_name, description) VALUES
('Electronics', 'Gadgets, components, and consumer electronics'),
('Apparel', 'Clothing, footwear, and wearable accessories'),
('Home & Kitchen', 'Furniture, cookware, and home appliances');

-- 4. Insert Data Products
INSERT INTO products (category_id, product_name, description, price, stock_quantity) VALUES
(1, 'Wireless Mechanical Keyboard', 'RGB tactile switch keyboard', 89.99, 45),
(1, 'Ergonomic Gaming Mouse', 'High precision 26K DPI optical sensor', 49.99, 120),
(2, 'Cotton Hoodie', '100% organic heavy fleece sweater', 39.50, 200),
(2, 'Running Shoes', 'Lightweight breathable mesh sneakers', 79.00, 30),
(3, 'Stainless Steel Coffee Maker', '12-cup programmable coffee brewer', 59.99, 15);

-- 5. Insert Data Orders
INSERT INTO orders (user_id, total_amount, status) VALUES
(1, 139.98, 'completed'),
(1, 39.50, 'processing'),
(2, 138.99, 'completed');

-- 6. Insert Data Order Items
INSERT INTO order_items (order_id, product_id, quantity, unit_price) VALUES
(1, 1, 1, 89.99),
(1, 2, 1, 49.99),
(2, 3, 1, 39.50),
(3, 4, 1, 79.00),
(3, 3, 1, 59.99);