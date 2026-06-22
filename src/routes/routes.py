from flask import Blueprint

from src.controllers import health_controller as healthContr
from src.controllers import product_controller as productContr

route = Blueprint("api_v2", __name__)

route.route("/healthCheck", methods=["GET"])(healthContr.health_check)
route.route("/products", methods=["GET"])(productContr.get_product)
route.route("/products/<int:product_id>", methods=["GET"])(productContr.get_product_by_id)
route.route("/products", methods=["POST"])(productContr.create_product)
route.route("/products/<int:product_id>", methods=["POST"])(productContr.update_product)

# route.route("/users", methods=["GET", "POST"])(userConrtoller.get_user) 
