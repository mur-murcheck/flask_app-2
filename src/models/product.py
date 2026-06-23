from src.models.database import get_db

def get_all_products():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    cursor.close()

    return products


def get_product_by_id(product_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "SELECT * FROM products WHERE id = %s",
        (product_id,)
    )
    product = cursor.fetchone()
    cursor.close()

    return product


def create_product(name, price, description, stock):
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO products (name, price, description, stock) VALUES (%s, %s, %s, %s)",
        (name, price, description, stock)
    )
    db.commit()
    new_product_id = cursor.lastrowid
    cursor.close()

    return new_product_id

def update_product(product_id, name, price, description, stock):
    product_before_update = get_product_by_id(product_id)

    if name is None:
        name = product_before_update["name"]

    if price is None:
        price = product_before_update["price"]

    if description is None:
        description = product_before_update["description"]

    if stock is None:
        stock = product_before_update["stock"]
    
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        """
        UPDATE products
        SET 
            name = %s,
            price = %s,
            description = %s,
            stock = %s
        WHERE id = %s
        """,
        (name, price, description, stock, product_id)
    )
    db.commit()
    cursor.close()

    return get_product_by_id(product_id)