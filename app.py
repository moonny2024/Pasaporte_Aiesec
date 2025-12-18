from flask import Flask, redirect, render_template, session, request, url_for
from database import mysql, init_db
from functools import wraps
from datetime import datetime
from MySQLdb.cursors import DictCursor
from controllers.cn_badges import *
from controllers.cn_events import *
from controllers.cn_users import *

app = Flask(__name__)
app.secret_key = 'passport_secret_key'

# Inicializar BD
init_db(app)


# LOGIN
@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        cur = mysql.connection.cursor()
        cur.execute("""
            SELECT id_user, type, state
            FROM Users
            WHERE email=%s AND password=%s
        """, (email, password))
        user = cur.fetchone()
        cur.close()

        if user and user['state'] == 1:
            session['user_id'] = user['id_user']
            session['type'] = user['type']  # 'A' o 'U'

            if user['type'] == 'A':
                return redirect(url_for('admin_events'))
            else:
                return redirect(url_for('badges'))

        return "Credenciales incorrectas"

    return render_template('auth/login.html')


# DECORADOR POR TIPO
def login_required(type=None):
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if 'user_id' not in session:
                return redirect(url_for('login'))

            if type and session.get('type') != type:
                return redirect(url_for('badges'))

            return f(*args, **kwargs)
        return wrapped
    return decorator

# PROFILE
@app.route('/profile')
@login_required(type='U')
def profile():
    user_id = session['user_id']
    profile = get_profile_by_user(user_id)

    profile = dict(profile)  # Formatear la salida de la fecha
    profile['date_start'] = profile['date_start'].strftime('%d/%m/%Y')

    return render_template(
        "components/profile.html",
        user=profile
    )


# USER
@app.route('/badges')
@login_required(type='U')
def badges():
    user_id = session['user_id']

    badges = get_monthly_badges_by_user(user_id)

    return render_template(
        'user/badges.html',
        badges=badges,
        active='badges'
    )

@app.route('/events')
@login_required(type='U')
def events():
    events = get_events_current_month()

    return render_template(
        'user/events.html',
        events=events,
        active='events'
    )

@app.route('/achievements')
@login_required(type='U')
def achievements():
    return render_template(
        'user/achievements.html',
        active='achievements'
    )

@app.route('/birthdays')
@login_required(type='U')
def birthdays():
    return render_template(
        'user/birthdays.html',
        active='birthdays'
    )

@app.route('/progress')
@login_required(type='U')
def progress():
    return render_template(
        'user/progress.html',
        active='progress'
    )


# ADMIN
@app.route('/admin/events')
@login_required(type='A')
def admin_events():
    events = adm_get_events()
    return render_template(
        'admin/events.html',
        events=events,
        active='events'
    )

@app.route('/admin/events/<int:event_id>/attendance')
@login_required(type='A')
def admin_attendance(event_id):
    cur = mysql.connection.cursor(DictCursor)
    cur.execute("SELECT * FROM events WHERE id_event=%s", (event_id,))
    event = cur.fetchone()
    cur.close()

    return render_template(
        'admin/attendance.html',
        event=event,
        event_id=event['id_event']
    )


# LOGOUT
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


if __name__ == "__main__":
    app.run(debug=True)