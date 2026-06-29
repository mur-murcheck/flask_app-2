# import the halper function, responsible for opening, 
# providing and safely closing a database connection 
# for each HTTP request
from src.models.database import get_db

def create_order(user_id, items):
    # get database connection
    db = get_db()
    # create cursor - is the tool that sends SQL commands to MySQL
    cursor = db.cursor()

    total_amount = 0
    total_categories = len(items)
    prepared_items = []

    # check every product before creating the order
    for item in items:
        product_id = item["product_id"]
        quantity = item["quantity"]

        cursor.execute("SELECT * FROM products WHERE ID = %s", (product_id,))
        
        product = cursor.fetchone()

        if not product:
            cursor.close()
            return None, "Product does not exist"

        if product["stock"] < quantity:
            cursor.close()
            return None, "Not enough stock"

        item_total = product["price"] * quantity
        total_amount += item_total

        prepared_items.append({
            "product_id":product_id,
            "product_name": product["name"],
            "price": product["price"],
            "quantity": quantity,
            "total": item_total
        })

    # create main order record
    cursor.execute(
        """
        INSERT INTO orders
        (user_id, total_amount, total_categories)
        VALUES (%s, %s, %s)
        """,
        (user_id, total_amount, total_categories)
    )

    order_id = cursor.lastrowid

    # save order items and reduce product stock for item in prepared_items
    for item in prepared_items:
        cursor.execute(
            """INSERT INTO order_items
            (order_id, product_id, product_name, price, quantity, total)
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (
                order_id,
                item["product_id"],
                item["product_name"],
                item["price"],
                item["quantity"],
                item["total"]
            )
        )

        cursor.execute(
            """
            UPDATE products
            SET stock = stock - %s
            WHERE id = %s
            """,
            (item["quantity"], item["product_id"])
        )

    db.commit()
    cursor.close()

    return get_order_receipt(order_id), None


def get_order_receipt(order_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        """
        SELECT
            orders.id AS order_id,
            orders.user_id,
            users.name AS user_name,
            users.email,
            users.phone,
            orders.total_amount,
            orders.total_categories,
            orders.created_at
        FROM orders
        JOIN users ON orders.user_id = users.id
        WHERE orders.id = %s
        """,
        (order_id,)
    )

    order = cursor.fetchone()

    if not order:
        cursor.close()
        return None

    cursor.execute(
        """SELECT
            product_id,
            product_name,
            price,
            quantity,
            total
        FROM order_items
        WHERE order_id = %s
        """,
        (order_id,)
    )
    
    items = cursor.fetchall()

    cursor.close()

    order["items"] = items
    return order


def delete_order(order_id):
    # first check whether the order exists before deleting
    existing_order = get_order_receipt(order_id)

    print(existing_order)
    print(type(existing_order))

    # if order does not exist, return False to controller
    # controller will convert this result to 404 error response
    if not existing_order:
        return False

    db = get_db()
    cursor = db.cursor()
    # delete order from orders table by id
    cursor.execute(
        "DELETE FROM orders WHERE id = %s",
        (order_id,)
    )

    # save DELETE changes to MySQL
    db.commit()
    # close cursor after DELETE is done
    cursor.close()

    # return True to controller 
    # to indicate that order was deleted
    return True