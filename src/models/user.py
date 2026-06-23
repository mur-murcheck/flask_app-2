from src.models.database import get_db

def get_all_users():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    cursor.close()

    return users


def create_user(name, email, phone):
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        """
        INSERT INTO users (name, email, phone) 
        VALUES (%s, %s, %s)
        """,
        (name, email, phone)
    )
    db.commit()
    new_user_id = cursor.lastrowid
    cursor.close()

    return new_user_id


def check_user_exists(phone: str, name: str, email: str): 
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "SELECT * FROM users WHERE phone = %s AND name = %s OR email = %s LIMIT 1",
        (phone,name,email)
    )
    existing_user = cursor.fetchone()
    cursor.close()

    return existing_user


def get_user_by_id(user_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users WHERE id = %s",
        (user_id,)
    )
    user = cursor.fetchone()
    cursor.close()

    return user