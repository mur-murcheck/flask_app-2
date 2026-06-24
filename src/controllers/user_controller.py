# from flask import Flask, jsonify, request
# import uuid
from flask import request
from src.functions.response import success_response, error_response
from src.models import user


# def add_member():
def create_user():
    #
    inputData = request.json
    # print("input: ", inputData)

    name = inputData.get("name")
    phone = inputData.get("phone")
    # address = inputData.get("address")
    email = inputData.get("email")

    if not name:
        # return jsonify({
        #     "success": False,
        #     "message": "Name is required"
        # })
        return error_response(
            message="Name is required",
            status_code=400
        )

    if not isinstance(name, str):
        # return jsonify({
        #     "success": False,
        #     "message": "Name must be string"
        # })
        return error_response(
            message="Name must be string",
            status_code=400
        )

    if not phone:
        # return jsonify({
        #     "success": False,
        #     "message": "Phone is required"
        # })
        return error_response(
            message="Phone is required",
            status_code=400
        )

    if not isinstance(phone, str):
        # return jsonify({
        #     "success": False,
        #     "message": "Phone must be string"
        # })
        return error_response(
            message="Phone must be string",
            status_code=400
        )

    if not phone.isdigit() or len(phone) != 10:
    #     return jsonify({
    #         "success": False,
    #         "message": "Phone must contain 10 digits"
    #     })
        return error_response(
            message="Phone must contain 10 digits",
            status_code=400
        )

    # if not address:
    if not email:
    #     return jsonify({
    #         "success": False,
    #         "message": "Address is required"
    #     })
        return error_response(
            message="Email is required",
            status_code=400
        )

    # if not isinstance(address, str):
    if not isinstance(email, str):
    #     return jsonify({
    #         "success": False,
    #         "message": "Address must be string"
    #     })
        return error_response(
            message="Email must be string",
            status_code=400
        )

    # for existing_member_id, member in members.items():

    #     if member["name"] == name and member["phone"] == phone:
    #         return jsonify({
    #             "success": True,
    #             "member_id": existing_member_id,
    #             "message": "Member already exists"
    #         })

    #     if member["phone"] == phone:
    #         return jsonify({
    #             "success": False,
    #             "member_id": existing_member_id,
    #             "message": "Phone is used already"
    #         })

    user_exists = user.check_user_exists(phone=phone,
                name=name, email=email)
    if user_exists:
        return error_response(message="User already exists", status_code=400)

    # user_id = str(uuid.uuid4())

    # members[member_id] = {
    #     "name": name,
    #     "phone": phone,
    #     "address": address
    # }

    # save member data to db
    new_user_id = user.create_user(name, email, phone)
    created_user = user.get_user_by_id(new_user_id)

    return success_response(
        data=created_user,
        message="User created successfully",
        status_code=201
    )

    # carts[member_id] = []

    # return jsonify({
    #     "success": True,
    #     "message": "Order information added successfully",
    #     "member_id": member_id
    # })


# @app.route('/showMembers', methods=['GET', 'POST'])
# def show_members():
def get_users():
    # if request.method == 'POST':
    # name = inputData.get('name')
    # member_id = inputData.get('member_id')

    # if not inputData:
        #return jsonify(members)
    # ask model to get all users from MySQL
    users = user.get_all_users()
    # if name is not None and not isinstance(name, str):
        # return jsonify({
        #     "success": False,
        #     "message": "Name must be string"
        # })        
        # return error_response(
        #     message="Name must be string", 
        #     status_code=400
        # )

    # if member_id is not None and not isinstance(member_id, str):
        # return jsonify({
        #     "success": False,
        #     "message": "Member ID must be string"
        # })
    return success_response(
        data=users,
        message="Users retrieved successfully",
        status_code=200
    )


def get_user_by_id(user_id):
    inputData = request.json
    user_id = inputData.get("user_id")

    if not inputData:
        return user.get_all_users()
    # if name:
    #     result = {}
    #     for member_id in members:
    #         member = members[member_id]

    #         if name in member["name"]:
    #             result[member_id] = member

    #     return jsonify(result)
    if user_id is not None and not isinstance(user_id, str):
        return error_response(
            message="User ID must be string",
            status_code=400
        )
    # if member_id:
    #     if member_id in members:
    #         return jsonify({
    #             member_id: members[member_id]
    #         })
    #     return jsonify({})

    found_user = user.get_user_by_id(user_id)

    # return jsonify(members)
    return success_response(
        data=found_user,
        message="User retrieved successfully",
        status_code=200
    )
