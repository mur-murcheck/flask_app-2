from src.models.database import get_db

def get_all_users():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    cursor.close()

    return users


def get_user_by_id(user_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users WHERE id = %s",
        (user_id,)
    )
    user = cursor.fetchone()
    cursor.close()

    return user


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


def update_user(user_id, name, email, phone):
    user_before_update = get_user_by_id(user_id)

    if not user_before_update:
        return None

    if name is None:
        name = user_before_update["name"]

    if email is None:
        email = user_before_update["email"]

    if phone is None:
        phone = user_before_update["phone"]

    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        """
        UPDATE users
        SET
            name = %s,
            email = %s,
            phone = %s
        WHERE id = %s
        """,
        (name, email, phone, user_id)
    )
    db.commit()
    cursor.close()

    return get_user_by_id(user_id)