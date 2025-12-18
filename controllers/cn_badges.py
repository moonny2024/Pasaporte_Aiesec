from database import mysql
from datetime import datetime


def get_monthly_badges_by_user(user_id):
    today = datetime.today()
    month = today.month
    year = today.year

    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT
            b.id_badge,
            e.name,
            b.image,
            e.date,
            CASE
                WHEN p.id_presence IS NULL THEN 0
                ELSE 1
            END AS obtained
        FROM events e
        JOIN badges b ON e.Badgesid_badge = b.id_badge
        LEFT JOIN presence p
            ON p.Eventsid_event = e.id_event
            AND p.Usersid_user = %s
            AND p.state = 1
        WHERE
            e.state = 3
            AND MONTH(e.date) = %s
            AND YEAR(e.date) = %s
        ORDER BY e.date
    """, (user_id, month, year))

    result = cur.fetchall()
    cur.close()

    return result