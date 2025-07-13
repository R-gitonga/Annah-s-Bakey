from app import app, db
from models import Category, Product, Testimonial, User
import os

def init_db_with_sqlalchemy():
    # 🔒 Enter Flask app context
    with app.app_context():
        # Optional: print debug info
        db_uri = app.config['SQLALCHEMY_DATABASE_URI']
        print(f"DB URI: {db_uri}")
        # Create all tables if they don't exist
        db.drop_all()
        db.create_all()

        # insert initial categories
        cat1 = Category(category_name='Cakes')
        cat2 = Category(category_name='Pastries')
        cat3 = Category(category_name='Breads')
        cat4 = Category(category_name='Cookies')
        db.session.add_all([cat1, cat2, cat3, cat4])
        db.session.commit()

        # insert products
        products = [
            Product(name='Chocolate Fudge Cake', description='Rich and decadent chocolate cake.', price=1500.00, image_url='chocolate_cake.jpg', is_available=True, category=cat1),
            Product(name='Apple Pie', description='Classic apple pie with a flaky crust.', price=700.50, image_url='cupcake.jpg', is_available=True, category=cat2),
            Product(name='Condensed milk Loaf', description='Artisan condensed milk bread.', price=400.00, image_url='condensed-milk-toast.jpg', is_available=True, category=cat3),
            Product(name='Oatmeal Raisin Cookies', description='Soft and chewy oatmeal raisin cookies (pack of 6).', price=1000.00, image_url='oatmeal_cookies.jpg', is_available=True, category=cat4),
            Product(name='Vanilla Bean Cupcakes', description='Fluffy vanilla cupcakes with buttercream frosting (pack of 4).', price=1100.00, image_url='vanilla_cupcake.jpg', is_available=True, category=cat1),
        ]
        db.session.add_all(products)

        # insert testimonials
        testimonials = [
            Testimonial(customer_name='Jane Doe', customer_location='Nairobi', testimonial_text='The best cake I\'ve ever had! Truly delicious and fresh.', rating=5, image_url=None, is_approved=True),
            Testimonial(customer_name='John Smith', customer_location='Nakuru', testimonial_text='Fast delivery and amazing pastries. Highly recommended!', rating=4, image_url=None, is_approved=True),
            Testimonial(customer_name='Sarah Lee', customer_location='Mombasa', testimonial_text='I loved the cookies, but the bread was a bit dry.', rating=3, image_url=None, is_approved=True),
            Testimonial(customer_name='Mike Ross', customer_location='Kisumu', testimonial_text='Good quality, but a bit pricey for everyday.', rating=3, image_url=None, is_approved=True),
            Testimonial(customer_name='Rachel Zane', customer_location='Kiambu', testimonial_text='Absolutely divine! The chocolate cake was a masterpiece.', rating=5, image_url=None, is_approved=True),
            Testimonial(customer_name='Sansa Stark', customer_location='The North', testimonial_text='Absolutely divine! The Direwolf cookies were a masterpiece.', rating=5, image_url=None, is_approved=True),
        ]
        db.session.add_all(testimonials)
        db.session.commit()

if __name__ == '__main__':
    init_db_with_sqlalchemy()
    print('✅ Database Initialized successfully with SQLAlchemy and sample data!')
