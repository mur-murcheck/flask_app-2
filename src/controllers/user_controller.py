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

    # if request.method == 'POST':
        # inputData = request.json
        # name = inputData.get('name')
        # member_id = inputData.get('member_id')

    # if not inputData:
        #return jsonify(members)

    # if name is not None and not isinstance(name, str):
        # return jsonify({
        #     "success": False,
        #     "message": "Name must be string"
        # })        

    # if member_id is not None and not isinstance(member_id, str):
        # return jsonify({
        #     "success": False,
        #     "message": "Member ID must be string"
        # })

    # if name:
    #     result = {}
    #     for member_id in members:
    #         member = members[member_id]

    #         if name in member["name"]:
    #             result[member_id] = member

    #     return jsonify(result)

    # if member_id:
    #     if member_id in members:
    #         return jsonify({
    #             member_id: members[member_id]
    #         })
    #     return jsonify({})

# user ID comes from route /users/search-by-id/<user_id>
def get_user_by_id(user_id):
    found_user = user.get_user_by_id(user_id)

    # if model returns None, it means user does not exist
    if not found_user:
        return error_response(
            message="User not found",
            status_code=404
        )
    # return found user using unified response helper
    return success_response(
        data=found_user,
        message="User retrieved successfully",
        status_code=200
    )

    # return jsonify(members)
def get_users():
    # ask model to get all users from MySQL
    users = user.get_all_users()

    return success_response(
        data=users,
        message="Users retrieved successfully",
        status_code=200
    )


def update_user(user_id):
    inputData = request.json

    name = inputData.get("name")
    email = inputData.get("email")
    phone = inputData.get("phone")

    updated_user = user.update_user(
        user_id,
        name,
        email,
        phone
    )

    if updated_user is None:
        return error_response(
            message="User not found",
            status_code=404
        )

    return success_response(
        data=updated_user,
        message="User updated successfully",
        status_code=200
    )


# V1 does not have delete member logic
# v2 adds delete user API based on CRUD requirements
def delete_user(user_id):
    result = user.delete_user(user_id)

    if not result:
        error_response(
            message="User not found",
            status_code=404
        )
    return success_response(
        data=result,
        message="User deleted successfully",
        status_code=200
    )
