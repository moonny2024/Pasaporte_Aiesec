from database import mysql
from datetime import datetime


def get_events_current_month():
    today = datetime.today()
    month = today.month
    year = today.year

    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT
            id_event,
            name,
            category,
            COALESCE(description, 'Sin descripción') AS description,
            image,
            date,
            DATE_FORMAT(time_start, '%%H:%%i') AS time_start,
            COALESCE(hours, '-') AS hours
        FROM events
        WHERE
            MONTH(date) = %s
            AND YEAR(date) = %s
        ORDER BY id_event DESC
    """, (month, year))
    events = cur.fetchall()
    cur.close()
    return events


def adm_get_events():
    today = datetime.today()
    month = today.month
    year = today.year
    
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT
            id_event,
            name,
            COALESCE(description, 'Sin descripción') AS description,
            image,
            date,
            DATE_FORMAT(time_start, '%%H:%%i') AS time_start,
            COALESCE(hours, '-') AS hours,
            state
        FROM events
        WHERE
            MONTH(date) = %s
            AND YEAR(date) = %s
        ORDER BY id_event DESC
    """, (month, year))
    events = cur.fetchall()
    cur.close()
    return events