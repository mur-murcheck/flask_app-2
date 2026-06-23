from flask import jsonify

# utility functions (helper)
# gonna be used in controllers to return a success response 
# with data and message in json format with status code 200
def success_response(data=None, message="Success", status_code=200):
  payload = {"success": True, "message": message}
  if data is not None:
    payload["data"] = data
  return jsonify(payload), status_code


def error_response(message, status_code=400):
  return jsonify({"success": False, "message": message}), status_code
