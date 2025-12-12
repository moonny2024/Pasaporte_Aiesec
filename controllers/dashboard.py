from flask import render_template, request, redirect, url_for, session
from . import dashboard_bp
from utils.db import get_db


def _render_user_section(active):
    if 'id' not in session:
        return redirect(url_for('dashboard.login'))
    conn = get_db()
    user = conn.execute("SELECT * FROM users WHERE id=?", (session['id'],)).fetchone()
    badges_rows = conn.execute("SELECT id, name, image, date FROM badges WHERE user_id=?", (session['id'],)).fetchall()
    badges = [dict(id=r['id'], name=r['name'], image=r['image'], date=r['date']) for r in badges_rows]
    users_rows = conn.execute("SELECT id, fullname, email FROM users").fetchall()
    users = [dict(id=r['id'], fullname=r['fullname'], email=r['email']) for r in users_rows]
    events = [
        {'id': 1, 'title': 'Leadership Summit', 'date': '2025-11-22'},
        {'id': 2, 'title': 'Workshop: Team Building', 'date': '2025-12-05'},
    ]
    total_badges = len(badges)
    porcentaje = min(100, total_badges * 10)
    return render_template(
        'dashboard_user.html',
        user=user,
        badges=badges,
        users=users,
        events=events,
        porcentaje=porcentaje,
        active=active
    )


@dashboard_bp.route('/dashboard_user')
def dashboard_user():
    if 'id' not in session:
        return redirect(url_for('dashboard.login'))
    return _render_user_section('perfil')


@dashboard_bp.route('/perfil')
def perfil():
    return _render_user_section('perfil')


@dashboard_bp.route('/sellos')
def sellos():
    return _render_user_section('sellos')


@dashboard_bp.route('/logros')
def logros():
    return _render_user_section('logros')


@dashboard_bp.route('/progreso')
def progreso():
    return _render_user_section('progreso')


@dashboard_bp.route('/eventos')
def eventos():
    return _render_user_section('eventos')


@dashboard_bp.route('/cumpleanos')
def cumpleanos():
    return _render_user_section('cumpleanos')


@dashboard_bp.route('/continuar', methods=['POST'])
def continuar():
    if session.get('id'):
        return redirect(url_for('dashboard.dashboard_user'))
    return redirect(url_for('dashboard.login'))


@dashboard_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        conn = get_db()
        user = conn.execute(
            'SELECT * FROM users WHERE email=? AND password=?',
            (email, password)
        ).fetchone()
        if user:
            session['id'] = user['id']
            session['role'] = user['role']
            if user['role'] == 'admin':
                return redirect(url_for('dashboard.admin'))
            return redirect(url_for('dashboard.dashboard_user'))
        return render_template('login.html', error='Credenciales incorrectas')
    return render_template('login.html')


@dashboard_bp.route('/logout', methods=['GET'])
def logout():
    session.clear()
    return redirect(url_for('dashboard.login'))


@dashboard_bp.route('/admin')
def admin():
    if session.get('role') != 'admin':
        return redirect(url_for('dashboard.login'))
    conn = get_db()
    users = conn.execute('SELECT * FROM users').fetchall()
    return render_template('dashboard_admin.html', users=users)
