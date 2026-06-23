from flask import request #to read body/JSON from Postman
from src.models import product # it is the Model; controller uses it to ask for data from SQL
from src.functions.response import success_response, error_response # unified responses

def get_product():
    # ask model to get all products from MySQL
    products = product.get_all_products()

    # return products using the unified success response format
    # return jsonify({
    #     "success": True,
    #     "message": "Products retrieved successfully",
    #     "items": products
    # }), 200
    return success_response(
        data=products, 
        message="Products retrieved successfully", 
        status_code=200
    )

def get_product_by_id(product_id):
    # get one products from MySQL by product_id
    found_product = product.get_product_by_id(product_id)

    # if product does not exist, return 404 error
    if not found_product:
    #     return jsonify({
    #         "success": False,
    #         "message": "Product not found"
    #     }), 404
        return error_response(
            message="Product not found",
            status_code=404
        )
    # if found product using the unified success response
    return success_response(
        data=found_product,
        message=""
    )

    return jsonify({
        "success": True,
        "message": "Product retrieved successfully",
        "item": found_product
    }), 200

def create_product():
    input_data = request.json

    name = input_data.get("name")
    price = input_data.get("price")
    description = input_data.get("description")
    stock = input_data.get("stock")

    if not name or price is None:
        return jsonify({
            "success": False,
            "message": "Name and price are required"
        }), 400
    
    new_product_id = product.create_product(name=name, description=description, stock=stock, price=price)
    created_product = product.get_product_by_id(new_product_id)

    return jsonify({
        "success": True,
        "message": "Product created successfully",
        "item": created_product
    }), 201


def update_product(product_id):
    input_data = request.json

    name = input_data.get("name")
    price = input_data.get("price")
    description = input_data.get("description")
    stock = input_data.get("stock")

    updated_product = product.update_product(
        product_id,
        name,
        price,
        description,
        stock
    )

    return jsonify({
        "success": True,
        "message": "Product updated successfully",
        "item": updated_product
    }),200