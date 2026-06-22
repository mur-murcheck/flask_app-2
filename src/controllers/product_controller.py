from flask import jsonify
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
