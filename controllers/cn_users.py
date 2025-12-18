from database import mysql

def get_profile_by_user(user_id):
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT
            CONCAT(name, ' ', lastname) AS fullname,
            role,
            area,
            date_start
        FROM users
        WHERE id_user = %s
    """, (user_id,))

    result = cur.fetchone()
    cur.close()

    return result