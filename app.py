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
        "dashboard_user.html",
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


if __name__ == "__main__":
    app.run(debug=True)
