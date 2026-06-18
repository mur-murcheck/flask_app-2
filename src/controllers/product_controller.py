from flask import jsonify

def get_product():
    return jsonify({
        "success": True,
        "message": "Products retrieved successfully",
        "data": []
    }), 200