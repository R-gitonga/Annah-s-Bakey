
from urllib.parse import quote_plus
from flask import Flask, render_template, request, jsonify, flash, redirect, url_for, session
import os
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone
from flask_login import login_required, LoginManager, login_user, logout_user, current_user, UserMixin
from werkzeug.utils import secure_filename



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

login_manager = LoginManager() # Create an instance of LoginManager
login_manager.init_app(app)    # Initialize it with your Flask app
login_manager.login_view = 'login' # Tell Flask-Login what route to use for login if @login_required fails


UPLOAD_FOLDER = 'static/images/products'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER) # os.makedirs creates all necessary intermediate directories
    print(f"Created upload folder: {UPLOAD_FOLDER}")

# User loader callback for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
# --- END NEW ---

# import database models

from models import Category, Product, Testimonial, User, Order


# app.py

# ... (your existing imports) ...

@app.route("/")
def index():
    # Fetch all categories to populate the category filter/navigation
    categories = Category.query.all()

    # The initial product display on the homepage should be ALL available products,
    # or you could default to a specific category if you prefer.
    # This aligns with what filter_products_ajax() would show if "All Categories" is selected.
    initial_products_display = Product.query.filter_by(is_available=True).order_by(Product.name).all()

    # Fetch approved testimonials
    testimonials_data = Testimonial.query.filter_by(is_approved=True).order_by(Testimonial.created_at.desc()).all()

    return render_template('index.html',
                           categories=categories,
                           products=initial_products_display, # Pass initial products directly
                           testimonials=testimonials_data,
                           selected_category="All Categories") # Keep track of selected category for UI
   
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
                is_approved=False
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

@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if "username" in session:
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Implement your authentication logic here
        if username == 'admin' and password == 'password':
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials. Please try again.', 'danger')
    return render_template('admin_login.html')

# login
@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':

        # collect info from form
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user) #log user in with flask login
            next_page = request.args.get('next') #redirect to page they tried to access
            
            return redirect(next_page or url_for('dashboard'))
        else:
            flash("Invalid Username or Password!", "danger")
    return render_template("admin_login.html")


# Register
@app.route("/register", methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user:
            flash('Username already exists', 'danger')
            return render_template("admin_login.html", error="user already exists")
        else:
            new_user = User(username=username)
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.commit()
            flash("Registration Successfull! please login.", 'success')
            # create a new session for user
            # session['username'] = username
            return redirect(url_for('login'))
        
    return render_template("admin_login.html")
    
# Dashbooard
@app.route("/dashboard")
@login_required
def dashboard():
    testimonials = Testimonial.query.all()
    return render_template("dashboard.html", username=current_user.username, testimonials=testimonials)

# logout
@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out", "info")
    return redirect(url_for('admin_login'))

# admin testimonials
@app.route("/admin/testimonials")
@login_required
def admin_testimonials():
    # fetch all testimonials ordered by creation date. later filters like pending only go here
    testimonials = Testimonial.query.order_by(Testimonial.created_at.desc()).all()
    return render_template("admin/testimonials.html", testimonials=testimonials, username=current_user.username)


@app.route("/admin/testimonial/<int:testimonial_id>/<action>")
@login_required
def admin_testimonial_action(testimonial_id, action):
    testimonial = Testimonial.query.get_or_404(testimonial_id)

    if action == 'approve':
        testimonial.is_approved = True
        flash(f'Testimonial from {testimonial.customer_name} approved!', 'success')
    elif action == 'reject':
        db.session.delete(testimonial)
        flash(f'Testimonial from {testimonial.customer_name} rejected and deleted!', 'danger')
    else:
        flash('Invalid action.', 'warning')

    db.session.commit()
    return redirect(url_for('admin_testimonials'))

# Manage Orders
@app.route('/create_whatsapp_order', methods=['POST'])
def create_whatsapp_order():
    product_id = request.form.get('product_id')
    customer_name = request.form.get('customer_name')
    customer_phone = request.form.get('customer_phone')
    customer_location = request.form.get('customer_location')

    product = Product.query.get_or_404(product_id)

    # 1. create new order record in the database with customer details
    new_order = Order(
        product_id=product.id,
        product_name=product.name,
        product_price=product.price,
        customer_name=customer_name,
        customer_phone=customer_phone,
        customer_location=customer_location,
        status='Pending'
    )
    db.session.add(new_order)
    db.session.commit()
    flash('Your order request has been noted! Redirecting to Whatsapp...', 'info')

    # 2. Prepare whataspp url with prefilled message including order id
    whatsapp_number = '254702397705'
    prefill_message = (
        f"Hello!, I'm interested in ordering the {product.name} (Ksh {product.price:.2f}). "
        f"My name is {customer_name}, and i'm located at {customer_location}. "
        f"My order tracking ID is #{new_order.id}. Please confirm details."
    )
    encoded_message = quote_plus(prefill_message)

    # 3 Redirect to whatsapp
    whatsapp_url = f"https://wa.me/{whatsapp_number}?text={encoded_message}"
    return redirect(whatsapp_url)


@app.route("/admin/orders")
@login_required
def admin_orders():
    orders = Order.query.order_by(Order.ordered_at.desc()).all()
    return render_template('admin/orders.html', orders=orders, username=current_user.username)


@app.route("/admin/order/<int:order_id>/<status_action>")
@login_required
def admin_order_status(order_id, status_action):
    order = Order.query.get_or_404(order_id)

    # validation action
    valid_statuses = ['Approved', 'Completed', 'Canceled', 'Pending']
    if status_action in valid_statuses:
        order.status = status_action
        db.session.commit()
        flash(f'Order #{order.id} status updated to {status_action}.', 'success')
    else:
        flash('Invalid Order action', 'warning')

    return redirect(url_for('admin_orders'))

@app.route("/admin/products")
@login_required
def admin_products():
    products = Product.query.order_by(Product.name).all()
    categories = Category.query.order_by(Category.category_name).all() # Fetch categories here


    return render_template("admin/products.html", products=products, categories=categories, username=current_user.username)

@app.route('/admin/add_product', methods=['GET', 'POST'])
@login_required
def add_product():
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        price_str = request.form.get('price')
        category_id_str = request.form.get('category')

        # input validation
        if not name or not price_str or not category_id_str:
            flash("Name, Price, and category are required fields.", 'danger')
            return redirect(url_for('add_product'))
        try:
            price = float(price_str)
            if price <= 0:
                flash("Price must be a positive number.", "danger")
                return redirect(url_for(add_product))
        except ValueError:
            flash("Invalid price format. Please enter a number.", "danger")
            return redirect(url_for("add_product"))
        try:
            category_id = float(category_id_str)
            # check of category exists in db
            if not Category.query.get(category_id):
                flash("Selected category does not exist.", "danger")
                return redirect(url_for(add_product))
        except ValueError:
            flash("Invalid category selected.", "danger")
            return redirect(url_for("add_product"))


        image_url = ''
        if 'file' in request.files:
            file = request.files['file'] #access directly after checking in requests.file
            if file.filename == '':
                flash('No selected image file. product will be added without an image.', 'info')
            elif not allowed_file(file.filename):
                flash(f"Invalid file type for image: {file.filename}. only {', '.join(ALLOWED_EXTENSIONS)} are allowed.", 'danger')
                return redirect(url_for('add_product'))
            else :
                filename = secure_filename(file.filename)
                try:
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    image_url = filename
                except Exception as e:
                    flash(f"Error saving image: {e}", 'danger')
                    return redirect(url_for('add_product'))

        new_product = Product(
            name=name,
            description=description,
            price=price,
            image_url=image_url,
            is_available=False,
            category_id=category_id
        )
        db.session.add(new_product)
        db.session.commit()
        flash(f"Product '{name}' added successfully!", 'success')
        return redirect(url_for('admin_products'))
    # GET request: Render the form
    categories = Category.query.all()
    return render_template('admin/add_edit_product.html', categories=categories, username=current_user.username)

@app.route('/admin/edit_product/<int:product_id>', methods=['GET', 'POST'])
@login_required
def edit_product(product_id):
    product = Product.query.get_or_404(product_id)
    categories = Category.query.all()

    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        price_str = request.form.get('price')
        category_id_str = request.form.get('category')
                # input validation

        is_available = 'is_available' in request.form

        if not name or not price_str or not category_id_str:
            flash("Name, Price, and category are required fields.", 'danger')
            return redirect(url_for('edit_product', product_id=product.id))
        try:
            price = float(price_str)
            if price <= 0:
                flash("Price must be a positive number.", "danger")
                return redirect(url_for('edit_product', product_id=product.id))
        except ValueError:
            flash("Invalid price format. Please enter a number.", "danger")
            return redirect(url_for('edit_product', product_id=product.id))
        try:
            category_id = int(category_id_str)
            # check of category exists in db
            if not Category.query.get(category_id):
                flash("Selected category does not exist.", "danger")
                return redirect(url_for('edit_product', product_id=product.id))
        except ValueError:
            flash("Invalid category selected.", "danger")
            return redirect(url_for('edit_product', product_id=product.id))


        if 'file' in request.files:
            file = request.files['file'] #access directly after checking in requests.file
            if file.filename == '':
                pass
            elif not allowed_file(file.filename):
                flash(f"Invalid file type for image: {file.filename}. only {', '.join(ALLOWED_EXTENSIONS)} are allowed.", 'danger')
                return redirect(url_for('edit_product', product_id=product.id))
            else :
                filename = secure_filename(file.filename)
                try:
                    # delete old image if it exists and is not default/empty image
                    if product.image_url and product.image_url != filename:
                      old_image_path = os.path.join(app.config['UPLOAD_FOLDER', product.image_url])  
                      if os.path.exists(old_image_path):
                          os.remove(old_image_path)
                          print(f'Deleted old image: {old_image_path}')
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    product.image_url = filename
                except Exception as e:
                    flash(f"Error saving image: {e}", 'danger')
                    return redirect(url_for('edit_product', product_id=product.id))
                
        # update product object
        product.name = name
        product.description = description
        product.price = price
        product.is_available = is_available
        product.category_id = category_id

        db.session.commit()
        flash(f"Product '{product.name}' updated successfully!", 'success')
        return redirect(url_for('admin_products'))
    return render_template('admin/add_edit_product.html', product=product, categories=categories, username=current_user.username)

@app.route('/admin/categories')
@login_required
def admin_categories():
    # fetch categories ordered by name
    categories = Category.query.order_by(Category.category_name).all()
    return render_template("admin/categories.html", categories=categories, username=current_user.username)


# route for adding category
@app.route('/admin/add_category', methods=["GET", "POST"])
@login_required
def admin_add_category():
    if request.method == 'POST':
        category_name = request.form.get('category_name')

        if not category_name:
            flash("Category name is required.", "danger")
            return redirect(url_for('admin_add_category'))
        # check if category already exists. case sensitive
        existing_category = Category.query.filter(db.func.lower(Category.category_name) == db.func.lower(category_name)).first()
        if existing_category:
            flash(f"Category '{category_name}' already exists.", "warning")
            return redirect(url_for('admin_add_category'))

        new_category = Category(category_name=category_name)
        db.session.add(new_category)
        db.session.commit()
        flash(f"Category '{category_name}' added succesfully", 'success')
        return redirect(url_for('admin_categories'))
    
    # GET request: Render the form
    return render_template('admin/add_edit_category.html', username=current_user.username)

# placeholder dor edit categories
@app.route("/admin/edit_category/<int:category_id>", methods=['GET', 'POST'])
@login_required
def admin_edit_category(category_id):
    category = Category.query.get_or_404(category_id)
    if request.method == 'POST':
        flash(f"Category: '{category.category_name}' (ID: {category_id}) should be updated here.", "info")
        return redirect(url_for('admin_categories'))

    # GET request: render the form with existing category data
    flash(f"This is the 'Edit Category' page for '{category.category_name}' (ID: {category_id}). coming soon!", "info")
    return render_template('admin/add_edit_category.html', category=category, username=current_user.username)

# route for deleting category
@app.route("/admin/delete_category/<int:category_id>", methods=['GET', 'POST'])
@login_required
def admin_delete_category(category_id):
    category = Category.query.get_or_404(category_id)
    associated_products = Product.query.filter_by(category_id=category.id).count()

    if associated_products > 0:
        flash(f"Cannot delete category '{category.category_name}' because it has {associated_products} associated product(s). please reassign or delete these products first", 'danger')
    else:
        try:
            db.session.delete(category)
            db.session.commit()
            flash(f"Category '{category.category_name}' deleted successfully!", 'success')
        except Exception as e:
            db.session.rollback()
            flash(f"Error deleteing category '{category.category_name}': {e}", 'danger')
    return redirect(url_for('admin_categories'))