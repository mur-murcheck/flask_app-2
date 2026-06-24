from flask import Blueprint

from src.controllers import health_controller as healthContr
from src.controllers import product_controller as productContr
from src.controllers import user_controller as userContr

route = Blueprint("api_v2", __name__)

route.route("/healthCheck", methods=["GET"])(healthContr.health_check)
route.route("/products/list", methods=["GET"])(productContr.get_products)
route.route("/products/search-by-id/<int:product_id>", methods=["GET"])(productContr.get_product_by_id)
route.route("/products/create", methods=["POST"])(productContr.create_product)
route.route("/products/update-by-id/<int:product_id>", methods=["POST"])(productContr.update_product)
route.route("/products/delete/<int:product_id>", methods=["POST"])(productContr.delete_product)

route.route("/users/create", methods=["POST"])(userContr.create_user)
route.route("/users/list", methods=["GET"])(userContr.get_users)
route.route("/users/search-by-id/<int:user_id>", methods=["GET"])(userContr.get_user_by_id)
route.route("/users/update-by-id/<int:user_id>", methods=["POST"])(userContr.update_user)
route.route("/users/delete/<int:user_id>", methods=["POST"])(userContr.delete_user)