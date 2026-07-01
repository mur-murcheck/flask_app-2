from flask import request
from src.models import order, order_item # it is the Models; controller uses it to ask for data from SQL
from src.functions.response import success_response, error_response # unified responses


def add_product():
    # read and auth key from request headers
    auth_token = request.headers.get("X-Auth-Token")

    # Auth key is required
    if not auth_token:
        return error_response(
            message="Auth key is required",
            status_code=401
        )

    order_id = order.get_existing_order_id(auth_token)

    if order_id is None:
        return error_response(
            message="Order does not exist",
            status_code=400
        )

    item = request.json

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


def get_order_item(item_id):
    item = order_item.get_order_item_by_id(item_id)

    if not item:
        return error_response(
            message="Order item does not exist",
            status_code=404
        )

    return success_response(
        data=item,
        message="Order item retrieved successfully",
        status_code=200
    )

def update_order_item(item_id):
    # read and auth key from request headers
    auth_token = request.headers.get("X-Auth-Token")

    # Auth key is required
    if not auth_token:
        return error_response(
            message="Auth key is required",
            status_code=401
        )

    item = request.json

    item, error = order_item.update_order_item(item_id, item)

    if error:
        return error_response(
            message=error,
            status_code=400
        )

    return success_response(
        data=item,
        message="Order item updated successfully",
        status_code=200
    )


def delete_order_item(item_id):
    # read and auth key from request headers
    auth_token = request.headers.get("X-Auth-Token")

    # Auth key is required
    if not auth_token:
        return error_response(
            message="Auth key is required",
            status_code=401
        )

    error = order_item.delete_order_item(item_id)

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
