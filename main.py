from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re

app = Flask(__name__)
app.debug = True

# Change this to your secret key (it can be anything, it's for extra protection)
app.secret_key = 'ishaan'

# Enter your database connection details below
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'ishaan'
app.config['MYSQL_DB'] = 'pythonlogin'

# Initialize MySQL
mysql = MySQL(app)

@app.route('/pythonlogin/', methods=['GET', 'POST'])
def login():
    # Output a message if something goes wrong...
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']

        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = %s AND password = %s', (username, password,))
        # Fetch one record and return result
        account = cursor.fetchone()
        # If account exists in accounts table in our database
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            # Redirect to home page
            return redirect(url_for('home'))
        else:
            # Account doesn't exist or username/password incorrect
            msg = 'Incorrect username/password!'
    # Show the login form with message (if any)
    return render_template('indextest.html', msg=msg)

# http://localhost:5000/python/logout - this will be the logout page
@app.route('/pythonlogin/logout')
def logout():
    # Remove session data, this will log the user out
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    # Redirect to the login page
    return redirect(url_for('login'))

# http://localhost:5000/python/register - this will be the registration page, we need to use both GET and POST requests
@app.route('/pythonlogin/register', methods=['GET', 'POST'])
def register():
    # Initialize an empty message
    msg = ''

    # Check if the form was submitted via a POST request and if 'username', 'password', and 'email' fields exist
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        # Extract values from the form
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        # Check if an account with the same username already exists
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = %s', (username,))
        account = cursor.fetchone()

        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password or not email:
            msg = 'Please fill out the form!'
        else:
            # Insert the new account into the 'accounts' table
            cursor.execute('INSERT INTO accounts VALUES (NULL, %s, %s, %s)', (username, password, email,))
            mysql.connection.commit()  # Commit the changes to the database
            msg = 'You have successfully registered!'
    # Render the 'register.html' template with the message (if any)
    return render_template('register.html', msg=msg)

# http://localhost:5000/python/home - this will be the home page, only accessible for logged-in users
@app.route('/pythonlogin/home')
def home():
    # Check if the user is logged in
    if 'loggedin' in session:
        # Fetch the 6 products from the database
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM products')  # Assumes your products table is named 'products'
        products = cursor.fetchall()
        
        # Render the 'home.html' template with both the username and products
        return render_template('home.html', username=session['username'], products=products)
    
    # User is not logged in, redirect to the login page
    return redirect(url_for('login'))


# http://localhost:5000/pythinlogin/profile - this will be the profile page, only accessible for logged in users
@app.route('/pythonlogin/profile')
def profile():
    # Check if the user is logged in
    if 'loggedin' in session:
        # We need all the account info for the user so we can display it on the profile page
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE id = %s', (session['id'],))
        account = cursor.fetchone()
        # Show the profile page with account info
        return render_template('profile.html', account=account)
    # User is not logged in redirect to login page
    return redirect(url_for('login'))
from flask import request, jsonify

# ...

@app.route('/pythonlogin/add_to_cart/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    if 'loggedin' in session:
        # Get the user's ID from the session
        user_id = session['id']
        
        # Check if the product is already in the cart
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM cart WHERE user_id = %s AND product_id = %s', (user_id, product_id))
        cart_item = cursor.fetchone()

        if cart_item:
            # Product is already in the cart
            return jsonify({'message': 'Product is already in the cart'})

        # Add the product to the cart
        cursor.execute('INSERT INTO cart (user_id, product_id) VALUES (%s, %s)', (user_id, product_id))
        mysql.connection.commit()
        
        return jsonify({'message': 'Product added to the cart'})

    return jsonify({'error': 'User is not logged in'})

@app.route('/pythonlogin/add_to_wishlist/<int:product_id>', methods=['POST'])
def add_to_wishlist(product_id):
    if 'loggedin' in session:
        # Get the user's ID from the session
        user_id = session['id']
        
        # Check if the product is already in the wishlist
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM wishlist WHERE user_id = %s AND product_id = %s', (user_id, product_id))
        wishlist_item = cursor.fetchone()

        if wishlist_item:
            # Product is already in the wishlist
            return jsonify({'message': 'Product is already in the wishlist'})

        # Add the product to the wishlist
        cursor.execute('INSERT INTO wishlist (user_id, product_id) VALUES (%s, %s)', (user_id, product_id))
        mysql.connection.commit()
        
        return jsonify({'message': 'Product added to the wishlist'})

    return jsonify({'error': 'User is not logged in'})

# Render the Wishlist page
@app.route('/pythonlogin/wishlist')
def wishlist():
    if 'loggedin' in session:
        # Retrieve the user's wishlist products from the database
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT products.* FROM wishlist JOIN products ON wishlist.product_id = products.product_id WHERE wishlist.user_id = %s', (session['id'],))
        wishlist_products = cursor.fetchall()

        return render_template('wishlist.html', wishlist_products=wishlist_products)

    return redirect(url_for('login'))

# Render the Cart page
@app.route('/pythonlogin/cart')
def cart():
    if 'loggedin' in session:
        # Retrieve the user's cart products from the database
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT products.* FROM cart JOIN products ON cart.product_id = products.product_id WHERE cart.user_id = %s', (session['id'],))
        cart_products = cursor.fetchall()

        return render_template('cart.html', cart_products=cart_products)

    return redirect(url_for('login'))
@app.route('/pythonlogin/clear_cart', methods=['POST'])
def clear_cart():
    if 'loggedin' in session:
        user_id = session['id']

        # Clear the user's cart in the database
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('DELETE FROM cart WHERE user_id = %s', (user_id,))
        mysql.connection.commit()

        # Redirect back to the cart page or any other desired page
        return redirect(url_for('cart'))
    
    return redirect(url_for('login'))
@app.route('/pythonlogin/clear_wishlist', methods=['POST'])
def clear_wishlist():
    if 'loggedin' in session:
        # Get the user's ID from the session
        user_id = session['id']

        # Clear the user's wishlist by deleting all their wishlist items
        cursor = mysql.connection.cursor()
        cursor.execute('DELETE FROM wishlist WHERE user_id = %s', (user_id,))
        mysql.connection.commit()

        return redirect(url_for('wishlist'))

    return redirect(url_for('login'))
# Render the Checkout page
@app.route('/pythonlogin/checkout')
def checkout():
    if 'loggedin' in session:
        # Retrieve the user's cart products from the database
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT products.* FROM cart JOIN products ON cart.product_id = products.product_id WHERE cart.user_id = %s', (session['id'],))
        cart_products = cursor.fetchall()

        # Calculate the total price of products in the cart
        total_price = sum(product['product_price'] for product in cart_products)

        return render_template('checkout.html', cart_products=cart_products, total_price=total_price)

    return redirect(url_for('login'))
# Purchase action
@app.route('/pythonlogin/purchase')
@app.route('/pythonlogin/purchase')
def purchase():
    if 'loggedin' in session:
        # Get the user's ID from the session
        user_id = session['id']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        # Retrieve the products in the user's cart
        cursor.execute('SELECT * FROM cart WHERE user_id = %s', (user_id,))
        cart_products = cursor.fetchall()

        if not cart_products:
            return jsonify({'message': 'Nothing in the cart'})  # Show a message if the cart is empty

        # Insert the products from the cart into the orders table
        for product in cart_products:
            cursor.execute('INSERT INTO orders (user_id, product_id) VALUES (%s, %s)', (user_id, product['product_id']))

        # Clear the user's cart by deleting all records
        cursor.execute('DELETE FROM cart WHERE user_id = %s', (user_id,))

        mysql.connection.commit()

        # Render the purchase confirmation template
        return render_template('purchase_successful.html')

    return redirect(url_for('home'))

def search_products(query):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    query = f"SELECT * FROM products WHERE product_name LIKE '%{query}%'"
    cursor.execute(query)
    return cursor.fetchall()

# Define the route for your search page
@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query')
    if query:
        # Perform the search
        results = search_products(query)
    else:
        results = []

    return render_template('search_results.html', query=query, results=results)
@app.route('/pythonlogin/order_history')
def order_history():
    if 'loggedin' in session:
        user_id = session['id']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        # Retrieve the order history for the user
        cursor.execute('SELECT orders.*, products.product_name, products.product_description, products.product_price, products.image_url FROM orders JOIN products ON orders.product_id = products.product_id WHERE orders.user_id = %s', (user_id,))
        order_history = cursor.fetchall()

        return render_template('order_history.html', order_history=order_history)

    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)  # Change the port to 8080 or any other available port