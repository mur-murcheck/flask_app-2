from flask import request #to read body/JSON from Postman
from src.models import product # it is the Model; controller uses it to ask for data from SQL
from src.functions.response import success_response, error_response # unified responses; 
# keep all API responses in the same format


def get_products():
# v1 
# @app.route("/showGoods", methods=["GET", "POST"])
# def show_goods():

# In v1 GET returned all goods
# POST searched goods by name, product_id or price

# v2 keeps the same business logic,
# but data comes from MySQL through the product model

    # v1 
    # goods_list = []

    # v1 
    # for product_id in goods:
    #     item = goods[product_id]
    #     goods_list.append({
    #         "product_id": product_id,
    #         "name": item["name"],
    #         "price": item["price"]
    #     })

    # v1 
    # if request.method == "POST":
    #     inputData = request.json
    inputData = request.json or {}

    # .get search conditions from request body.
    # In v2 search conditions still come from request JSON, 
    # but actual searching is done by model/MySQL
   
    # v1
    #     name = inputData.get("name")
    #     product_id = inputData.get("product_id")
    #     price = inputData.get("price")

    # read possible search fields from request JSON
    name = inputData.get("name")
    price = inputData.get("price")
    product_id = inputData.get("product_id")

    # if request body is empty, return all products list

    # v1 
    # if not inputData:
    if not inputData:
        # ask model to get all products from MySQL
        products = product.get_all_products()
    #   v1 
    #   return jsonify(goods_list)

        # return product list with  unified success response helper
        return success_response(
            data=products, 
            message="Products retrieved successfully", 
            status_code=200
        )

    # search products by partial name if name was provided
    if name:
        # ask model to search products by LIKE query in MySQL
        found_product = product.get_product_by_name(name)
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

        # return all products that matched the name condition
        return success_response(
            data=found_product,
            message="Products retrieved successfully",
            status_code=200
        )

    # if product_id:
    if product_id:
        found_product = product.get_product_by_id(product_id)
    #     if not isinstance(product_id, int):
    #         return jsonify({
    #             "success": False,
    #             "message": "Product ID must be integer"
    #         })
        if not found_product:
            return error_response(
                message="Product not found",
                status_code=404
            )
    #     result = []
    #     for item in goods_list:
    #         if item["product_id"] == product_id:
    #             result.append(item)

    #     return jsonify(result)    
        return success_response(
            data=found_product,
            message="Product found successfully",
            status_code=200
        )
        
        # if price:
    # search product by price condition if price was provided
    # expected format follows v1 logic: ">= 40" or "<= 40"
    if price:
        #     if not isinstance(price, str):
        #         return jsonify({
        #             "success": False,
        #             "message": "Price format must be '>= value' or '<= value'"
        #         })

        #     split_data = price.split(" ", 2)

        # split price string into operator and value
        # Exe: "<= 40" becomes operator="<=", price_value="40"
        split_data = price.split(" ", 1)
        #     if len(split_data) != 2:
        #         return jsonify({
        #             "success": False,
        #             "message": "Price format must be '>= value' or '<= value'"
        #         })

        # if splited result does not have two parts, request format is invalid
        if len(split_data) != 2:
            return error_response(
                message="Price format must be '>= value' or '<= value'",
                status_code=400
            )

        #     result = []
        #     operator = split_data[0]

        # first part is operator: >= or <=
        operator = split_data[0]

        #     price = split_data[1]
        
        # second part is price value as text (string(str))
        price_value = split_data[1]

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

        # if operator ">=", search products with price greater than
        # or equal to price_value
        if operator == ">=":
            products = product.get_product_by_min_price(price_value)
        #         return jsonify(result)
            return success_response(
                data=products,
                message="Products retrieved successfully",
                status_code=200
            )

        #     elif operator == "<=":
        #         for item in goods_list:
        #             if item["price"] <= price:
        #                 result.append(item)

        # if operator "<=", search products with price less than
        # or equal to price_value
        if operator == "<=":
            products = product.get_product_by_max_price(price_value)
            # return jsonify(result)
            return success_response(
                data=products,
                message="Products retrieved successfully",
                status_code=200
            )
            # return jsonify({
            #     "success": False,
            #     "message": "Price format must be '>= value' or '<= value'"
            # })

        # if operator is not ">=" or "<=", return unified error response
        return error_response(
            message="Invalid price operator",
            status_code=400
        )

     # return jsonify(goods_list)

    # if no search condition is provided, return error_response
    return error_response(
        message="No search condition is provided",
        status_code=200
    )

# v1 did'n use MySQL. Product data was stored in a Python dictionary
# v2 creates a product in MySQL and returns the created product
def create_product():
    # get product data from request body
    input_data = request.json

    # read product fields from JSON body
    name = input_data.get("name")
    price = input_data.get("price")
    description = input_data.get("description")
    stock = input_data.get("stock")

    # name is required according to README 
    if not name:
        return error_response(
            message="Name is required",
            status_code=400
        )

    # price is required according to README
    if price is None:
        return error_response(
            message="Price is required",
            status_code=400
        )

    # price can't be negative according to README
    if price < 0:
        return error_response(
            message="Price cannot be negative",
            status_code=400
        )

    # stock is optional. If client does not send stock,
    # default value is 0
    if stock is None:
        stock = 0
    
    # ask model to insert new product into MySQL
    new_product_id = product.create_product(
        name=name, 
        description=description, 
        stock=stock, 
        price=price
    )
    # get created product by generated id 
    # so response contains full product data
    created_product = product.get_product_by_id(new_product_id)

    # return created product with 201 created status
    return success_response(
        data=created_product,
        message="Product created successfully",
        status_code=201
    )


# v2 updates an existing product by id
# it supports partial update: only fields sent in request body are changed
def update_product(product_id):
    # get update data from request body
    input_data = request.json

    # read optional fields from JSON body
    name = input_data.get("name")
    price = input_data.get("price")
    description = input_data.get("description")
    stock = input_data.get("stock")

    # if name was sent as empty string, treat it as invalid input
    if name == "":
        return error_response(
            message="Name is required",
            status_code=400
        )

    # if price was sent, it can not be negative
    if price is not None and price < 0:
        return error_response(
            message="Price cannot be negative",
            status_code=400
        )

    # ask model to update product in MySQL
    updated_product = product.update_product(
        product_id,
        name,
        price,
        description,
        stock
    )

    # if model returns None, product does not exist
    if updated_product is None:
        return error_response(
            message="Product not found",
            status_code=404
        )

    # return updated product
    return success_response(
        data=updated_product,
        message="Product updated successfully",
        status_code=200
    )


# V1 does not have delete product logic
# v2 adds delete product API based on CRUD requirements
def delete_product(product_id):
    # ask model to delete model product by id
    result = product.delete_product(product_id)

    # if model returns False/None, product was not found
    if not result:
        return error_response(
            message="Product not found",
            status_code=404
        )

    # return success response after product was deleted
    return success_response(
        message="Product deleted successfully",
        status_code=200
    )