from crypt import methods
from re import search
from flask import Blueprint

from src.controllers import health_controller as healthContr
from src.controllers import product_controller as productContr
from src.controllers import user_controller as userContr
from src.controllers import order_controller as orderContr
from src.controllers import order_items_controller as itemContr

route = Blueprint("api_v2", __name__)

route.route("/healthCheck", methods=["GET"])(healthContr.health_check)
route.route("/products/list", methods=["GET", "POST"])(productContr.get_products)
route.route("/products/create", methods=["POST"])(productContr.create_product)
route.route("/products/update-by-id/<int:product_id>", methods=["POST"])(productContr.update_product)
route.route("/products/delete/<int:product_id>", methods=["POST"])(productContr.delete_product)

route.route("/users/create", methods=["POST"])(userContr.create_user)
route.route("/users/list", methods=["GET"])(userContr.get_users)
route.route("/users/search-by-id/<int:user_id>", methods=["GET"])(userContr.get_user_by_id)
route.route("/users/update-by-id/<int:user_id>", methods=["POST"])(userContr.update_user)
route.route("/users/delete/<int:user_id>", methods=["POST"])(userContr.delete_user)

route.route("/orders/create", methods=["POST"])(orderContr.create_order)
route.route("/orders/receipt/<int:order_id>", methods=["GET"])(orderContr.get_order_receipt)
route.route("/orders/delete/<int:order_id>", methods=["POST"])(orderContr.delete_order)
route.route("/orders/purchase/<int:order_id>", methods=["POST"])(orderContr.purchase)

route.route("/orders/items/create", methods=["POST"])(itemContr.add_product)
route.route("/orders/items/update/<int:item_id>", methods=["POST"])(itemContr.update_order_item)
route.route("/orders/items/delete/<int:item_id>", methods=["POST"])(itemContr.delete_order_item)