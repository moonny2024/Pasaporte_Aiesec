from flask import Flask, redirect
from controllers.dashboard import dashboard_bp

app = Flask(__name__)
app.secret_key = "supersecret"

app.register_blueprint(dashboard_bp)

@app.route("/")
def home():
    return redirect("/login")

if __name__ == "__main__":
    app.run(debug=True)
