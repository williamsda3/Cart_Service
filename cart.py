# cart_service.py

from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

PRODUCT_SERVICE_URL = 'http://localhost:5050'

# Implement this using a db for cart instead of dict or array
# Implement quantities of products, keeping track of how much is available in the products db and syncing it here too 


# Assume you have a cart implementation
# In a real application,  have a proper cart implementation with a database

carts = {}  # Dictionary to store cart information for each user

@app.route('/cart/<int:user_id>', methods=['GET'])
def get_cart(user_id):
    if user_id not in carts:
        return jsonify({'message': 'Cart not found'}), 404

    cart = carts[user_id]

    # Fetch product details for each item in the cart from Product Service
    cart_items = []
    for item in cart['items']:
        product_id = item['product_id']
        product_details = requests.get(f'{PRODUCT_SERVICE_URL}/products/{product_id}').json()
        cart_items.append({
            'product_id': product_id,
           
            'name': product_details['name'],
            'price': product_details['price']
        })

    response = {
        'user_id': user_id,
        'items': cart_items
      
    }
    return (f'{user_id} Your Cart:\n{cart_items}'), 200
    return jsonify(response), 200

@app.route('/cart/<int:user_id>/add/<int:product_id>', methods=['GET'])
def add_to_cart(user_id, product_id):
    # Assume you have a cart implementation
    # In a real application,  update the cart in the database
    product = requests.get(f'{PRODUCT_SERVICE_URL}/products/{product_id}').json()

    if user_id not in carts:
        carts[user_id] = {'items': []}

    carts[user_id]['items'].append({'product_id': product_id, 'item':product['name']})
    return jsonify(carts[user_id]), 200
    return jsonify({'message': f'Product {product_id} added to cart for user {user_id}'}), 200

@app.route('/cart/<int:user_id>/remove/<int:product_id>', methods=['POST'])# To test it out you can change to 'GET' # User should be able to specify item quantity to remove
def remove_from_cart(user_id, product_id):
    # Assume you have a cart implementation
    # In a real application,  update the cart in the database
    if user_id not in carts or 'items' not in carts[user_id]:
        return jsonify({'message': 'Cart not found'}), 404

    cart_items = carts[user_id]['items']
    for item in cart_items:
        if item['product_id'] == product_id:
            cart_items.remove(item)
            return jsonify({'message': f'Product {product_id} removed from cart for user {user_id}'}), 200

    return jsonify({'message': f'Product {product_id} not found in cart for user {user_id}'}), 404

def client():
    while True:
        print("Welcome to you cart!\nPress Ctrl+Z to quit...")
        print("1) Create a new cart\n2) Add product to cart\n 3) Remove product from cart\n 4) View all products\n>>")
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5001, debug=True)
