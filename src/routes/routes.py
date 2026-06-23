from flask import Blueprint

from src.controllers import health_controller as healthContr
from src.controllers import product_controller as productContr
# from src.controllers import member_controller as memberContr

route = Blueprint("api_v2", __name__)

route.route("/healthCheck", methods=["GET"])(healthContr.health_check)
route.route("/products/list", methods=["GET"])(productContr.get_products)
# route.route("/products/search-by-id/<int:product_id>", methods=["GET"])(productContr.get_product_by_id)
# route.route("/products/create", methods=["POST"])(productContr.create_product)
# route.route("/products/update-by-id/<int:product_id>", methods=["POST"])(productContr.update_product)

# # route.route("/users", methods=["GET", "POST"])(userConrtoller.get_user) 
# route.route("/member/add", methods=["POST"])(memberContr.register)
# route.route("/member/list", methods=["GET"])(memberContr.get_member)