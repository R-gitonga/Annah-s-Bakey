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



INSERT INTO product(product_name, product_description, price, image_url, category_id, is_available) VALUES
    ('Cupcake', 'Classic cupcake with buttercream frosting', 200.00, 'images/cupcake.jpg', 1, 0);

