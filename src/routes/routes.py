from flask import Blueprint

from src.controllers import health_controller as healthContr
from src.controllers import product_controller as productContr

route = Blueprint("api_v2", __name__)

route.route("/healthCheck", methods=["GET"])(healthContr.health_check)
route.route("/products", methods=["GET", "POST"])(productContr.get_product)
# route.route("/users", methods=["GET", "POST"])(userConrtoller.get_user) 
