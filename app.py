from flask import Flask, g, render_template
import sqlite3
import os


app = Flask(__name__)

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
def home():
    db = get_db()
    products = db.execute('SELECT * FROM product WHERE is_available = 1').fetchall()



    return render_template('index.html', products=products)



if __name__ == '__main__':
    app.run(debug=True)