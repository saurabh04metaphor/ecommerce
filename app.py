from flask import Flask, render_template, request, session, redirect, url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = 'queue'  # Required for session management

# MySQL configurations
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'queue'
app.config['MYSQL_DB'] = 'ecommerce'

mysql = MySQL(app)

@app.route('/')
def index():
    # Using a context manager ensures the cursor is properly closed.
    with mysql.connection.cursor() as cur:
        cur.execute("SELECT * FROM products")
        products = cur.fetchall()
    return render_template('index.html', products=products)

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    product_id = request.form.get('product_id')
    if not product_id:
        flash("Invalid product selected.", "danger")
        return redirect(url_for('index'))
    
    # Retrieve or initialize the cart, then append the new product.
    cart = session.get('cart', [])
    cart.append(product_id)
    session['cart'] = cart  # Reassign to notify Flask the session has been updated.
    flash("Product added to cart!", "success")
    return redirect(url_for('index'))

@app.route('/cart')
def cart():
    cart_items = session.get('cart', [])
    return render_template('cart.html', cart_items=cart_items)

if __name__ == '__main__':
    app.run(debug=True)
