from flask import Flask, url_for, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "supersecret"

# -----------------------
# DB Helper
# -----------------------
def get_db():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn

# -----------------------
# ROUTES
# -----------------------

@app.route("/")
def home():
    return redirect("/login")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        conn = get_db()
        user = conn.execute(
            "SELECT * FROM users WHERE email=? AND password=?", 
            (email, password)
        ).fetchone()

        if user:
            session["id"] = user["id"]
            session["role"] = user["role"]

            if user["role"] == "admin":
                return redirect("/admin")
            else:
                return redirect("/dashboard")

        return render_template("login.html", error="Credenciales incorrectas")

    return render_template("login.html")

@app.route('/logout', methods=['GET'])
def logout():
    session.clear()
    return redirect(url_for('login'))


@app.route("/dashboard")
def dashboard():
    if "id" not in session:
        return redirect("/login")

    conn = get_db()
    user = conn.execute(
        "SELECT * FROM users WHERE id=?", (session["id"],)
    ).fetchone()

    badges = conn.execute(
        "SELECT * FROM badges WHERE user_id=?", (session["id"],)
    ).fetchall()

    total_badges = len(badges)
    participation = min(100, total_badges * 10)  # ejemplo simple

    porcentaje = participation  # o el valor que quieras
    return render_template(
        "home.html",
        user=user,
        badges=badges,
        participation=participation,
        porcentaje=porcentaje
    )


@app.route("/admin")
def admin():
    if session.get("role") != "admin":
        return redirect("/login")

    conn = get_db()
    users = conn.execute("SELECT * FROM users").fetchall()

    return render_template("dashboard_admin.html", users=users)

@app.route("/usuario")
def usuario():
    porcentaje = 75  # o el valor que calcules
    return render_template("index.html", porcentaje=porcentaje)




@app.route('/continuar', methods=['POST'])
def continuar():
    # Si el usuario tiene sesión, redirige a la vista que muestra
    # la plantilla `dashboard_user.html`; si no, al login.
    if session.get('id'):
        return redirect(url_for('dashboard_user'))
    return redirect(url_for('login'))


@app.route('/dashboard_user')
def dashboard_user():
    # Muestra la plantilla `dashboard_user.html` con datos del usuario
    if "id" not in session:
        return redirect(url_for('login'))

    conn = get_db()
    user = conn.execute(
        "SELECT * FROM users WHERE id=?", (session["id"],)
    ).fetchone()

    badges = conn.execute(
        "SELECT * FROM badges WHERE user_id=?", (session["id"],)
    ).fetchall()

    total_badges = len(badges)
    participation = min(100, total_badges * 10)
    porcentaje = participation

    return render_template(
        "dashboard_user.html",
        user=user,
        badges=badges,
        participation=participation,
        porcentaje=porcentaje,
        active='perfil'
    )


def _render_user_section(active):
    """Renderiza el dashboard de usuario con secciones dinámicas sin crear nuevas plantillas."""
    if 'id' not in session:
        return redirect(url_for('login'))
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

@app.route('/perfil')
def perfil():
    return _render_user_section('perfil.html')

@app.route('/sellos')
def sellos():
    return _render_user_section('sellos.html')

@app.route('/logros')
def logros():
    return _render_user_section('logros.html')

@app.route('/progreso')
def progreso():
    return _render_user_section('progreso.html')

@app.route('/eventos')
def eventos():
    return _render_user_section('eventos.html')

@app.route('/cumpleanos')
def cumpleanos():
    return _render_user_section('cumpleanos.html')

if __name__ == "__main__":
    app.run(debug=True)
