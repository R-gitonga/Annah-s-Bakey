from flask import Flask, g, render_template, request, jsonify, flash, redirect, url_for
import sqlite3
import os


app = Flask(__name__)
#generate a random 24-byte key 
app.config['SECRET_KEY'] = os.urandom(24)



DB_NAME = 'bakery.db'

def get_db():
    db = getattr(g, '_database', None)  # Get the database connection from the Flask global 'g' object
    if db is None:
        # Use app.root_path to get the absolute path to your application's root directory
        # Then join it with your 'data' subdirectory and the database file name
        db_path = os.path.join(app.root_path, 'data', DB_NAME)
        db = g._database = sqlite3.connect(db_path)
        db.row_factory = sqlite3.Row  # allows you to access columns by name
    return db

@app.teardown_appcontext
def close_db(exception=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()


@app.route("/")
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

    testimonials_query = """
                SELECT 
                    t.id,
                    t.customer_name,
                    t.customer_location,
                    t.testimonial_text,
                    t.rating,
                    t.image_url,
                    t.is_approved
                FROM
                    testimonials t
                WHERE 
                    is_approved = 1
                ORDER BY
                    created_at DESC

    """
    testimonials_cursor = db.execute(testimonials_query)
    testimonials = testimonials_cursor.fetchall()

    print("Fetched testimonials:", testimonials) # This will print to your Flask terminal


    return render_template('index.html', 
                           products=filtered_products,
                           categories=all_categories,
                           selected_category=selected_category_name,
                           testimonials=testimonials)

@app.route('/add_testimonial', methods=['GET', 'POST'])
def add_testimonial():
    if request.method == 'POST':
        customer_name = request.form['customer_name']
        customer_location = request.form.get('customer_location') #use .get for optional fields
        testimonial_text = request.form['testimonial_text']
        rating = request.form.get('rating')
        image_url = request.form.get('image_url') #placeholder for image. yet to implement

        #basic validation
        if not customer_name or not testimonial_text:
            flash('Name and Testimony are required!', 'danger')
            return render_template('add_testimonial.html')
        
        try:
            db = get_db()
            db.execute(
                "INSERT INTO testimonials(customer_name, customer_location, testimonial_text, rating, image_url, is_approved) VALUES (?, ?, ?, ?, ?, ?)",
                (customer_name, customer_location, testimonial_text, rating, image_url, 0)
            )
            db.commit()
            flash('Your testimony has been submitted for approval!', 'success')
            return redirect(url_for('index', _anchor='testimonials-tab')) #redirect back to home, testimonials tab
        except sqlite3.Error as e:
            flash(f'An error occurred: {e}', 'danger')
            return render_template('add_testimonials.html')
    return render_template('add_testimonial.html')

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



# if __name__ == '__main__':
app.run(debug=True)