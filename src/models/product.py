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
    cursor.execute("SELECT * FROM products WHERE id = %s",
    (product_id,))
    product = cursor.fetchone()
    cursor.close()

    return product
