# Cart_Service

/cart/{user id} (GET): Retrieve the current contents of a user’s shopping cart, including prod-
uct names, quantities, and total prices.

/cart/{user id}/add/{product id}/{quantity} (POST): Add a specified quantity of a product to the user’s cart.
/cart/{user id}/remove/{product id}{quantity} (POST): Remove a specified quantity of a product from the
user’s cart.