from flask import jsonify


def health_check():
  return jsonify({
    "success": True,
    "message": "I am healthy!",
    "version": "v2",
  }), 200
