
from flask import Flask, render_template, request, jsonify, flash, redirect, url_for
import os
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone


app = Flask(__name__)



@app.context_processor
def inject_now():
    return {'now': datetime.now(timezone.utc)}
#configuration for sqlalchemy
# Get DATABASE_URL from environment variable or use a fallback for local development
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///bakery.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #disable tracking modifications for perfomence
#generate a random 24-byte key 
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your_super_secret_dev_key')
# The 'or' part is a fallback for local development if SECRET_KEY isn't set as an env var there.
# In production on Render, os.environ.get('SECRET_KEY') will be used.
db = SQLAlchemy(app)

# import database models

from models import Category, Product, Testimonial


@app.route("/")
def index():

    #fetch category and product using sqlalchemy
    categories =Category.query.all()
    products_by_category = {}
    for category in categories:
        products_by_category[category.category_name] = Product.query.filter_by(category=category, is_available=True).all()

    initial_products_display = Product.query.filter_by(is_available=True).order_by(Product.name).all()


    #fetch approved testimonials
    testimonials_data = Testimonial.query.filter_by(is_approved=True).order_by(Testimonial.created_at.desc()).all()
    #might want to structure testimonials_data differently if you have groups of 3
    #for now just pass the list directly here, template will adapt slightly
    #can implement grouping logic with python here
    selected_category = "All Categories"

    return render_template('index.html',
                           categories=categories,
                           products_by_category=products_by_category,
                           testimonials=testimonials_data,
                           products=initial_products_display,
                           selected_category=selected_category)
   
@app.route('/products/<int:category_id>')
def products_by_category(category_id):
    category = Category.query.get_or_404(category_id)
    products = Product.query.filter_by(category_id=category_id, is_available=True).all()
    return render_template('category_products.html', category=category, products=products)


@app.route('/add_testimonial', methods=['GET', 'POST'])
def add_testimonial():
    if request.method == 'POST':
        customer_name = request.form['customer_name']
        customer_location = request.form.get('customer_location') #use .get for optional fields
        testimonial_text = request.form['testimonial_text']
        rating = request.form.get('rating')
        # image_url = request.form.get('image_url') #placeholder for image. yet to implement
        #convert rating to integer, handle potential errors or default
        try:
            rating = int(rating) if rating else None
        except ValueError:
            rating = None

        #basic validation
        if not customer_name or not testimonial_text:
            flash('Name and Testimony are required!', 'danger')
            return render_template('add_testimonial.html')
        
        try:
            #create a new testimonial object
            new_testimonial = Testimonial(
                customer_name=customer_name,
                customer_location=customer_location,
                testimonial_text=testimonial_text,
                rating=rating,
                image_url=None, #image upload not implemented yet
                is_approved=True
            )
            db.session.add(new_testimonial)
            db.session.commit()

            flash('Your testimony has been submitted for approval!', 'success')
            return redirect(url_for('index', _anchor='testimonials-tab')) #redirect back to home, testimonials tab
        except Exception as e: #catch a broader exception for debugging
            flash(f'An error occurred: {e}', 'danger')
            #log error for server-side debugging
            app.logger.error(f'Error adding testimonial: {e}')
            return render_template('add_testimonial.html')
        
    return render_template('add_testimonial.html')

# AJAX endpoint for filtering
@app.route('/filter_products', methods=['GET'])
def filter_products_ajax():
    selected_category_name = request.args.get('category')

    #start by with a query for all available products
    products_query = Product.query.filter_by(is_available=True)

    #if a specific category is selected, filter by category name
    if selected_category_name and selected_category_name != "All Categories":
        #we need to join with the category table to filter by category_name. we use the relationship we defined in the product model
        products_query =  products_query.join(Category).filter(Category.category_name == selected_category_name)

    # Order the result
    products_query = products_query.order_by(Product.name)

    # execute query and fetch all products
    filtered_products = products_query.all()

    #Render only the product cards HTML snippet

    return render_template('_product_cards.html', products=filtered_products)

#view products route
@app.route('/product/<int:product_id>')
def product_detail(product_id):
    #query database for specific product id, ensuring its availble.
    # use .get_or_404() for a cleaner way to handle not found products
    product = Product.query.filter_by(id=product_id, is_available=True).first_or_404()

    # the category name can be accessed directly through the category relationship
    # defined in the product model eg product.category.category_name
    # the category relationship will automatically load the category object
    
    return render_template('product_detail.html', product=product)

