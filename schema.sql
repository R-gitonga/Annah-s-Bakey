CREATE TABLE IF NOT EXISTS category(
    category_id INTEGER PRIMARY KEY AUTOINCREMENT,
    category_name TEXT NOT NULL,
    category_description TEXT
);

CREATE TABLE IF NOT EXISTS product(
    product_id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_name TEXT NOT NULL,
    product_description TEXT,
    price REAL NOT NULL,
    image_url TEXT,
    category_id INTEGER,
    is_available BOOLEAN DEFAULT 1,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES category(category_id)
);



INSERT INTO category(category_name, category_description) VALUES
    ('Cakes', 'Delicious baked cakes for all occasions'),
    ('Breads', 'Freshly baked breads and buns'),
    ('Cookies', 'Crunchy and soft cookies');


INSERT INTO product(product_name, product_description, price, image_url, category_id, is_available) VALUES
    ('Chocolate Cake', 'Moist and rich chocolate layer cake', 1200.00, 'images/chocolate_cake.jpg', 1, 1),
    ('Banana Bread', 'Soft and sweet banana bread loaf', 450.00, 'images/banana_bread.jpg', 2, 1),
    ('Oatmeal Cookies', 'Healthy cookies with oats and raisins', 250.00, 'images/oatmeal_cookies.jpg', 3, 1),
    ('Vanilla Cupcake', 'Classic cupcake with buttercream frosting', 150.00, 'images/vanilla_cupcake.jpg', 1, 1);

