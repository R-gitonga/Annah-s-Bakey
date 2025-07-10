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

CREATE TABLE IF NOT EXISTS testimonials(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_name TEXT NOT NULL,
    customer_location TEXT,
    testimonial_text TEXT NOT NULL,
    rating INTEGER,
    image_url TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_approved BOOLEAN DEFAULT 0
);


-- INSERT INTO product(product_name, product_description, price, image_url, category_id, is_available) VALUES
--     ('Chocolate Cake', 'A vibrant, moist chocolate cake with a rich cream cheese frosting.', 1500.00, 'images/chocolate_cake.jpg', 1, 1),
--     ('Condensed Milk Toast', 'Soft and sweet condensed milk bread.', 500.00, 'images/condensed-milk-toast.jpg', 1, 2),
--     ('Banana Bread', 'Sweet Banana Bread.', 500.00, 'images/banana_bread.jpg', 2, 1),
--     ('Oatmeal Cookies', 'A classic comfort treat.', 300.00, 'images/oatmeal_cookies.jpg', 3, 1),
--     ('Blueberry Muffins', 'Sweet Muffins.', 300.00, 'images/blueberry-muffins.jpg', 10, 1),
--     ('Butter Croissants', 'Soft and soft buttery croissants.', 500.00, 'images/butter-croissant.jpg', 10, 1),
--     ('Blue Cupcakes', 'Moist and spiced cupcake, topped with tangy cream cheese frosting.', 600.00, 'images/blue-cupcakes.jpg', 12, 1),
--     ('Cupcakes', 'Moist and sweet cupcakes topped with tangy cream cheese frosting.', 600.00, 'images/cupcake.jpg', 12, 1),
--     ('Chocolated Frosted Donut', 'A classic yeast donut, generously topped with a decadent chocolate frosting.', 200, 'images/delicious-donuts.jpg', 13, 1),
--     ('Pastel Iced Donuts', 'A classic pastel icing donuts', 200.00, 'images/pastel-iced-donuts.jpg', 13, 1),
--     ('Savory Bites', 'Sweet pastries and baked goods', 200.00, 'images/savory-bites.jpg', 14, 1),
--     ('Vanilla Cupcake', 'Moist and sweet vanilla cupcakes topped with tangy cream cheese frosting.', 600.00, 'images/vanilla_cupcake.jpg', 12, 1),
--     ('Pecan Pie Tart', 'A mini version of the classic pecan pie, with a rich, nutty filling and buttery crust.', 500.00, 'images/tarts.jpg', 11, 1),
--     ('American Heritage Cookie', 'A classic comfort treat.', 300.00, 'images/american-heritage-chocolate-cookie,jpg', 3, 1),
--     ('Red Cupcake', 'Moist and sweet cupcakes topped with tangy cream cheese frosting.', 600.00, 'images/red-cupcakes.jpg', 12, 1),
--     ('Brown Bread', 'Sour brown Bread', 500.00, 'images/debbie-bread.jpg', 2, 1),
--     ('White Icing Cake', 'Cake with white Icing and flower on top', 2000.00, 'images/white-icing-cake.jpg', 1, 1),
--     ('Pink White Cake', 'Cake with white and pink icing on ceramic plate', 1500.00, 'images/pink-white-cake.jpg', 1, 1),
--     ('Fondant Cake', 'Fondant cake with stand', 2000.00, 'images/fondant-cake.jpg', 1, 1);




