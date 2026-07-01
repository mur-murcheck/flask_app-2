from flask import request
from src.models import order, order_item, user # it is the Models; controller uses it to ask for data from SQL
from src.functions.response import success_response, error_response # unified responses


def get_current_user_from_token():
    auth_token = request.headers.get("X-Auth-Token")

    if not auth_token:
        return None, error_response(
            message="Auth key is required",
            status_code=401
        )

    current_user = user.get_user_by_auth_key(auth_token)

    if not current_user:
        return None, error_response(
            message="Invalid auth token",
            status_code=401
        )

    return current_user, None


# add product to current user's unpaid order
def add_product():
    current_user, auth_error = get_current_user_from_token()
    if auth_error:
        return auth_error

    # find current user's unpaid order
    order_id = order.get_unpaid_order_by_user_id(current_user["id"])

    if order_id is None:
        return error_response(
            message="Order does not exist",
            status_code=400
        )

    item = request.json or {}

    product_id = item.get("product_id")
    quantity = item.get("quantity")

    if not product_id:
        return error_response(
            message="Product ID is required"
        )

    if not quantity:
        return error_response(
            message="Quantity is required"
        )

    if not isinstance(product_id, int):
        return error_response(
            message="Product ID must be integer",
            status_code=400
        )

    if not isinstance(quantity, int):
        return error_response(
            message="Quantity must be integer",
            status_code=400
        )

    if quantity <= 0:
        return error_response(
            message="Quantity must be greater than zero",
            status_code=400
        )

    item_id, error = order_item.create_order_item(order_id, item)

    if error:
        return error_response(
            message=error,
            status_code=400
        )

    item = order_item.get_order_item_by_id(item_id)

    return success_response(
        data=item,
        message="Product added successfully",
        status_code=201
    )


# update product quantity in current user's unpaid order
def update_order_item(item_id):
    current_user, auth_error = get_current_user_from_token()
    if auth_error:
        return auth_error

    item = request.json or {}

    updated_item, error = order_item.update_order_item(item_id, item, current_user["id"])

    if error:
        return error_response(
            message=error,
            status_code=400
        )

    return success_response(
        data=updated_item,
        message="Order item updated successfully",
        status_code=200
    )


# delete product from current user's unpaid order
def delete_order_item(item_id):
    current_user, auth_error = get_current_user_from_token()
    if auth_error:
        return auth_error

    error = order_item.delete_order_item(item_id, current_user["id"])

    if error:
        return error_response(
            message=error,
            status_code=400
        )

    return success_response(
        data=None,
        message="Order item deleted successfully",
        status_code=200
    )
