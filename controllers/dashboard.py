from flask import render_template, request, redirect, url_for, session
from . import dashboard_bp
from utils.db import get_db


def _require_login():
    if 'id' not in session:
        return redirect(url_for('dashboard.login'))
    return None


@dashboard_bp.route('/dashboard_user')
def dashboard_user():
    must = _require_login()
    if must:
        return must
    return render_template('home.html')


@dashboard_bp.route('/perfil')
def perfil():
    must = _require_login()
    if must:
        return must
    return render_template('profile.html')


@dashboard_bp.route('/sellos')
def sellos():
    must = _require_login()
    if must:
        return must
    return render_template('stamps.html')


@dashboard_bp.route('/logros')
def logros():
    must = _require_login()
    if must:
        return must
    return render_template('achievements.html')


@dashboard_bp.route('/progreso')
def progreso():
    must = _require_login()
    if must:
        return must
    return render_template('progress.html')


@dashboard_bp.route('/eventos')
def eventos():
    must = _require_login()
    if must:
        return must
    return render_template('events.html')


@dashboard_bp.route('/cumpleanos')
def cumpleanos():
    must = _require_login()
    if must:
        return must
    return render_template('birthday.html')


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
            return redirect(url_for('dashboard.sellos'))
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
