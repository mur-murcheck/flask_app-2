from src.models.database import get_db

def create_order_item(order_id, item):
    db = get_db()
    cursor = db.cursor()
    
    # Get product_id from current item
    product_id = item["product_id"]
    # Get quantity from current item
    quantity = item["quantity"]

    # V1 used goods[product_id] to find a product in the goods dictionary
    # V2 uses SELECT to find the product in MySQL
    cursor.execute("SELECT * FROM products WHERE id = %s", (product_id,))
    
    # fetchone() returns one product row if it exists, 
    # otherwise it returns None
    product = cursor.fetchone()

    # If product does not exist in MySQL, stop order creation
    if not product:
        cursor.close()
        return None, "Product does not exist"

    # Check whether product stock is enough for requested quantity
    if product["stock"] < quantity:
        cursor.close()
        return None, "Not enough stock"


    # insert one receipt item into order_items
    cursor.execute(
        """INSERT INTO order_items
        (order_id, product_id, price, product_name, quantity)
        VALUES (%s, %s, %s, %s, %s)
        """,
        (
            order_id,
            item["product_id"],
            product["price"],
            product["name"],
            item["quantity"]
        )
    )
    order_item_id = cursor.lastrowid

    # reduce product stock after the item is added to the order
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

    return order_item_id, None


def get_order_item_by_id(item_id):
    # get database connection
    db = get_db()
    # create cursor - is the tool that sends SQL commands to MySQL
    cursor = db.cursor()

    # select all item rows that belong to this order
    cursor.execute(
        """SELECT
            id,
            product_id,
            product_name,
            price,
            quantity
        FROM order_items
        WHERE id = %s
        """,
        (item_id,)
    )
    
    item = cursor.fetchone()

    # close cursor after reading all data
    cursor.close()

    return item


def update_order_item(item_id, item):
    existing_item = get_order_item_by_id(item_id)

    if not existing_item:
        return None, "Order item does not exist"

    quantity = item.get("quantity")

    if not quantity:
        return None, "Quantity is required"

    # Quantity must be positive
    if quantity <= 0:
        return None, "Quantity must be greater than zero"

    # get database connection
    db = get_db()
    # create cursor - is the tool that sends SQL commands to MySQL
    cursor = db.cursor()   

    cursor.execute("SELECT * FROM products WHERE id = %s", (existing_item["product_id"],))
    
    # fetchone() returns one product row if it exists, 
    # otherwise it returns None
    product = cursor.fetchone()

    new_stock = product["stock"] + existing_item["quantity"] - quantity

    if new_stock < 0:
        cursor.close()
        return None, "Not enough stock"

    cursor.execute("UPDATE order_items SET quantity = %s WHERE id = %s", (quantity, item_id))

    cursor.execute("UPDATE products SET stock = %s WHERE id = %s", (new_stock,existing_item["product_id"]))

    db.commit()
    cursor.close()
    
    return get_order_item_by_id(item_id), None


def delete_order_item(item_id):
    existing_item = get_order_item_by_id(item_id)

    if not existing_item:
        return "Order item does not exist"

    # get database connection
    db = get_db()
    # create cursor - is the tool that sends SQL commands to MySQL
    cursor = db.cursor()

    cursor.execute("DELETE FROM order_items WHERE id = %s", (item_id,))

    cursor.execute("UPDATE products SET stock = stock + %s WHERE id = %s", 
                (existing_item["quantity"], existing_item["product_id"]))

    db.commit()
    cursor.close()

    return None