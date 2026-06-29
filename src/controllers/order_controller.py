from flask import request #to read body/JSON from Postman
from src.models import order, user # it is the Models; controller uses it to ask for data from SQL
from src.functions.response import success_response, error_response # unified responses


# V1 reference:
# @app.route('/buy', methods=['POST'])
# def buy():
#     inputData = request.json
#     product_id = inputData.get("product_id")
#     quantity = inputData.get("quantity")
#     member_id = inputData.get("member_id")
#
#     if member_id not in members:
#         return jsonify({"success": False, "message": "Member does not exist"})
#
#     item = goods[product_id]
#     total = item["price"] * quantity
#     member_cart = carts[member_id]
#     member_cart.append({...})
#
# V2 change:
# This API creates a real order in MySQL directly.
# It receives user_id and a list of items instead of one product at a time
def create_order():
    # Get JSON body sent from Postman
    inputData = request.json

    # Read user_id from request body
    user_id = inputData.get("user_id")
    # Read items list from request body.
    # Expected format: [{"product_id": 1, "quantity": 2}, ...]
    items = inputData.get('items')

    # Validate required user_id.
    if not user_id:
        return error_response(
            message="User ID is required",
            status_code=400
        )

    # Validate user_id type.
    # It must be integer because users.id in MySQL is INT.
    if not isinstance(user_id, int):
        return error_response(
            message="User Id must be integer",
            status_code=400
        )

    # Validate required items
    if not items:
        return error_response(
            message="Items are required",
            status_code=400
        )

    # Validate items type.
    # It must be a list because one order can contain multiple products
    if not isinstance(items, list):
        return error_response(
            message="Items must be list",
            status_code=400
        )

    # Ask user model to check whether user exists in MySQL.
    found_user = user.get_user_by_id(user_id)

    # If user does not exist, order cannot be created.
    if not found_user:
        return error_response(
            message="User does not exist",
            status_code=404
        )

    # Validate every item before calling order model.
    # Controller checks request format; model checks product existence and stock
    for item in items:
        # Get product_id from current item.
        product_id = item.get("product_id")
        # Get quantity from current item
        quantity = item.get("quantity")

        # Validate required product_id.
        if not product_id:
            return error_response(
                message="Product Id is required",
                status_code=400
            )

       # Validate required quantity
        if not quantity:
            return error_response(
                message="Quantity is required",
                status_code=400
            )

        # Validate product_id type
        if not isinstance(product_id, int):
            return error_response(
                message="Product ID must be integer",
                status_code=400
            )

        # Validate quantity type
        if not isinstance(quantity, int):
            return error_response(
                message="Quantity must be integer",
                status_code=400
            )

        # Quantity must be positive
        if quantity <= 0:
            return error_response(
                message="Quantity must be greater than zero",
                status_code=400
            )

    # Ask order model to create order in MySQL.
    # Model returns receipt if successful, or error_message if something is wrong
    receipt, error_message = order.create_order(user_id, items)

    # If model returned error_message, convert it into error response
    if error_message:
        return error_response(
            message=error_message,
            status_code=400
        )

    # Return created receipt to Postman.
    return success_response(
        data=receipt,
        message="Order created successfully",
        status_code=201
    )


# V1 reference:
# @app.route('/order', methods=['GET'])
# def order():
#     member_id = request.args.get("member_id")
#     member = members[member_id]
#     member_cart = carts[member_id]
#     return jsonify({...})
#
# V2 change:
# Receipt is retrieved by order_id from MySQL
def get_order_receipt(order_id):
    # Ask order model to get receipt by order_id
    receipt = order.get_order_receipt(order_id)

    # If model returns None, order was not found
    if not receipt:
        return error_response(
            message="Order not found",
            status_code=404
        )

    # Return receipt in unified success response format
    return success_response(
        data=receipt,
        message="Order receipt retrieved successfully",
        status_code=200
    )


# V1 reference:
# V1 did not have a separate delete order endpoint.
# After creating an order, it cleared the temporary cart:
# carts[member_id] = []
#
# V2 change:
# Since orders are saved in MySQL, we add a delete endpoint.
def delete_order(order_id):
    # Ask order model to delete order by id.
    result = order.delete_order(order_id)

    # If model returns False, order was not found
    if not result:
        return error_response(
            message="Order not found",
            status_code=404
        )

    # Return success response after order deletion
    return success_response(
        message="Order deleted successfully",
        status_code=200
    )