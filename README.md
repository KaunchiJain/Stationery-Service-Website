# Stationery-Service-Website
An interactive stationery service website integrated with MySQL database for dynamic display of stationery items, implemented using HTML, CSS, JavaScript, Python and Flask framework to enhance interactivity and functionality

Make the required changes in directories and database connection details. Run the python file in terminal. You will encounter the address of local host. For eg: Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:8080
 * Running on http://192.168.31.41:8080

To run the website, paste the URL 'http://127.0.0.1:8080/pythonlogin/register' in the browser (for this example)

Here's a summary of the routes I've defined in my Flask application along with their corresponding URLs:

Login Page:
URL: http://127.0.0.1:8080/pythonlogin/ (Assuming your local Flask server is running on port 8080)
Method: GET for rendering the login page, POST for form submission.

Registration Page:
URL: http://127.0.0.1:8080/pythonlogin/register
Method: GET for rendering the registration page, POST for form submission.

Logout:
URL: http://127.0.0.1:8080/pythonlogin/logout
Method: GET for handling the logout action.

Home Page (Accessible after login):
URL: http://127.0.0.1:8080/pythonlogin/home
Method: GET for rendering the home page.

Profile Page (Accessible after login):
URL: http://127.0.0.1:8080/pythonlogin/profile
Method: GET for rendering the profile page.

Wishlist Page (Accessible after login):
URL: http://127.0.0.1:8080/pythonlogin/wishlist
Method: GET for rendering the wishlist page.

Cart Page (Accessible after login):
URL: http://127.0.0.1:8080/pythonlogin/cart
Method: GET for rendering the cart page.

Checkout Page (Accessible after login):
URL: http://127.0.0.1:8080/pythonlogin/checkout
Method: GET for rendering the checkout page.

Search Results Page:
URL: http://127.0.0.1:8080/search
Method: GET for rendering the search results page.

Order History Page (Accessible after login):
URL: http://127.0.0.1:8080/pythonlogin/order_history
Method: GET for rendering the order history page.

You can access these pages by navigating to their respective URLs in your web browser while the Flask server is running locally. Make sure to replace 127.0.0.1 with localhost if you prefer.
