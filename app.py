from flask import Flask, g, render_template, request
import sqlite3
import os


app = Flask(__name__)

products_data = [
    {"id": 1, "name": "Classic Chocolate Cake", "category": "Cakes", "image": "chocolate_cake.jpg", "description": "Rich, moist, and decadent classic chocolate cake."},
    {"id": 2, "name": "Strawberry Delight Cake", "category": "Cakes", "image": "strawberry_cake.jpg", "description": "Light sponge cake layered with fresh strawberries."},
    {"id": 3, "name": "Apple Crumble Pie", "category": "Pies", "image": "apple_pie.jpg", "description": "Warm apple filling with a buttery, crispy oat crumble."},
    {"id": 4, "name": "Blueberry Muffins", "category": "Muffins & Pastries", "image": "blueberry_muffin.jpg", "description": "Fluffy muffins bursting with sweet blueberries."},
    {"id": 5, "name": "Buttery Croissant", "category": "Muffins & Pastries", "image": "croissant.jpg", "description": "Authentic, flaky, and buttery French croissant."},
    {"id": 6, "name": "Tangy Lemon Tart", "category": "Tarts", "image": "lemon_tart.jpg", "description": "A zesty lemon filling in a delicate shortbread crust."},
    {"id": 7, "name": "Red Velvet Cupcake", "category": "Cupcakes", "image": "red_velvet.jpg", "description": "Moist red velvet with a luscious cream cheese frosting."},
    {"id": 8, "name": "Vanilla Bean Cupcake", "category": "Cupcakes", "image": "vanilla_cupcake.jpg", "description": "Simple yet elegant vanilla cupcake with vanilla bean frosting."},
    {"id": 9, "name": "Chocolate Chip Cookies", "category": "Cookies", "image": "chocolate_chip_cookies.jpg", "description": "Chewy, golden brown cookies loaded with chocolate chips."},
    {"id": 10, "name": "Oatmeal Raisin Cookies", "category": "Cookies", "image": "oatmeal_raisin_cookies.jpg", "description": "Hearty oatmeal cookies with plump raisins and spices."}
]

DATABASE = os.path.join(os.path.dirname(__file__), 'data', 'bakery.db')

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
    return g.db

@app.teardown_appcontext
def close_db(exception=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()


@app.route("/")
# def home():
#     db = get_db()
#     products = db.execute('SELECT * FROM product WHERE is_available = 1').fetchall()

def index():
    selected_category = request.args.get('category')

    if selected_category and selected_category != 'All Category':
        filtered_products = [p for p in products_data if p['category'] == selected_category]
    else:
        filtered_products = products_data

    unique_categories = sorted(list(set(p['category'] for p in products_data)))



    return render_template('index.html', products=filtered_products, categories=unique_categories, selected_category=selected_category)



if __name__ == '__main__':
    app.run(debug=True)