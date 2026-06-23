from flask import request #to read body/JSON from Postman
from src.models import product # it is the Model; controller uses it to ask for data from SQL
from src.functions.response import success_response, error_response # unified responses




# def update_product(product_id):
#     input_data = request.json

#     name = input_data.get("name")
#     price = input_data.get("price")
#     description = input_data.get("description")
#     stock = input_data.get("stock")

#     updated_product = product.update_product(
#         product_id,
#         name,
#         price,
#         description,
#         stock
#     )

#     return jsonify({
#         "success": True,
#         "message": "Product updated successfully",
#         "item": updated_product
#     }),200

# @app.route("/showGoods", methods=["GET", "POST"])
# def show_goods():
def get_products():
    # ask model to get all products from MySQL
    products = product.get_all_products()
    # goods_list = []

    # for product_id in goods:
    #     item = goods[product_id]
    #     goods_list.append({
    #         "product_id": product_id,
    #         "name": item["name"],
    #         "price": item["price"]
    #     })
    return success_response(
        data=products, 
        message="Products retrieved successfully", 
        status_code=200
    )

    # if request.method == "POST":
    #     inputData = request.json
    #     name = inputData.get("name")
    #     product_id = inputData.get("product_id")
    #     price = inputData.get("price")

    #     if not inputData:
    #         return jsonify(goods_list)

        # if name:
        #     if not isinstance(name, str):
        #         return jsonify({
        #             "success": False,
        #             "message": "Name must be string"
        #         })

        #     result = []
        #     for item in goods_list:
        #         if name in item["name"]:
        #             result.append(item)

        #     return jsonify(result)

def get_product_by_id(product_id):
    # if product_id:
    #     if not isinstance(product_id, int):
    #         return jsonify({
    #             "success": False,
    #             "message": "Product ID must be integer"
    #         })

    #     result = []
    #     for item in goods_list:
    #         if item["product_id"] == product_id:
    #             result.append(item)

    #     return jsonify(result)    

    # get one products from MySQL by product_id
    found_product = product.get_product_by_id(product_id)

    # if product does not exist, return 400 error
    if not found_product:
        return error_response(
            message="Product not found",
            status_code=400
        )
    # if found product using the unified success response
    return success_response(
        data=found_product,
        message="Product retrieved successfully",
        status_code=200
    )

        # if price:
        #     if not isinstance(price, str):
        #         return jsonify({
        #             "success": False,
        #             "message": "Price format must be '>= value' or '<= value'"
        #         })

        #     split_data = price.split(" ", 2)
        #     if len(split_data) != 2:
        #         return jsonify({
        #             "success": False,
        #             "message": "Price format must be '>= value' or '<= value'"
        #         })

        #     result = []
        #     operator = split_data[0]
        #     price = split_data[1]

        #     if not price:
        #         return jsonify({
        #             "success": False,
        #             "message": "Price must not be empty"
        #         })

        #     try:
        #         price = int(price)
        #     except ValueError:
        #         return jsonify({
        #             "success": False,
        #             "message": "Price must be integer"
        #         })

        #     if operator == ">=":
        #         for item in goods_list:
        #             if item["price"] >= price:
        #                 result.append(item)

        #         return jsonify(result)

        #     elif operator == "<=":
        #         for item in goods_list:
        #             if item["price"] <= price:
        #                 result.append(item)

            # return jsonify(result)

            # return jsonify({
            #     "success": False,
            #     "message": "Price format must be '>= value' or '<= value'"
            # })

    # return jsonify(goods_list)

def create_product():
    input_data = request.json

    name = input_data.get("name")
    price = input_data.get("price")
    description = input_data.get("description")
    stock = input_data.get("stock")

    if not name:
        return error_response(
            message="Name is required",
            status_code=400
        )

    if price is None:
        return error_response(
            message="Price is required",
            status_code=400
        )
    
    new_product_id = product.create_product(name=name, description=description, stock=stock, price=price)
    created_product = product.get_product_by_id(new_product_id)

    return success_response(
        data=created_product,
        message="Product created successfully",
        status_code=201
    )
