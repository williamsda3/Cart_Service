# cart_service.py

from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

PRODUCT_SERVICE_URL = 'https://productservice-0lvt.onrender.com'

# Implement this using a db for cart instead of dict or array
# Implement quantities of products, keeping track of how much is available in the products db and syncing it here too 




carts = {}  # Dictionary to store cart information for each user

# Retrieve the current contents of a user’s shopping cart, including product names, quantities, and total prices

@app.route('/cart/<int:user_id>', methods=['GET'])
def get_cart(user_id):
    if user_id not in carts:
        return jsonify({'message': 'Cart not found - Creating new Cart'}), 404

    cart = carts[user_id]

    # Fetch product details for each item in the cart from Product Service
    cart_items = []
    for item in cart['items']:
        product_id = item['product_id']
        product_details = requests.get(f'{PRODUCT_SERVICE_URL}/products/{product_id}').json()
        cart_items.append({
            'product_id': product_id,
            'name': product_details['name'],
            'price': product_details['price'],
            'quantity': item['quantity']
        })


    return (f'{user_id} Your Cart:\n{cart_items}'), 200
   
# Add a specified quantity of a product to the user’s cart
@app.route('/cart/<int:user_id>/add/<int:product_id>/<int:quantity>', methods=['POST'])
def add_to_cart(user_id, product_id, quantity):
    # Assume you have a cart implementation
    # In a real application, update the cart in the database
    product = requests.get(f'{PRODUCT_SERVICE_URL}/products/{product_id}').json()

    if user_id not in carts:
        carts[user_id] = {'items': []}

    # Reduce the product quantity and get the last transaction
    response = requests.post(f'{PRODUCT_SERVICE_URL}/products/{product_id}/reduce/{quantity}')
    if response.status_code <= 201:
        product = response.json()
        last_transaction = product.get('last_transaction', 0)

        # Check if the item is already in the cart
        item_found = False
        for item in carts[user_id]['items']:
            if item['product_id'] == product_id:
                item['quantity'] += quantity
                item['last_transaction'] = last_transaction
                item_found = True
                break

        # If the item is not already in the cart, add it
        if not item_found:
            carts[user_id]['items'].append({
                'product_id': product_id,
                'item': product['name'],
                'quantity': quantity,
                'last_transaction': last_transaction
            })

        return jsonify(carts[user_id]), 200
    else:
        return jsonify({'error': 'Invalid data'}), 400


# Remove a specified quantity of a product from the user’s cart

@app.route('/cart/<int:user_id>/remove/<int:product_id>/<int:quantity>', methods=['POST'])# To test it out you can change to 'GET' # User should be able to specify item quantity to remove
def remove_from_cart(user_id, product_id,quantity):
    
    if user_id not in carts or 'items' not in carts[user_id]:
        return jsonify({'message': 'Cart not found'}), 404

    cart_items = carts[user_id]['items']
    for item in cart_items:
        if item['product_id'] == product_id:
            item['quantity'] -= quantity
            if item['quantity'] <= 0:
                cart_items.remove(item)
            return jsonify({'message': f'Product {product_id} removed from cart for user {user_id}'}), 200

    return jsonify({'message': f'Product {product_id} not found in cart for user {user_id}'}), 404

if __name__ == '__main__':
    app.run( debug=True)
