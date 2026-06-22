from flask import jsonify
from src.models import product

def get_product():
    products = product.get_all_products()

    return jsonify({
        "success": True,
        "message": "Products retrieved successfully",
        "items": products
    }), 200