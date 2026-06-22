from flask import jsonify, request
from src.models import product

def get_product():
    products = product.get_all_products()

    return jsonify({
        "success": True,
        "message": "Products retrieved successfully",
        "items": products
    }), 200

def get_product_by_id(product_id):
    found_product = product.get_product_by_id(product_id)

    if not found_product:
        return jsonify({
            "success": False,
            "message": "Product not found"
        }), 404

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
    
    new_product_id = product.create_product(name, price, description, stock)
    created_product = product.get_product_by_id(new_product_id)

    return jsonify({
        "success": True,
        "message": "Product created successfully",
        "item": created_product
    }), 201