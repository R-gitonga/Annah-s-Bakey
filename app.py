from flask import Flask, g, render_template, request, jsonify
import sqlite3
import os


app = Flask(__name__)



DATABASE = os.path.join(os.path.dirname(__file__), 'data', 'bakery.db')

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row    #allows you to access columns by name
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
    db = get_db()

    selected_category_name = request.args.get('category')

    # 1. get all categories for dropdon menu
    #query the category table

    categories_cursor = db.execute('SELECT category_id, category_name FROM category ORDER BY category_name')
    all_categories = categories_cursor.fetchall() #fetches rows, accesible as dictionaries

    # 2. Build the query for products

    # need to join product and category tabe=les to get the category name for display
    # and filter by category ID if category is selected

    product_query = """
            SELECT
                p.product_id,
                p.product_name AS product_name,
                p.product_description AS product_description,
                p.price AS price,
                p.image_url AS image_url,
                c.category_name AS category_name,
                p.is_available
            FROM
                product p
            JOIN
                category c ON p.category_id = c.category_id
            WHERE
                p.is_available == 1
    """
    query_params = []

    if selected_category_name and selected_category_name != "All Categories":
        #if a specific category is selected add to where clause
        product_query += " AND c.category_name = ?"
        query_params.append(selected_category_name)

    product_query += " ORDER BY p.product_name" #order products for consistent display


    products_cursor = db.execute(product_query, query_params)
    filtered_products = products_cursor.fetchall()

    return render_template('index.html', 
                           products=filtered_products,
                           categories=all_categories,
                           selected_category=selected_category_name)

# AJAX endpoint for filtering
@app.route('/filter_products', methods=['GET'])
def filter_products_ajax():
    db = get_db()
    selected_category_name = request.args.get('category')

    product_query = """
            SELECT
                p.product_id,
                p.product_name AS product_name,
                p.product_description AS product_description,
                p.price AS price,
                p.image_url AS image_url,
                c.category_name AS category_name,
                p.is_available
            FROM
                product p
            JOIN
                category c ON p.category_id = c.category_id
            WHERE
                p.is_available == 1
    """
    query_params = []
    if selected_category_name and selected_category_name != "All Categories":
        product_query += " AND c.category_name = ?"
        query_params.append(selected_category_name)

    product_query += " ORDER BY p.product_name"

    products_cursor = db.execute(product_query, query_params)
    filtered_products = products_cursor.fetchall()

    #Render only the product cards HTML snippet

    return render_template('_product_cards.html', products=filtered_products)

#view products route
@app.route('/product/<int:product_id>')
def product_detail(product_id):
    db = get_db()

    #query database for specific product and its category name
    product_query = """
                SELECT 
                    p.product_id,
                    p.product_name AS product_name,
                    p.product_description AS product_description,
                    p.image_url AS image_url,
                    p.price AS price,
                    c.category_name AS category_name
                FROM 
                    product p
                JOIN 
                    category c on p.category_id = c.category_id
                WHERE 
                    p.product_id = ? AND p.is_available = 1
        """
    product_cursor = db.execute(product_query, (product_id,))

    product = product_cursor.fetchone()
    if product is None:
        #case wwhere there are no products
        return render_template('404.html'), 404 #will need to create 404.html
    return render_template('product_detail.html', product=product)


if __name__ == '__main__':
    app.run(debug=True)