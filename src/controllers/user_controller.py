# v1 imports
from flask import Flask, jsonify, request
import uuid
# v2 only needs request in controller because JSON responses are
# created by response helpers
from flask import request
# import unified response helpers to keep response format consistent 
# in all controllers
from src.functions.response import success_response, error_response
# import user model
# controller asks model to read/write data in MySQL
from src.models import user


# v1 def add_member():
# v2 function creates a user in MySQL 
# instead of saving mamber data in a Python dictionary
def create_user():
    # get JSON body sent from Postman 
    inputData = request.json
    # print("input: ", inputData)

    # get fields from request body
    # .get() returns value if key exists, otherwise returns None
    name = inputData.get("name")
    phone = inputData.get("phone")
    # address = inputData.get("address")
    # v1 used address field
    # but v2_README uses email instead
    email = inputData.get("email")

    # validate required name field
    if not name:
        # v1 returned jsonify directly
        # return jsonify({
        #     "success": False,
        #     "message": "Name is required"
        # })
        
        # v2 uses unified error_response helper 
        return error_response(
            message="Name is required",
            status_code=400
        )

    # validate name type
    # name must be string because database should store text,
    # but not number/list/boolean
    if not isinstance(name, str):
        # return jsonify({
        #     "success": False,
        #     "message": "Name must be string"
        # })
        return error_response(
            message="Name must be string",
            status_code=400
        )

    # phone is not required according to v2_README
    # v1 required phone, so old required-phone validation is kept as comment
    # if not phone:
        # return jsonify({
        #     "success": False,
        #     "message": "Phone is required"
        # })

    # v1 phone validation 
    # if not isinstance(phone, str):
        # return jsonify({
        #     "success": False,
        #     "message": "Phone must be string"
        # })

    # v1 phone digit validation
    # if not phone.isdigit() or len(phone) != 10:
    #     return jsonify({
    #         "success": False,
    #         "message": "Phone must contain 10 digits"
    #     })

    # v2: if phone is provided, it must be string
    # if phone is None, controller skip this check because phone is optional
    if phone is not None and not isinstance(phone, str):
        return error_response(
            message="Phone must be string",
            status_code=400
        )

    # v2: if phone is provided, it must contain exactly 10 digits
    if phone is not None and (not phone.isdigit() or len(phone) != 10):
        return error_response(
            message="Phone must contain 10 digits",
            status_code=400
        )

    # v1 required address, but v2 requires email instead
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

    # v1 checked address type, v2 checks email type
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

    # validate email format
    # this is a simple check required by v2_README
    if "@" not in email:
        return error_response(
            message="Invalid email format",
            status_code=400
        )

    # v1 checked duplicate member data in Python dictioinary
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

    # v2 checks duplicate user by email in MySQL
    # email must be unique according to v2_README
    user_exists = user.check_user_exists(email=email)

    # if model found an existing user, return 409 conflict
    if user_exists:
        return error_response(
            message="User already exists", 
            status_code=409
        )

    # v1 created member_id by uuid and stored member in memory dictionary
    # user_id = str(uuid.uuid4())

    # members[member_id] = {
    #     "name": name,
    #     "phone": phone,
    #     "address": address
    # }

    # v2 saves user data to db MySQL through model function
    new_user_id = user.create_user(name, email, phone)
    # get new user data from MySQL by id
    # this allows response the real database record
    created_user = user.get_user_by_id(new_user_id)

    # return created user with 201 status code 
    return success_response(
        data=created_user,
        message="User created successfully",
        status_code=201
    )

    # v1 also created empty cart for new member
    # carts[member_id] = []

    # v1 response
    # return jsonify({
    #     "success": True,
    #     "message": "Order information added successfully",
    #     "member_id": member_id
    # })

# v1 showMembers endpoint
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

# v2: user ID comes from route /users/search-by-id/<user_id>
def get_user_by_id(user_id):
    # ask model to find one user by id in MySQL
    found_user = user.get_user_by_id(user_id)

    # if model returns None, it means user does not exist
    if not found_user:
        return error_response(
            message="User not found",
            status_code=404
        )

    # v1 returned members dictionary directly
    # return jsonify(members)

    # v2 returns found user using unified response helper
    return success_response(
        data=found_user,
        message="User retrieved successfully",
        status_code=200
    )


def get_users():
    # ask model to get all users from MySQL
    users = user.get_all_users()

    # return all users using unified resonse helper
    return success_response(
        data=users,
        message="Users retrieved successfully",
        status_code=200
    )


# V1 does not have update member logic
# v2 adds updates user API based on CRUD requirements
def update_user(user_id):
    # get JSON body sent from Postman
    inputData = request.json

    # get update fields from request body
    # any fields can be None because update supports partial update
    name = inputData.get("name")
    email = inputData.get("email")
    phone = inputData.get("phone")

    # ask model to update user in MySQL
    # model will keep old values for fields that are None
    updated_user = user.update_user(
        user_id,
        name,
        email,
        phone
    )

    # if model returns None, user wasn't found
    if updated_user is None:
        return error_response(
            message="User not found",
            status_code=404
        )

    # return updated user using unified response helper
    return success_response(
        data=updated_user,
        message="User updated successfully",
        status_code=200
    )


# V1 does not have delete member logic
# v2 adds delete user API based on CRUD requirements
def delete_user(user_id):
    # ask model to delete user by id
    result = user.delete_user(user_id)

    # if model returns False/None, user was not found
    if not result:
        return error_response(
            message="User not found",
            status_code=404
        )

    # return success response after user was deleted
    return success_response(
        data=result,
        message="User deleted successfully",
        status_code=200
    )
