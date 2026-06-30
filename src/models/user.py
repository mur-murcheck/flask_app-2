from src.models.database import get_db

def get_all_users():
    # get database connection from database model
    db = get_db()
    # create cursor object to execute SQL commands
    cursor = db.cursor()
    # select all users records from users table
    cursor.execute("SELECT * FROM users")
    # fetchall() returns all rows from the SELECT result
    users = cursor.fetchall()
    # close cursor after database operation is done
    cursor.close()

    # return all users back to controller
    return users


def get_user_by_id(user_id):
    db = get_db()
    cursor = db.cursor()
    # search one user by id
    # %s is a placeholder
    # user_id is passed separetly to avoid SQL injection
    cursor.execute("SELECT * FROM users WHERE id = %s",
        (user_id,)
    )
    # fetchone() returns one row if found 
    # or None if user does not exist    
    user = cursor.fetchone()
    cursor.close()

    # return found user or None back to controller
    return user


def create_user(name, email, phone, address):
    db = get_db()
    cursor = db.cursor()
    # insert new user data into users table
    # id is not provided because it is autoincrement in MySQL
    cursor.execute(
        """
        INSERT INTO users (name, email, phone, address) 
        VALUES (%s, %s, %s, %s)
        """,
        (name, email, phone, address)
    )
    # save INSERT changes to MySQL
    db.commit()
    # get id of the new created user
    new_user_id = cursor.lastrowid
    # close cursor after INSERT is done
    cursor.close()

    # return newly created user data
    return new_user_id


def check_user_exists(email: str): 
    db = get_db()
    cursor = db.cursor()
    # check whether a user with the same email already exists
    # email must be unique according to v2_README
    cursor.execute(
        "SELECT * FROM users WHERE email = %s LIMIT 1",
        (email,)
    )
    # fetchone() returns existing user data or None
    existing_user = cursor.fetchone()
    cursor.close()

    # return existing user to controller
    # if result is None, controller knows this email can be used
    return existing_user


def update_user(user_id, name, email, phone):
    # first get current user data before update
    user_before_update = get_user_by_id(user_id)

    # if user doesn't exist, return None to controller
    # controller will convert this result to 404 response
    if not user_before_update:
        return None
    # if name was not provided in request, keep old name 
    if name is None:
        name = user_before_update["name"]
    # if email was not provided in request, keep old email
    if email is None:
        email = user_before_update["email"]
    # if phone was not provided in request, keep old phone
    if phone is None:
        phone = user_before_update["phone"]
    # if address was not provided in request, keep old address
    if address is None:
        address = user_before_update["address"]

    db = get_db()
    cursor = db.cursor()
    # update user data by ID
    # only one user should be updated 
    # because WHERE id = %s is used
    cursor.execute(
        """
        UPDATE users
        SET
            name = %s,
            email = %s,
            phone = %s,
            address = %s
        WHERE id = %s
        """,
        (name, email, phone, user_id)
    )
    # save UPDATE changes to MySQL
    db.commit()
    # close cursor after UPDATE is done
    cursor.close()

    # return updated user data back to controller
    return get_user_by_id(user_id)


def delete_user(user_id):
    # first check whether user exists before deleting
    desired_user = get_user_by_id(user_id)

    # if user doesn't exist, return False to controller
    # controller will convert this result to 404 response
    if not desired_user:
        return False

    db = get_db()
    cursor = db.cursor()
    # delete user from users table by id
    cursor.execute(
        "DELETE FROM users WHERE id = %s",
        (user_id,)
    )
    # save delete changes to MySQL 
    db.commit()
    # close cursor after DELETE is done
    cursor.close()

    # return True to tell controller that delete operation succeeded
    return True