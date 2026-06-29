from flask import request #to read body/JSON from Postman
from src.models import order, user # it is the Models; controller uses it to ask for data from SQL
from src.functions.response import success_response, error_response # unified responses

def create_order():
    inputData = request.json

    user_id = inputData.get("user_id")
    items = inputData.get('items')

    if not user_id:
        return error_response(
            message="User ID is required",
            status_code=400
        )

    if not isinstance(user_id, int):
        return error_response(
            message="User Id must be integer",
            status_code=400
        )

    if not items:
        return error_response(
            message="Items are required",
            status_code=400
        )

    if not isinstance(items, list):
        return error_response(
            message="Items must be list",
            status_code=400
        )

    found_user = user.get_user_by_id(user_id)

    if not found_user:
        return error_response(
            message="User does not exist",
            status_code=404
        )

    for item in items:
        product_id = item.get("product_id")
        quantity = item.get("quantity")

        if not product_id:
            return error_response(
                message="Product Id is required",
                status_code=400
            )

        if not quantity:
            return error_response(
                message="Quantity is required",
                status_code=400
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

    receipt, error_message = order.create_order(user_id, items)

    if error_message:
        return error_response(
            message=error_message,
            status_code=400
        )

    return success_response(
        data=receipt,
        message="Order created successfully",
        status_code=201
    )


def get_order_receipt(order_id):
    receipt = order.get_order_receipt(order_id)

    if not receipt:
        return error_response(
            message="Order not found",
            status_code=404
        )

    return success_response(
        data=receipt,
        message="Order receipt retrieved successfully",
        status_code=200
    )


def delete_order(order_id):
    result = order.delete_order(order_id)

    if not result:
        return error_response(
            message="Order not found",
            status_code=404
        )

    return success_response(
        message="Order deleted successfully",
        status_code=200
    )