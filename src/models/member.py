from src.models.database import get_db

def check_member_exists(phone: str, name: str): 
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "SELECT * FROM members WHERE phone = %s AND name = %s LIMIT 1",
        (phone,name)
    )
    existing_member = cursor.fetchone()
    cursor.close()

    return existing_member

