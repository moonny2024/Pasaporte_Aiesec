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

def get_members_of_month_by_area():
    """Devuelve el top de asistencia del mes por área.
    Para cada área, retorna el usuario con mayor número de asistencias
    a eventos del mes en curso (Presence.state=1)."""
    from datetime import datetime

    today = datetime.today()
    month = today.month
    year = today.year

    cur = mysql.connection.cursor()
    # Contamos asistencias por usuario filtrando por mes/año del evento
    cur.execute("""
        SELECT
            u.id_user,
            CONCAT(u.name, ' ', u.lastname) AS fullname,
            u.area,
            COALESCE(u.image, '') AS image,
            COUNT(p.id_presence) AS attendances
        FROM users u
        LEFT JOIN presence p
            ON p.Usersid_user = u.id_user
            AND p.state = 1
        LEFT JOIN events e
            ON e.id_event = p.Eventsid_event
            AND MONTH(e.date) = %s
            AND YEAR(e.date) = %s
        GROUP BY u.id_user, u.name, u.lastname, u.area, u.image
    """, (month, year))

    rows = cur.fetchall()
    cur.close()

    # Elegimos el de mayor asistencia por área
    best_by_area = {}
    for r in rows:
        area = r['area']
        current_best = best_by_area.get(area)
        if not current_best or r['attendances'] > current_best['attendances']:
            best_by_area[area] = {
                'area': area,
                'id_user': r['id_user'],
                'fullname': r['fullname'],
                'image': r['image'],
                'attendances': int(r['attendances'] or 0)
            }

    # Convertimos a lista ordenada por área
    return sorted(best_by_area.values(), key=lambda x: x['area'])